"""Child-process entry point used by ``sandbox``. Reads one JSON request on
stdin, writes one JSON response on stdout. Not a public API."""

from __future__ import annotations

import base64
import json
import sys

from .convert import write_design
from .design import DesignError, load_design
from .hoops import HOOPS, check_fit, smallest_hoop
from .inspect import analyze
from .render import render_png


def _handle(request: dict) -> dict:
    data = base64.b64decode(request["data"])
    params = request.get("params", {})
    pattern = load_design(data, request["extension"])
    op = request["op"]

    if op == "info":
        info = analyze(pattern)
        best = smallest_hoop(info)
        return {"info": info.to_dict(), "smallest_hoop": best.hoop.key if best else None}
    if op == "convert":
        result = write_design(pattern, params["target"], pes_version=params.get("pes_version", 6))
        return {"data": base64.b64encode(result.data).decode(), "extension": result.extension, "warnings": result.warnings}
    if op == "preview_png":
        return {"data": base64.b64encode(render_png(pattern, fancy=params.get("fancy", True))).decode()}
    if op == "fit":
        info = analyze(pattern)
        fit = check_fit(info, HOOPS[params["hoop"]])
        return {"fits": fit.fits, "needs_rotation": fit.needs_rotation, "scale_to_fit": fit.scale_to_fit}
    raise ValueError(f"unknown op {op!r}")


def main() -> int:
    try:
        request = json.loads(sys.stdin.buffer.read())
        response = {"ok": True, "result": _handle(request)}
    except DesignError as exc:
        response = {"ok": False, "code": exc.code, "message": str(exc)}
    except Exception as exc:  # never leak tracebacks of untrusted-input failures to callers
        response = {"ok": False, "code": "internal_error", "message": type(exc).__name__}
    sys.stdout.write(json.dumps(response))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
