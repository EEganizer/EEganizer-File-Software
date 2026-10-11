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
| Combine designs | `compose.compose` | Place several designs in one hoop (position, rotate, mirror, guarded resize, recolor). Sewn in order with a trim between pieces; a color stop only when the thread changes. Reports size, overlaps and hoop fit. |
| Lettering | `lettering.layout_text` | Spells text from an embroidery alphabet pack (one file per letter: `A.pes`, `aa.pes`, `a_lower.jef`, `Upper B.dst`, `Question Mark Symbol.vp3` …). `Alphabet.discover` finds every size/format in an unpacked pack and `choose_alphabet` picks the size nearest the requested height. Handles all-caps fonts (no descenders) on a common baseline, with descenders, spacing, alignment and multiple lines. Computer fonts (TTF) are not supported — that needs auto-digitizing. |
| Hoop fit | `hoops.check_fit`, `smallest_hoop` | Fit with clearance, with/without 90° rotation, scale-to-fit. Hoop table is nominal sizes — replace with per-machine sewing areas. |
| Previews | `render.render_png`, `render_svg` | PNG with thread shading (1 px = 0.1 mm), SVG for a zoomable viewer. |
| Isolation | `sandbox.run_isolated` | Parses untrusted uploads in a child process with timeout, memory and CPU limits. Use this for every customer file. |

## HTTP service

A private API for EEganizer.com (bearer-token auth, every file parsed in the sandbox):

| Endpoint | Returns |
|---|---|
| `GET /healthz` | liveness (no auth) |
| `GET /v1/formats` | readable/writable formats, store-only formats, machine brand → format, hoop table |
| `POST /v1/inspect` | properties JSON + smallest fitting hoop |
| `POST /v1/thumbnail?size=256` | PNG thumbnail |
| `POST /v1/convert?target=jef` or `?machine=brother` | converted file; warnings in `X-EEfile-Warnings` |
| `POST /v1/fit?hoop=5x7` | fits / needs rotation / scale to fit |
| `POST /v1/compose` (`files=` many, `layout=` JSON) | combined file + `X-EEfile-Compose-Report` (see `layout.py` for the layout format) |
| `POST /v1/transform?scale=1.1&rotate=90&machine=janome` | transformed file + `X-EEfile-Transform-Report`; `422` with the report when blocked |

Uploads are multipart `file=` with the original file name (its extension picks the format).

```bash
pip install -e ".[service]"
EEFILE_API_TOKEN=change-me uvicorn --factory eeganizer_files.service:create_app --port 8080
curl -H "Authorization: Bearer change-me" -F file=@design.pes "localhost:8080/v1/convert?machine=janome" -o design.jef
```

The service refuses to start without `EEFILE_API_TOKEN`. A `Dockerfile` runs it
as a non-root user; run the container read-only on an internal network.

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
eefile compose layout.json combined.pes   # designs + lettering from a JSON layout
```

## Known limits

- **No stitch recalculation.** Resizing beyond ~10–20% needs re-digitizing or
  a commercial engine. The 10/20% thresholds are practitioner guidance, not a
  measured standard; validate them with test stitch-outs.
- **Native/object formats** (Bernina ART, Wilcom EMB, VIP, EDO, JAN, VP4) can be
  stored but not opened.
- **Parsers are not fuzzed.** Always go through `sandbox.run_isolated`, and run
  the worker in a no-network, read-only container in production.
- Unit tests use synthetic designs; `tests/test_corpus.py` checks real
  commercial files kept outside the repo (see [`docs/CORPUS.md`](docs/CORPUS.md)).
- pystitch's SEW writer overflows on long moves; `convert.WRITER_OVERRIDES`
  works around it. PES files with a stray byte before the PEC end marker are
  repaired in `design.load_design`. Report both upstream.

## Embroidery knowledge wiki

[`docs/wiki/`](docs/wiki/README.md) explains machine embroidery and digitizing
for the team and collects the **boundary conditions** the code must respect
(hoop fields, stitch-length and density limits, resize bands, minimum letter
heights, per-format limits), each marked sourced / rule of thumb / observed
in our test files.

## Plan

See [`docs/PLAN.md`](docs/PLAN.md) for phases, milestones, status and the
decisions still needed from EEganizer.

## License

Proprietary — license not yet chosen by EEganizer. Third-party licenses:
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
