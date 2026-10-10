"""Run parsing of untrusted uploads in a separate, resource-limited process.

The format parsers have never been fuzzed. A hostile or broken file can make
them hang or allocate huge buffers, so production code paths that touch
customer uploads go through ``run_isolated`` rather than calling the library
in-process. This is a first layer only: deploy the worker in a container with
no network and a read-only filesystem as well.
"""

from __future__ import annotations

import base64
import json
import subprocess
import sys

DEFAULT_TIMEOUT_S = 20.0
DEFAULT_MEMORY_BYTES = 1024 * 1024 * 1024


class SandboxError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _limits(memory_bytes: int, cpu_seconds: int):
    def apply() -> None:
        import resource

        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))

    return apply


def run_isolated(
    op: str,
    data: bytes,
    extension: str,
    params: dict | None = None,
    *,
    timeout_s: float = DEFAULT_TIMEOUT_S,
    memory_bytes: int = DEFAULT_MEMORY_BYTES,
) -> dict:
    """Run ``op`` (info, convert, preview_png, fit) on ``data`` in a child process.

    Returns the op's result dict. Raises SandboxError with code ``timeout``,
    ``crashed``, or the DesignError code reported by the worker."""
    request = json.dumps(
        {"op": op, "extension": extension, "params": params or {}, "data": base64.b64encode(data).decode()}
    ).encode()
    preexec = _limits(memory_bytes, int(timeout_s) + 1) if sys.platform != "win32" else None
    try:
        proc = subprocess.run(
            [sys.executable, "-I", "-m", "eeganizer_files.worker"],
            input=request,
            capture_output=True,
            timeout=timeout_s,
            preexec_fn=preexec,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise SandboxError("timeout", f"{op} exceeded {timeout_s}s") from exc

    if proc.returncode != 0 or not proc.stdout:
        raise SandboxError("crashed", f"worker exited with status {proc.returncode}")
    response = json.loads(proc.stdout)
    if not response["ok"]:
        raise SandboxError(response["code"], response["message"])
    return response["result"]
