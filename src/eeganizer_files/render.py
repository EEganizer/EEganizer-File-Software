"""Preview rendering (PNG thumbnails, SVG for zoomable web viewing)."""

from __future__ import annotations

import io

import pystitch

from .design import clone_pattern
from .inspect import command_of, stitch_bounds


def render_png(pattern: pystitch.EmbPattern, *, fancy: bool = True, background: str | None = None) -> bytes:
    """Full-size PNG (1 px = 0.1 mm). ``fancy`` adds pystitch's thread shading.
    Downscale for thumbnails in the web tier."""
    settings: dict = {"fancy": fancy}
    if background:
        settings["background"] = background
    buffer = io.BytesIO()
    pystitch.write_png(clone_pattern(pattern), buffer, settings)
    return buffer.getvalue()


def render_svg(pattern: pystitch.EmbPattern) -> bytes:
    buffer = io.BytesIO()
    pystitch.write_svg(clone_pattern(pattern), buffer)
    return buffer.getvalue()


def render_thumbnail(pattern: pystitch.EmbPattern, size: int = 256, *, fancy: bool = True) -> bytes:
    """PNG whose longest side is about ``size`` pixels.

    pystitch draws 1 px per 0.1 mm, so the design is scaled to the target
    pixel size first instead of downsampling a full-size image (no Pillow)."""
    if not 16 <= size <= 2048:
        raise ValueError("thumbnail size must be between 16 and 2048 px")
    clone = clone_pattern(pattern)
    min_x, min_y, max_x, max_y = stitch_bounds(clone)
    longest = max(max_x - min_x, max_y - min_y, 1)
    factor = (size - 1) / longest
    matrix = pystitch.EmbMatrix()
    matrix.post_translate(-min_x, -min_y)
    matrix.post_scale(factor, factor)
    clone.transform(matrix)
    # pystitch sizes the image from all commands; drop jumps outside the sewn
    # area (e.g. to the hoop corner) so they cannot inflate the image.
    clone.stitches = [
        s for s in clone.stitches
        if command_of(s) != pystitch.JUMP or (0 <= s[0] <= size and 0 <= s[1] <= size)
    ]
    buffer = io.BytesIO()
    pystitch.write_png(clone, buffer, {"fancy": fancy})
    return buffer.getvalue()
