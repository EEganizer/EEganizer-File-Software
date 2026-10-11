# Real-file test corpus

`tests/test_corpus.py` runs against real commercial designs kept **outside**
this repository (purchased designs may not be redistributed, and this repo is
public). To run it:

```bash
EEFILE_CORPUS_DIR=/path/to/designs pytest -q
```

Without the variable the corpus tests are skipped.

## First corpus (2026-10-10)

4 commercial designs (applique and sketch fill), 17 sizes, each in PES, DST,
EXP, HUS, JEF and VP3 = 102 files, plus the designer's Wilcom production
worksheets. Result: **all 102 files read, render and convert**; 294 tests pass.

| Check | Result |
|---|---|
| Size vs. designer worksheet | within 0.1 mm on all 4 worksheets |
| Size across 6 formats | identical (PES/JEF sometimes rotated 90° — the designer's choice for portrait hoops) |
| Stitch count across formats | within 2% (each format encodes ties/trims differently) |
| Color changes across formats | identical |
| Thread colors (PES/HUS/JEF/VP3) | same sequence as the worksheet, mapped to each brand's nearest palette color |
| Fits the hoop named in the file | yes for every "4x4/5x7/6x10/8x8" file (after removing a default 2 mm clearance) |
| Parse time | 0.1–0.3 s per file including sandbox start-up |

## What the corpus changed

- **Hoop fit:** default clearance removed. Designs sold as "4x4" measure up to
  98.6 mm and "6x10" up to 257.4 mm; a 2 mm margin wrongly pushed them to the
  next hoop.
- **VP3 travel moves:** VP3 has no jump command; moves between areas are
  stored as stitches (41–126 mm). Moves over 12.1 mm are now counted as
  `travel_move_count` and excluded from stitch statistics. Shorter VP3 moves
  (10–11 mm) are indistinguishable from stitches, so VP3's longest stitch can
  read higher than other formats.
- **Resize report:** only flags long/short stitches the resize created; an
  exact 10% resize is "ok".
- **Distinct colors:** added `unique_color_count` (the worksheet "Colors"
  figure: e.g. 5 colors used across 19 stops).

## Known differences (not bugs)

- Our stitch count is 1–4% lower than Wilcom's worksheet count; Wilcom
  appears to count jumps and trims as stitches, we count sewn stitches only.
- `trim_count` depends on how each format encodes trims (0 in HUS/VP3, 32 in
  PES for the same design). Don't show it to customers as a design property.
- DST/EXP carry no colors; previews show placeholder colors.

## Still needed

More designers and digitizing software, plus XXX, SEW and larger
(10k+ stitch, multi-hoop) designs; then test stitch-outs on real machines.

## Alphabet pack (2026-10-11)

One commercial embroidery font ("Benjamin", JKD 101): 61 characters × 6 sizes
(0.75–3.0 inch) × 8 formats (DST, EXP, HUS, JEF, PES, VIP, VP3, XXX) plus
Embrilliance BX files — 2,934 files. Run with
`EEFILE_FONT_DIR=/path/to/font pytest -q`.

| Check | Result |
|---|---|
| Files read | all 2,562 non-VIP letter files; VIP (366) and BX (6) are store-only |
| Alphabets discovered | 42 (6 sizes × 7 readable formats), 61 characters each |
| Size label | "1.0 inch" = capital height (~24 mm); sizes chosen by nearest capital height |
| Letters across formats | same size within 0.3 mm (1 mm for repaired PES letters) |
| Name below a design | "Benjamin" under a real 4x4 design → one PES, one thread color for the name, fits 5x7 rotated |

### What the font changed

- **Real pack naming**: lowercase files are doubled letters (`aa.pes` —
  Windows file names ignore case), symbols are spelled out with filler words
  (`_Question Mark Symbol`, `Pound Sign Symbol Hashtag`, `Exclamation Point`),
  and one file is misspelled (`Exlamation`). The parser handles all of these;
  unrecognised files are listed in `Alphabet.unrecognized` so a customer can
  be asked which character they are.
- **All-caps style fonts**: lowercase is as tall as the capitals, so g/j/p/q/y
  must not drop below the baseline. Descender handling now switches on only
  when the font's x-height is clearly below its capital height.
- **Broken PES letters**: 20 of 366 PES files have a stray byte before the
  PEC end marker; pystitch then reads the thumbnail images as stitches (a
  letter ~1 m tall). 17 of them also store stitches turned 90° clockwise
  against their own header and the DST/JEF/VP3 copies. `load_design` now
  checks decoded size against the PEC header, re-reads only up to the
  recorded block end, and turns those 17 back upright (flagged in
  `pattern.extras["eefile_repaired"]`). Worth reporting upstream to pystitch
  and to the designer.
