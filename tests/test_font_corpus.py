"""Checks against a real embroidery alphabet pack kept outside the repository.

Set EEFILE_FONT_DIR to an unpacked pack (folders per size and format, one
file per character). Skipped otherwise.
"""

import collections
import os

import pytest

from eeganizer_files import analyze
from eeganizer_files.compose import compose
from eeganizer_files.lettering import Alphabet, choose_alphabet, layout_text

FONT_DIR = os.environ.get("EEFILE_FONT_DIR")
pytestmark = pytest.mark.skipif(not FONT_DIR, reason="EEFILE_FONT_DIR not set")


@pytest.fixture(scope="module")
def alphabets():
    found = Alphabet.discover(FONT_DIR)
    assert found, "no alphabets found"
    return found


def _size_key(name):
    return name.rsplit("/", 1)[0] if "/" in name else name.rsplit(" [", 1)[0]


def test_every_format_has_the_same_characters(alphabets):
    by_size = collections.defaultdict(dict)
    for name, alphabet in alphabets.items():
        by_size[_size_key(name)][name] = set(alphabet.letters)
    for size, sets in by_size.items():
        assert len({frozenset(s) for s in sets.values()}) == 1, f"{size}: formats disagree on characters"


def test_letters_match_across_formats(alphabets):
    by_size = collections.defaultdict(list)
    for name, alphabet in alphabets.items():
        by_size[_size_key(name)].append(alphabet)
    for size, group in by_size.items():
        ref = group[0]
        for other in group[1:]:
            for char, pattern in ref.letters.items():
                a, b = analyze(pattern), analyze(other.letters[char])
                # A repaired PES letter can lose the stitch next to its stray byte.
                repaired = "eefile_repaired" in pattern.extras or "eefile_repaired" in other.letters[char].extras
                tol = 1.0 if repaired else 0.3
                assert a.width_mm == pytest.approx(b.width_mm, abs=tol), (size, other.name, char)
                assert a.height_mm == pytest.approx(b.height_mm, abs=tol), (size, other.name, char)


@pytest.mark.parametrize("word", ["Benjamin", "Ella", "Hello World!"])
def test_names_sew_in_one_color(alphabets, word):
    for alphabet in alphabets.values():
        if alphabet.missing(word):
            continue
        out, report = compose(layout_text(alphabet, word, thread="#1f4e79"))
        assert report.color_change_count == 0
        assert analyze(out).height_mm <= alphabet.cap_height / 10 * 1.6


def test_size_choice(alphabets):
    caps = sorted(a.cap_height for a in alphabets.values())
    for target in (caps[0] / 10, caps[-1] / 10):
        chosen = choose_alphabet(alphabets, target)
        assert abs(chosen.cap_height / 10 - target) < 1.0
