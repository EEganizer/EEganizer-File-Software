"""Machine catalog and "My Machines" profiles.

Published sewing fields per brand hoop, from docs/wiki/machine-embroidery-basics.md
(see its Sources). ``confirmed=False`` marks figures the wiki could only
verify from a single retailer listing or search excerpt; confirm them against
the manufacturer before relying on them for a hard "won't fit".

Fit checks use no safety margin: designers digitize right up to the
nominal field (wiki M-section, observed in our test files).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .formats import MACHINE_FORMATS, WRITABLE, normalize_extension
from .hoops import FitResult, Hoop, check_fit
from .inspect import DesignInfo


@dataclass(frozen=True)
class CatalogHoop(Hoop):
    brand: str = ""
    confirmed: bool = True


def _h(brand: str, key: str, label: str, w: float, h: float, confirmed: bool = True) -> CatalogHoop:
    return CatalogHoop(f"{brand}:{key}", label, w, h, brand=brand, confirmed=confirmed)


_HOOPS = [
    _h("brother", "4x4", '4" x 4"', 100, 100),
    _h("brother", "5x7", '5" x 7"', 130, 180),
    _h("brother", "6x10", '6" x 10"', 160, 260),
    _h("brother", "8x12", '8" x 12"', 200, 300),
    _h("brother", "8x14", '8" x 14"', 200, 360),
    _h("brother", "9.5x14", '9.5" x 14"', 240, 360),
    _h("janome", "sq10", "SQ10", 100, 100),
    _h("janome", "sq14", "SQ14", 140, 140),
    _h("janome", "re20", "RE20", 140, 200),
    _h("janome", "sq20", "SQ20", 200, 200),
    _h("janome", "re28", "RE28", 200, 280),
    _h("janome", "gr", "GR (MC12000)", 230, 300, confirmed=False),
    _h("bernina", "small", "Small", 50, 72, confirmed=False),
    _h("bernina", "medium", "Medium", 100, 130, confirmed=False),
    _h("bernina", "large_oval", "Large Oval", 145, 255, confirmed=False),
    _h("bernina", "maxi", "Maxi", 210, 400),
    _h("bernina", "jumbo", "Jumbo", 260, 400),
    _h("husqvarna_viking", "square", "Square 120", 120, 120),
    _h("husqvarna_viking", "quilters", "Quilter's 200", 200, 200),
    _h("husqvarna_viking", "large_metal", "Large Metal 240x150", 240, 150),
    _h("husqvarna_viking", "deluxe", "Deluxe 360x200", 360, 200),
    _h("husqvarna_viking", "grand_dream", "Grand Dream 360x350", 360, 350),
    _h("singer", "40", "40 x 40 mm", 40, 40),
    _h("singer", "100", "100 x 100 mm", 100, 100),
]

# Baby Lock shares Brother hoops and formats; Pfaff shares Husqvarna Viking's.
_BRAND_ALIASES = {"baby_lock": "brother", "pfaff": "husqvarna_viking", "elna": "janome"}

CATALOG: dict[str, CatalogHoop] = {h.key: h for h in _HOOPS}


def brand_key(brand: str) -> str:
    b = brand.strip().lower().replace(" ", "_").replace("-", "_")
    return _BRAND_ALIASES.get(b, b)


def hoops_for_brand(brand: str) -> list[CatalogHoop]:
    b = brand_key(brand)
    return [h for h in _HOOPS if h.brand == b]


@dataclass
class MachineProfile:
    """One of the customer's machines."""

    name: str
    brand: str
    hoops: list[str] = field(default_factory=list)  # catalog keys; empty = all hoops of the brand
    export_format: str | None = None  # overrides the brand default (e.g. "dst" for a commercial machine)
    max_stitches: int | None = None  # some machines refuse designs above a stitch count

    def hoop_list(self) -> list[CatalogHoop]:
        if not self.hoops:
            return hoops_for_brand(self.brand)
        unknown = [k for k in self.hoops if k not in CATALOG]
        if unknown:
            raise ValueError(f"unknown hoops: {', '.join(unknown)}")
        return [CATALOG[k] for k in self.hoops]

    def format(self) -> str:
        if self.export_format:
            return self.export_format
        formats = MACHINE_FORMATS.get(self.brand.strip().lower().replace(" ", "_")) or MACHINE_FORMATS.get(
            brand_key(self.brand))
        if not formats:
            raise ValueError(f"no default format for brand {self.brand!r}; set export_format")
        return formats[0]


@dataclass
class MachineFit:
    machine: str
    fits: bool
    hoop: CatalogHoop | None  # smallest hoop that fits, or the largest hoop when nothing fits
    needs_rotation: bool
    scale_to_fit: float
    export_format: str
    messages: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "machine": self.machine,
            "fits": self.fits,
            "hoop": None if self.hoop is None else {
                "key": self.hoop.key, "label": self.hoop.label,
                "width_mm": self.hoop.width_mm, "height_mm": self.hoop.height_mm,
                "confirmed": self.hoop.confirmed,
            },
            "needs_rotation": self.needs_rotation,
            "scale_to_fit": self.scale_to_fit,
            "export_format": self.export_format,
            "messages": self.messages,
        }


def fit_machine(info: DesignInfo, profile: MachineProfile) -> MachineFit:
    hoops = sorted(profile.hoop_list(), key=lambda h: h.width_mm * h.height_mm)
    if not hoops:
        raise ValueError(f"no hoops known for {profile.brand!r}")
    messages: list[str] = []
    best: FitResult | None = None
    for hoop in hoops:
        result = check_fit(info, hoop)
        if result.fits:
            best = result
            break
    if best is None:
        largest = check_fit(info, hoops[-1])
        messages.append(
            f"Too big for every hoop of {profile.name}; the largest ({hoops[-1].label}) needs the design "
            f"at {largest.scale_to_fit:.0%} of its size."
        )
        result = MachineFit(profile.name, False, hoops[-1], largest.needs_rotation, largest.scale_to_fit,
                            profile.format(), messages)
    else:
        if best.needs_rotation:
            messages.append(f"Rotate 90° to fit the {best.hoop.label} hoop.")
        if not best.hoop.confirmed:
            messages.append(f"The {best.hoop.label} sewing field is not yet confirmed with the manufacturer.")
        result = MachineFit(profile.name, True, best.hoop, best.needs_rotation, 1.0, profile.format(), messages)
    if profile.max_stitches and info.stitch_count > profile.max_stitches:
        result.fits = False
        result.messages.append(
            f"{info.stitch_count:,} stitches is more than {profile.name} accepts ({profile.max_stitches:,})."
        )
    return result


def profile_from_dict(data: dict) -> MachineProfile:
    if not isinstance(data, dict) or not data.get("brand"):
        raise ValueError("machine profile needs a brand")
    hoops = data.get("hoops") or []
    if not isinstance(hoops, list) or not all(isinstance(h, str) for h in hoops):
        raise ValueError("hoops must be a list of catalog keys")
    max_stitches = data.get("max_stitches")
    if max_stitches is not None and (not isinstance(max_stitches, int) or max_stitches <= 0):
        raise ValueError("max_stitches must be a positive integer")
    export_format = data.get("export_format")
    if export_format is not None:
        export_format = normalize_extension(str(export_format))
        if export_format not in WRITABLE:
            raise ValueError(f"cannot write .{export_format} files")
    profile = MachineProfile(
        name=str(data.get("name") or data["brand"]),
        brand=str(data["brand"]),
        hoops=hoops,
        export_format=export_format,
        max_stitches=max_stitches,
    )
    profile.hoop_list()  # validates hoop keys / brand
    profile.format()
    return profile


def catalog_to_dict() -> dict:
    brands: dict[str, list[dict]] = {}
    for hoop in _HOOPS:
        brands.setdefault(hoop.brand, []).append({
            "key": hoop.key, "label": hoop.label, "width_mm": hoop.width_mm,
            "height_mm": hoop.height_mm, "confirmed": hoop.confirmed,
        })
    return {"brands": brands, "aliases": dict(_BRAND_ALIASES)}
