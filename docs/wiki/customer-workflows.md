# Customer workflows

What home and small-business embroiderers actually do with design files, where
it hurts, and what license terms allow.

Evidence labels: **sourced** (link), **rule of thumb**, **observed in our test
files**.

---

## 1. The typical journey

| Step | What the customer does | Pain points | EEganizer touchpoint |
|---|---|---|---|
| 1. Buy | Buys from designer sites, Etsy, Creative Fabrica, subscriptions; downloads a **zip** | Zips contain every size × every format (+ PDFs); 100+ files per design pack | Ingest zips; group by design and size |
| 2. Unzip & file | Saves into folders by designer/theme | Duplicates, cryptic names, lost purchases | Library, search, thumbnails |
| 3. Choose size | Picks the size made for their hoop (sizes named "4x4", "5x7", "6x10") | Nominal names vs real field; rotated files | Fit badge per machine |
| 4. Check colors | Opens the **PDF color sheet / worksheet** (thread sequence, stitch counts, size) | DST has no colors; brand thread names differ | Thread list, printable chart |
| 5. Convert (if needed) | Uses desktop software when their format is missing | Lossy conversion; license doubts | Convert in place |
| 6. Personalize | Adds names/monograms from an alphabet pack or a keyboard font; combines designs | Spacing letters by hand; size of text | Compose + lettering |
| 7. Transfer | USB stick, or Wi-Fi app (Artspira, mySewnet, BERNINA WiFi Device) | Machine doesn't show the file (names, folders, limits) | Download for my machine |
| 8. Stitch out | Hoops fabric + stabilizer; re-threads at every stop on single-needle machines | Thread breaks, puckering | Stop list, time estimate |

Basis: steps and pain points are **rule of thumb** except where linked below.

### What a purchased design pack looks like (observed in our test files)

| Item | Example |
|---|---|
| Designs | 4 designs (appliqué and sketch fill) from one designer |
| Sizes | several per design (17 sizes total), named after hoops: 4x4, 5x7, 6x10, 8x8 |
| Formats | PES, DST, EXP, HUS, JEF, VP3 → **102 stitch files** |
| Extras | the designer's Wilcom EmbroideryStudio production worksheets (PDF): size, stitch count, colors, color sequence |
| Accuracy | sizes match worksheets within 0.1 mm; formats agree on size and color changes; stitch counts within 2% |
| Alphabet pack | 61 characters × 6 sizes × 8 formats + BX fonts (JKD 101 "Benjamin"); see [lettering-and-fonts.md](lettering-and-fonts.md) |

## 2. Organizing libraries

| Tool | Model | Price/limits | Basis |
|---|---|---|---|
| Hatch Organizer | Desktop, catalog with 522 hoop presets | ~$149 | sourced: [Hatch pricing](https://www.hatchembroidery.com/pricing) |
| Embrilliance Essentials | Desktop, edit/resize/lettering | $139–159 | sourced: [Embrilliance](https://embrilliance.com/product/essentials) |
| SewWhat-Pro | Desktop | ~$65 | sourced: [machineembroiderygeek](https://www.machineembroiderygeek.com/?p=20167) |
| Brother Artspira | Phone app + cloud | ~20 cloud files free, ~100 with Artspira+ ($12.99/month at launch) | sourced: [Brother plans](https://support.brother.com/g/s/hf/mobileapp_info/artspira/plan/en.html) |
| mySewnet Cloud | Cloud + desktop | 100 MB on one-purchase plan; subscription designs encrypted | sourced: [mySewnet](https://mysewnet.com/products-and-plans/one-purchase) |
| Wilcom Workspace Library | Browser, 10 GB, aimed at businesses/teams | | sourced: [Wilcom](https://wilcom.com/workspace/library) |
| StitchBuddy (iOS/macOS) | App; free tier saves ≤ 1,000 stitches | | sourced: [App Store](https://apps.apple.com/us/app/-/id522499369) |

(Details from the project research report: [../research/README.md](../research/README.md).)

## 3. Converting formats

- Customers convert when a pack lacks their machine's format or when they
  change machines (**rule of thumb**).
- Conversion is lossy: colors (to palette), trims (re-encoded), object data
  dropped ([pyembroidery](https://pypi.org/project/pyembroidery/)).
- DST → PES/JEF shows default colors; the UI must say so
  ([Brother manual](https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html)).
- BERNINA owners need EXP + INF + BMP, not bare EXP
  ([OESD](https://support.oesd.com/article/64-how-do-i-use-exp-format-with-my-bernina-machine)).

## 4. Checking hoop fit

- Customers think in hoop names. Designs are digitized right up to the
  nominal field (98.6 mm in "4x4", 257.4 mm in "6x10") (**observed in our test
  files**).
- Some machines measure slightly under nominal (3.93 in on a Brother 4x4)
  ([Inkscape forum](https://inkscape.org/it/forums/embroidery/solving-the-pattern-is-too-large-for-frame)).
- Rotation matters: portrait vs landscape hoops; designers already rotate PES/JEF
  (**observed in our test files**).

## 5. Thread charts

- Designers ship PDF color sheets listing stop order, thread color names,
  often in one or two brands (**rule of thumb**; our corpus had Wilcom
  worksheets).
- Brand matching is approximate; palettes differ per machine format
  (PEC 63 colors, JEF 78, HUS 29 in pystitch) (sourced: [file-formats.md](file-formats.md)).
- Single-needle users need the **stop list** (19 stops even if 5 colors)
  (**observed in our test files**).

## 6. Combining designs and names

- Common requests: name under a motif, monogram in a frame, several small
  designs in one hooping (**rule of thumb**).
- Alphabet packs require placing letters one by one; keyboard fonts (BX,
  Hatch) type directly ([Creative Appliques](https://creativeappliques.com/blog/embrilliance-software-how-to-use-bx-fonts-format/)).
- The combined design must still fit the hoop and stay under the machine's
  stitch and color limits ([Brother manual](https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html), [Emblibrary limits](https://emblibrary.com/page/help/embroidery-limits)).

## 7. Transferring to the machine

| Problem | Cause | Basis |
|---|---|---|
| File not shown on Brother | special characters in name; file inside a folder; stitch/color/combined limits exceeded | sourced: Brother manual excerpts |
| Wrong format | machine reads only its own formats (Brother: `.pes`, `.dst`, some `.phc`/`.phx`) | sourced: Brother manual, [Swing Design PRS100](https://www.swingdesign.com/a/answers/6520321/File-type-for-the-Brother-PRS100) |
| Corrupted file | messaging apps (e.g. WhatsApp) compress/alter files | sourced: [makema](https://makema.de/en/blogs/faq/stickdatei-wird-nicht-angezeigt) |
| Wi-Fi locked to brand | Artspira (Brother), mySewnet (Viking/Pfaff), BERNINA WiFi Device | sourced: see [machine-embroidery-basics.md §6](machine-embroidery-basics.md#6-getting-designs-onto-the-machine) |

## 8. Designer license terms

| Term | Typical rule | Basis |
|---|---|---|
| Sharing files | **Never allowed** ("may not sell or share the design file itself"; "never permitted") | sourced: [Urban Threads](https://urbanthreads.com/design/thistle-crest-ut2186), [EmbroideryMonkey](https://www.etsy.com/shop/EmbroideryMonkey) |
| Personal use | Default license; some allow selling finished items at craft fairs / small online shops, not mass production | sourced: Urban Threads |
| Stricter personal | No resale of finished items at all without permission | sourced: [Ignite Wonder](https://ignitewonder.patternbyetsy.com/policy) |
| Commercial use | Separate license / individual approval | sourced: EmbroideryMonkey, Ignite Wonder |
| Format conversion for own use | Varies: explicitly allowed by some (Creative Fabrica); others forbid redistribution "in any format"; some offer to convert on request | sourced: [Creative Fabrica](https://creativefabrica.com/de/single-sales-license), [Creative Appliques](https://creativeappliques.com/?p=240337), EmbroideryMonkey |
| Fonts | BX/alphabet fonts "cannot be shared or sold under any circumstances" | sourced: Embroidery Legacy BX listings |
| Encrypted designs | mySewnet subscription designs encrypted and tied to an active subscription | sourced: [mySewnet](https://www.mySewnet.com/en-us/crafting/crafting-in-library) |

"Conversion usually allowed" is a fair summary only for conversion **for the
buyer's own machine**; sharing converted files is never allowed (**sources
agree on sharing, disagree on conversion wording**).

---

## Boundary conditions for EEganizer software

| # | Condition | Basis |
|---|---|---|
| W1 | Ingest zips: group files by design + size across formats; one "design" can have 6–9 format siblings and several sizes. | observed in our test files |
| W2 | Keep PDF color sheets/worksheets attached to their design; they are the designer's truth for colors. | observed |
| W3 | Converted files stay in the owner's account; no public links; no sharing features for design files. | sourced (licenses) + policy |
| W4 | Never decrypt or strip protection; store encrypted files unopened. | sourced + policy |
| W5 | Export names: letters, digits, `-`, `_`; root of USB by default. | sourced (Brother manual) |
| W6 | Before export, check hoop fit, stitch count limit and format for the customer's machine. | sourced |
| W7 | Show stop list and unique colors separately on printed charts. | observed |
| W8 | For DST/EXP sources, prefer the designer's PDF color sheet over placeholder colors. | sourced + observed |

## Sources

- https://www.hatchembroidery.com/pricing ; https://embrilliance.com/product/essentials ; https://www.machineembroiderygeek.com/?p=20167
- https://support.brother.com/g/s/hf/mobileapp_info/artspira/plan/en.html ; https://mysewnet.com/products-and-plans/one-purchase ; https://wilcom.com/workspace/library ; https://apps.apple.com/us/app/-/id522499369
- https://pypi.org/project/pyembroidery/
- https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html ; https://www.swingdesign.com/a/answers/6520321/File-type-for-the-Brother-PRS100
- https://support.oesd.com/article/64-how-do-i-use-exp-format-with-my-bernina-machine
- https://inkscape.org/it/forums/embroidery/solving-the-pattern-is-too-large-for-frame
- https://emblibrary.com/page/help/embroidery-limits
- https://makema.de/en/blogs/faq/stickdatei-wird-nicht-angezeigt
- https://creativeappliques.com/blog/embrilliance-software-how-to-use-bx-fonts-format/
- https://urbanthreads.com/design/thistle-crest-ut2186 ; https://www.etsy.com/shop/EmbroideryMonkey ; https://ignitewonder.patternbyetsy.com/policy ; https://creativefabrica.com/de/single-sales-license ; https://creativeappliques.com/?p=240337 ; https://embroiderylegacy.com/?p=199826
- https://www.mySewnet.com/en-us/crafting/crafting-in-library
- Project research and corpus: [../research/README.md](../research/README.md), [../CORPUS.md](../CORPUS.md)
