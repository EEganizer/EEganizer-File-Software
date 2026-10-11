import json

import pystitch
import pytest
from alphabet_helpers import make_alphabet, make_letter
from conftest import make_pattern

from eeganizer_files import HOOPS, analyze, load_design, write_design
from eeganizer_files.compose import ComposeError, Placement, compose
from eeganizer_files.inspect import stitch_bounds
from eeganizer_files.layout import compose_layout
from eeganizer_files.lettering import Alphabet, layout_text, parse_letter_name


def test_compose_two_designs(pattern):
    out, report = compose([Placement(pattern, 0, 0, label="a"), Placement(make_pattern(), 0, 40, label="b")])
    info = analyze(out)
    assert info.width_mm == 80.0
    assert info.height_mm == pytest.approx(70.0, abs=0.2)
    assert info.stitch_count == 2 * analyze(pattern).stitch_count
    # red, blue, red, blue -> 3 color stops
    assert info.color_change_count == 3
    assert report.overlaps == []
    # centred on the origin
    min_x, min_y, max_x, max_y = stitch_bounds(out)
    assert abs(min_x + max_x) < 1 and abs(min_y + max_y) < 1


def test_overlap_and_hoop(pattern):
    _, report = compose([Placement(pattern, 0, 0, label="a"), Placement(make_pattern(), 10, 10, label="b")],
                        hoop=HOOPS["4x4"])
    assert report.overlaps == [("a", "b")]
    assert report.fit.fits
    _, report = compose([Placement(pattern, 0, 0), Placement(make_pattern(), 0, 90)], hoop=HOOPS["4x4"])
    assert not report.fit.fits and report.messages


def test_same_color_letters_sew_without_stops():
    text = layout_text(make_alphabet(), "Ella", thread="#c0392b")
    out, report = compose(text)
    assert report.color_change_count == 0
    assert [t.hex_color() for t in out.threadlist] == ["#c0392b"]


def test_recolor_does_not_touch_source(pattern):
    compose([Placement(pattern, thread="#00ff00")])
    assert pattern.threadlist[0].hex_color() == "#ff0000"


def test_blocked_resize_raises(pattern):
    with pytest.raises(ComposeError) as err:
        compose([Placement(pattern, scale=2.0)])
    assert err.value.code == "transform_blocked"


@pytest.mark.parametrize(
    "stem,char",
    [("A", "A"), ("a_lower", "a"), ("Upper B", "B"), ("Script_A", "A"), ("lower_z", "z"),
     ("seven", "7"), ("Font 3", "3"), ("question mark", "?"), ("exclamation", "!"),
     ("Brand", None), ("4x4 Panda Bear", None)],
)
def test_letter_names(stem, char):
    assert parse_letter_name(stem) == char


def test_baseline_and_descenders():
    ab = make_alphabet()
    items = layout_text(ab, "Ely", y_mm=0)
    out, _ = compose(items)
    tops_bottoms = {}
    for item in items:
        b = stitch_bounds(item.pattern)
        h = (b[3] - b[1]) / 10
        tops_bottoms[item.label] = (item.y_mm - h / 2, item.y_mm + h / 2)
    # E and l sit on the same baseline; y hangs below it and its top is at x-height.
    assert tops_bottoms["'E'"][1] == pytest.approx(tops_bottoms["'l'"][1])
    assert tops_bottoms["'y'"][1] > tops_bottoms["'E'"][1] + 3
    assert tops_bottoms["'y'"][0] > tops_bottoms["'E'"][0] + 3


def test_letter_spacing_and_lines():
    ab = make_alphabet()
    one = layout_text(ab, "II", letter_spacing_mm=5)
    assert one[1].x_mm - one[0].x_mm == pytest.approx(5 + 0.8, abs=0.05)
    two = layout_text(ab, "I\nI")
    assert two[1].y_mm > two[0].y_mm + 15
    left = layout_text(ab, "II", align="left", x_mm=10)
    assert left[0].x_mm == pytest.approx(10 + 0.4, abs=0.05)


def test_height_resizes_letters():
    # Capital height is the alphabet's median capital (E, H, I = 15 mm).
    out, _ = compose(layout_text(make_alphabet(), "I", height_mm=16.5))
    assert analyze(out).height_mm == pytest.approx(16.5, abs=0.2)
    with pytest.raises(ComposeError):
        compose(layout_text(make_alphabet(), "E", height_mm=30))  # 100% larger: blocked at compose


def test_missing_letters():
    with pytest.raises(ComposeError) as err:
        layout_text(make_alphabet(), "Hello")
    assert err.value.code == "missing_letters" and "h" in str(err.value) and "o" in str(err.value)


def _letter_files():
    return {f"{n}.pes": write_design(make_letter(c), "pes").data
            for c, n in [("E", "E"), ("l", "l_lower"), ("a", "a_lower"), ("!", "exclamation")]}


def test_compose_layout_document(pattern):
    files = {"design.pes": write_design(pattern, "pes").data, **_letter_files()}
    layout = {
        "items": [
            {"type": "design", "file": "design.pes", "x_mm": 0, "y_mm": 0},
            {"type": "text", "text": "Ella!", "alphabet": "block", "y_mm": 30, "thread": "#c0392b"},
        ],
        "alphabets": {"block": [n for n in files if n != "design.pes"]},
        "machine": "janome",
        "hoop": "5x7",
    }
    result, report = compose_layout(files, layout)
    assert result.extension == "jef"
    info = analyze(load_design(result.data, "jef"))
    assert info.color_change_count == 2  # red, blue, then lettering
    assert report.fit.fits


@pytest.mark.parametrize(
    "layout,code",
    [
        ({"items": []}, "bad_layout"),
        ({"items": [{"type": "design", "file": "nope.pes"}], "target": "pes"}, "missing_file"),
        ({"items": [{"type": "design", "file": "design.pes", "scale": "big"}], "target": "pes"}, "bad_layout"),
        ({"items": [{"type": "design", "file": "design.pes", "thread": "red"}], "target": "pes"}, "bad_layout"),
        ({"items": [{"type": "text", "text": "E", "alphabet": "x"}], "target": "pes"}, "bad_layout"),
        ({"items": [{"type": "design", "file": "design.pes"}]}, "missing_target"),
        ({"items": [{"type": "design", "file": "design.pes"}], "target": "pes", "hoop": "1x1"}, "unknown_hoop"),
    ],
)
def test_layout_validation(pattern, layout, code):
    with pytest.raises(ComposeError) as err:
        compose_layout({"design.pes": write_design(pattern, "pes").data}, layout)
    assert err.value.code == code


def test_service_compose(pattern):
    from fastapi.testclient import TestClient

    from eeganizer_files.service import create_app

    client = TestClient(create_app(token="t"))
    letters = _letter_files()
    files = [("files", ("design.pes", write_design(pattern, "pes").data, "application/octet-stream"))]
    files += [("files", (name, data, "application/octet-stream")) for name, data in letters.items()]
    layout = {
        "name": "Ella pillow",
        "items": [{"file": "design.pes"}, {"type": "text", "text": "Ella", "alphabet": "a", "y_mm": 30}],
        "alphabets": {"a": list(letters)},
        "machine": "brother",
        "hoop": "4x4",
    }
    r = client.post("/v1/compose", headers={"Authorization": "Bearer t"}, files=files,
                    data={"layout": json.dumps(layout)})
    assert r.status_code == 200, r.text
    assert 'filename="Ella pillow.pes"' in r.headers["content-disposition"]
    report = json.loads(r.headers["x-eefile-compose-report"])
    assert report["fits"] is True
    assert analyze(load_design(r.content, "pes")).stitch_count > analyze(pattern).stitch_count

    bad = client.post("/v1/compose", headers={"Authorization": "Bearer t"}, files=files,
                      data={"layout": json.dumps({**layout, "items": [{"type": "text", "text": "Zz", "alphabet": "a"}]})})
    assert bad.status_code == 422 and bad.json()["error"] == "missing_letters"


@pytest.mark.parametrize(
    "stem,char",
    [("JKD101 1.0inch aa", "a"), ("JKD101 0.75inch A", "A"), ("JKD101 0.75inch _Ampersand Symbol", "&"),
     ("JKD101 1.0inch BackSlash Symbol", "\\"), ("JKD101 1.0inch Exclamation Point", "!"),
     ("JKD101 1.5inch Exlamation", "!"), ("JKD101 1.0inch Pound Sign Symbol Hashtag", "#"),
     ("JKD101 1.0inch Question Mark Symbol", "?"), ("JKD101 0.75inch _Period Symbol", "."), ("zz", "z")],
)
def test_alphabet_pack_names(stem, char):
    assert parse_letter_name(stem) == char


def test_all_caps_font_has_no_descenders():
    # Lowercase files as tall as capitals: g/y must sit on the baseline.
    tall = {c: make_letter("E") for c in "Egxy"}
    ab = Alphabet.from_patterns({("gg" if c == "g" else "xx" if c == "x" else "yy" if c == "y" else c): p
                                 for c, p in tall.items()})
    assert not ab.has_descenders
    items = layout_text(ab, "Egy")
    assert len({round(i.y_mm, 3) for i in items}) == 1


def test_choose_alphabet_by_height():
    from eeganizer_files.lettering import choose_alphabet

    small = make_alphabet()
    big = make_alphabet()  # separate letter objects
    for p in big.letters.values():
        p.stitches = [[s[0] * 2, s[1] * 2, s[2]] for s in p.stitches]
    assert choose_alphabet({"s": small, "b": big}, 28) is big
    assert choose_alphabet({"s": small, "b": big}, 16) is small
