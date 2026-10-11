# Embroidery file formats

Per-format facts that our parsers, converters and UI must respect.

Evidence labels: **sourced** (link), **rule of thumb**, **observed in our test
files**. "pystitch" means the source code of pystitch 1.0.1 (MIT, Ink/Stitch
team), read directly from the PyPI wheel; constants are quoted from it.

Units: almost all formats store coordinates in **0.1 mm** units
(pystitch `PPMM = 10`; [EduTechWiki DST](https://edutechwiki.unige.ch/en/Embroidery_format_DST)).

---

## 1. Summary table

| Format | Owner / machines | Type | Colors in file | Max stitch / jump per record | Notes |
|---|---|---|---|---|---|
| **PES** (+ embedded **PEC**) | Brother, Baby Lock, (BERNINA reads PEC) | Stitch (+ PE-Design objects in PES part) | PEC: index into Brother palette (64 entries); PES v5+: also RGB + catalog/brand thread list | PEC long form 12-bit signed: ±2047 units = **±204.7 mm** | Versions `#PES0001`–`#PES0100`; PEC block same in all versions |
| **DST** | Tajima; universal commercial format; Brother reads it | Stitch | **None** (optional non-standard `TC` tag) | **121 units = 12.1 mm** stitch and jump | 512-byte text header; trim = N jumps (often 3) |
| **EXP** | Melco; BERNINA (USB EXP) | Stitch | **None** in EXP itself; BERNINA adds `.INF` (colors) + `.BMP` (preview) | **127 units = 12.7 mm** | 2-byte records, `0x80` escape for commands |
| **JEF** (`JEF+`) | Janome, Elna | Stitch | Index into Janome palette (78 entries in pystitch) | **127 units = 12.7 mm** | Header has hoop code 0–4 |
| **SEW** | Older Janome / Elna / Kenmore | Stitch | Index into palette (79 entries in pystitch) | pystitch writes it; limits not documented | Legacy |
| **HUS** | Husqvarna Viking (older) | Stitch, **compressed** | Index into Husqvarna palette (29 entries in pystitch) | — | Proprietary compression (ARJ-like) |
| **VIP** | Husqvarna Viking / Pfaff (after HUS) | Stitch, compressed | Thread/color blocks | — | **pystitch 1.0.1 has no VIP reader or writer** (no `VipReader.py` in the wheel) |
| **VP3** | Husqvarna Viking / Pfaff (current) | Stitch | **RGB** per thread block | normal stitch 8-bit; long record 16-bit signed (writer splits > 3200 units) | **No jump command**: moves are long stitches |
| **XXX** | Singer | Stitch | RGB (32-bit) list | **124 units = 12.4 mm**; long moves via `0x7D` 16-bit | |
| **EMB** | Wilcom / Hatch | **Object** (working file) | Full | n/a | Proprietary; no open reader |
| **ART** | BERNINA | **Object** (native) | Full | n/a | Only BERNINA software writes ART; Hatch reads ART V1–4 |
| **BX** | Embrilliance | Keyboard font | n/a | n/a | Only Embrilliance programs use it |

Sources per row: see sections below.

## 2. PES / PEC (Brother)

**Structure.** A PES file = PES header + (optional) PE-Design object section
+ **PEC block**. The PEC block is the same in all versions so the file stays
compatible with Brother (and BERNINA) machines
([libpes wiki](https://github.com/frno7/libpes/wiki/PES-format)). Machines sew
the PEC block.

| Item | Fact | Basis |
|---|---|---|
| Versions | `#PES0001`, 0020, 0022, 0030, 0040, 0050, 0055, 0056, 0060, 0070, 0080, 0090, 0100 handled by pystitch's reader; unknown versions fall back to the PEC block | sourced: pystitch `PesReader.py` |
| Current version | PE-Design 11 writes v11-era files; older PE-Design cannot open newer PES | sourced: [zdigitizing PES](https://zdigitizing.com/what-is-a-pes-file/) (vendor blog) |
| Machine compatibility | older machines may need v1 or v6; Luminaire-class handle v10+ | sourced: zdigitizing (not an official Brother table) |
| Writer support | pystitch writes **v1 or v6 only** | sourced: pystitch `PesWriter.py` |
| PEC label | `LA:` + 16-char name | sourced: pystitch `PecReader.py` |
| Color count | stored as (colors − 1); then one palette index byte per color | sourced: pystitch, [EduTechWiki PEC](https://edutechwiki.unige.ch/en/Embroidery_format_PEC) |
| Palette | indices 1–64; 63 thread colors + index 64 "Applique"; verified against a Brother Innov-is 955 per EduTechWiki | sourced: pystitch `EmbThreadPec.py`, EduTechWiki PEC |
| RGB threads | PES v5 and later store a thread list with catalog number, RGB, description, brand, chart | sourced: pystitch `PesReader.read_pes_thread` |
| Stitch-block length | 24-bit little-endian length field before the stitches | sourced: pystitch `PecReader.py` |
| Header extents | 6 × 16-bit values after the block length incl. design width and height | sourced: pystitch `PecReader.py`/`PecWriter.py` |
| Stitch encoding | short form 7-bit signed (±63); long form 12-bit signed (±2047) with jump (`0x10`) / trim (`0x20`) flags | sourced: pystitch |
| Color change | `0xFE 0xB0` + 1 byte | sourced: pystitch |
| End marker | `0xFF 0x00` (reader also stops at `0xFF` + EOF) | sourced: pystitch |
| Thumbnails | after the stitch block: 1 overview + 1 per color, **48 × 38 px, 1 bit/pixel** (6 bytes × 38 rows = 228 bytes each) | sourced: pystitch `PecWriter.py` (`PEC_ICON_WIDTH = 48`, `PEC_ICON_HEIGHT = 38`); EduTechWiki PEC (height 38) |
| Brother machines | read `.pes` and `.dst` (some models also `.phc`, `.phx`); DST shown with Brother default color sequence | sourced: [Brother manual](https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html) |

### PES/PEC defects seen in the wild

**Observed in our test files** (alphabet pack JKD 101 "Benjamin"):

- **20 of 366 PES files** have a **stray byte before the PEC end marker**. A
  naive decoder that only looks for `0xFF 0x00` at a 2-byte boundary misses
  the end and decodes the 48 × 38 thumbnail bitmaps as stitches; one letter
  then reads as **~1 m tall**.
- **17 of those 20** also store the PEC stitches **rotated 90° clockwise**
  relative to their own PEC header and relative to the same letter in the
  other 7 formats.
- **Detection and repair:** use the PEC header. (1) The **stitch-block length**
  field says where stitches end; stop decoding there instead of trusting the
  end marker. (2) Compare decoded width/height with the header's
  **width/height**; if they match only after swapping, rotate the stitches
  90° counter-clockwise. (3) Sanity-check: any design larger than the
  largest hoop (~0.5 m) is a decode error, not a design.

Other PES observations (**observed in our test files**):

- Some PES/JEF files are stored **rotated 90°** compared with the DST of the
  same design (designer rotates for portrait hoops).
- PES had the most trims of all formats for the same design (up to 32 vs 0
  in HUS/VP3).

## 3. DST (Tajima)

| Item | Fact | Basis |
|---|---|---|
| Header | fixed **512 bytes**; ~125 used, rest padded with spaces (`0x20`) | sourced: [EduTechWiki DST](https://edutechwiki.unige.ch/en/Embroidery_format_DST) |
| Header fields | `LA:` label (16 chars), `ST:` stitch count, `CO:` color changes, `+X/-X/+Y/-Y` extents, `AX/AY` end offset, `MX/MY`, `PD:`; optional `AU:` author, `CP:` copyright, `TC:` thread colors (non-standard) | sourced: pystitch `DstWriter.py`/`DstReader.py` |
| Header reliability | many programs write incorrect header values; recompute from stitches | sourced: [Image::Embroidery](https://metacpan.org/pod/Image::Embroidery) |
| Records | 3 bytes per record, balanced-ternary coded X/Y | sourced: [KDE Tajima Ternary](https://community.kde.org/Projects/Liberty/File_Formats/Tajima_Ternary) |
| Max displacement | **121 units = 12.1 mm** for stitch and jump | sourced: EduTechWiki DST; pystitch `MAX_STITCH_DISTANCE = 121` |
| Colors | **none**; thread colors not stored | sourced: EduTechWiki DST, KDE, Brother manual |
| Trim | no trim command; trim = consecutive jumps, "often 3 but could be as high as 5"; machine setting | sourced: EduTechWiki DST; Wilcom trim functions; pystitch `trim_at = 3` |
| Color change | stop/color-change command; machine assigns needle | sourced: KDE |

## 4. EXP (Melco / BERNINA)

| Item | Fact | Basis |
|---|---|---|
| Records | signed 8-bit dx, dy; X = `0x80` (−128) escapes a command named by the next byte | sourced: [EduTechWiki EXP](https://edutechwiki.unige.ch/en/Embroidery_format_EXP) (one table says −127; **sources disagree** on the escape value), pystitch `ExpReader.py` uses `0x80` |
| Commands | `0x80 0x01` color change/stop; `0x80 0x04` jump; `0x80 0x80` trim (pystitch) / end (EduTechWiki); odd codes like `0x80 0x06` seen in real files | sourced: EduTechWiki EXP, pystitch |
| Max displacement | **127 units = 12.7 mm** | sourced: pystitch `ExpWriter.py` |
| Colors | Melco EXP: none. BERNINA "USB EXP" = 3 files: `.EXP` stitches, `.INF` thread colors, `.BMP` preview | sourced: [OESD](https://support.oesd.com/article/64-how-do-i-use-exp-format-with-my-bernina-machine), [Embroidery Online](https://embroideryonline.com/exp-formats-for-bernina/) |
| BERNINA resize | EXP on the machine should only be scaled ±20% | sourced: BERNINA help (quoted via search) |

## 5. JEF (Janome)

| Item | Fact | Basis |
|---|---|---|
| Header | stitch-start offset, date, version letter (model), color count, point count, **hoop code**, extents from hoop center | sourced: [EduTechWiki JEF](https://edutechwiki.unige.ch/en/Embroidery_format_JEF), [KDE JEF](https://community.kde.org/Projects/Liberty/File_Formats/Janome_Embroidery_Format) |
| Hoop codes | 0 = 110×110, 1 = 50×50, 2 = 140×200, 3 = 126×110, 4 = 200×200 mm | sourced: EduTechWiki JEF, pystitch `JefWriter.py` |
| Records | 2 bytes, signed −127..127; X = −128 (`0x80`) escapes END, COLOR_CHANGE, STOP, JUMP, TRIM | sourced: EduTechWiki JEF |
| Max displacement | **127 units = 12.7 mm** | sourced: pystitch |
| Colors | index into Janome palette (78 colors in pystitch) | sourced: pystitch `EmbThreadJef.py` |
| JEF+ | editable variant created on machine or Horizon Link / Suite | sourced: [Janome formats](https://www.janome.com/create-learn/janome-embroidery-formats/), [emborado JEF](https://emborado.de/en/glossary/jef-file) |
| Observed | stored rotated 90° vs DST in some designs (portrait hoop) | observed in our test files |

Caveat: the hoop code is chosen by the writer from design size; a design may
fit a hoop the code does not name. Use measured bounds, not the code
(**rule of thumb**).

## 6. Husqvarna Viking / Pfaff: HUS, VIP, VP3

| Item | Fact | Basis |
|---|---|---|
| Lineage | HUS (Viking) → VIP (after merger with PFAFF, late 1990s) → VP3/VP4 | sourced: [PRONOM fmt/2001](https://www.nationalarchives.gov.uk/PRONOM/fmt/2001), [fmt/2002](https://www.nationalarchives.gov.uk/PRONOM/fmt/2002) |
| HUS | stitch + attribute data compressed with a proprietary (ARJ-related) scheme | sourced: [KDE HUS](https://community.kde.org/Projects/Liberty/File_Formats/Husqvarna_HUS), [emborado HUS](https://emborado.de/en/glossary/hus-file) |
| HUS colors | index into a Husqvarna palette (29 entries in pystitch) | sourced: pystitch `EmbThreadHus.py` |
| HUS commands | `0x81` jump, `0x88` trim (pystitch reader) | sourced: pystitch `HusReader.py` |
| VIP | ARJ-style compressed blocks for colors and stitches | sourced: [emborado VIP](https://www.emborado.de/en/glossary/vip-file) |
| VP3 structure | magic string, hoop/design info, tagged stitch blocks per thread | sourced: [EduTechWiki VP3](https://edutechwiki.unige.ch/en/Embroidery_format_VP3), [KDE Viking Pfaff](https://community.kde.org/Projects/Liberty/File_Formats/Viking_Pfaff) |
| VP3 colors | 24-bit RGB per thread, plus catalog/brand strings | sourced: pystitch `Vp3Reader.py` |
| VP3 moves | **no jump command**: `0x80 0x01` + two signed 16-bit values is a long *stitch*; pystitch writer comment: "jump is stitch" | sourced: pystitch `Vp3Reader.py`/`Vp3Writer.py` |
| VP3 trim | `0x80 0x03` | sourced: pystitch |
| Observed | moves between areas stored as long stitches of **41–126 mm**; short moves of 10–11 mm are indistinguishable from stitches; 0 trims in HUS/VP3 for designs that had up to 32 in PES | observed in our test files |

## 7. XXX (Singer) and SEW (Janome legacy)

| Item | Fact | Basis |
|---|---|---|
| XXX header | color count at offset 0x27; stitches from 0x100 | sourced: pystitch `XxxReader.py` |
| XXX records | 2-byte stitch; `0x7D` + 16-bit X/Y = long move; `0x7F` escapes (01 move, 03 trim, 08/0A–17 color change, 7F/18 end) | sourced: pystitch |
| XXX max | **124 units = 12.4 mm** (`0xFD..0xFF` reserved) | sourced: pystitch `XxxWriter.py` |
| XXX colors | list of 32-bit color values at end | sourced: pystitch |
| SEW | older Janome/Elna/Kenmore; stitch-only; header 0x1D78 bytes in pystitch writer; palette 79 entries | sourced: pystitch `SewWriter.py`; [emborado](https://www.emborado.de/en/glossary/embroidery-file-format) |

## 8. Object and proprietary formats: EMB, ART, BX

| Format | Facts | Basis |
|---|---|---|
| EMB (Wilcom, Hatch) | "Working file"; Hatch exports EMB 26.0, 27.0, e4.15, Hatch 3; not lower | sourced: [Hatch formats](https://help.hatchembroidery.com/portal/en/kb/articles/what-file-formats-does-hatch-embroidery-v2-v3-read-and-write) |
| ART (BERNINA) | native; contains everything to stitch and edit; only BERNINA software saves ART; Hatch reads ART V1–4, ART42/50/60/70, exports EXP for BERNINA | sourced: [BERNINA machine files](https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/machine_files/Machine_Files.htm), Hatch formats, [Pulse](https://hmsupport.pulsemicro.com/support/solutions/articles/9000238695-catalog-xpress-and-art-file-support) |
| ART in open source | reader commented out in pyembroidery; pystitch 1.0.1 ships `ArtReader.py` fully commented out (sketch: OLE compound file, `Contents` stream, byte swizzle + zlib) | sourced: [pyembroidery EmbPattern.py](https://raw.githubusercontent.com/EmbroidePy/pyembroidery/main/pyembroidery/EmbPattern.py), pystitch `ArtReader.py` |
| BX | Embrilliance keyboard font | sourced: see [lettering-and-fonts.md](lettering-and-fonts.md) |

## 9. Same design across formats

**Observed in our test files** (102 files: 4 designs × several sizes × PES,
DST, EXP, HUS, JEF, VP3; digitized in Wilcom EmbroideryStudio):

| Property | Agreement across formats |
|---|---|
| Size (bounds) | Identical; within 0.1 mm of the designer's worksheet. PES/JEF sometimes rotated 90° |
| Color-change count | Identical |
| Stitch count | Within 2% (ties/trims encoded differently) |
| Stitch count vs Wilcom worksheet | Worksheet 1–4% higher (appears to count jumps/trims) |
| Thread colors | DST/EXP: none. PES/HUS/JEF/VP3: same sequence, each mapped to that brand's nearest palette color |
| Trim count | Not stable: 0 (HUS/VP3) to 32 (PES) |
| Longest stitch | VP3 can read higher (unflagged 10–11 mm moves) |

---

## Boundary conditions for EEganizer software

| # | Condition | Basis |
|---|---|---|
| F1 | Coordinates are 0.1 mm units; report sizes in mm with 0.1 mm precision. | sourced |
| F2 | Per-record limits when **writing**: DST 12.1 mm, XXX 12.4 mm, EXP/JEF 12.7 mm, PEC 204.7 mm. Longer moves must be split into jumps (pystitch does this). | sourced (pystitch) |
| F3 | When **reading**, classify any move > 12.1 mm as travel (VP3 stores them as stitches); exclude travel from stitch-length statistics. | observed + sourced |
| F4 | DST/EXP have no colors: show "colors not stored in this format" and placeholder colors; never invent thread names. BERNINA EXP: look for a sibling `.INF`. | sourced |
| F5 | Converting to PES/JEF/HUS maps RGB to the nearest palette entry (PEC 63 colors, JEF 78, HUS 29); conversion is lossy for color. | sourced (pystitch palettes) + observed |
| F6 | Don't show trim count as a design property; show color stops and unique colors. | observed |
| F7 | Expect ±2% stitch-count differences across formats and 1–4% vs vendor worksheets. | observed |
| F8 | PES: trust the PEC stitch-block length over the end marker; compare decoded size with PEC header width/height; repair 90° rotation when only the swapped size matches. Reject decoded designs larger than any hoop. | observed in our test files |
| F9 | Recompute DST header values from stitches; never trust `ST:`/`CO:`/extents. | sourced |
| F10 | Fit/orientation: allow 90° rotation; PES/JEF may be stored rotated vs DST. | observed |
| F11 | PES output: pystitch writes v1/v6 only; that is the most compatible choice for older machines. | sourced |
| F12 | EMB, ART, BX, VIP (no pystitch reader), encrypted files: store and label "preview unavailable"; never decrypt. | sourced + policy |
| F13 | Treat every file as untrusted: parse in the sandbox with size/time limits (HUS/VIP decompression in particular). | policy ([../PLAN.md](../PLAN.md)) |

## Sources

- pystitch 1.0.1 source (read directly): https://pypi.org/project/pystitch/ ; https://github.com/inkstitch/pystitch — files `DstWriter.py`, `DstReader.py`, `ExpReader.py`, `ExpWriter.py`, `JefWriter.py`, `PecReader.py`, `PecWriter.py`, `PesReader.py`, `PesWriter.py`, `Vp3Reader.py`, `Vp3Writer.py`, `XxxReader.py`, `XxxWriter.py`, `HusReader.py`, `SewWriter.py`, `EmbThreadPec.py`, `EmbThreadJef.py`, `EmbThreadHus.py`, `EmbThreadSew.py`
- https://github.com/frno7/libpes/wiki/PES-format
- https://edutechwiki.unige.ch/en/Embroidery_format_PEC ; https://edutechwiki.unige.ch/en/Embroidery_format_PES ; https://edutechwiki.unige.ch/en/Embroidery_format_DST ; https://edutechwiki.unige.ch/en/Embroidery_format_EXP ; https://edutechwiki.unige.ch/en/Embroidery_format_JEF ; https://edutechwiki.unige.ch/en/Embroidery_format_VP3 ; https://edutechwiki.unige.ch/en/Embroidery_format
- https://community.kde.org/Projects/Liberty/File_Formats/Tajima_Ternary ; https://community.kde.org/Projects/Liberty/File_Formats/Janome_Embroidery_Format ; https://community.kde.org/Projects/Liberty/File_Formats/Viking_Pfaff ; https://community.kde.org/Projects/Liberty/File_Formats/Husqvarna_HUS
- https://metacpan.org/pod/Image::Embroidery
- https://zdigitizing.com/what-is-a-pes-file/
- https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html
- https://support.oesd.com/article/64-how-do-i-use-exp-format-with-my-bernina-machine ; https://embroideryonline.com/exp-formats-for-bernina/
- https://www.janome.com/create-learn/janome-embroidery-formats/ ; https://emborado.de/en/glossary/jef-file
- https://www.nationalarchives.gov.uk/PRONOM/fmt/2001 ; https://www.nationalarchives.gov.uk/PRONOM/fmt/2002
- https://emborado.de/en/glossary/hus-file ; https://www.emborado.de/en/glossary/vip-file ; https://www.emborado.de/en/glossary/embroidery-file-format
- https://help.hatchembroidery.com/portal/en/kb/articles/what-file-formats-does-hatch-embroidery-v2-v3-read-and-write
- https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/machine_files/Machine_Files.htm
- https://hmsupport.pulsemicro.com/support/solutions/articles/9000238695-catalog-xpress-and-art-file-support
- https://docs.wilcom.com/embroiderystudio/27/en/OnlineHelp/Setup/machines/machines-4.htm
- Our corpus: [../CORPUS.md](../CORPUS.md)
