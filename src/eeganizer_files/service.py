"""Private HTTP API used by EEganizer.com.

Stateless: each request carries one design file and gets JSON or a file back.
All parsing happens in ``sandbox.run_isolated``. Run with::

    EEFILE_API_TOKEN=... uvicorn --factory eeganizer_files.service:create_app --host 0.0.0.0 --port 8080
"""

from __future__ import annotations

import base64
import hmac
import json
import os
from pathlib import PurePath

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse, Response

from .formats import KNOWN_UNREADABLE, MACHINE_FORMATS, READABLE, WRITABLE, normalize_extension
from .hoops import HOOPS
from .sandbox import SandboxError, run_isolated

DEFAULT_MAX_UPLOAD_BYTES = 25 * 1024 * 1024

_STATUS_BY_CODE = {
    "unsupported_format": 415,
    "unreadable_format": 415,
    "too_large": 413,
    "corrupt": 422,
    "empty_design": 422,
    "too_many_stitches": 422,
    "crashed": 422,
    "timeout": 504,
    "bad_layout": 400,
    "missing_file": 400,
    "missing_target": 400,
    "unknown_machine": 400,
    "unknown_hoop": 400,
    "empty_layout": 400,
    "empty_text": 400,
    "missing_letters": 422,
    "transform_blocked": 422,
}

_MEDIA_TYPES = {"png": "image/png"}


class ApiError(HTTPException):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(status_code=status, detail={"error": code, "message": message})


def _filename_extension(upload: UploadFile) -> str:
    name = upload.filename or ""
    ext = normalize_extension(PurePath(name).suffix) if PurePath(name).suffix else ""
    if not ext:
        raise ApiError(400, "missing_extension", "uploaded file name must include its format extension")
    return ext


def _resolve_target(target: str | None, machine: str | None) -> str:
    if target:
        ext = normalize_extension(target)
        if ext not in WRITABLE:
            raise ApiError(415, "unsupported_format", f"cannot write .{ext} files")
        return ext
    if machine:
        formats = MACHINE_FORMATS.get(machine.strip().lower())
        if not formats:
            raise ApiError(400, "unknown_machine", f"unknown machine brand {machine!r}")
        return formats[0]
    raise ApiError(400, "missing_target", "give a target format or a machine brand")


def _download_name(filename: str | None, ext: str) -> str:
    stem = PurePath(filename or "design").stem or "design"
    safe = "".join(c for c in stem if c.isalnum() or c in "-_ ").strip() or "design"
    return f"{safe}.{ext}"


def create_app(
    *,
    token: str | None = None,
    allow_no_auth: bool = False,
    max_upload_bytes: int = DEFAULT_MAX_UPLOAD_BYTES,
    sandbox_timeout_s: float = 20.0,
) -> FastAPI:
    token = token if token is not None else os.environ.get("EEFILE_API_TOKEN")
    if not token and not allow_no_auth:
        raise RuntimeError("EEFILE_API_TOKEN is not set; refusing to start without authentication")

    app = FastAPI(title="EEganizer File Service", version="0.2.0")

    def require_token(authorization: str | None = Header(default=None)) -> None:
        if not token:
            return
        expected = f"Bearer {token}"
        if authorization is None or not hmac.compare_digest(authorization.encode(), expected.encode()):
            raise ApiError(401, "unauthorized", "missing or invalid bearer token")

    def read_upload(upload: UploadFile) -> tuple[bytes, str]:
        ext = _filename_extension(upload)
        data = upload.file.read(max_upload_bytes + 1)
        if len(data) > max_upload_bytes:
            raise ApiError(413, "too_large", f"upload exceeds {max_upload_bytes} bytes")
        return data, ext

    def run(op: str, data: bytes, ext: str, params: dict | None = None) -> dict:
        try:
            return run_isolated(op, data, ext, params, timeout_s=sandbox_timeout_s)
        except SandboxError as exc:
            raise ApiError(_STATUS_BY_CODE.get(exc.code, 500), exc.code, str(exc)) from exc

    def file_response(result: dict, filename: str, extra_headers: dict | None = None) -> Response:
        ext = result.get("extension", "png")
        headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
        if result.get("warnings"):
            headers["X-EEfile-Warnings"] = json.dumps(result["warnings"])
        headers.update(extra_headers or {})
        return Response(
            base64.b64decode(result["data"]),
            media_type=_MEDIA_TYPES.get(ext, "application/octet-stream"),
            headers=headers,
        )

    @app.exception_handler(ApiError)
    def _api_error(_request, exc: ApiError):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.get("/healthz")
    def healthz() -> dict:
        return {"ok": True}

    auth = [Depends(require_token)]

    @app.get("/v1/formats", dependencies=auth)
    def formats() -> dict:
        return {
            "read": READABLE,
            "write": WRITABLE,
            "store_only": KNOWN_UNREADABLE,
            "machines": {brand: list(exts) for brand, exts in MACHINE_FORMATS.items()},
            "hoops": {key: {"label": h.label, "width_mm": h.width_mm, "height_mm": h.height_mm} for key, h in HOOPS.items()},
        }

    @app.post("/v1/inspect", dependencies=auth)
    def inspect(file: UploadFile = File(...)) -> dict:
        data, ext = read_upload(file)
        result = run("info", data, ext)
        return {"format": ext, **result}

    @app.post("/v1/thumbnail", dependencies=auth)
    def thumbnail(file: UploadFile = File(...), size: int = Query(256, ge=16, le=2048)) -> Response:
        data, ext = read_upload(file)
        result = run("thumbnail", data, ext, {"size": size})
        return Response(base64.b64decode(result["data"]), media_type="image/png")

    @app.post("/v1/convert", dependencies=auth)
    def convert(
        file: UploadFile = File(...),
        target: str | None = Query(None, description="output format extension, e.g. jef"),
        machine: str | None = Query(None, description="machine brand, e.g. brother; picks its preferred format"),
        pes_version: int = Query(6),
    ) -> Response:
        data, ext = read_upload(file)
        target_ext = _resolve_target(target, machine)
        if pes_version not in (1, 6):
            raise ApiError(400, "bad_pes_version", "pes_version must be 1 or 6")
        result = run("convert", data, ext, {"target": target_ext, "pes_version": pes_version})
        return file_response(result, _download_name(file.filename, target_ext))

    @app.post("/v1/fit", dependencies=auth)
    def fit(file: UploadFile = File(...), hoop: str = Query(...)) -> dict:
        if hoop not in HOOPS:
            raise ApiError(400, "unknown_hoop", f"unknown hoop {hoop!r}")
        data, ext = read_upload(file)
        return {"hoop": hoop, **run("fit", data, ext, {"hoop": hoop})}

    @app.post("/v1/transform", dependencies=auth)
    def transform(
        file: UploadFile = File(...),
        target: str | None = Query(None),
        machine: str | None = Query(None),
        scale: float | None = Query(None, gt=0, le=10),
        width_mm: float | None = Query(None, gt=0, le=2000),
        height_mm: float | None = Query(None, gt=0, le=2000),
        rotate: float = Query(0.0, ge=-360, le=360),
        mirror_horizontal: bool = Query(False),
        mirror_vertical: bool = Query(False),
        free_standing_lace: bool = Query(False),
        allow_large_resize: bool = Query(False),
    ) -> Response:
        data, ext = read_upload(file)
        # Default: keep the uploaded format unless a target or machine is given.
        target_ext = _resolve_target(None if machine else (target or ext), machine)
        result = run(
            "transform",
            data,
            ext,
            {
                "target": target_ext,
                "scale": scale,
                "target_width_mm": width_mm,
                "target_height_mm": height_mm,
                "rotate_degrees": rotate,
                "mirror_horizontal": mirror_horizontal,
                "mirror_vertical": mirror_vertical,
                "free_standing_lace": free_standing_lace,
                "allow_large_resize": allow_large_resize,
            },
        )
        report = result["report"]
        if report["blocked"]:
            return JSONResponse(status_code=422, content={"error": "transform_blocked", "report": report})
        return file_response(result, _download_name(file.filename, target_ext), {"X-EEfile-Transform-Report": json.dumps(report)})

    @app.post("/v1/compose", dependencies=auth)
    def compose_endpoint(files: list[UploadFile] = File(...), layout: str = Form(...)) -> Response:
        """Combine designs and lettering. ``layout`` is a JSON document (see layout.py);
        it refers to the uploaded files by file name."""
        try:
            layout_doc = json.loads(layout)
        except ValueError as exc:
            raise ApiError(400, "bad_layout", "layout is not valid JSON") from exc
        blobs: dict[str, str] = {}
        total = 0
        for upload in files:
            name = upload.filename or ""
            _filename_extension(upload)
            data = upload.file.read(max_upload_bytes + 1)
            total += len(data)
            if total > max_upload_bytes:
                raise ApiError(413, "too_large", f"uploads exceed {max_upload_bytes} bytes in total")
            blobs[name] = base64.b64encode(data).decode()
        result = run("compose", b"", "", {"files": blobs, "layout": layout_doc})
        name = _download_name(str(layout_doc.get("name") or "combined"), result["extension"])
        return file_response(result, name, {"X-EEfile-Compose-Report": json.dumps(result["report"])})

    return app

