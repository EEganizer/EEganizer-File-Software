import json
import struct

import pytest
from fastapi.testclient import TestClient

from eeganizer_files import analyze, load_design
from eeganizer_files.service import create_app

TOKEN = "test-token"
AUTH = {"Authorization": f"Bearer {TOKEN}"}


@pytest.fixture
def client():
    return TestClient(create_app(token=TOKEN))


def upload(data, name="design.pes"):
    return {"file": (name, data, "application/octet-stream")}


def test_refuses_to_start_without_token(monkeypatch):
    monkeypatch.delenv("EEFILE_API_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        create_app()


def test_health_is_public_but_api_needs_token(client):
    assert client.get("/healthz").status_code == 200
    assert client.get("/v1/formats").status_code == 401
    assert client.get("/v1/formats", headers={"Authorization": "Bearer wrong"}).status_code == 401
    body = client.get("/v1/formats", headers=AUTH).json()
    assert "pes" in body["write"] and "hus" in body["read"]
    assert body["machines"]["janome"] == ["jef"]


def test_inspect(client, pes_bytes):
    r = client.post("/v1/inspect", headers=AUTH, files=upload(pes_bytes))
    assert r.status_code == 200
    body = r.json()
    assert body["format"] == "pes"
    assert body["info"]["width_mm"] == 80.0
    assert body["info"]["thread_count"] == 2
    assert body["smallest_hoop"] == "4x4"


def test_thumbnail_size(client, pes_bytes):
    r = client.post("/v1/thumbnail?size=128", headers=AUTH, files=upload(pes_bytes))
    assert r.status_code == 200 and r.headers["content-type"] == "image/png"
    width, height = struct.unpack(">II", r.content[16:24])
    assert max(width, height) <= 130 and max(width, height) >= 120


def test_convert_by_machine(client, pes_bytes):
    r = client.post("/v1/convert?machine=janome", headers=AUTH, files=upload(pes_bytes, "Rose Bouquet.pes"))
    assert r.status_code == 200
    assert 'filename="Rose Bouquet.jef"' in r.headers["content-disposition"]
    assert analyze(load_design(r.content, "jef")).width_mm == 80.0


def test_convert_to_dst_reports_warning(client, pes_bytes):
    r = client.post("/v1/convert?target=dst", headers=AUTH, files=upload(pes_bytes))
    assert r.status_code == 200
    assert "thread colors" in json.loads(r.headers["x-eefile-warnings"])[0]


@pytest.mark.parametrize(
    "query,status,code",
    [
        ("", 400, "missing_target"),
        ("?target=docx", 415, "unsupported_format"),
        ("?machine=acme", 400, "unknown_machine"),
    ],
)
def test_convert_bad_targets(client, pes_bytes, query, status, code):
    r = client.post(f"/v1/convert{query}", headers=AUTH, files=upload(pes_bytes))
    assert r.status_code == status and r.json()["error"] == code


def test_bad_uploads(client):
    r = client.post("/v1/inspect", headers=AUTH, files=upload(b"junk", "design"))
    assert r.json()["error"] == "missing_extension"
    r = client.post("/v1/inspect", headers=AUTH, files=upload(b"junk", "design.art"))
    assert r.status_code == 415 and r.json()["error"] == "unreadable_format"
    r = client.post("/v1/inspect", headers=AUTH, files=upload(b"junk", "design.dst"))
    assert r.status_code == 422


def test_upload_size_limit(pes_bytes):
    small = TestClient(create_app(token=TOKEN, max_upload_bytes=100))
    r = small.post("/v1/inspect", headers=AUTH, files=upload(pes_bytes))
    assert r.status_code == 413


def test_fit(client, pes_bytes):
    r = client.post("/v1/fit?hoop=4x4", headers=AUTH, files=upload(pes_bytes))
    assert r.json()["fits"] is True
    assert client.post("/v1/fit?hoop=99x99", headers=AUTH, files=upload(pes_bytes)).status_code == 400


def test_transform_ok_and_blocked(client, pes_bytes):
    r = client.post("/v1/transform?scale=1.05", headers=AUTH, files=upload(pes_bytes))
    assert r.status_code == 200
    report = json.loads(r.headers["x-eefile-transform-report"])
    assert report["level"] == "ok"
    assert analyze(load_design(r.content, "pes")).width_mm == pytest.approx(84.0, abs=0.2)

    r = client.post("/v1/transform?scale=1.5", headers=AUTH, files=upload(pes_bytes))
    assert r.status_code == 422 and r.json()["report"]["blocked"] is True

    r = client.post("/v1/transform?rotate=90&machine=janome", headers=AUTH, files=upload(pes_bytes))
    assert r.status_code == 200
    assert analyze(load_design(r.content, "jef")).height_mm == pytest.approx(80.0, abs=0.2)
