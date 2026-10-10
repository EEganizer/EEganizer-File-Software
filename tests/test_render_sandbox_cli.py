import base64
import json

import pytest

from eeganizer_files import load_design, render_png, render_svg
from eeganizer_files.cli import main
from eeganizer_files.sandbox import SandboxError, run_isolated


def test_png_and_svg(pattern):
    assert render_png(pattern)[:8] == b"\x89PNG\r\n\x1a\n"
    assert b"<svg" in render_svg(pattern)


def test_sandbox_info(pes_bytes):
    result = run_isolated("info", pes_bytes, "pes")
    assert result["info"]["width_mm"] == 80.0
    assert result["smallest_hoop"] == "4x4"


def test_sandbox_convert(pes_bytes):
    result = run_isolated("convert", pes_bytes, "pes", {"target": "jef"})
    load_design(base64.b64decode(result["data"]), "jef")


def test_sandbox_reports_design_errors():
    with pytest.raises(SandboxError) as err:
        run_isolated("info", b"garbage", "dst")
    assert err.value.code in {"corrupt", "empty_design"}


def test_sandbox_memory_limit(pes_bytes):
    with pytest.raises(SandboxError):
        run_isolated("info", pes_bytes, "pes", memory_bytes=8 * 1024 * 1024)


def test_cli_round_trip(tmp_path, pes_bytes, capsys):
    src = tmp_path / "design.pes"
    src.write_bytes(pes_bytes)
    assert main(["info", str(src)]) == 0
    assert json.loads(capsys.readouterr().out)["thread_count"] == 2
    assert main(["convert", str(src), str(tmp_path / "out.jef")]) == 0
    assert main(["resize", str(src), str(tmp_path / "big.pes"), "--scale", "1.5"]) == 2
    assert main(["preview", str(src), str(tmp_path / "p.png")]) == 0
    assert main(["fit", str(src), "--hoop", "4x4"]) == 0


def test_render_does_not_mutate_input(pattern):
    before = [list(s) for s in pattern.stitches]
    render_png(pattern)
    render_svg(pattern)
    assert [list(s) for s in pattern.stitches] == before
