"""Loading design files from untrusted bytes."""

from __future__ import annotations

import io
from pathlib import Path

import pystitch

from .formats import KNOWN_UNREADABLE, get_format, normalize_extension

DEFAULT_MAX_BYTES = 25 * 1024 * 1024
DEFAULT_MAX_STITCHES = 2_000_000


class DesignError(ValueError):
    """The file could not be read as an embroidery design.

    ``code`` is stable and safe to show/translate in the UI:
    ``unsupported_format``, ``unreadable_format``, ``too_large``,
    ``empty_design``, ``corrupt``, ``too_many_stitches``.
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

    stitch_count = pattern.count_stitch_commands(pystitch.STITCH)
    if stitch_count == 0:
        raise DesignError("empty_design", "file contains no stitches")
    if len(pattern.stitches) > max_stitches:
        raise DesignError("too_many_stitches", f"design has {len(pattern.stitches)} commands")
    return pattern


def clone_pattern(pattern: pystitch.EmbPattern) -> pystitch.EmbPattern:
    """Deep copy. ``EmbPattern.copy()`` shares the stitch lists, and several
    pystitch writers and transforms mutate stitches in place."""
    clone = pattern.copy()
    clone.stitches = [list(stitch) for stitch in pattern.stitches]
    return clone


def load_design_file(path: str | Path, **limits) -> pystitch.EmbPattern:
    path = Path(path)
    return load_design(path.read_bytes(), path.suffix, **limits)
