"""Guarded geometric transforms: resize, rotate, mirror.

Every open-source engine (pystitch included) resizes by multiplying stitch
coordinates. Stitch count stays the same, so enlarging opens gaps and long
stitches, and shrinking packs stitches until thread breaks. This module does
the same geometric scale, but measures and reports the consequences so the UI
can warn or block. It does NOT recalculate stitches.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pystitch

from .design import clone_pattern
from .formats import get_format
from .inspect import MAX_SEWN_STITCH_MM, stitch_bounds, stitch_lengths

# Commonly cited safe band for scaling stitch files. Practitioner guidance,
# not a measured standard: validate with test stitch-outs before relying on it.
CAUTION_PERCENT = 10.0
WARNING_PERCENT = 20.0

# Longest stitch a typical home machine sews without auto-trim/jump
# (DST's 121 * 0.1 mm limit is the common lowest denominator).
DEFAULT_MAX_STITCH_MM = 12.1
# Stitches shorter than this tend to cause thread nests and breaks.
SHORT_STITCH_MM = 0.5


@dataclass
class TransformReport:
    scale_x: float
    scale_y: float
    rotate_degrees: float
    mirrored: bool
    level: str  # "ok" | "caution" | "warning" | "blocked"
    messages: list[str] = field(default_factory=list)
    density_factor: float = 1.0
    longest_stitch_mm: float = 0.0
    long_stitch_count: int = 0
    short_stitch_count: int = 0
    max_stitch_mm: float = DEFAULT_MAX_STITCH_MM

    @property
    def blocked(self) -> bool:
        return self.level == "blocked"


_LEVELS = ["ok", "caution", "warning", "blocked"]


def _raise_level(current: str, new: str) -> str:
    return new if _LEVELS.index(new) > _LEVELS.index(current) else current


def transform(
    pattern: pystitch.EmbPattern,
    *,
    scale: float | None = None,
    target_width_mm: float | None = None,
    target_height_mm: float | None = None,
    rotate_degrees: float = 0.0,
    mirror_horizontal: bool = False,
    mirror_vertical: bool = False,
    target_extension: str | None = None,
    free_standing_lace: bool = False,
    allow_large_resize: bool = False,
) -> tuple[pystitch.EmbPattern | None, TransformReport]:
    """Return a transformed copy of ``pattern`` and a report.

    Size can be given as a uniform ``scale`` or a target width and/or height
    (aspect ratio is kept when only one is given). When the report is
    ``blocked`` the returned pattern is None.
    """
    min_x, min_y, max_x, max_y = stitch_bounds(pattern)
    width, height = (max_x - min_x) / 10.0, (max_y - min_y) / 10.0

    sx = sy = 1.0
    if scale is not None:
        sx = sy = float(scale)
    elif target_width_mm is not None or target_height_mm is not None:
        if target_width_mm is not None and width > 0:
            sx = target_width_mm / width
        if target_height_mm is not None and height > 0:
            sy = target_height_mm / height
        if target_width_mm is None:
            sx = sy
        if target_height_mm is None:
            sy = sx
    if sx <= 0 or sy <= 0:
        raise ValueError("scale must be positive")

    spec = get_format(target_extension) if target_extension else None
    max_stitch = (spec.max_stitch_mm if spec and spec.max_stitch_mm else None) or DEFAULT_MAX_STITCH_MM
    max_stitch = min(max_stitch, DEFAULT_MAX_STITCH_MM)

    report = TransformReport(
        scale_x=round(sx, 4),
        scale_y=round(sy, 4),
        rotate_degrees=rotate_degrees,
        mirrored=mirror_horizontal or mirror_vertical,
        level="ok",
        density_factor=round(1.0 / (sx * sy), 3),
        max_stitch_mm=max_stitch,
    )

    resized = abs(sx - 1.0) > 1e-9 or abs(sy - 1.0) > 1e-9
    # Rounded so an exact 10% / 20% request lands in the lower band.
    change_pct = round(max(abs(sx - 1.0), abs(sy - 1.0)) * 100, 6)

    if resized and free_standing_lace:
        report.level = "blocked"
        report.messages.append(
            "Free-standing lace depends on exact stitch spacing to hold together; "
            "it should not be resized. Use a version digitized at the size you need."
        )
        return None, report

    if abs(sx - sy) > 1e-6:
        report.level = _raise_level(report.level, "caution")
        report.messages.append("Width and height are scaled differently; satin columns and lettering may distort.")

    if change_pct > WARNING_PERCENT:
        if allow_large_resize:
            report.level = _raise_level(report.level, "warning")
            report.messages.append(
                f"Size changed by {change_pct:.0f}%. Stitches are not recalculated, so density "
                f"changes to {report.density_factor:.2f}x of the original. Test stitch-out strongly recommended."
            )
        else:
            report.level = "blocked"
            report.messages.append(
                f"Size change of {change_pct:.0f}% is beyond the {WARNING_PERCENT:.0f}% limit for "
                "resizing without recalculating stitches."
            )
            return None, report
    elif change_pct > CAUTION_PERCENT:
        report.level = _raise_level(report.level, "caution")
        report.messages.append(
            f"Size changed by {change_pct:.0f}%. Density becomes {report.density_factor:.2f}x of the original; "
            "do a test stitch-out."
        )

    result = clone_pattern(pattern)
    cx, cy = (min_x + max_x) / 2, (min_y + max_y) / 2
    matrix = pystitch.EmbMatrix()
    matrix.post_translate(-cx, -cy)
    matrix.post_scale(sx * (-1 if mirror_horizontal else 1), sy * (-1 if mirror_vertical else 1))
    if rotate_degrees:
        matrix.post_rotate(rotate_degrees)
    matrix.post_translate(cx, cy)
    result.transform(matrix)

    # Compare stitch by stitch (a transform keeps the sequence) so moves that
    # were already longer than the limit (travel moves in VP3 etc.) are not
    # blamed on the resize.
    before = stitch_lengths(pattern)
    lengths = stitch_lengths(result)
    sewn = [after for orig, after in zip(before, lengths) if orig <= MAX_SEWN_STITCH_MM]
    report.longest_stitch_mm = round(max(sewn, default=0.0), 2)
    report.long_stitch_count = sum(1 for n in sewn if n > max_stitch)
    # Only stitches the resize made short (tie-ins are short by design).
    report.short_stitch_count = sum(
        1 for orig, after in zip(before, lengths) if after < SHORT_STITCH_MM <= orig
    )

    if report.long_stitch_count:
        report.level = _raise_level(report.level, "warning")
        report.messages.append(
            f"{report.long_stitch_count} stitches are longer than {max_stitch} mm. They will be split "
            "on export or the machine may trim/jump them; satin areas will look different."
        )
    if report.short_stitch_count:
        report.level = _raise_level(report.level, "caution")
        report.messages.append(
            f"{report.short_stitch_count} stitches become shorter than {SHORT_STITCH_MM} mm; "
            "watch for thread breaks and nests."
        )
    return result, report
