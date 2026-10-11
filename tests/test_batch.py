import io
import json
import zipfile

from fastapi.testclient import TestClient

from eeganizer_files import analyze, load_design, write_design
from eeganizer_files.service import create_app

AUTH = {"Authorization": "Bearer t"}


def test_batch_export_zip(pattern, pes_bytes):
    client = TestClient(create_app(token="t"))
    files = [
        ("files", ("Rose.pes", pes_bytes)),
        ("files", ("rose.dst", write_design(pattern, "dst").data)),  # same name on a FAT32 USB stick
        ("files", ("broken.pes", b"#PES0001 not really")),
    ]
    r = client.post("/v1/export-batch?machine=janome&worksheets=true", headers=AUTH, files=files)
    assert r.status_code == 200, r.text
    assert r.headers["x-eefile-converted"] == "2" and r.headers["x-eefile-failed"] == "1"
    archive = zipfile.ZipFile(io.BytesIO(r.content))
    names = set(archive.namelist())
    assert {"Rose.jef", "rose (2).jef", "eeganizer-export.json"} <= names
    assert "thread charts/Rose.html" in names
    assert analyze(load_design(archive.read("Rose.jef"), "jef")).width_mm == 80.0
    report = json.loads(archive.read("eeganizer-export.json"))
    assert report["target"] == "jef"
    assert [e["error"] is None for e in report["files"]] == [True, True, False]


def test_batch_limits(pes_bytes):
    client = TestClient(create_app(token="t"))
    files = [("files", (f"d{i}.pes", pes_bytes)) for i in range(101)]
    assert client.post("/v1/export-batch?target=dst", headers=AUTH, files=files).status_code == 400
    assert client.post("/v1/export-batch", headers=AUTH, files=files[:1]).json()["error"] == "missing_target"
