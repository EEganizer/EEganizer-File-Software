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
