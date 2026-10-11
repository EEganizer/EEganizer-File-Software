# Digitizing fundamentals

Digitizing turns artwork into machine instructions. The digitizer draws
**objects** (shapes with a stitch type, density, angle, underlay and
compensation), and the software generates the **stitches**. What customers buy
and what EEganizer handles is almost always the stitch output.

Evidence labels: **sourced** (link), **rule of thumb**, **observed in our test
files**. Where sources disagree, the range is given.

---

## 1. Object files vs stitch files

| | Object ("working", "native", "outline") file | Stitch ("machine", "expanded") file |
|---|---|---|
| Examples | Wilcom/Hatch EMB, BERNINA ART, mySewnet EDO, Janome JAN | PES*, DST, EXP, JEF, VP3, HUS, VIP, XXX, SEW |
| Contains | Shapes + stitch parameters; stitches recomputed on demand | Needle positions + commands only |
| Resize | Stitches regenerated: density preserved | Coordinates scaled: density changes (see [resizing-and-editing.md](resizing-and-editing.md)) |
| Runs on a machine | No ("not meant to run directly on machines") | Yes |
| Basis | sourced: [emborado](https://www.emborado.de/en/glossary/embroidery-file-format), [BERNINA machine files](https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/machine_files/Machine_Files.htm) | |

\* PES from PE-Design can carry some object data next to the stitch block; the
PEC stitch block is what the machine sews ([libpes wiki](https://github.com/frno7/libpes/wiki/PES-format)).

Software that opens a stitch file and "converts to outlines" (BERNINA V9,
Wilcom stitch processing) is guessing objects back from stitches; Wilcom
says "not all objects will be restored"
([Wilcom docs](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/functions/functions-9.htm)).

## 2. Stitch types

| Type | What it is | Typical numbers | Basis |
|---|---|---|---|
| Running (walk) | Single line of stitches | Stitch length 0.8–5 mm, commonly ~2–3 mm; Ink/Stitch default 2.5 mm | sourced: [Ignition glossary](https://ignitiondrawing.com/blog/embroidery-glossary-stitch-types-88), [Ink/Stitch source](https://github.com/inkstitch/inkstitch/blob/main/lib/elements/stroke.py) |
| Bean / triple run | Each stitch sewn forward-back-forward (3x) | Wilcom Triple Run default 3 passes | sourced: [Ink/Stitch bean stitch](https://inkstitch.org/docs/stitches/bean-stitch/), [Wilcom run count](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Digitizing/stitches/stitches-5.htm) |
| Satin (column) | Zigzag across a narrow column; each stitch spans the full width | Width see §4; spacing ~0.36–0.4 mm | sourced: Wilcom (below) |
| Fill / tatami | Rows of running stitches with staggered penetrations | Row spacing 0.25–0.45 mm; stitch length ~3–4 mm | sourced (see §3) |
| Appliqué | Fabric piece sewn on: **placement** line → stop → **tack-down** → stop → (trim) → **cover** satin/blanket | One color stop per step | sourced: [BERNINA appliqué eBook](https://www.bernina.com/en-US/Learn-Create-US/Projects-Downloads/Embroidery-Projects/Embroidery-ebooks/Just-EMBROIDER-It-Embroidery-Machine-Applique/JustEmbroiderIt-eBook-Applique.pdf), [Ink/Stitch appliqué](https://inkstitch.org/tutorials/applique/), [OESD trim-in-place](https://support.oesd.com/article/35-trim-in-place-applique-tutorial) |
| Free-standing lace (FSL) | Stitched on wash-away only; stitches must interlock into a mesh | Much higher stitch counts than normal designs | sourced: [EduTechWiki Stitch Era FSL](https://edutechwiki.unige.ch/en/Stitch_Era_-_free_standing_lace), [Linda's FSL](https://lindas.com/blogs/tips-and-tricks/free-standing-lace-embroidery-designs) |
| 3D puff | Satin over 2–3 mm foam; dense, with end caps | Column width min 2–3 mm, max 7 mm (Hatch) to 10–12 mm (Wilcom/Ignition); spacing as tight as 0.16 mm | sourced: [Hatch puff](https://blog.hatchembroidery.com/how-to-digitize-for-3d-puffy-foam-machine-embroidery/), [Wilcom puff Q&A](https://wilcom.com/resources/blog/qa-from-3d-puff-embroidery-webinar), [Ignition](https://blog.ignitiondrawing.com/working-with-3d-puff-embroidery-part-2/print/) — **sources disagree on width** |
| Cross-stitch | X stitches on a grid | Ink/Stitch default pattern size 3 mm; max cross stitch length 11 mm | sourced: [Ink/Stitch fill_stitch.py](https://github.com/inkstitch/inkstitch/blob/main/lib/elements/fill_stitch.py) |

## 3. Density (stitch spacing)

Density is expressed as the distance between parallel stitch lines in mm
(smaller = denser). Some software uses "points" (1 pt = 0.1 mm) or lines per
inch.

| Stitch type | Typical spacing | Basis |
|---|---|---|
| Satin | 0.4 mm worked example; Wilcom auto-spacing reduces a 4 mm wide column at 0.4 mm to ~0.36 mm | sourced: [Wilcom spacing blog](https://wilcom.com/resources/blog/stitch-spacing-or-density) |
| Satin (Ink/Stitch default) | 0.4 mm | sourced: [Ink/Stitch satin_column.py](https://github.com/inkstitch/inkstitch/blob/main/lib/elements/satin_column/satin_column.py) |
| Satin (Hatch default) | 0.36 mm | sourced: Hatch puff article |
| Tatami fill (Wilcom default) | 0.38 mm spacing, 4 mm stitch length | sourced: [Wilcom satin & tatami](https://wilcom.com/resources/blog/mastering-basic-stitch-types-satin-stitch-and-tatami-stitch) |
| Fill (Ink/Stitch default) | 0.25 mm row spacing, 4.0 mm max stitch length | sourced: Ink/Stitch fill_stitch.py |
| Fill (Madeira guidance for Polyneon 40) | "4.0 density" (= 0.4 mm) | sourced: retailer listings of Madeira Polyneon |
| Fill underlay (Ink/Stitch) | 3x the top row spacing by default | sourced: Ink/Stitch fill_stitch.py |
| Puff satin | 0.16 mm | sourced: Hatch puff article |
| 60 wt thread | some digitizers raise density ~20% | sourced: [Impressions](https://impressionsmagazine.com/how-to-digitize-small-lettering/) (single digitizer) |

Fill density ranges from 0.25 mm (Ink/Stitch) to ~0.4–0.45 mm (Wilcom/Madeira
guidance); defaults differ by software and are not directly comparable
(**sources disagree**).

**Stitch-count estimates.** About 1,000 stitches per square inch of fill at
6 mm stitch length, 1,500 at 4 mm ([emborado stitch count](https://www.emborado.de/en/glossary/stitch-count));
ASI's worked example gives ~1,550–1,730 per square inch for dense fill
([ASI](https://members.asicentral.com/news/how-to/october-2019/how-to-reduce-stitch-count-without-jeopardizing-quality/), our arithmetic).

**Over-density.** Brother warns that third-party data with "stitch density
that is too fine" or "three or more overlapping stitches" can break thread or
needle ([Brother manual](https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html)).

## 4. Stitch length limits

| Limit | Value | Basis |
|---|---|---|
| Minimum stitch, safe | **≥ 1 mm** for normal designs; under 0.5 mm the needle sews in one spot and breaks thread | sourced: [Embroidery Legacy cheat sheet](https://www.embroiderylegacy.com/wp-content/uploads/2025/08/ELCheatSheet-1.pdf) (0.5 / 1 mm), [ABDigitizing](https://abdigitizing.com/stop-the-thread-breaks-digitizing-issues-vs-machine-issues/) (<1 mm "extremely dangerous"), [ASI fonts](https://members.asicentral.com/news/how-to/april-2018/choose-the-right-font-for-embroidery/) (never <1 mm; author avoids <2 mm) — **range 0.5–2 mm** |
| Ink/Stitch short-stitch distance in satins | 0.25 mm (deliberately short stitches on curves) | sourced: Ink/Stitch satin_column.py |
| Lock (tie) stitch size | ~0.7 mm (Ink/Stitch default lock scale) | sourced: [Ink/Stitch element.py](https://github.com/inkstitch/inkstitch/blob/main/lib/elements/element.py) |
| Satin width, recommended max | ~10 mm; 12 mm workable; up to 15 mm possible but snags | sourced: [Wilcom stitch techniques](https://wilcom.com/resources/blog/embroidery-stitch-techniques) |
| Satin width, conservative max | ~7 mm (puff, auto-split concerns) | sourced: Hatch puff article; also widespread practitioner guidance — **sources disagree (7–12 mm)** |
| Satin width, min | ~1 mm; a satin cannot be narrower than the needle | rule of thumb; sourced principle: [ASI small letters](https://members.asicentral.com/news/how-to/may-2018/keep-your-small-letters-crisp/) |
| Wide satin handling | Split into shorter stitches (Wilcom Auto Split, BERNINA Satin Special) | sourced: [BERNINA split satin](https://softwarehelp.bernina.com/en/MainHelp/PART_Digitizing/stitches/Split_long_stitches_in_satin_fills.htm), [Wilcom satin](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Digitizing/stitches/stitches-7.htm) |
| Max stitch the file can hold | DST 12.1 mm; EXP/JEF 12.7 mm; XXX 12.4 mm; PES/PEC 204.7 mm | sourced: format code (see [file-formats.md](file-formats.md)) |
| Max stitch the machine sews | Longer moves become jumps/trims; machine/software setting ("max stitch length", "auto jump") | sourced: [Wilcom stitch & jump length](https://docs.wilcom.com/embroiderystudio/27/en/OnlineHelp/Setup/machines/machines-3.htm) |

## 5. Underlay

Low-density stitching sewn first to stabilize fabric and lift the top stitches.

| Underlay | Used for | Numbers | Basis |
|---|---|---|---|
| Center run | Narrow satin (~2–3 mm) | single run down the middle | sourced: [Wilcom run underlay](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/stabilizing/stabilizing-10.htm) |
| Edge run (contour) | Satin and fill edges | inset ~0.3–0.4 mm; Ink/Stitch contour inset 0.4 mm | sourced: [ABDigitizing underlay](https://abdigitizing.com/the-secret-to-perfect-embroidery-understanding-underlay-stitches/), Ink/Stitch |
| Zigzag | Wide satin (~4–8 mm) | Ink/Stitch zigzag underlay spacing 3 mm | sourced: ABDigitizing (single blog); Ink/Stitch |
| Tatami underlay | Large fills | lower density, inset, angle opposed to top fill | sourced: [Graphics Pro underlay](https://graphics-pro.com/feature/your-guide-to-underlay-stitching/) |
| For small columns | Prefer center walk over edge walk (edge walk can poke out) | | sourced: ASI small letters |

## 6. Pull and push compensation

Thread tension pulls fabric in perpendicular to stitches (shapes get narrower)
and pushes it out along them (shapes get longer). Digitizers widen columns to
compensate.

| Setting | Value | Basis |
|---|---|---|
| BERNINA default pull comp | 0.2 mm ("suitable for most designs"); 0.4 mm for auto-digitizing | sourced: [BERNINA help](https://softwarehelp.bernina.com/en/MainHelp/PART_Digitizing/quality/quality-8.htm) |
| Common practice | raise from 0.20 to 0.40 mm on most objects | sourced: [Univ. of Illinois tutorial](https://art.illinois.edu/tutorial-editing-a-digitized-embroidery-file/) |
| Wider stitches | need more compensation | sourced: [Embroidery Legacy](https://embroiderylegacy.com/?p=29477), [Wilcom](https://wilcom.com/resources/blog/push-and-pull-compensation) |
| Knits | need more; no published mm value found | sourced (qualitative): [Hatch](https://hatchembroidery.com/resources/blog/what-you-need-to-know-about-pull-compensation) |

Consequence for software: a stitch file's outline is **wider than the art** by
the compensation; scaling a file scales its compensation too, which is wrong
for the new size (**rule of thumb**).

## 7. Tie-ins, tie-offs, trims, jumps

| Element | What it is | Basis |
|---|---|---|
| Tie-in / tie-off (lock stitches) | 2–4 tiny stitches at start/end of a segment so it does not unravel after a trim | sourced: Ink/Stitch lock stitches (`lock_start`/`lock_end`, 0.7 mm) |
| Jump | Needle-up move of the frame between areas | sourced: format docs |
| Trim | Thread cut. DST has no trim code: trim = N consecutive jumps, often 3, up to 5; pystitch uses 3 | sourced: [EduTechWiki DST](https://edutechwiki.unige.ch/en/Embroidery_format_DST), [Wilcom trim functions](https://docs.wilcom.com/embroiderystudio/27/en/OnlineHelp/Setup/machines/machines-4.htm), pystitch `DstWriter.trim_at = 3` |
| Machines without trimmer | may misinterpret trim codes or shift; Wilcom lets you turn off trim output | sourced: Wilcom trim functions |
| Travel / underpath | Running stitches hidden under later fill instead of jump+trim | sourced: Ink/Stitch `underpath` option |

Trim count is **not** a stable property of a design: the same design had 0
trims in HUS/VP3 and 32 in PES (**observed in our test files**).

## 8. Sequencing, pathing and color stops

- Digitizers order objects back-to-front and group by color to minimize stops
  and trims; they end one object near where the next begins (pathing)
  (**rule of thumb**).
- Each color change in the file is a machine stop. Files can reuse a color in
  several stops (e.g. 5 unique colors, 19 stops) (**observed in our test files**).
- Appliqué and FSL use extra stops that are **not** color changes (placement,
  tack-down, trim). Software must not "optimize" them away (**rule of thumb**).
- Reordering colors changes what lies on top; only safe when objects do not
  overlap (**rule of thumb**).

---

## Boundary conditions for EEganizer software

| # | Condition | Basis |
|---|---|---|
| D1 | Treat stitch files as final output; never claim to change density or underlay. | sourced |
| D2 | Flag stitches **< 0.5 mm** as "short" (thread-break risk); 0.5–1 mm as notable in dense areas. Do not flag lock stitches (~0.7 mm) or deliberate satin short stitches as errors in isolation. | sourced range 0.5–2 mm |
| D3 | Flag sewn stitches **> 12.1 mm** as long (DST limit, lowest common denominator); moves above this are travel, not stitches. | sourced (DST) + observed (VP3) |
| D4 | Warn on satin-like zigzag segments wider than **~10 mm** (snag risk); 7–12 mm is a grey zone. | sourced, sources disagree |
| D5 | Never merge, drop or reorder color stops automatically: they may be appliqué or FSL steps. | rule of thumb |
| D6 | Do not display trim count as a design property; it depends on the format. | observed in our test files |
| D7 | Density estimates: show stitches per cm² (or per in²) before/after any change; 1,000–1,750 per in² is normal fill range. | sourced range |
| D8 | Expect file outlines slightly larger than artwork (pull compensation 0.2–0.4 mm). | sourced |

## Sources

- File format classes: https://www.emborado.de/en/glossary/embroidery-file-format ; https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/machine_files/Machine_Files.htm ; https://github.com/frno7/libpes/wiki/PES-format
- Wilcom stitch processing: https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/functions/functions-9.htm
- Running / bean stitch: https://ignitiondrawing.com/blog/embroidery-glossary-stitch-types-88 ; https://inkstitch.org/docs/stitches/running-stitch/ ; https://inkstitch.org/docs/stitches/bean-stitch/ ; https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Digitizing/stitches/stitches-5.htm
- Ink/Stitch source (defaults read directly): https://github.com/inkstitch/inkstitch/blob/main/lib/elements/fill_stitch.py ; https://github.com/inkstitch/inkstitch/blob/main/lib/elements/satin_column/satin_column.py ; https://github.com/inkstitch/inkstitch/blob/main/lib/elements/stroke.py ; https://github.com/inkstitch/inkstitch/blob/main/lib/elements/element.py
- Appliqué: https://www.bernina.com/en-US/Learn-Create-US/Projects-Downloads/Embroidery-Projects/Embroidery-ebooks/Just-EMBROIDER-It-Embroidery-Machine-Applique/JustEmbroiderIt-eBook-Applique.pdf ; https://inkstitch.org/tutorials/applique/ ; https://support.oesd.com/article/35-trim-in-place-applique-tutorial
- FSL: https://edutechwiki.unige.ch/en/Stitch_Era_-_free_standing_lace ; https://lindas.com/blogs/tips-and-tricks/free-standing-lace-embroidery-designs
- Puff: https://blog.hatchembroidery.com/how-to-digitize-for-3d-puffy-foam-machine-embroidery/ ; https://wilcom.com/resources/blog/qa-from-3d-puff-embroidery-webinar ; https://blog.ignitiondrawing.com/working-with-3d-puff-embroidery-part-2/print/
- Density: https://wilcom.com/resources/blog/stitch-spacing-or-density ; https://wilcom.com/resources/blog/mastering-basic-stitch-types-satin-stitch-and-tatami-stitch ; https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Digitizing/stitches/stitches-14.htm ; https://impressionsmagazine.com/how-to-digitize-small-lettering/
- Stitch counts: https://www.emborado.de/en/glossary/stitch-count ; https://members.asicentral.com/news/how-to/october-2019/how-to-reduce-stitch-count-without-jeopardizing-quality/
- Brother density warning: https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html
- Short stitches: https://www.embroiderylegacy.com/wp-content/uploads/2025/08/ELCheatSheet-1.pdf ; https://abdigitizing.com/stop-the-thread-breaks-digitizing-issues-vs-machine-issues/ ; https://members.asicentral.com/news/how-to/april-2018/choose-the-right-font-for-embroidery/ ; https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/quality/quality-7.htm ; https://help.hatchembroidery.com/portal/en/kb/articles/how-to-remove-small-stitches
- Satin width: https://wilcom.com/resources/blog/embroidery-stitch-techniques ; https://softwarehelp.bernina.com/en/MainHelp/PART_Digitizing/stitches/Split_long_stitches_in_satin_fills.htm ; https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Digitizing/stitches/stitches-7.htm ; https://members.asicentral.com/news/how-to/may-2018/keep-your-small-letters-crisp/
- Stitch/jump settings and trims: https://docs.wilcom.com/embroiderystudio/27/en/OnlineHelp/Setup/machines/machines-3.htm ; https://docs.wilcom.com/embroiderystudio/27/en/OnlineHelp/Setup/machines/machines-4.htm ; https://edutechwiki.unige.ch/en/Embroidery_format_DST
- Underlay: https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/stabilizing/stabilizing-10.htm ; https://abdigitizing.com/the-secret-to-perfect-embroidery-understanding-underlay-stitches/ ; https://graphics-pro.com/feature/your-guide-to-underlay-stitching/
- Compensation: https://softwarehelp.bernina.com/en/MainHelp/PART_Digitizing/quality/quality-8.htm ; https://art.illinois.edu/tutorial-editing-a-digitized-embroidery-file/ ; https://embroiderylegacy.com/?p=29477 ; https://wilcom.com/resources/blog/push-and-pull-compensation ; https://hatchembroidery.com/resources/blog/what-you-need-to-know-about-pull-compensation
- pystitch 1.0.1 source (read directly from the PyPI wheel): https://pypi.org/project/pystitch/
