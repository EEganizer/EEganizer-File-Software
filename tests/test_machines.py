import json

import pytest
from fastapi.testclient import TestClient

from eeganizer_files import analyze
from eeganizer_files.machines import CATALOG, MachineProfile, fit_machine, hoops_for_brand, profile_from_dict
from eeganizer_files.service import create_app


def _info(pattern, w, h, stitches=None):
    info = analyze(pattern)
    info.width_mm, info.height_mm = w, h
    if stitches is not None:
        info.stitch_count = stitches
    return info


def test_aliases_share_hoops():
    assert hoops_for_brand("Baby Lock") == hoops_for_brand("brother")
    assert hoops_for_brand("pfaff") == hoops_for_brand("husqvarna_viking")


def test_smallest_fitting_hoop(pattern):
    fit = fit_machine(_info(pattern, 98.6, 90.2), MachineProfile("PE800", "brother"))
    assert fit.fits and fit.hoop.key == "brother:4x4" and fit.export_format == "pes"
    fit = fit_machine(_info(pattern, 257.4, 149.8), MachineProfile("NQ", "brother", ["brother:4x4", "brother:6x10"]))
    assert fit.fits and fit.hoop.key == "brother:6x10" and fit.needs_rotation


def test_too_big_reports_scale(pattern):
    fit = fit_machine(_info(pattern, 200, 100), MachineProfile("PE535", "brother", ["brother:4x4"]))
    assert not fit.fits and fit.scale_to_fit == 0.5 and fit.messages


def test_unconfirmed_hoop_is_flagged(pattern):
    fit = fit_machine(_info(pattern, 90, 60), MachineProfile("B 535", "bernina"))
    assert fit.hoop.key == "bernina:medium" and not fit.hoop.confirmed
    assert any("not yet confirmed" in m for m in fit.messages)


def test_stitch_limit(pattern):
    fit = fit_machine(_info(pattern, 50, 50, 250_000), MachineProfile("Old", "brother", max_stitches=200_000))
    assert not fit.fits


def test_export_format_override_and_validation():
    assert profile_from_dict({"brand": "brother", "export_format": "DST"}).format() == "dst"
    with pytest.raises(ValueError):
        profile_from_dict({"brand": "brother", "hoops": ["janome:nope"]})
    with pytest.raises(ValueError):
        profile_from_dict({"brand": "brother", "export_format": "docx"})
    with pytest.raises(ValueError):
        profile_from_dict({"brand": "acme"})


def test_catalog_keys_unique():
    assert len(CATALOG) == len({h.key for h in CATALOG.values()})


def test_service_fit_machines(pes_bytes):
    client = TestClient(create_app(token="t"))
    auth = {"Authorization": "Bearer t"}
    assert "brother" in client.get("/v1/machines", headers=auth).json()["brands"]
    machines = [{"name": "My PE800", "brand": "brother"}, {"name": "Janome", "brand": "janome", "hoops": ["janome:sq10"]}]
    r = client.post("/v1/fit-machines", headers=auth, files={"file": ("d.pes", pes_bytes)},
                    data={"machines": json.dumps(machines)})
    assert r.status_code == 200, r.text
    body = r.json()
    assert [m["fits"] for m in body["machines"]] == [True, True]
    assert body["machines"][1]["export_format"] == "jef"
    bad = client.post("/v1/fit-machines", headers=auth, files={"file": ("d.pes", pes_bytes)},
                      data={"machines": json.dumps([{"brand": "acme"}])})
    assert bad.status_code == 400 and bad.json()["error"] == "bad_machine"
