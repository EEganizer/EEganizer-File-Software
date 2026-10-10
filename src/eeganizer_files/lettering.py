"""Lettering from embroidery alphabet packs.

Embroidery fonts are usually sold as one stitch file per character
("A.pes", "a_lower.pes", "Upper B.jef", "exclamation.dst" ...). This module
recognises those names, lines the letters up on a common baseline with
spacing, and returns placements for ``compose``.

Turning a computer font (TTF) into stitches is auto-digitizing and is out of
scope here.
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass
from pathlib import Path

import pystitch

from .compose import ComposeError, Placement
from .design import load_design_file
from .formats import UNITS_PER_MM
from .inspect import stitch_bounds

_PUNCTUATION = {
    "exclamation": "!", "exclamationmark": "!", "exclaim": "!",
    "question": "?", "questionmark": "?",
    "period": ".", "dot": ".", "fullstop": ".",
    "comma": ",",
    "apostrophe": "'", "quote": "'",
    "doublequote": '"', "quotes": '"',
    "ampersand": "&", "and": "&",
    "hyphen": "-", "dash": "-", "minus": "-",
    "colon": ":", "semicolon": ";",
    "at": "@", "hash": "#", "pound": "#", "number": "#",
    "heart": "♥",
    "plus": "+", "slash": "/",
    "openparen": "(", "leftparen": "(", "closeparen": ")", "rightparen": ")",
}
_DIGIT_WORDS = {w: str(i) for i, w in enumerate(
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"])}

DESCENDERS = set("gjpqy,;")
# Letters whose top sits at the x-height line (no ascender, no descender).
_X_HEIGHT_LETTERS = set("acemnorsuvwxz")


def parse_letter_name(stem: str) -> str | None:
    """Map an alphabet file name (without extension) to its character."""
    s = stem.strip()
    # Many packs prefix the font name: "Script_A", "Block-a_lower", "Ella A".
    tokens = [t for t in re.split(r"[\s_\-\.]+", s) if t]
    if not tokens:
        return None
    words = [t.lower() for t in tokens]

    case = None
    for marker, value in (("upper", "upper"), ("uppercase", "upper"), ("cap", "upper"),
                          ("capital", "upper"), ("lower", "lower"), ("lowercase", "lower"),
                          ("small", "lower")):
        if marker in words:
            case = value
            words.remove(marker)
            tokens = [t for t in tokens if t.lower() != marker]
            break

    last = tokens[-1] if tokens else ""
    lw = last.lower()
    if len(last) == 1 and last.isalnum():
        if case == "upper":
            return last.upper()
        if case == "lower":
            return last.lower()
        return last
    if lw in _DIGIT_WORDS:
        return _DIGIT_WORDS[lw]
    if lw in _PUNCTUATION:
        return _PUNCTUATION[lw]
    if len(words) >= 2 and words[-2] + lw in _PUNCTUATION:  # "question mark"
        return _PUNCTUATION[words[-2] + lw]
    return None


@dataclass
class Alphabet:
    letters: dict[str, pystitch.EmbPattern]
    name: str = ""

    @classmethod
    def from_files(cls, paths, name: str = "") -> "Alphabet":
        letters: dict[str, pystitch.EmbPattern] = {}
        for path in map(Path, paths):
            char = parse_letter_name(path.stem)
            if char is not None:
                letters[char] = load_design_file(path)
        return cls(letters, name)

    @classmethod
    def from_patterns(cls, named: dict[str, pystitch.EmbPattern], name: str = "") -> "Alphabet":
        letters = {}
        for stem, pattern in named.items():
            char = parse_letter_name(stem)
            if char is not None:
                letters[char] = pattern
        return cls(letters, name)

    def _heights(self, chars) -> list[float]:
        out = []
        for c in chars:
            if c in self.letters:
                b = stitch_bounds(self.letters[c])
                out.append(b[3] - b[1])
        return out

    @property
    def cap_height(self) -> float:
        """Typical uppercase height in 0.1 mm units (falls back to all letters)."""
        heights = self._heights([c for c in self.letters if c.isupper()]) or self._heights(
            [c for c in self.letters if c not in DESCENDERS])
        return statistics.median(heights) if heights else 0.0

    @property
    def x_height(self) -> float | None:
        heights = self._heights(_X_HEIGHT_LETTERS)
        return statistics.median(heights) if heights else None

    def missing(self, text: str) -> list[str]:
        return sorted({c for c in text if not c.isspace() and c not in self.letters})


def layout_text(
    alphabet: Alphabet,
    text: str,
    *,
    x_mm: float = 0.0,
    y_mm: float = 0.0,
    height_mm: float | None = None,
    letter_spacing_mm: float | None = None,
    word_spacing_mm: float | None = None,
    line_spacing_mm: float | None = None,
    align: str = "center",
    thread: str | None = None,
    allow_large_resize: bool = False,
) -> list[Placement]:
    """Placements spelling ``text`` (``\\n`` for new lines), centred on (x_mm, y_mm).

    ``height_mm`` resizes the letters to that capital height; it uses the
    same guarded resize as single designs, so alphabets should be bought in
    a size close to what is needed.
    """
    if not text.strip():
        raise ComposeError("empty_text", "no text to stitch")
    missing = alphabet.missing(text)
    if missing:
        raise ComposeError("missing_letters", "the alphabet has no file for: " + " ".join(missing))
    if align not in ("left", "center", "right"):
        raise ValueError("align must be left, center or right")

    cap = alphabet.cap_height / UNITS_PER_MM
    scale = (height_mm / cap) if (height_mm and cap) else 1.0
    cap_mm = cap * scale
    x_height_mm = (alphabet.x_height / UNITS_PER_MM * scale) if alphabet.x_height else cap_mm * 0.65
    gap = letter_spacing_mm if letter_spacing_mm is not None else cap_mm * 0.08
    space = word_spacing_mm if word_spacing_mm is not None else cap_mm * 0.4
    leading = line_spacing_mm if line_spacing_mm is not None else cap_mm * 0.45

    # Lay out each line with baseline at y=0, then position lines.
    lines: list[tuple[float, list[Placement]]] = []
    for line in text.split("\n"):
        cursor = 0.0
        items: list[Placement] = []
        for char in line:
            if char.isspace():
                cursor += space
                continue
            b = stitch_bounds(alphabet.letters[char])
            w = (b[2] - b[0]) / UNITS_PER_MM * scale
            h = (b[3] - b[1]) / UNITS_PER_MM * scale
            if char in DESCENDERS and char.isalpha():
                top = -x_height_mm  # top of a g/j/p/q/y sits on the x-height line
            elif char in ",;":
                top = -min(h, x_height_mm * 0.3)  # hangs just below the baseline
            else:
                top = -h  # sits on the baseline
            items.append(Placement(
                alphabet.letters[char], x_mm=cursor + w / 2, y_mm=top + h / 2, scale=scale,
                thread=thread, label=f"'{char}'", allow_large_resize=allow_large_resize,
            ))
            cursor += w + gap
        width = max(cursor - gap, 0.0) if items else 0.0
        lines.append((width, items))

    block_height = len(lines) * cap_mm + (len(lines) - 1) * leading
    placements: list[Placement] = []
    for index, (width, items) in enumerate(lines):
        offset_x = {"left": 0.0, "center": -width / 2, "right": -width}[align]
        baseline = y_mm - block_height / 2 + cap_mm + index * (cap_mm + leading)
        for item in items:
            item.x_mm += x_mm + offset_x
            item.y_mm += baseline
            placements.append(item)
    return placements
