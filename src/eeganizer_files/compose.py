"""Combine several designs (and lettering) into one machine file.

Each piece is placed by the position of its center in a shared layout
(millimetres, y pointing down as on screen), optionally rotated, mirrored or
resized through the guarded ``transform``. Pieces are sewn in the order
given: a trim between pieces, and a color stop only when the thread actually
changes, so a word in one color sews without stopping after every letter.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pystitch

from .design import DesignError, clone_pattern
from .formats import UNITS_PER_MM
from .hoops import FitResult, Hoop, check_fit
from .inspect import analyze, command_of, stitch_bounds
from .transform import TransformReport, transform

_STITCH = pystitch.STITCH
_JUMP = pystitch.JUMP
_COLOR_CHANGE = pystitch.COLOR_CHANGE
_END = pystitch.END


class ComposeError(DesignError):
    pass


@dataclass
class Placement:
    pattern: pystitch.EmbPattern
    x_mm: float = 0.0
    y_mm: float = 0.0
    rotate_degrees: float = 0.0
    scale: float = 1.0
    mirror: bool = False
    thread: str | None = None  # recolor every block to this hex color, e.g. "#c0392b"
    label: str = ""
    allow_large_resize: bool = False


@dataclass
class ComposeReport:
    width_mm: float
    height_mm: float
    color_change_count: int
    stitch_count: int
    overlaps: list[tuple[str, str]] = field(default_factory=list)
    transforms: dict[str, TransformReport] = field(default_factory=dict)
    fit: FitResult | None = None
    messages: list[str] = field(default_factory=list)


def _color_blocks(pattern: pystitch.EmbPattern) -> list[tuple[list[list[float]], pystitch.EmbThread]]:
    """Split into (stitches, thread) per color, dropping color-change and end commands."""
    blocks: list[tuple[list[list[float]], pystitch.EmbThread]] = []
    current: list[list[float]] = []
    index = 0
    for stitch in pattern.stitches:
        cmd = command_of(stitch)
        if cmd == _COLOR_CHANGE:
            if current:
                blocks.append((current, pattern.get_thread_or_filler(index)))
            current = []
            index += 1
        elif cmd == _END:
            break
        else:
            current.append(list(stitch))
    if current:
        blocks.append((current, pattern.get_thread_or_filler(index)))
    # Blocks with only jumps/trims add nothing to sew.
    return [(b, t) for b, t in blocks if any(command_of(s) == _STITCH for s in b)]


def _same_thread(a: pystitch.EmbThread, b: pystitch.EmbThread) -> bool:
    return a.hex_color() == b.hex_color()


def _bbox(pattern: pystitch.EmbPattern) -> tuple[float, float, float, float]:
    return stitch_bounds(pattern)


def _overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def compose(
    placements: list[Placement],
    *,
    hoop: Hoop | None = None,
    merge_same_colors: bool = True,
) -> tuple[pystitch.EmbPattern, ComposeReport]:
    """Merge ``placements`` into one pattern centred on the origin."""
    if not placements:
        raise ComposeError("empty_layout", "nothing to combine")

    report_transforms: dict[str, TransformReport] = {}
    placed: list[tuple[str, pystitch.EmbPattern]] = []
    for n, item in enumerate(placements):
        label = item.label or f"item {n + 1}"
        piece = clone_pattern(item.pattern)
        if item.scale != 1.0 or item.rotate_degrees or item.mirror:
            piece, tr = transform(
                piece,
                scale=item.scale,
                rotate_degrees=item.rotate_degrees,
                mirror_horizontal=item.mirror,
                allow_large_resize=item.allow_large_resize,
            )
            report_transforms[label] = tr
            if piece is None:
                raise ComposeError("transform_blocked", f"{label}: " + " ".join(tr.messages))
        min_x, min_y, max_x, max_y = _bbox(piece)
        dx = item.x_mm * UNITS_PER_MM - (min_x + max_x) / 2
        dy = item.y_mm * UNITS_PER_MM - (min_y + max_y) / 2
        piece.translate(dx, dy)
        if item.thread:
            # New thread objects: clones share EmbThread instances with the source.
            piece.threadlist = [pystitch.EmbThread(item.thread) for _ in piece.threadlist] or [
                pystitch.EmbThread(item.thread)
            ]
        placed.append((label, piece))

    out = pystitch.EmbPattern()
    last_thread: pystitch.EmbThread | None = None
    for _label, piece in placed:
        for stitches, thread in _color_blocks(piece):
            if last_thread is not None:
                out.trim()
                if not (merge_same_colors and _same_thread(thread, last_thread)):
                    out.color_change()
                    out.add_thread(thread)
            else:
                out.add_thread(thread)
            first = next(s for s in stitches if command_of(s) in (_STITCH, _JUMP))
            out.add_stitch_absolute(_JUMP, first[0], first[1])
            out.stitches.extend(stitches)
            last_thread = thread
    out.end()

    # Centre the combined design on the origin, as machines center on the hoop.
    min_x, min_y, max_x, max_y = stitch_bounds(out)
    out.translate(-(min_x + max_x) / 2, -(min_y + max_y) / 2)

    info = analyze(out)
    report = ComposeReport(
        width_mm=info.width_mm,
        height_mm=info.height_mm,
        color_change_count=info.color_change_count,
        stitch_count=info.stitch_count,
        transforms=report_transforms,
    )
    boxes = [(label, _bbox(piece)) for label, piece in placed]
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if _overlap(boxes[i][1], boxes[j][1]):
                report.overlaps.append((boxes[i][0], boxes[j][0]))
    if report.overlaps:
        report.messages.append(
            "Some pieces overlap; later pieces sew on top of earlier ones. Check the preview."
        )
    if hoop is not None:
        report.fit = check_fit(info, hoop)
        if not report.fit.fits:
            report.messages.append(f"The combined design does not fit the {hoop.label} hoop.")
    return out, report
