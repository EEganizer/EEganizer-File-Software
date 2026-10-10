"""Preview rendering (PNG thumbnails, SVG for zoomable web viewing)."""

from __future__ import annotations

import io

import pystitch

from .design import clone_pattern


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
