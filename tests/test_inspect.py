import pystitch

from eeganizer_files import analyze
from eeganizer_files.inspect import stitch_lengths


def test_dimensions_ignore_jumps(pattern):
    # Add a far-away jump that must not count toward size.
    pattern.stitches.insert(0, [5000, 5000, pystitch.JUMP])
    info = analyze(pattern)
    assert info.width_mm == 80.0
    assert info.height_mm == 30.0


def test_counts_and_threads(pattern):
    info = analyze(pattern)
    assert info.stitch_count == pattern.count_stitch_commands(pystitch.STITCH)
    assert info.color_change_count == 1
    assert info.trim_count == 1
    assert [t.hex_color for t in info.threads] == ["#ff0000", "#0000ff"]
    assert info.threads[0].stitch_count + info.threads[1].stitch_count == info.stitch_count
    assert info.estimated_sew_minutes > 0
    assert info.to_dict()["width_in"] == round(80 / 25.4, 2)


def test_stitch_lengths_skip_jump_moves(pattern):
    lengths = stitch_lengths(pattern)
    # The 50 mm jump to the square must not count as a stitch.
    assert max(lengths) < 6.0
    assert analyze(pattern).longest_stitch_mm == round(max(lengths), 2)
