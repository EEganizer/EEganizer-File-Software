# Resizing and editing stitch files

What can safely be changed in a stitch file, what cannot, and where the
"±10–20%" guidance comes from.

Evidence labels: **sourced** (link), **rule of thumb**, **observed in our test
files**.

---

## 1. Why scaling a stitch file is risky

A stitch file stores needle positions, not shapes. Plain scaling multiplies
every coordinate; stitch count stays the same
([makema](https://makema.de/en/blogs/faq/stickdateien-skalieren),
[Wilcom blog](https://productblog.wilcom.com/?p=5321)).

| Change | Effect | Failure mode | Basis |
|---|---|---|---|
| Enlarge | Spacing between stitch lines grows; stitch lengths grow | Gaps, fabric shows through; satins get wider and snag; stitches cross the 12.1 mm DST limit and turn into jumps/trims | sourced: Wilcom blog, [zdigitizing](https://zdigitizing.com/how-to-properly-resize-embroidery-designs/), [EduTechWiki DST](https://edutechwiki.unige.ch/en/Embroidery_format_DST) |
| Shrink | Spacing shrinks; stitches shorten | Too dense, bulletproof patch feel, thread/needle breaks, tiny stitches < 0.5–1 mm | sourced: makema; see [digitizing-fundamentals.md §4](digitizing-fundamentals.md#4-stitch-length-limits) |
| Either | Pull compensation, underlay inset and lock stitches scale too | Outlines misregister, small letters fill in | rule of thumb |
| Small detail / small text | Little headroom | "resizing odds are minimal" | sourced: [Embroidery Legacy](https://embroiderylegacy.com/?p=403722) |

## 2. The ±10–20% guidance: provenance

| Claim | Who | Basis |
|---|---|---|
| "Some say don't resize at all, some preach 10% up or down, others 20% or 30%... there is no one single correct answer" | Embroidery Legacy | sourced: [Embroidery Legacy resize](https://embroiderylegacy.com/?p=403722) |
| Many machines offer ±20% scaling; stitch count unchanged, so density changes | makema | sourced |
| BERNINA: designs on the machine are EXP and "should therefore only be scaled +/-20%" | BERNINA help (quoted in search results; page not loadable from our sandbox) | sourced, partly verified |
| Even +20–30% can create stitch lengths unsuitable for garments | zdigitizing | sourced |
| Keep the purchased size; buy the size you need | OML Embroidery, Linda's (FSL) | sourced: [OML](https://omlembroidery.com/resizing-stitch-files-yay-or-nay) |

Conclusion: **±10% is the widely repeated "usually safe" band, ±20% the
common machine/maker ceiling. Neither is a measured standard.** The
practitioner consensus is that the safe band depends on the design (small
text and FSL: ~0%).

## 3. Resizing with stitch recalculation (commercial tools)

| Tool | Method | Range | Basis |
|---|---|---|---|
| Embrilliance Essentials | "Stitch processor" recalculates satin and fill lines to keep density; Ctrl-drag disables recalculation | 50–250% | sourced: [Embrilliance resizing help](https://embrilliance.com/Help/Platform%20Win%201143/resizing.htm), [Essentials](https://embrilliance.com/product/essentials) |
| mySewnet Embroidery | separate "Resize" (density-preserving) and "Scale" (plain) | not stated | sourced: [mySewnet help](https://softwarehelp.mysewnet.com/MSW/100/Embroidery/Topics/Resize_and_Scale.htm) |
| Wilcom EmbroideryStudio / Hatch | convert stitches back to objects, then regenerate; "not all objects will be restored" | not stated | sourced: [Wilcom docs](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/functions/functions-9.htm) |
| BERNINA V9 | converts machine files to outlines on open | not stated | sourced: [BERNINA machine files](https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/machine_files/Machine_Files.htm) |
| Open source (pystitch, pyembroidery, tsembroidery...) | coordinate scaling only; shape processing "out of scope" | — | sourced: [pystitch](https://github.com/inkstitch/pystitch) |

Even recalculating tools can't recreate underlay, compensation or the
digitizer's hand edits perfectly; big changes still need re-digitizing
(**sourced**: [Kimberbell](https://kimberbell.com/blogs/thekimberbellablog/resizing-embroidery-designs-without-losing-quality), zdigitizing).

## 4. What is safe to edit in a stitch file

| Edit | Safe? | Caveats | Basis |
|---|---|---|---|
| Rotate 90/180/270° | Yes | Exact; no density change. Designers already store PES/JEF rotated 90° vs DST for portrait hoops | observed in our test files |
| Rotate arbitrary angle | Mostly | Coordinates are rounded to 0.1 mm grid; fill angle changes visually vs fabric grain | rule of thumb |
| Mirror | Yes geometrically | **Text becomes unreadable**; satin slant flips | rule of thumb |
| Recolor (thread colors) | Yes | DST/EXP have no colors; PES/JEF/HUS map to brand palette (nearest match) | sourced (see [file-formats.md](file-formats.md)) |
| Combine designs / add lettering | Yes | Each part keeps its own density; overlaps create dense stacks (Brother warns about 3+ overlapping stitches) | sourced: [Brother manual](https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html) |
| Reorder colors / merge same-color stops | Caution | Changes layering; can break appliqué/FSL step order | rule of thumb |
| Delete a color block | Caution | Underlay of the next object may be exposed | rule of thumb |
| Remove small stitches | Caution | Wilcom/Hatch offer a filter with user-set minimum length | sourced: [Wilcom](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/quality/quality-7.htm), [Hatch](https://help.hatchembroidery.com/portal/en/kb/articles/how-to-remove-small-stitches) |
| Convert format | Mostly | "Conversion is always lossy" (colors, trims, metadata, object data); stitch-out test per output format | sourced: [pyembroidery PyPI](https://pypi.org/project/pyembroidery/) |
| Resize ≤ ±10% | Usually | Report density factor and longest/shortest stitch | rule of thumb |
| Resize 10–20% | Risky | Warn; recommend test stitch-out | rule of thumb |
| Resize > 20% | Not without recalculation | Recommend buying the right size / re-digitizing | sourced (Embroidery Legacy, zdigitizing) |

## 5. Free-standing lace (FSL)

- Built entirely of thread on wash-away; stitches must interlock
  ([EduTechWiki FSL](https://edutechwiki.unige.ch/en/Stitch_Era_-_free_standing_lace)).
- **Do not resize** purchased FSL: scaling changes the mesh so it may fall
  apart after rinsing or be too dense; pick the size made for your hoop
  ([Linda's FSL](https://lindas.com/blogs/tips-and-tricks/free-standing-lace-embroidery-designs)).
- A normal design sewn on wash-away is **not** FSL; it unravels
  ([Anita Goodesign](https://anitagoodesign.com/blogs/fundamentals/how-to-free-standing-lace-fundamentals)).
- File cannot reliably be detected as FSL from stitches alone; use the
  product name/metadata ("FSL", "lace") (**rule of thumb**).

## 6. Appliqué and die-cut alignment

- Appliqué designs include placement and tack-down steps as separate stops
  ([OESD](https://support.oesd.com/article/35-trim-in-place-applique-tutorial),
  [Ink/Stitch](https://inkstitch.org/tutorials/applique/)).
- Many designers sell matching cut files (SVG/FCM/STUDIO) for cutting
  machines so pre-cut fabric matches the placement line. **Any resize or
  rotation of the stitch file breaks the match with the cut file** unless the
  cut file gets the same transform (**rule of thumb**; we found no source
  documenting die-cut tolerances).
- Our corpus contained appliqué designs; size matched the designer's worksheet
  within 0.1 mm in every format (**observed in our test files**), so the stitch
  files themselves are consistent; the risk is introduced by editing.

---

## Boundary conditions for EEganizer software

| # | Condition | Basis |
|---|---|---|
| R1 | Resize = geometric scale only; never label it "recalculate". Always keep the original file. | sourced (pystitch scope) |
| R2 | Levels: **ok ≤ ±10%**, **caution ±10–20%**, **warning > ±20%**; exactly ±10% counts as ok. | rule of thumb; matches transform.py |
| R3 | After any scale, report: density factor (1/scale²), longest sewn stitch, count of stitches > 12.1 mm and < 0.5 mm **created by the resize** (not pre-existing VP3 travel moves). | sourced limits + observed |
| R4 | Block resize of FSL designs (by name/metadata) or require explicit override. | sourced (Linda's) |
| R5 | Warn when resizing appliqué designs that have a matching cut file. | rule of thumb |
| R6 | Rotation by 90° multiples and recolor are always "ok"; mirror warns if the design is known to contain lettering. | rule of thumb |
| R7 | Never silently merge or reorder color stops when combining or converting. | rule of thumb |
| R8 | After conversion, stitch count may differ by up to ~2% (ties/trims encoding); that is not an error. | observed in our test files |

## Sources

- https://makema.de/en/blogs/faq/stickdateien-skalieren
- https://productblog.wilcom.com/?p=5321
- https://zdigitizing.com/how-to-properly-resize-embroidery-designs/
- https://edutechwiki.unige.ch/en/Embroidery_format_DST
- https://embroiderylegacy.com/?p=403722 ; https://embroiderylegacy.com/?p=25541
- https://omlembroidery.com/resizing-stitch-files-yay-or-nay
- https://kimberbell.com/blogs/thekimberbellablog/resizing-embroidery-designs-without-losing-quality
- BERNINA ±20% for EXP (quoted in search results): https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/network/network-15.htm
- https://embrilliance.com/Help/Platform%20Win%201143/resizing.htm ; https://embrilliance.com/product/essentials
- https://softwarehelp.mysewnet.com/MSW/100/Embroidery/Topics/Resize_and_Scale.htm
- https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/functions/functions-9.htm
- https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/machine_files/Machine_Files.htm
- https://github.com/inkstitch/pystitch ; https://pypi.org/project/pyembroidery/
- https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html
- https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/quality/quality-7.htm ; https://help.hatchembroidery.com/portal/en/kb/articles/how-to-remove-small-stitches
- https://edutechwiki.unige.ch/en/Stitch_Era_-_free_standing_lace ; https://lindas.com/blogs/tips-and-tricks/free-standing-lace-embroidery-designs ; https://anitagoodesign.com/blogs/fundamentals/how-to-free-standing-lace-fundamentals
- https://support.oesd.com/article/35-trim-in-place-applique-tutorial ; https://inkstitch.org/tutorials/applique/
- Our corpus: [../CORPUS.md](../CORPUS.md)
