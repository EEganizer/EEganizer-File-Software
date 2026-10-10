"""A tiny synthetic stroke alphabet for lettering tests (satin zigzag along polylines)."""

import math

import pystitch

# Strokes per glyph on a grid: x 0..4, y 0..6 (y down; baseline y=6, x-height y=3, descender to y=8).
GLYPHS = {
    "E": [[(4, 0), (0, 0), (0, 6), (4, 6)], [(0, 3), (3, 3)]],
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    "I": [[(2, 0), (2, 6)]],
    "l": [[(1, 0), (1, 6)]],
    "a": [[(3, 3), (3, 6)], [(3, 3), (0, 3), (0, 6), (3, 6)]],
    "i": [[(1, 3), (1, 6)]],
    "g": [[(3, 3), (3, 8), (0, 8)], [(3, 3), (0, 3), (0, 6), (3, 6)]],
    "y": [[(0, 3), (0, 6), (3, 6)], [(3, 3), (3, 8), (0, 8)]],
    "!": [[(1, 0), (1, 4)], [(1, 5.4), (1, 6)]],
}
UNIT = 25  # 2.5 mm per grid unit -> 15 mm capitals
WIDTH = 8  # satin column width in 0.1 mm


def _satin(pattern, a, b):
    ax, ay, bx, by = a[0] * UNIT, a[1] * UNIT, b[0] * UNIT, b[1] * UNIT
    length = math.dist((ax, ay), (bx, by))
    steps = max(int(length / 4), 1)
    nx, ny = -(by - ay) / (length or 1) * WIDTH / 2, (bx - ax) / (length or 1) * WIDTH / 2
    for i in range(steps + 1):
        t = i / steps
        x, y = ax + (bx - ax) * t, ay + (by - ay) * t
        side = 1 if i % 2 else -1
        pattern.add_stitch_absolute(pystitch.STITCH, x + nx * side, y + ny * side)


def make_letter(char, color="#202020"):
    p = pystitch.EmbPattern()
    p.add_thread(pystitch.EmbThread(color))
    for stroke in GLYPHS[char]:
        p.add_stitch_absolute(pystitch.JUMP, stroke[0][0] * UNIT, stroke[0][1] * UNIT)
        for a, b in zip(stroke, stroke[1:]):
            _satin(p, a, b)
        p.add_command(pystitch.TRIM)
    p.add_command(pystitch.END)
    return p


def make_alphabet(names=None):
    from eeganizer_files.lettering import Alphabet

    names = names or {c: ("exclamation" if c == "!" else c) for c in GLYPHS}
    return Alphabet.from_patterns({names[c]: make_letter(c) for c in names})
