"""Customer-facing design properties."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field

import pystitch

from .formats import UNITS_PER_MM

_STITCH = pystitch.STITCH
_JUMP = pystitch.JUMP
_TRIM = pystitch.TRIM
_COLOR_CHANGE = pystitch.COLOR_CHANGE
_END = pystitch.END
_NEEDLE_POSITION_COMMANDS = {_STITCH, _JUMP}


@dataclass
class ThreadInfo:
    index: int
    hex_color: str
    description: str | None = None
    brand: str | None = None
    catalog_number: str | None = None
    stitch_count: int = 0


@dataclass
class DesignInfo:
    width_mm: float
    height_mm: float
    stitch_count: int
    jump_count: int
    trim_count: int
    color_change_count: int
    thread_count: int
    threads: list[ThreadInfo] = field(default_factory=list)
    longest_stitch_mm: float = 0.0
    mean_stitch_mm: float = 0.0
    thread_length_m: float = 0.0
    estimated_sew_minutes: float = 0.0
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def width_in(self) -> float:
        return self.width_mm / 25.4

    @property
    def height_in(self) -> float:
        return self.height_mm / 25.4

    def to_dict(self) -> dict:
        data = asdict(self)
        data["width_in"] = round(self.width_in, 2)
        data["height_in"] = round(self.height_in, 2)
        return data


def command_of(stitch) -> int:
    return stitch[2] & pystitch.COMMAND_MASK


def stitch_bounds(pattern: pystitch.EmbPattern) -> tuple[float, float, float, float]:
    """Bounds of sewn stitches only (jumps and trims to the hoop corner ignored)."""
    xs = [s[0] for s in pattern.stitches if command_of(s) == _STITCH]
    ys = [s[1] for s in pattern.stitches if command_of(s) == _STITCH]
    if not xs:
        return 0.0, 0.0, 0.0, 0.0
    return min(xs), min(ys), max(xs), max(ys)


def stitch_lengths(pattern: pystitch.EmbPattern) -> list[float]:
    """Length (in mm) of every sewn stitch, i.e. needle moves that lay thread."""
    lengths: list[float] = []
    prev = None
    sewing = False
    for stitch in pattern.stitches:
        cmd = command_of(stitch)
        if cmd in _NEEDLE_POSITION_COMMANDS:
            point = (stitch[0], stitch[1])
            # The first stitch after a jump/trim/color change only positions the
            # needle; it does not lay a thread segment from the previous point.
            if cmd == _STITCH and prev is not None and sewing:
                lengths.append(math.dist(prev, point) / UNITS_PER_MM)
            sewing = cmd == _STITCH
            prev = point
        elif cmd in (_TRIM, _COLOR_CHANGE, _END):
            sewing = False
    return lengths


def analyze(
    pattern: pystitch.EmbPattern,
    *,
    stitches_per_minute: int = 650,
    seconds_per_color_change: float = 60.0,
    seconds_per_trim: float = 4.0,
) -> DesignInfo:
    """Summarize a design. Sew time is an estimate for a home machine;
    expose the parameters per machine profile rather than trusting defaults."""
    min_x, min_y, max_x, max_y = stitch_bounds(pattern)
    lengths = stitch_lengths(pattern)
    stitch_count = pattern.count_stitch_commands(_STITCH)
    trims = pattern.count_stitch_commands(_TRIM)
    color_changes = pattern.count_color_changes()

    threads: list[ThreadInfo] = []
    per_block = [
        sum(1 for s in block if command_of(s) == _STITCH)
        for block, _thread in pattern.get_as_colorblocks()
    ]
    for index, thread in enumerate(pattern.threadlist):
        threads.append(
            ThreadInfo(
                index=index,
                hex_color=thread.hex_color(),
                description=thread.description,
                brand=thread.brand,
                catalog_number=thread.catalog_number,
                stitch_count=per_block[index] if index < len(per_block) else 0,
            )
        )

    sew_seconds = (
        stitch_count / max(stitches_per_minute, 1) * 60
        + color_changes * seconds_per_color_change
        + trims * seconds_per_trim
    )
    metadata = {str(k): str(v) for k, v in (pattern.extras or {}).items() if isinstance(v, (str, int, float))}

    return DesignInfo(
        width_mm=round((max_x - min_x) / UNITS_PER_MM, 1),
        height_mm=round((max_y - min_y) / UNITS_PER_MM, 1),
        stitch_count=stitch_count,
        jump_count=pattern.count_stitch_commands(_JUMP),
        trim_count=trims,
        color_change_count=color_changes,
        thread_count=len(pattern.threadlist),
        threads=threads,
        longest_stitch_mm=round(max(lengths, default=0.0), 2),
        mean_stitch_mm=round(sum(lengths) / len(lengths), 2) if lengths else 0.0,
        # Top thread only; bobbin and take-up are excluded.
        thread_length_m=round(sum(lengths) / 1000, 2),
        estimated_sew_minutes=round(sew_seconds / 60, 1),
        metadata=metadata,
    )
