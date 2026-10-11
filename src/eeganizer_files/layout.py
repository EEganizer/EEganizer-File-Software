"""JSON layout documents for compose (used by the service and CLI).

Example::

    {
      "items": [
        {"type": "design", "file": "whale.pes", "x_mm": 0, "y_mm": 0},
        {"type": "text", "text": "Ella", "alphabet": "script",
         "below": true, "gap_mm": 8, "height_mm": 15, "thread": "#c0392b"}
      ],
      "alphabets": {"script": ["A.pes", "E.pes", "l_lower.pes", "a_lower.pes"]},
      "target": "pes",            # or "machine": "brother"
      "hoop": "5x7"
    }

File names refer to the files supplied alongside the layout.
"""

from __future__ import annotations

from .compose import ComposeError, ComposeReport, Placement, compose
from .convert import ConversionResult, write_design
from .design import load_design
from .formats import MACHINE_FORMATS, normalize_extension
from .hoops import HOOPS
from .lettering import Alphabet, choose_alphabet, layout_text

MAX_ITEMS = 50
MAX_FILES = 150
_HEX = set("0123456789abcdefABCDEF")


def _number(item: dict, key: str, default: float, low: float, high: float) -> float:
    value = item.get(key, default)
    if value is None:
        return default
    if not isinstance(value, (int, float)) or not low <= value <= high:
        raise ComposeError("bad_layout", f"{key} must be a number between {low} and {high}")
    return float(value)


def _thread(item: dict) -> str | None:
    value = item.get("thread")
    if value is None:
        return None
    if not (isinstance(value, str) and len(value) == 7 and value[0] == "#" and set(value[1:]) <= _HEX):
        raise ComposeError("bad_layout", "thread must be a hex color like #c0392b")
    return value


def _vertical_extent(items: list[Placement]) -> tuple[float, float]:
    """Top and bottom (mm, y down) of placements after their scale and rotation."""
    from .inspect import stitch_bounds

    top, bottom = float("inf"), float("-inf")
    for item in items:
        b = stitch_bounds(item.pattern)
        w, h = (b[2] - b[0]) / 10 * item.scale, (b[3] - b[1]) / 10 * item.scale
        if round(item.rotate_degrees) % 180 == 90:
            w, h = h, w
        top, bottom = min(top, item.y_mm - h / 2), max(bottom, item.y_mm + h / 2)
    return top, bottom


def target_extension(layout: dict) -> str:
    if layout.get("machine"):
        formats = MACHINE_FORMATS.get(str(layout["machine"]).lower())
        if not formats:
            raise ComposeError("unknown_machine", f"unknown machine brand {layout['machine']!r}")
        return formats[0]
    if layout.get("target"):
        return normalize_extension(str(layout["target"]))
    raise ComposeError("missing_target", "layout needs a target format or a machine brand")


def compose_layout(files: dict[str, bytes], layout: dict) -> tuple[ConversionResult, ComposeReport]:
    if not isinstance(layout, dict) or not isinstance(layout.get("items"), list) or not layout["items"]:
        raise ComposeError("bad_layout", "layout must have a non-empty items list")
    if len(layout["items"]) > MAX_ITEMS:
        raise ComposeError("bad_layout", f"at most {MAX_ITEMS} items")
    if len(files) > MAX_FILES:
        raise ComposeError("bad_layout", f"at most {MAX_FILES} files")

    loaded: dict[str, object] = {}

    def design(name: str):
        if name not in files:
            raise ComposeError("missing_file", f"layout refers to {name!r}, which was not uploaded")
        if name not in loaded:
            loaded[name] = load_design(files[name], name)
        return loaded[name]

    alphabets: dict[str, Alphabet] = {}
    for key, names in (layout.get("alphabets") or {}).items():
        if not isinstance(names, list):
            raise ComposeError("bad_layout", f"alphabet {key!r} must be a list of file names")
        alphabets[key] = Alphabet.from_patterns(
            {name.rsplit(".", 1)[0].rsplit("/", 1)[-1]: design(name) for name in names}, key
        )

    placements: list[Placement] = []
    for n, item in enumerate(layout["items"]):
        if not isinstance(item, dict):
            raise ComposeError("bad_layout", f"item {n + 1} must be an object")
        kind = item.get("type", "design")
        x = _number(item, "x_mm", 0.0, -1000, 1000)
        y = _number(item, "y_mm", 0.0, -1000, 1000)
        thread = _thread(item)
        allow = bool(item.get("allow_large_resize", False))
        if kind == "design":
            placements.append(Placement(
                design(str(item.get("file", ""))),
                x_mm=x, y_mm=y,
                rotate_degrees=_number(item, "rotate", 0.0, -360, 360),
                scale=_number(item, "scale", 1.0, 0.1, 10),
                mirror=bool(item.get("mirror", False)),
                thread=thread,
                label=str(item.get("file")),
                allow_large_resize=allow,
            ))
        elif kind == "text":
            # "alphabet" may list several sizes of one font; the size nearest
            # height_mm is used instead of stretching letters (wiki L5).
            keys = item.get("alphabet", "")
            keys = keys if isinstance(keys, list) else [keys]
            if not keys or any(str(k) not in alphabets for k in keys):
                raise ComposeError("bad_layout", f"item {n + 1}: unknown alphabet {item.get('alphabet')!r}")
            choices = {str(k): alphabets[str(k)] for k in keys}
            if len(choices) > 1 and item.get("height_mm"):
                alphabet = choose_alphabet(choices, _number(item, "height_mm", 0, 2, 300))
            else:
                alphabet = next(iter(choices.values()))
            text = item.get("text")
            if not isinstance(text, str) or len(text) > 200:
                raise ComposeError("bad_layout", "text must be a string of at most 200 characters")
            align = item.get("align", "center")
            if align not in ("left", "center", "right"):
                raise ComposeError("bad_layout", "align must be left, center or right")
            letters = layout_text(
                alphabet, text, x_mm=x, y_mm=y,
                height_mm=item.get("height_mm") and _number(item, "height_mm", 0, 2, 300),
                letter_spacing_mm=item.get("letter_spacing_mm") and _number(item, "letter_spacing_mm", 0, 0, 100),
                word_spacing_mm=item.get("word_spacing_mm") and _number(item, "word_spacing_mm", 0, 0, 200),
                line_spacing_mm=item.get("line_spacing_mm") and _number(item, "line_spacing_mm", 0, 0, 200),
                align=align, thread=thread, allow_large_resize=allow,
            )
            if item.get("below") or item.get("above"):
                # Anchor the text under (or over) everything placed so far, y_mm becoming the gap.
                if not placements:
                    raise ComposeError("bad_layout", f"item {n + 1}: nothing to place the text below/above")
                top, bottom = _vertical_extent(placements)
                t_top, t_bottom = _vertical_extent(letters)
                gap = _number(item, "gap_mm", 5.0, 0, 200)
                shift = (bottom + gap - t_top) if item.get("below") else (top - gap - t_bottom)
                for letter in letters:
                    letter.y_mm += shift - y  # y_mm was used as the text centre; drop it
            placements.extend(letters)
        else:
            raise ComposeError("bad_layout", f"item {n + 1}: unknown type {kind!r}")

    hoop = None
    if layout.get("hoop"):
        hoop = HOOPS.get(str(layout["hoop"]))
        if hoop is None:
            raise ComposeError("unknown_hoop", f"unknown hoop {layout['hoop']!r}")

    pattern, report = compose(placements, hoop=hoop)
    result = write_design(pattern, target_extension(layout))
    return result, report


def report_to_dict(report: ComposeReport) -> dict:
    return {
        "width_mm": report.width_mm,
        "height_mm": report.height_mm,
        "stitch_count": report.stitch_count,
        "color_change_count": report.color_change_count,
        "overlaps": [list(pair) for pair in report.overlaps],
        "fits": None if report.fit is None else report.fit.fits,
        "needs_rotation": None if report.fit is None else report.fit.needs_rotation,
        "transforms": {k: {"level": v.level, "messages": v.messages} for k, v in report.transforms.items()},
        "level": report.level,
        "messages": report.messages,
    }

