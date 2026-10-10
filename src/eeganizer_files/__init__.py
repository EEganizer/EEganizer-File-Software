"""EEganizer embroidery design file toolkit.

Thin, EEganizer-owned layer over the MIT-licensed ``pystitch`` format engine.
pystitch reads and writes the bytes; this package owns everything customers
see: properties, previews, safe conversion, guarded resizing and hoop fit.
"""

from .design import DesignError, load_design, load_design_file
from .inspect import DesignInfo, analyze
from .convert import ConversionResult, convert, write_design
from .transform import TransformReport, transform
from .hoops import HOOPS, Hoop, FitResult, check_fit
from .render import render_png, render_svg

__all__ = [
    "DesignError",
    "load_design",
    "load_design_file",
    "DesignInfo",
    "analyze",
    "ConversionResult",
    "convert",
    "write_design",
    "TransformReport",
    "transform",
    "HOOPS",
    "Hoop",
    "FitResult",
    "check_fit",
    "render_png",
    "render_svg",
]

__version__ = "0.1.0"
