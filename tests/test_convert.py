import pytest

from eeganizer_files import DesignError, analyze, convert, load_design, write_design
from eeganizer_files.formats import WRITABLE

MACHINE_FORMATS = ["pes", "dst", "jef", "exp", "vp3", "xxx", "u01", "pec", "sew", "tbf"]


@pytest.mark.parametrize("ext", MACHINE_FORMATS)
def test_round_trip_keeps_geometry(pattern, ext):
    assert ext in WRITABLE
    original = analyze(pattern)
    data = write_design(pattern, ext).data
    reloaded = analyze(load_design(data, ext))
    assert reloaded.stitch_count >= original.stitch_count  # writers may split, never drop
    assert reloaded.width_mm == pytest.approx(original.width_mm, abs=0.5)
    assert reloaded.height_mm == pytest.approx(original.height_mm, abs=0.5)


def test_color_formats_keep_colors(pattern):
    data = write_design(pattern, "vp3").data
    info = analyze(load_design(data, "vp3"))
    assert [t.hex_color for t in info.threads] == ["#ff0000", "#0000ff"]


def test_dst_warns_about_lost_colors(pes_bytes):
    result = convert(pes_bytes, "pes", "dst")
    assert result.extension == "dst"
    assert any("thread colors" in w for w in result.warnings)


def test_pes_version_choice(pattern):
    assert write_design(pattern, "pes", pes_version=1).data[:8] == b"#PES0001"
    assert write_design(pattern, "pes", pes_version=6).data[:8] == b"#PES0060"
    with pytest.raises(DesignError):
        write_design(pattern, "pes", pes_version=5)


@pytest.mark.parametrize(
    "data,ext,code",
    [
        (b"not an embroidery file at all", "pes", None),
        (b"", "dst", None),
        (b"x", "art", "unreadable_format"),
        (b"x", "docx", "unsupported_format"),
    ],
)
def test_bad_input_raises_design_error(data, ext, code):
    with pytest.raises(DesignError) as err:
        load_design(data, ext)
    if code:
        assert err.value.code == code
    else:
        assert err.value.code in {"corrupt", "empty_design"}


def test_size_limit():
    with pytest.raises(DesignError) as err:
        load_design(b"0" * 11, "dst", max_bytes=10)
    assert err.value.code == "too_large"


def test_truncated_file_is_rejected(pes_bytes):
    with pytest.raises(DesignError):
        load_design(pes_bytes[: len(pes_bytes) // 3], "pes")


def test_sew_long_jump_regression(pattern):
    # pystitch's SEW writer overflows on moves > 12.7 mm; our override must split them.
    data = write_design(pattern, "sew").data
    assert analyze(load_design(data, "sew")).height_mm == 30.0
