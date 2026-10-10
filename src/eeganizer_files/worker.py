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
from .layout import compose_layout, report_to_dict
from .render import render_png, render_thumbnail
from .transform import transform


def _handle(request: dict) -> dict:
    data = base64.b64decode(request["data"])
    params = request.get("params", {})
    if request["op"] == "compose":
        files = {name: base64.b64decode(blob) for name, blob in params["files"].items()}
        result, report = compose_layout(files, params["layout"])
        return {
            "data": base64.b64encode(result.data).decode(),
            "extension": result.extension,
            "warnings": result.warnings,
            "report": report_to_dict(report),
        }
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
    if op == "thumbnail":
        png = render_thumbnail(pattern, int(params.get("size", 256)), fancy=params.get("fancy", True))
        return {"data": base64.b64encode(png).decode()}
    if op == "transform":
        target = params["target"]
        new, report = transform(
            pattern,
            scale=params.get("scale"),
            target_width_mm=params.get("target_width_mm"),
            target_height_mm=params.get("target_height_mm"),
            rotate_degrees=params.get("rotate_degrees", 0.0),
            mirror_horizontal=params.get("mirror_horizontal", False),
            mirror_vertical=params.get("mirror_vertical", False),
            target_extension=target,
            free_standing_lace=params.get("free_standing_lace", False),
            allow_large_resize=params.get("allow_large_resize", False),
        )
        out = {"report": dict(vars(report), blocked=report.blocked)}
        if new is not None:
            result = write_design(new, target, pes_version=params.get("pes_version", 6))
            out.update(data=base64.b64encode(result.data).decode(), extension=result.extension, warnings=result.warnings)
        return out
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
