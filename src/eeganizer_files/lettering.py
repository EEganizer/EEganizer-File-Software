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
from dataclasses import dataclass, field
from pathlib import Path

import pystitch

from .compose import ComposeError, Placement
from .design import DesignError, load_design_file
from .formats import UNITS_PER_MM, get_format
from .inspect import stitch_bounds

_PUNCTUATION = {
    "exclamation": "!", "exclamationmark": "!", "exclaim": "!",
    "exlamation": "!", "exclamtion": "!", "exclimation": "!",  # seen in real packs
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
    "plus": "+", "slash": "/", "backslash": "\\", "hashtag": "#",
    "openparen": "(", "leftparen": "(", "closeparen": ")", "rightparen": ")",
}
_DIGIT_WORDS = {w: str(i) for i, w in enumerate(
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"])}

# Words some packs add around a symbol's name: "Question Mark Symbol",
# "Exclamation Point", "Pound Sign Symbol Hashtag".
_FILLER = {"symbol", "sign", "point", "mark", "character", "char", "letter", "glyph"}

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
            tokens = [t for t in tokens if t.lower() != marker]
            words = [t.lower() for t in tokens]
            break

    if not tokens:
        return None
    last = tokens[-1]
    lw = last.lower()
    if len(last) == 1 and last.isalnum():
        if case == "upper":
            return last.upper()
        if case == "lower":
            return last.lower()
        return last
    # Lowercase as a doubled letter ("aa.pes"): Windows file names ignore case,
    # so packs can't ship both "A.pes" and "a.pes".
    if len(last) == 2 and last[0] == last[1] and last.isalpha():
        if case == "upper":
            return last[0].upper()
        return last[0].lower() if case == "lower" or last.islower() else last[0]
    if lw in _DIGIT_WORDS:
        return _DIGIT_WORDS[lw]
    while words:
        lw = words[-1]
        if len(words) >= 2 and words[-2] + lw in _PUNCTUATION:  # "question mark"
            return _PUNCTUATION[words[-2] + lw]
        if lw in _PUNCTUATION:
            return _PUNCTUATION[lw]
        if lw in _FILLER:
            words.pop()
            continue
        break
    return None


@dataclass
class Alphabet:
    letters: dict[str, pystitch.EmbPattern]
    name: str = ""
    # File names in the alphabet's folder that matched no character, so the
    # customer can be asked which character they are.
    unrecognized: list[str] = field(default_factory=list)

    @classmethod
    def from_files(cls, paths, name: str = "") -> "Alphabet":
        letters: dict[str, pystitch.EmbPattern] = {}
        for path in map(Path, paths):
            char = parse_letter_name(path.stem)
            if char is None:
                continue
            try:
                letters[char] = load_design_file(path)
            except DesignError:
                continue  # store-only formats (VIP, BX ...) or a broken letter
        return cls(letters, name)

    @classmethod
    def discover(cls, root, min_letters: int = 10) -> dict[str, "Alphabet"]:
        """Find alphabets in an unpacked font pack.

        Packs ship one folder per size and format ("1.0 inch/PES/..."); each
        (folder, format) with at least ``min_letters`` recognised characters
        becomes one alphabet, keyed by its relative folder path and format."""
        root = Path(root)
        groups: dict[tuple[Path, str], list[Path]] = {}
        unknown: dict[tuple[Path, str], list[str]] = {}
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            key = (path.parent, path.suffix.lower())
            if parse_letter_name(path.stem) is not None:
                groups.setdefault(key, []).append(path)
            else:
                unknown.setdefault(key, []).append(path.name)
        found: dict[str, Alphabet] = {}
        for (folder, ext), paths in sorted(groups.items()):
            if len(paths) < min_letters or get_format(ext) is None:
                continue
            key = f"{folder.relative_to(root).as_posix()} [{ext[1:]}]"
            alphabet = cls.from_files(paths, key)
            alphabet.unrecognized = sorted(unknown.get((folder, ext), []))
            if len(alphabet.letters) >= min_letters:
                found[key] = alphabet
        return found

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

    @property
    def has_descenders(self) -> bool:
        """False for all-caps style fonts whose lowercase files are as tall as
        the capitals (then g, j, p, q, y sit on the baseline like every letter)."""
        x = self.x_height
        return x is not None and x < 0.85 * self.cap_height

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
            if char in DESCENDERS and char.isalpha() and alphabet.has_descenders:
                top = -x_height_mm  # top of a g/j/p/q/y sits on the x-height line
            elif char in ",;" and alphabet.has_descenders:
                top = -min(h, x_height_mm * 0.3)  # hangs just below the baseline
            else:
                top = -h  # sits on the baseline
            items.append(Placement(
                alphabet.letters[char], x_mm=cursor + w / 2, y_mm=top + h / 2, scale=scale,
                thread=thread, label=f"'{char}'", allow_large_resize=allow_large_resize,
                text_cap_height_mm=cap_mm,
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


def choose_alphabet(alphabets: dict[str, Alphabet], height_mm: float) -> Alphabet:
    """The alphabet whose capital height is closest (by ratio) to ``height_mm``,
    so lettering is resized as little as possible."""
    import math

    candidates = [a for a in alphabets.values() if a.cap_height > 0]
    if not candidates:
        raise ComposeError("bad_layout", "no usable alphabet")
    return min(candidates, key=lambda a: abs(math.log(height_mm * UNITS_PER_MM / a.cap_height)))
