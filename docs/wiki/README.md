# Embroidery knowledge wiki

Domain knowledge for the EEganizer File Software team: how machine embroidery
works, what is inside design files, and above all the **boundary conditions**
(numeric limits, rules of thumb, constraints) our software must respect.

## Pages

| Page | Read it when you work on |
|---|---|
| [machine-embroidery-basics.md](machine-embroidery-basics.md) | Hoop tables, fit checks, machine profiles, stitch-time estimates, transfer to machine |
| [digitizing-fundamentals.md](digitizing-fundamentals.md) | Stitch statistics, warnings (short/long stitches, density), color stops, trims |
| [resizing-and-editing.md](resizing-and-editing.md) | Transform/resize guards, combine, recolor, FSL and appliqué rules |
| [lettering-and-fonts.md](lettering-and-fonts.md) | Alphabet packs, letter-name parsing, minimum text size, compose |
| [file-formats.md](file-formats.md) | Parsers, converters, per-format limits and quirks, PES/PEC repair |
| [customer-workflows.md](customer-workflows.md) | Product decisions, library/ingest, thread charts, licensing |
| [glossary.md](glossary.md) | Terms A–Z |

Related project docs: [../PLAN.md](../PLAN.md), [../CORPUS.md](../CORPUS.md),
[../research/README.md](../research/README.md).

## How to use this wiki

- Every page ends with a **"Boundary conditions for EEganizer software"**
  table (IDs like M1, D3, R2, L4, F8, W5) and a **Sources** list.
- Every number carries one of three labels:
  - **sourced** — linked to a manual, help page, format doc or source code;
  - **rule of thumb** — practitioner guidance, not a measured standard;
  - **observed in our test files** — our own corpus (102 commercial design
    files + one alphabet pack; see [../CORPUS.md](../CORPUS.md)).
- Where sources disagree, the page gives the range and says so.
- When you change a threshold in code, cite the boundary-condition ID in the
  code comment, and update the page if the evidence changes.

### How the facts were checked

- **Read directly:** pystitch 1.0.1 source (PyPI wheel; format constants,
  palettes, reader/writer logic) and Ink/Stitch source on GitHub (stitch
  parameter defaults).
- **Read via search-engine excerpts only:** EduTechWiki format pages,
  inkstitch.org docs, embird.net, manufacturer sites (Brother, BERNINA,
  Janome, Singer/Pfaff/Viking, mySewnet), Wilcom/Hatch/Embrilliance help, thread
  and stabilizer makers. These sites could not be loaded from the research
  sandbox (egress proxy denied or DNS failure, Oct 2026), so quotes come from
  search results that summarized those pages. Treat single-source numbers
  (marked as such) as needing confirmation before they become hard limits.

---

## Boundary conditions cheat sheet

| Area | Limit / rule | Value | Basis | Page |
|---|---|---|---|---|
| Units | Coordinate unit in stitch files | 0.1 mm | sourced (pystitch, EduTechWiki) | [formats](file-formats.md) |
| Hoop fit | Field to compare against | Published sewing field per model, not nominal name or frame | sourced | [basics](machine-embroidery-basics.md) |
| Hoop fit | Default safety margin | **0 mm** (designers fill nominal field: 98.6 mm in "4x4", 257.4 mm in "6x10") | observed in our test files | [basics](machine-embroidery-basics.md) |
| Hoop fit | Brother/Baby Lock fields | 4x4 = 100×100; 5x7 = 130×180; 6x10 = 160×260; 8x12 = 200×300; 9.5x14 = 240×360 mm | sourced | [basics](machine-embroidery-basics.md) |
| Hoop fit | Measured under-size | Brother 4x4 grid measured 3.93 in (99.8 mm) | sourced (user report) | [basics](machine-embroidery-basics.md) |
| Hoop fit | Rotation | Always try 90°; PES/JEF may be stored rotated vs DST | observed in our test files | [formats](file-formats.md) |
| Machine | Stitch-count limits (examples) | Baby Lock 200k / 500k / 700k by model | sourced (Emblibrary) | [basics](machine-embroidery-basics.md) |
| Machine | Speed for time estimates | Home 400–1,000 spm (PE800 650); commercial up to 1,200 spm | sourced | [basics](machine-embroidery-basics.md) |
| Stitch | Max per record when writing | DST 12.1 mm; XXX 12.4 mm; EXP/JEF 12.7 mm; PEC 204.7 mm | sourced (pystitch) | [formats](file-formats.md) |
| Stitch | Long sewn stitch / travel threshold | > 12.1 mm = travel move, not a stitch | sourced (DST) + observed (VP3 moves 41–126 mm) | [formats](file-formats.md) |
| Stitch | Short stitch warning | < 0.5 mm warn; ≥ 1 mm considered safe (sources range 0.5–2 mm) | sourced, sources disagree | [digitizing](digitizing-fundamentals.md) |
| Stitch | Satin width | ~10 mm recommended max; 12 mm workable; 15 mm snags; conservative 7 mm | sourced, sources disagree | [digitizing](digitizing-fundamentals.md) |
| Stitch | Running stitch length | 0.8–5 mm, typically ~2–3 mm (Ink/Stitch default 2.5) | sourced | [digitizing](digitizing-fundamentals.md) |
| Density | Satin spacing | ~0.36–0.4 mm | sourced (Wilcom, Ink/Stitch, Hatch) | [digitizing](digitizing-fundamentals.md) |
| Density | Fill row spacing | 0.25 mm (Ink/Stitch) to 0.38–0.4 mm (Wilcom, Madeira) | sourced, sources disagree | [digitizing](digitizing-fundamentals.md) |
| Density | Stitches per in² of fill | ~1,000–1,750 | sourced | [digitizing](digitizing-fundamentals.md) |
| Density | Pull compensation | 0.2 mm default, 0.4 mm common | sourced (BERNINA, Illinois) | [digitizing](digitizing-fundamentals.md) |
| Resize | Plain scaling band | ok ≤ ±10%; caution ±10–20%; warning > ±20% | rule of thumb (BERNINA: EXP ±20%) | [resizing](resizing-and-editing.md) |
| Resize | Recalculating tools | Embrilliance 50–250% | sourced | [resizing](resizing-and-editing.md) |
| Resize | FSL | Do not resize | sourced | [resizing](resizing-and-editing.md) |
| Resize | Appliqué with cut files | Any transform breaks match with cut file | rule of thumb | [resizing](resizing-and-editing.md) |
| Lettering | Min satin cap height, 40 wt | hard 5 mm, soft 6.35 mm (1/4 in) | sourced, sources disagree | [lettering](lettering-and-fonts.md) |
| Lettering | Min satin cap height, 60 wt | ~4–5 mm (~25% smaller than 40 wt) | sourced | [lettering](lettering-and-fonts.md) |
| Lettering | Alphabet size name | ≈ cap height ("1.0 inch" caps ~24.8 mm) | observed in our test files | [lettering](lettering-and-fonts.md) |
| Lettering | Lowercase file names | doubled letters `aa`–`zz`; symbols spelled out | observed in our test files | [lettering](lettering-and-fonts.md) |
| Lettering | All-caps fonts | lowercase same height as capitals; no descenders | observed in our test files | [lettering](lettering-and-fonts.md) |
| Colors | DST / Melco EXP | no thread colors | sourced | [formats](file-formats.md) |
| Colors | Palettes when converting | PEC 63 colors (+ "Applique"), JEF 78, HUS 29; VP3/XXX/PES v5+ RGB | sourced (pystitch) | [formats](file-formats.md) |
| Counts | Stitch count across formats | within 2%; vendor worksheet 1–4% higher | observed in our test files | [formats](file-formats.md) |
| Counts | Trim count | not a design property (0 in HUS/VP3 to 32 in PES) | observed in our test files | [formats](file-formats.md) |
| Counts | Colors | show stops and unique colors separately (e.g. 19 stops, 5 colors) | observed in our test files | [digitizing](digitizing-fundamentals.md) |
| DST | Trim encoding | N consecutive jumps, often 3 (up to 5) | sourced | [formats](file-formats.md) |
| DST | Header | 512 bytes; values unreliable, recompute | sourced | [formats](file-formats.md) |
| PES | Decoder safety | stop at PEC stitch-block length; compare with header width/height; fix 90° rotation; reject designs > largest hoop | observed in our test files (20/366 PES with stray byte, 17 rotated) | [formats](file-formats.md) |
| PES | Writing | pystitch writes v1 or v6 only | sourced | [formats](file-formats.md) |
| Formats | No open reader | EMB, ART, BX, VIP (pystitch 1.0.1) → store, "preview unavailable" | sourced | [formats](file-formats.md) |
| USB | File names on Brother | letters, digits, `-`, `_`; no folders on stick | sourced (Brother manual) | [workflows](customer-workflows.md) |
| Legal | Sharing / decrypting | never share converted files; never decrypt vendor-encrypted designs | sourced + policy | [workflows](customer-workflows.md) |

## Glossary

See [glossary.md](glossary.md).

## Sources

Each page has its own source list. Key primary sources:

- pystitch 1.0.1 (format code, read directly): https://pypi.org/project/pystitch/ ; https://github.com/inkstitch/pystitch
- Ink/Stitch source (stitch defaults, read directly): https://github.com/inkstitch/inkstitch
- EduTechWiki embroidery format pages: https://edutechwiki.unige.ch/en/Embroidery_format
- Brother machine manual excerpts: https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html
- Wilcom EmbroideryStudio help: https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/
- BERNINA software help: https://softwarehelp.bernina.com/en/MainHelp/
- Emblibrary machine limits: https://emblibrary.com/page/help/embroidery-limits
