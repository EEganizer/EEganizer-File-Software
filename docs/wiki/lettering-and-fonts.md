# Lettering and embroidery fonts

How customers put names and words into embroidery, how alphabet packs are
built and named, and the size limits for readable text.

Evidence labels: **sourced** (link), **rule of thumb**, **observed in our test
files**.

---

## 1. Embroidery fonts vs computer fonts

| | Computer font (TTF/OTF) | Embroidery font |
|---|---|---|
| Content | Vector outlines | Pre-digitized stitches (or objects) per character |
| Size | Any size | A tested **size range**; outside it quality drops ([Hatch fonts](https://help.hatchembroidery.com/portal/en/kb/articles/what-should-i-know-about-hatch-fonts-truetype-fonts-and-third-party-fonts)) |
| Install | OS font folder | Depends on format: keyboard font in software (BX, Hatch/Wilcom ESA), or just a folder of stitch files |
| Typing | Yes | Only keyboard fonts; alphabet packs are placed letter by letter |

**Auto-digitizing TTF text is hard.** Wilcom converts installed TrueType/OpenType
fonts on the fly, but quality "may not be quite as good" as hand-digitized
fonts and depends on the shapes; narrow serif fonts convert better than block
fonts ([Wilcom select fonts](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Lettering/lettering_create/lettering_create-4.htm)).
Hatch: "not all TTFs are optimized for embroidery", always test-stitch (Hatch
fonts). Reasons (**rule of thumb**): stroke widths vary within a glyph (satin
too narrow or too wide), counters close up at small sizes, no pull
compensation tuned per glyph, and no sensible stitch angles or entry/exit
points. EEganizer's lettering engine does **not** auto-digitize; it places
pre-digitized letters ([`lettering.py`](../../src/eeganizer_files/lettering.py)).

## 2. Font formats customers own

| Format | What it is | Basis |
|---|---|---|
| Alphabet pack (stitch files) | One stitch file per character, per size, per machine format; "not fonts or .ttf files, or files you can install" | sourced: [Emblibrary alphabets](https://emblibrary.com/page/help/tips-alphabets), [Embroidery Legacy](https://help.embroiderylegacy.com/article/45-what-are-alphabet-stitch-file-fonts) |
| BX (Embrilliance) | Pre-mapped keyboard font: type on the keyboard to produce word designs; works only in Embrilliance (Essentials, AlphaTricks) and Designer's Gallery EmbroideryWorks | sourced: [Creative Appliques BX tutorial](https://creativeappliques.com/blog/embrilliance-software-how-to-use-bx-fonts-format/), [Embroidery Legacy BX listings](https://embroiderylegacy.com/?p=199826) |
| Hatch / Wilcom native fonts | Object fonts with recommended size range and preset join method | sourced: Hatch fonts; [Hatch included fonts](https://help.hatchembroidery.com/portal/en/kb/articles/which-fonts-are-included-in-hatch-embroidery-4) |
| Machine built-in fonts | Fixed set on the machine screen | rule of thumb |

BX files are a proprietary container; we have no published spec and do not
parse them (**rule of thumb / our scope**). Treat them as "store, don't preview".

## 3. Alphabet pack structure and naming

Typical pack: every character × several sizes × every machine format,
delivered as zips, often with a PDF chart (**rule of thumb**).

**Naming conventions** seen in packs (**observed in our test files** and in
`lettering.py`'s parser):

| Character class | Names seen |
|---|---|
| Capitals | `A.pes`, `Upper B.jef`, `Script_A.dst` |
| Lowercase | **doubled letter** `aa.pes`, `bb.pes`; or `a_lower`, `Lower a` |
| Symbols | spelled out: `Question Mark Symbol`, `Exclamation Point`, `Pound Sign Symbol Hashtag`, `Ampersand`, `Apostrophe`, `Backslash`, `Comma`, `Hyphen`, `Period` |
| Digits | `1.pes` or `One.pes` |
| Misspellings | `exlamation`, `exclamtion` occur in real packs |

Why doubled lowercase: Windows file names are case-insensitive by default, so
`A.pes` and `a.pes` cannot coexist in one folder. Microsoft documents that
NTFS supports case-sensitive (POSIX) semantics "but this is not the default
behavior" ([Microsoft: Naming Files](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file)).
The link between that and the `aa` convention is our inference; we found no
designer documentation stating it (**rule of thumb**). Symbols are spelled out
because `? \ / : * " < > |` are reserved in Windows file names (Microsoft,
same page).

### Example pack: JKD 101 "Benjamin" (observed in our test files)

| Property | Value |
|---|---|
| Characters | **61**: A–Z, lowercase as doubled letters `aa`–`zz`, symbols `& ' \ , - ! . # ?` |
| Sizes | 6: 0.75, 1.0, 1.5, 2.0, 2.5, 3.0 inch |
| Size meaning | ≈ capital letter height: "1.0 inch" capitals measure ~24.8 mm (nominal 25.4 mm) |
| Formats | DST, EXP, HUS, JEF, PES, VIP, VP3, XXX, plus Embrilliance BX fonts |
| PES files | 366 (61 × 6) |
| Style | All-caps style: lowercase files are the same height as capitals; no descenders |
| Defect | 20 of 366 PES files have a stray byte before the PEC end marker; 17 of those store PEC stitches rotated 90° clockwise (details in [file-formats.md](file-formats.md#pespec-defects-seen-in-the-wild)) |

## 4. Minimum readable letter height

Height is usually measured on capitals; lowercase in normal fonts is about
70% of cap height ([Wilcom select fonts](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Lettering/lettering_create/lettering_create-4.htm)),
so measure the smallest letter, including lowercase
([Graphics Pro](https://graphics-pro.com/education/what-can-embroiderers-do-to-execute-small-lettering-successfully/)).

| Stitch type / thread | Minimum height | Basis |
|---|---|---|
| Satin, 40 wt, 75/11 needle | **~5 mm**; below that "may cause stitching problems" | sourced: Graphics Pro |
| Satin, general quality guideline | **~6.35 mm (1/4 in)** | sourced: [ASI small letters](https://members.asicentral.com/news/how-to/may-2018/keep-your-small-letters-crisp/), [Impressions](https://impressionsmagazine.com/how-to-digitize-small-lettering/) |
| Satin, 60 wt, 70/10 or 65/9 needle | ~4–5 mm; about 25% smaller than 40 wt | sourced: [Amann](https://www.amann.com/knowledgehub/blog/small-embroidery-designs-precision-starts-with-the-right-thread/), Graphics Pro |
| Running stitch | smallest letters are made with running stitch | sourced (qualitative): Impressions |
| Fill (tatami) letters | Only for large/bold letters whose strokes exceed satin width (~7–12 mm) | rule of thumb, derived from satin max width ([digitizing-fundamentals.md](digitizing-fundamentals.md#4-stitch-length-limits)) |
| Column width | as important as height; satin can't be narrower than the needle | sourced: ASI small letters |

Sources disagree: 5 mm (Graphics Pro) vs 6.35 mm (ASI/Impressions) for 40 wt
satin. Use 5 mm as the hard warning, 6.35 mm as the soft warning.

## 5. Spacing, baselines, descenders

| Topic | Guidance | Basis |
|---|---|---|
| Letter spacing (tracking) | Packs rarely ship kerning data; spacing must be set by the software | rule of thumb |
| Baseline | Align letters on a common baseline; descenders (g j p q y , ;) go below it | rule of thumb; implemented in `lettering.py` |
| x-height letters | a c e m n o r s u v w x z sit at x-height in normal fonts | rule of thumb |
| All-caps style fonts | "Lowercase" files are capitals or small caps of the same height; no descenders | observed in our test files (Benjamin) |
| Join method | Hatch presets per font; "closest join" reduces trims | sourced: Hatch fonts |
| Underlay for small text | center walk instead of edge walk | sourced: ASI small letters |

## 6. Monograms

Monograms are 1–3 letters, often with a larger middle initial (last name) in
classic 3-letter monograms; sold as monogram alphabet sets with frames
(**rule of thumb**; no numeric standard found). Order and sizing are a
layout concern for our compose engine, not a file-format concern.

---

## Boundary conditions for EEganizer software

| # | Condition | Basis |
|---|---|---|
| L1 | Parse alphabet file names: doubled letters = lowercase; spelled-out symbol names (with filler words "symbol", "sign", "mark", "point") and common misspellings. | observed in our test files |
| L2 | Never assume a lowercase file is shorter than the capital; detect all-caps fonts by comparing heights. | observed in our test files |
| L3 | Alphabet size names (e.g. "1.0 inch") ≈ cap height, within ~3% (24.8 vs 25.4 mm). Use measured bounds, not the name. | observed in our test files |
| L4 | Warn when composed text has cap height < **6.35 mm** (soft) or < **5 mm** (hard) for satin lettering; suggest 60 wt below 5 mm. | sourced, sources disagree |
| L5 | Do not scale alphabet letters beyond the pack's size steps; pick the nearest provided size instead (sizes are digitized separately). | rule of thumb + resize guidance |
| L6 | Treat BX and native font formats as opaque: store, don't preview or convert. | scope; no public spec |
| L7 | Do not auto-digitize TTF fonts; out of scope and quality-sensitive. | sourced (Wilcom, Hatch) |
| L8 | Validate each letter file independently: one bad file in a pack (e.g. stray PEC byte) must not break the whole word. | observed in our test files |

## Sources

- https://help.hatchembroidery.com/portal/en/kb/articles/what-should-i-know-about-hatch-fonts-truetype-fonts-and-third-party-fonts
- https://help.hatchembroidery.com/portal/en/kb/articles/which-fonts-are-included-in-hatch-embroidery-4
- https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Lettering/lettering_create/lettering_create-4.htm
- https://emblibrary.com/page/help/tips-alphabets
- https://help.embroiderylegacy.com/article/45-what-are-alphabet-stitch-file-fonts
- https://creativeappliques.com/blog/embrilliance-software-how-to-use-bx-fonts-format/
- https://embroiderylegacy.com/?p=199826
- https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file
- https://graphics-pro.com/education/what-can-embroiderers-do-to-execute-small-lettering-successfully/
- https://members.asicentral.com/news/how-to/may-2018/keep-your-small-letters-crisp/
- https://impressionsmagazine.com/how-to-digitize-small-lettering/
- https://www.amann.com/knowledgehub/blog/small-embroidery-designs-precision-starts-with-the-right-thread/
- https://abdigitizing.com/how-to-digitize-small-text-for-embroidery-under-5mm-without-messing-up/
- Our corpus and parser: [../CORPUS.md](../CORPUS.md), [../../src/eeganizer_files/lettering.py](../../src/eeganizer_files/lettering.py)
