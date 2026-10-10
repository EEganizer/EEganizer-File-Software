"""Format conversion."""

from __future__ import annotations

import io
from dataclasses import dataclass, field

import pystitch

from .design import DesignError, clone_pattern, load_design
from .formats import get_format, normalize_extension

# PES v6 is what current Brother/Baby Lock software writes; v1 is the most
# widely readable. Default to v6 and let callers choose v1 for older machines.
DEFAULT_PES_VERSION = 6


# pystitch's SewWriter declares no jump/stitch limits, so moves over 12.7 mm
# overflow its signed 8-bit deltas and corrupt the design (found by
# tests/test_convert.py round-trip). Force splitting at the encodable maximum.
WRITER_OVERRIDES: dict[str, dict] = {
    "sew": {"max_jump": 127, "max_stitch": 127},
}


@dataclass
class ConversionResult:
    data: bytes
    extension: str
    warnings: list[str] = field(default_factory=list)


def write_design(
    pattern: pystitch.EmbPattern,
    extension: str,
    *,
    pes_version: int = DEFAULT_PES_VERSION,
) -> ConversionResult:
    ext = normalize_extension(extension)
    spec = get_format(ext)
    if spec is None or not spec.can_write:
        raise DesignError("unsupported_format", f"cannot write .{ext} files")

    warnings: list[str] = []
    if not spec.stores_thread_colors and len(pattern.threadlist) > 0:
        warnings.append(
            f".{ext} does not store thread colors; the machine will show default colors "
            "and only the color-change stops are kept."
        )

    settings: dict = {}
    if ext == "pes":
        if pes_version not in (1, 6):
            raise DesignError("unsupported_format", "PES output supports version 1 or 6 only")
        settings["version"] = pes_version

    settings.update(WRITER_OVERRIDES.get(ext, {}))

    buffer = io.BytesIO()
    # write_embroidery normalizes the pattern for the writer, including splitting
    # stitches longer than the format allows. It works on a copy.
    pystitch.EmbPattern.write_embroidery(spec.writer, clone_pattern(pattern), buffer, settings)
    return ConversionResult(data=buffer.getvalue(), extension=ext, warnings=warnings)


def convert(data: bytes, source_extension: str, target_extension: str, **kwargs) -> ConversionResult:
    """Convert raw file bytes from one format to another.

    Conversion between stitch formats is always somewhat lossy (thread palette
    matching, format-specific metadata). It never re-digitizes."""
    pattern = load_design(data, source_extension)
    return write_design(pattern, target_extension, **kwargs)
