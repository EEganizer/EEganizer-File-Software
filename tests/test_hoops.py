from eeganizer_files import HOOPS, analyze, check_fit
from eeganizer_files.hoops import smallest_hoop


def test_fits_and_rotation(pattern):
    info = analyze(pattern)  # 80 x 30 mm
    assert check_fit(info, HOOPS["4x4"]).fits
    info.width_mm, info.height_mm = 170.0, 120.0
    fit = check_fit(info, HOOPS["5x7"])  # 130 x 180
    assert fit.fits and fit.needs_rotation


def test_scale_to_fit(pattern):
    info = analyze(pattern)
    info.width_mm, info.height_mm = 192.0, 96.0
    fit = check_fit(info, HOOPS["4x4"], clearance_mm=0)
    assert not fit.fits
    assert fit.scale_to_fit == round(100 / 192, 3)


def test_smallest_hoop(pattern):
    info = analyze(pattern)
    info.width_mm, info.height_mm = 150.0, 150.0
    assert smallest_hoop(info).hoop.key == "8x8"
    info.width_mm = 1000.0
    assert smallest_hoop(info) is None
