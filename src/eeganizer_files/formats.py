"""Format registry: what pystitch can read/write and which machines use what."""

from __future__ import annotations

from dataclasses import dataclass
from types import ModuleType

import pystitch

# Stitch coordinates in pystitch are in units of 0.1 mm.
UNITS_PER_MM = 10.0


@dataclass(frozen=True)
class FormatSpec:
    extension: str
    description: str
    reader: ModuleType | None
    writer: ModuleType | None

    @property
    def can_read(self) -> bool:
        return self.reader is not None

    @property
    def can_write(self) -> bool:
        return self.writer is not None

    @property
    def max_stitch_mm(self) -> float | None:
        """Longest single stitch the format can encode, if the writer declares one."""
        if self.writer is None:
            return None
        value = getattr(self.writer, "MAX_STITCH_DISTANCE", None)
        if value is None or value == float("inf"):
            return None
        return value / UNITS_PER_MM

    @property
    def stores_thread_colors(self) -> bool:
        # DST, EXP, U01 and TBF carry stitch commands only; colors are lost.
        return self.extension not in {"dst", "exp", "u01", "tbf"}


def _build_registry() -> dict[str, FormatSpec]:
    registry: dict[str, FormatSpec] = {}
    for entry in pystitch.supported_formats():
        # Only binary machine-embroidery formats. Text/debug/quilting formats
        # (csv, json, plt, qcc, gcode) are not customer-facing.
        if entry.get("category") != "embroidery" or entry["extension"] == "gcode":
            continue
        reader = entry.get("reader")
        if reader is not None and getattr(reader, "READ_FILE_IN_TEXT_MODE", False):
            reader = None
        registry[entry["extension"]] = FormatSpec(
            extension=entry["extension"],
            description=entry.get("description", entry["extension"]),
            reader=reader,
            writer=entry.get("writer"),
        )
    return registry


FORMATS: dict[str, FormatSpec] = _build_registry()

READABLE = sorted(ext for ext, spec in FORMATS.items() if spec.can_read)
WRITABLE = sorted(ext for ext, spec in FORMATS.items() if spec.can_write)

# Native/object formats customers will upload that no open-source library
# can read. Store them, but show "preview unavailable".
KNOWN_UNREADABLE = {
    "art": "Bernina ART (proprietary)",
    "emb": "Wilcom EMB (object file)",
    "vip": "Husqvarna Viking VIP",
    "edo": "Embird EDO (object file)",
    "jan": "Janome JAN (object file)",
    "bx": "Embrilliance BX font",
    "vp4": "Pfaff/Husqvarna VP4",
}

# Machine family -> export formats, preferred first.
MACHINE_FORMATS: dict[str, tuple[str, ...]] = {
    "brother": ("pes",),
    "baby_lock": ("pes",),
    "janome": ("jef",),
    "elna": ("jef",),
    "husqvarna_viking": ("vp3",),
    "pfaff": ("vp3",),
    "singer": ("xxx", "vp3"),
    "bernina": ("exp",),
    "melco": ("exp",),
    "tajima": ("dst",),
    "commercial_generic": ("dst",),
}


def normalize_extension(name_or_ext: str) -> str:
    ext = name_or_ext.rsplit(".", 1)[-1] if "." in name_or_ext else name_or_ext
    return ext.strip().lower()


def get_format(name_or_ext: str) -> FormatSpec | None:
    return FORMATS.get(normalize_extension(name_or_ext))
