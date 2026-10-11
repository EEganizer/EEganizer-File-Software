"""PES files with a stray byte before the PEC end marker (seen in a commercial alphabet pack)."""

import struct

import pystitch

from eeganizer_files import analyze, load_design, write_design


def _with_stray_byte(pes: bytes) -> bytes:
    pec = struct.unpack_from("<I", pes, 8)[0]
    block_length = pes[pec + 514] | pes[pec + 515] << 8 | pes[pec + 516] << 16
    end = pec + 512 + block_length
    marker = pes.rfind(b"\xff\x00", 0, end + 1)
    assert marker > pec
    data = bytearray(pes)
    data[marker:marker] = b"\x7b"  # a lone 7-bit byte: the decoder now reads FF 00 as a long y value
    block_length += 1
    data[pec + 514:pec + 517] = bytes([block_length & 0xFF, block_length >> 8 & 0xFF, block_length >> 16])
    return bytes(data)


def test_stray_byte_is_repaired(pattern):
    good = write_design(pattern, "pes", pes_version=1).data
    bad = _with_stray_byte(good)

    naive = pystitch.EmbPattern()
    import io

    pystitch.PesReader.read(io.BytesIO(bad), naive, {})
    from eeganizer_files.inspect import stitch_bounds

    b = stitch_bounds(naive)
    assert (b[3] - b[1]) / 10 > 40  # the naive read runs into the thumbnail bytes

    repaired = load_design(bad, "pes")
    assert repaired.extras["eefile_repaired"].startswith("pec_block_overrun")
    info = analyze(repaired)
    assert info.width_mm == analyze(pattern).width_mm
    assert info.height_mm == analyze(pattern).height_mm


def test_clean_files_untouched(pattern):
    p = load_design(write_design(pattern, "pes").data, "pes")
    assert "eefile_repaired" not in p.extras
