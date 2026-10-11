"""Loading design files from untrusted bytes."""

from __future__ import annotations

import io
import struct
from pathlib import Path

import pystitch

from .formats import KNOWN_UNREADABLE, get_format, normalize_extension

DEFAULT_MAX_BYTES = 25 * 1024 * 1024
DEFAULT_MAX_STITCHES = 2_000_000
# Larger than any embroidery field, including commercial jumbo frames. A
# bigger result means the file was misread (wiki: reject anything bigger
# than the largest hoop); found by scripts/fuzz.py.
MAX_DESIGN_MM = 1200.0


class DesignError(ValueError):
    """The file could not be read as an embroidery design.

    ``code`` is stable and safe to show/translate in the UI:
    ``unsupported_format``, ``unreadable_format``, ``too_large``,
    ``empty_design``, ``corrupt``, ``too_many_stitches``, ``implausible_size``.
    """

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def load_design(
    data: bytes,
    extension: str,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_stitches: int = DEFAULT_MAX_STITCHES,
) -> pystitch.EmbPattern:
    """Parse ``data`` as an embroidery file of type ``extension``.

    Raises DesignError for anything that is not a usable design. This does
    not protect against hangs or memory blow-ups in the parser itself; run
    it through ``eeganizer_files.sandbox`` for customer uploads.
    """
    ext = normalize_extension(extension)
    if len(data) > max_bytes:
        raise DesignError("too_large", f"file is {len(data)} bytes; limit is {max_bytes}")
    if ext in KNOWN_UNREADABLE:
        raise DesignError(
            "unreadable_format",
            f"{KNOWN_UNREADABLE[ext]} files can be stored but not previewed or converted",
        )
    spec = get_format(ext)
    if spec is None or not spec.can_read:
        raise DesignError("unsupported_format", f".{ext} is not a supported embroidery format")

    pattern = pystitch.EmbPattern()
    try:
        spec.reader.read(io.BytesIO(data), pattern, {})
    except Exception as exc:  # parsers raise anything from struct.error to IndexError
        raise DesignError("corrupt", f"could not parse .{ext} file: {type(exc).__name__}") from exc

    if ext in ("pes", "pec"):
        pattern = _check_pec_block(data, ext, pattern, spec.reader)

    stitch_count = pattern.count_stitch_commands(pystitch.STITCH)
    if stitch_count == 0:
        raise DesignError("empty_design", "file contains no stitches")
    if len(pattern.stitches) > max_stitches:
        raise DesignError("too_many_stitches", f"design has {len(pattern.stitches)} commands")

    from .inspect import stitch_bounds

    min_x, min_y, max_x, max_y = stitch_bounds(pattern)
    if max(max_x - min_x, max_y - min_y) / 10.0 > MAX_DESIGN_MM:
        raise DesignError("implausible_size", "design is larger than any embroidery field; the file is damaged")

    # Damaged color tables can leave empty thread slots (fuzz finding, JEF).
    pattern.threadlist = [
        t if t is not None else pystitch.EmbThread("#808080", description="Unknown")
        for t in pattern.threadlist
    ]
    return pattern


def _pec_layout(data: bytes, ext: str) -> tuple[int, int, float, float] | None:
    """(stitch start, stitch block end, width mm, height mm) from the PEC header, or None."""
    try:
        pec = struct.unpack_from("<I", data, 8)[0] if ext == "pes" else 8
        block_length = data[pec + 514] | data[pec + 515] << 8 | data[pec + 516] << 16
        width, height = struct.unpack_from("<HH", data, pec + 520)
    except (struct.error, IndexError):
        return None
    return pec + 532, pec + 512 + block_length, width / 10.0, height / 10.0


def _check_pec_block(data: bytes, ext: str, pattern: pystitch.EmbPattern, reader) -> pystitch.EmbPattern:
    """Guard against pystitch reading past the PEC stitch block.

    pystitch stops only at an FF 00 end marker. A file with a stray byte
    before the marker (seen in a commercial alphabet pack) desynchronises the
    decoder, which then reads the preview images as hundreds of random
    stitches. The PEC header records the block end and the design size, so
    when the decoded size disagrees we re-read with the stream cut at the
    block end, and reject the file if it still disagrees.
    """
    from .inspect import stitch_bounds  # local import: inspect imports formats only

    layout = _pec_layout(data, ext)
    if layout is None:
        return pattern
    _start, block_end, width, height = layout

    def matches(p: pystitch.EmbPattern, swapped: bool = False) -> bool:
        b = stitch_bounds(p)
        w, h = (b[2] - b[0]) / 10, (b[3] - b[1]) / 10
        if swapped:
            w, h = h, w
        return abs(w - width) <= 1.0 and abs(h - height) <= 1.0

    if width == 0 or height == 0 or matches(pattern):
        return pattern
    if not 0 < block_end <= len(data):
        raise DesignError("corrupt", "PES stitch data does not match its header")
    retry = pystitch.EmbPattern()
    try:
        reader.read(io.BytesIO(data[:block_end]), retry, {})
    except Exception as exc:
        raise DesignError("corrupt", f"could not parse .{ext} file: {type(exc).__name__}") from exc
    if matches(retry):
        retry.extras["eefile_repaired"] = "pec_block_overrun"
        return retry
    if matches(retry, swapped=True):
        # Every such file in the alphabet pack that exposed this had its PEC
        # stitches turned 90 degrees clockwise relative to its own header and
        # to the same letter in DST/JEF/VP3; turning them back restores both.
        b = stitch_bounds(retry)
        matrix = pystitch.EmbMatrix()
        matrix.post_rotate(-90, (b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        retry.transform(matrix)
        retry.extras["eefile_repaired"] = "pec_block_overrun,rotated_to_header"
        return retry
    raise DesignError("corrupt", "PES stitch data does not match its header")


def clone_pattern(pattern: pystitch.EmbPattern) -> pystitch.EmbPattern:
    """Deep copy. ``EmbPattern.copy()`` shares the stitch lists, and several
    pystitch writers and transforms mutate stitches in place."""
    clone = pattern.copy()
    clone.stitches = [list(stitch) for stitch in pattern.stitches]
    return clone


def load_design_file(path: str | Path, **limits) -> pystitch.EmbPattern:
    path = Path(path)
    return load_design(path.read_bytes(), path.suffix, **limits)
