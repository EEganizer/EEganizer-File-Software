import pystitch
import pytest


def make_pattern() -> pystitch.EmbPattern:
    """Two-color test design: a 40 x 20 mm zigzag fill, then a 30 mm running-stitch square."""
    p = pystitch.EmbPattern()
    p.add_thread(pystitch.EmbThread("#ff0000", description="Red", brand="Test", catalog_number="100"))
    p.add_thread(pystitch.EmbThread("#0000ff", description="Blue", brand="Test", catalog_number="200"))

    # Block 1: zigzag columns 0.4 mm apart, 20 mm tall -> stitch length ~20 mm is too long,
    # so use 5 mm rows instead (like a tatami fill).
    x = 0
    p.add_stitch_absolute(pystitch.JUMP, 0, 0)
    for row in range(0, 201, 4):  # y in 0.1 mm, rows 0.4 mm apart
        for col in range(0, 401, 30):  # 3 mm stitches across 40 mm
            px = col if (row // 4) % 2 == 0 else 400 - col
            p.add_stitch_absolute(pystitch.STITCH, px, row)
    p.add_command(pystitch.TRIM)
    p.add_command(pystitch.COLOR_CHANGE)

    # Block 2: running stitch square 30 mm, 2.5 mm stitches, offset to the right.
    p.add_stitch_absolute(pystitch.JUMP, 500, 0)
    for edge in range(4):
        for i in range(1, 13):
            d = i * 25
            pts = [(500 + d, 0), (800, d), (800 - d, 300), (500, 300 - d)]
            p.add_stitch_absolute(pystitch.STITCH, *pts[edge])
    p.add_command(pystitch.END)
    return p


@pytest.fixture
def pattern():
    return make_pattern()


@pytest.fixture
def pes_bytes(pattern):
    from eeganizer_files import write_design

    return write_design(pattern, "pes").data
