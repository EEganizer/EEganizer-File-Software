import pystitch
from fastapi.testclient import TestClient

from eeganizer_files import load_design, write_design
from eeganizer_files.service import create_app
from eeganizer_files.worksheet import block_stats, worksheet_html


def test_block_stats_match_threads(pattern):
    stats = block_stats(pattern)
    assert len(stats) == 2
    assert stats[0][0] + stats[1][0] == pattern.count_stitch_commands(pystitch.STITCH)
    assert all(m > 0 for _, m in stats)


def test_worksheet_lists_every_stop(pattern):
    page = worksheet_html(pattern, title="Rose")
    assert page.count("<tr><td class=n>") == 2
    assert "#ff0000" in page and "Test 100 Red" in page and "data:image/png;base64," in page


def test_dst_worksheet_has_rows_without_colors(pattern):
    dst = load_design(write_design(pattern, "dst").data, "dst")
    page = worksheet_html(dst, has_colors=False)
    assert page.count("<tr><td class=n>") == 2
    assert "stores no thread colors" in page


def test_thread_names_are_escaped(pattern):
    pattern.threadlist[0].description = '<script>alert(1)</script>'
    page = worksheet_html(pattern, title="<b>x</b>")
    assert "<script>" not in page and "&lt;script&gt;" in page and "<b>x</b>" not in page


def test_service_worksheet(pes_bytes):
    client = TestClient(create_app(token="t"))
    r = client.post("/v1/worksheet", headers={"Authorization": "Bearer t"}, files={"file": ("Rose.pes", pes_bytes)})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert "default-src 'none'" in r.headers["content-security-policy"]
    assert "<title>Rose" in r.text
