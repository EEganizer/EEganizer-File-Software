"""Hoop fit checks.

Sizes below are NOMINAL hoop names converted to mm. The usable sewing field
varies by machine model (a Brother "4x4" sews about 100 x 100 mm), so the
production catalog must store each model's published sewing area. Treat this
table as defaults until that catalog exists.
"""

from __future__ import annotations

from dataclasses import dataclass

from .inspect import DesignInfo


@dataclass(frozen=True)
class Hoop:
    key: str
    label: str
    width_mm: float
    height_mm: float


HOOPS: dict[str, Hoop] = {
    h.key: h
    for h in [
        Hoop("4x4", '4" x 4"', 100, 100),
        Hoop("5x7", '5" x 7"', 130, 180),
        Hoop("6x10", '6" x 10"', 160, 260),
        Hoop("8x8", '8" x 8"', 200, 200),
        Hoop("8x12", '8" x 12"', 200, 300),
        Hoop("9.5x14", '9.5" x 14"', 240, 360),
    ]
}


@dataclass
class FitResult:
    hoop: Hoop
    fits: bool
    needs_rotation: bool
    margin_x_mm: float
    margin_y_mm: float
    scale_to_fit: float  # 1.0 if it fits; otherwise the uniform scale needed


def check_fit(info: DesignInfo, hoop: Hoop, *, clearance_mm: float = 2.0, allow_rotation: bool = True) -> FitResult:
    avail_w = hoop.width_mm - 2 * clearance_mm
    avail_h = hoop.height_mm - 2 * clearance_mm
    w, h = info.width_mm, info.height_mm

    if w <= avail_w and h <= avail_h:
        return FitResult(hoop, True, False, round(avail_w - w, 1), round(avail_h - h, 1), 1.0)
    if allow_rotation and h <= avail_w and w <= avail_h:
        return FitResult(hoop, True, True, round(avail_w - h, 1), round(avail_h - w, 1), 1.0)

    def needed(dw: float, dh: float) -> float:
        return min(avail_w / dw if dw else float("inf"), avail_h / dh if dh else float("inf"))

    best = needed(w, h)
    rotated = False
    if allow_rotation and needed(h, w) > best:
        best, rotated = needed(h, w), True
    dw, dh = (h, w) if rotated else (w, h)
    return FitResult(hoop, False, rotated, round(avail_w - dw, 1), round(avail_h - dh, 1), round(best, 3))


def smallest_hoop(info: DesignInfo, hoops: list[Hoop] | None = None, **kwargs) -> FitResult | None:
    """The smallest-area hoop the design fits in, or None."""
    candidates = sorted(hoops or HOOPS.values(), key=lambda hp: hp.width_mm * hp.height_mm)
    for hoop in candidates:
        result = check_fit(info, hoop, **kwargs)
        if result.fits:
            return result
    return None
