# EEganizer File Software

Embroidery design file toolkit behind EEganizer.com's in-library file tools:
open a customer's stored design, show its properties and a preview, check it
against their hoop, make small guarded size changes, and export it in their
machine's format.

The format layer is [pystitch](https://github.com/inkstitch/pystitch) (MIT),
the maintained Ink/Stitch fork of pyembroidery. Everything customer-facing on
top of it is EEganizer code. The research behind this choice is in
[`docs/research/`](docs/research/README.md).

## What it does

| Feature | Module | Notes |
|---|---|---|
| Read ~40 formats | `design.load_design` | PES (v1–v10), DST, JEF, EXP, VP3, HUS, XXX, SEW, U01, PEC and more. Returns typed `DesignError` codes for unsupported, unreadable (ART, EMB, VIP…), corrupt, empty or oversized files. |
| Properties | `inspect.analyze` | Size (mm/in), stitch/jump/trim/color-change counts, thread list with colors and per-thread stitch counts, longest and mean stitch, top-thread length, sew-time estimate. |
| Convert | `convert.convert`, `write_design` | Writes PES (v1 or v6), DST, JEF, EXP, VP3, XXX, SEW, U01, PEC, TBF. Warns when the target drops thread colors (DST/EXP/U01/TBF). |
| Resize / rotate / mirror | `transform.transform` | Geometric only — stitches are **not** recalculated. Reports density change, stitches over the format's max length (12.1 mm cap), new short stitches. ≤10% ok, 10–20% caution, >20% blocked unless `allow_large_resize`. Free-standing lace is never resized. |
| Hoop fit | `hoops.check_fit`, `smallest_hoop` | Fit with clearance, with/without 90° rotation, scale-to-fit. Hoop table is nominal sizes — replace with per-machine sewing areas. |
| Previews | `render.render_png`, `render_svg` | PNG with thread shading (1 px = 0.1 mm), SVG for a zoomable viewer. |
| Isolation | `sandbox.run_isolated` | Parses untrusted uploads in a child process with timeout, memory and CPU limits. Use this for every customer file. |

## Quick start

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[test]"
pytest -q

eefile formats
eefile info design.pes
eefile convert design.pes design.jef
eefile resize design.pes bigger.pes --scale 1.1
eefile fit design.pes --hoop 5x7
eefile preview design.pes preview.png
```

## Known limits

- **No stitch recalculation.** Resizing beyond ~10–20% needs re-digitizing or
  a commercial engine. The 10/20% thresholds are practitioner guidance, not a
  measured standard; validate them with test stitch-outs.
- **Native/object formats** (Bernina ART, Wilcom EMB, VIP, EDO, JAN, VP4) can be
  stored but not opened.
- **Parsers are not fuzzed.** Always go through `sandbox.run_isolated`, and run
  the worker in a no-network, read-only container in production.
- Tests use synthetic designs. A corpus of real customer-representative files
  per format (with permission) is the next testing step.
- pystitch's SEW writer overflows on long moves; `convert.WRITER_OVERRIDES`
  works around it. Report upstream.

## Roadmap

1. View & convert: thumbnails and properties at upload, one-click export per
   the customer's machine (`formats.MACHINE_FORMATS`).
2. Fit & light edit: per-model hoop catalog, "My Machines" profile, thread
   charts by brand, guarded resize UI.
3. In-browser viewer and, if customers want it, density-preserving resize.

## License

Proprietary — license not yet chosen by EEganizer. Third-party licenses:
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
