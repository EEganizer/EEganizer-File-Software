import pytest

from eeganizer_files import analyze, transform


def test_small_resize_is_ok(pattern):
    new, report = transform(pattern, scale=1.05)
    assert report.level == "ok"
    assert analyze(new).width_mm == pytest.approx(84.0, abs=0.2)
    assert report.density_factor == pytest.approx(1 / 1.05**2, abs=1e-3)


def test_caution_band(pattern):
    _, report = transform(pattern, scale=1.15)
    assert report.level == "caution"


def test_large_resize_blocked_unless_forced(pattern):
    new, report = transform(pattern, scale=2.0)
    assert report.blocked and new is None
    new, report = transform(pattern, scale=2.0, allow_large_resize=True)
    assert new is not None and report.level == "warning"


def test_enlarging_flags_long_stitches(pattern):
    # 3 mm stitches x 4.5 = 13.5 mm > 12.1 mm limit.
    _, report = transform(pattern, scale=4.5, allow_large_resize=True, target_extension="dst")
    assert report.long_stitch_count > 0
    assert report.max_stitch_mm == 12.1


def test_shrinking_flags_short_stitches(pattern):
    _, report = transform(pattern, scale=0.15, allow_large_resize=True)
    assert report.short_stitch_count > 0


def test_lace_never_resized(pattern):
    new, report = transform(pattern, scale=1.02, free_standing_lace=True)
    assert report.blocked and new is None
    # rotating lace is fine
    new, report = transform(pattern, rotate_degrees=90, free_standing_lace=True)
    assert new is not None


def test_target_width_keeps_aspect(pattern):
    new, report = transform(pattern, target_width_mm=88.0)
    info = analyze(new)
    assert info.width_mm == pytest.approx(88.0, abs=0.2)
    assert info.height_mm == pytest.approx(33.0, abs=0.2)
    assert report.scale_x == report.scale_y


def test_rotate_swaps_dimensions(pattern):
    new, _ = transform(pattern, rotate_degrees=90)
    info = analyze(new)
    assert info.width_mm == pytest.approx(30.0, abs=0.2)
    assert info.height_mm == pytest.approx(80.0, abs=0.2)


def test_mirror_keeps_size_and_original_untouched(pattern):
    before = [list(s) for s in pattern.stitches]
    new, report = transform(pattern, mirror_horizontal=True)
    assert report.mirrored
    assert analyze(new).width_mm == analyze(pattern).width_mm
    assert [list(s) for s in pattern.stitches] == before


def test_exact_band_edges(pattern):
    assert transform(pattern, scale=1.10)[1].level == "ok"
    assert transform(pattern, scale=0.80)[1].level == "caution"


def test_existing_short_stitches_not_blamed(pattern):
    import pystitch

    # A tie-in: two 0.2 mm stitches already in the design.
    pattern.stitches[2:2] = [[0, 2, pystitch.STITCH], [0, 4, pystitch.STITCH]]
    _, report = transform(pattern, scale=1.05)
    assert report.short_stitch_count == 0 and report.level == "ok"
