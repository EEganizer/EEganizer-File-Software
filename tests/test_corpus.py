"""Checks against real commercial design files.

The files are NOT in this repository (purchased designs may not be
redistributed). Point EEFILE_CORPUS_DIR at a local folder of designs to run
these tests; they are skipped otherwise. The suite expects designs that are
sold in several formats with the same file stem (e.g. "5x7 Whale.PES" and
"5x7 Whale.DST"), and uses the formats as cross-checks for each other.
"""

import collections
import os
import re
from pathlib import Path

import pytest

from eeganizer_files import HOOPS, analyze, check_fit, load_design, load_design_file, write_design
from eeganizer_files.render import render_thumbnail

CORPUS = os.environ.get("EEFILE_CORPUS_DIR")
pytestmark = pytest.mark.skipif(not CORPUS, reason="EEFILE_CORPUS_DIR not set")

DESIGN_EXTENSIONS = {".pes", ".dst", ".exp", ".hus", ".jef", ".vp3", ".xxx", ".sew", ".pec", ".u01"}
COLOR_FORMATS = {"pes", "hus", "jef", "vp3", "xxx", "sew", "pec"}

# Size and distinct-color count printed on the designers' production
# worksheets (Wilcom). Numbers only; keyed by file stem.
WORKSHEETS = {
    "5x7 Panda Bear Zigzag Applique": (125.3, 137.0, 5),
    "5x7 Superhero Dog Sketch Embroidery": (176.0, 111.0, 5),  # 6.93 x 4.37 in
    "4 inch Swimming Dog Circle Applique": (97.0, 96.3, 9),  # 3.82 x 3.79 in
    "5x7 Whale Satin Applique": (174.6, 101.8, 3),
}


def _files():
    if not CORPUS:
        return []
    return sorted(p for p in Path(CORPUS).rglob("*") if p.suffix.lower() in DESIGN_EXTENSIONS)


def _groups():
    groups = collections.defaultdict(dict)
    for path in _files():
        groups[path.stem][path.suffix.lower()[1:]] = path
    return dict(groups)


FILES = _files()
GROUPS = _groups()


def _same_size(a, b, tol=0.25):
    """Equal size, allowing a 90 degree rotation (designers rotate PES/JEF to fit portrait hoops)."""
    straight = abs(a.width_mm - b.width_mm) <= tol and abs(a.height_mm - b.height_mm) <= tol
    rotated = abs(a.width_mm - b.height_mm) <= tol and abs(a.height_mm - b.width_mm) <= tol
    return straight or rotated


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_every_file_reads_and_renders(path):
    info = analyze(load_design_file(path))
    assert info.stitch_count > 0
    assert 0 < info.width_mm < 500 and 0 < info.height_mm < 500
    assert info.longest_stitch_mm <= 12.1
    png = render_thumbnail(load_design_file(path), 128)
    assert png[:8] == b"\x89PNG\r\n\x1a\n"


@pytest.mark.parametrize("stem", sorted(GROUPS), ids=str)
def test_formats_agree(stem):
    infos = {ext: analyze(load_design_file(p)) for ext, p in GROUPS[stem].items()}
    ref_ext = "dst" if "dst" in infos else next(iter(infos))
    ref = infos[ref_ext]
    for ext, info in infos.items():
        assert _same_size(info, ref), f"{ext} size {info.width_mm}x{info.height_mm} vs {ref_ext}"
        assert abs(info.stitch_count - ref.stitch_count) <= max(30, 0.02 * ref.stitch_count), ext
        assert info.color_change_count == ref.color_change_count, ext
        if ext != "vp3":
            # VP3 has no jump command: moves between areas under 12.7 mm are
            # stored as ordinary stitches and cannot be told apart by length.
            assert abs(info.longest_stitch_mm - ref.longest_stitch_mm) <= 0.3, ext
    thread_counts = {info.thread_count for ext, info in infos.items() if ext in COLOR_FORMATS}
    assert len(thread_counts) <= 1


@pytest.mark.parametrize("stem", sorted(GROUPS), ids=str)
def test_fits_the_hoop_in_its_name(stem):
    match = re.match(r"(\d+(?:\.\d+)?x\d+(?:\.\d+)?)\b", stem)
    if not match or match.group(1) not in HOOPS:
        pytest.skip("no hoop size in file name")
    for path in GROUPS[stem].values():
        assert check_fit(analyze(load_design_file(path)), HOOPS[match.group(1)]).fits, path.name


@pytest.mark.parametrize("stem", sorted(set(WORKSHEETS) & set(GROUPS)), ids=str)
def test_matches_designer_worksheet(stem):
    width, height, colors = WORKSHEETS[stem]
    for ext, path in GROUPS[stem].items():
        info = analyze(load_design_file(path))
        assert sorted([info.width_mm, info.height_mm]) == pytest.approx(sorted([width, height]), abs=0.25), ext
        if ext in COLOR_FORMATS:
            # Palettes differ per brand, so count distinct colors on the parsed threads.
            assert info.unique_color_count == colors, ext


@pytest.mark.parametrize("path", [p for p in FILES if p.suffix.lower() == ".pes"], ids=lambda p: p.name)
@pytest.mark.parametrize("target", ["dst", "jef", "vp3", "exp", "xxx", "pes"])
def test_convert_preserves_design(path, target):
    original = analyze(load_design_file(path))
    converted = analyze(load_design(write_design(load_design_file(path), target).data, target))
    assert _same_size(converted, original)
    assert converted.stitch_count >= original.stitch_count
    assert converted.color_change_count == original.color_change_count
