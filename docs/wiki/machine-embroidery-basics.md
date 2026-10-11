# Machine embroidery basics

How embroidery machines turn a design file into stitches, and which machine
facts limit what our software may do with a file.

Evidence labels used on every page: **sourced** (link), **rule of thumb**
(practitioner guidance, not a standard), **observed in our test files**
(our own corpus, see [`../CORPUS.md`](../CORPUS.md)). Source access notes are in
the [README](README.md#how-the-facts-were-checked).

---

## 1. How a machine forms a stitch

| Part | What it does | Why software cares |
|---|---|---|
| Needle + top thread | Goes down through fabric once per stitch | Every needle penetration is one "stitch" record in the file |
| Bobbin (lower thread) | Locks the top thread from below (lock stitch) | Bobbin runs out on long designs; stitch count drives bobbin changes |
| Hoop / frame | Clamps fabric + stabilizer taut | Design must fit the hoop's **sewing field**, not the outer frame |
| Pantograph / embroidery unit | Moves the hoop in X/Y under a needle that only goes up and down | The file is a list of X/Y moves of the hoop (in 0.1 mm units in most formats) |
| Trimmer | Cuts threads between areas (if fitted) | Files encode trims differently; some machines have no trimmer |

A stitch file is therefore just a sequence of relative moves plus commands
(stitch, jump/move, trim, color change/stop, end). See
[file-formats.md](file-formats.md).

## 2. Single-needle vs multi-needle

| Type | Typical users | Color changes | Typical top speed |
|---|---|---|---|
| Single-needle home machine (Brother PE/SE/NV, Janome MC, Bernina, Husqvarna Viking, Pfaff, Singer) | Hobby, small business | Machine **stops**; user re-threads the next color by hand, then restarts | 400–1,000 spm; e.g. Brother PE800 650 spm ([zdigitizing](https://zdigitizing.com/brother-pe800-embroidery-machine/)) |
| Multi-needle "semi-commercial" (Brother PR 6/10-needle, Baby Lock multi-needle, Janome MB, Bernina E-series) | Small business | Automatic needle switch per pre-assigned color; automatic trim ([Brother PR-600](https://www.brother-usa.com/products/pr-600)) | up to 1,000 spm, e.g. PR1055X 400–1,000 spm ([Rutgers makerspace](https://makerspace.rutgers.edu/equipment/brother-pr1055x-embroidery-machine)), PR680W 1,000 spm ([Brother Canada](https://www.brother.ca/en/business/c/had-bus)) |
| Commercial (Tajima, Barudan, Melco, ZSK) | Shops, factories; often multi-head | Automatic; up to 15–18 needles | Tajima TMBR up to 1,200 spm ([AllBrands](https://allbrands.com/categories/3396/printer_friendly)); Tajima SAI 800 spm ([Embroidery Legacy](https://embroiderylegacy.com/tajima-embroidery-machines/sai/)) |

Speeds are maximums. Machines slow down for long satin stitches, small
stitches and caps, so real throughput is lower (**rule of thumb**).

**Color stops on a single-needle machine.** Every color change in the file
becomes a stop. A design with 19 stops but 5 unique colors (as in our corpus)
means 19 re-threads on a single-needle machine unless the user merges stops
(**observed in our test files**: "5 colors used across 19 stops").

## 3. Hoops and real sewing fields

Hoops are sold by **nominal inch names** ("4x4", "5x7", "6x10"). For home
machines the published sewing field usually equals the metric figure behind
the name; commercial hoops differ ([sewingmachinefun](https://www.sewingmachinefun.com/embroidery-hoop-sizes/)).

| Brand | Hoop / name | Sewing field (mm) | Basis |
|---|---|---|---|
| Brother / Baby Lock | 4x4 | 100 x 100 | sourced: [Echidna Sewing](https://echidnasewing.com.au/article/machines/brother-machines-maximum-embroidery-field) |
| Brother / Baby Lock | 5x7 | 130 x 180 | sourced: Echidna (F540E) |
| Brother / Baby Lock | 6x10 | 160 x 260 | sourced: Echidna (NV880E); [Echidna frame](https://www.echidnasewing.com.au/160mm-x-260mm-brother-slide-on-embroidery-frame-sh) |
| Brother | 8x12 | 200 x 300 | sourced: Echidna (PR1X, VE2300) |
| Brother | 8x14 (PR1055X) | 200 x 360 | sourced: Echidna |
| Brother | 9.5x14 (XE2, XJ2) | 240 x 360 | sourced: Echidna |
| Brother | EV1 max field | 297 x 465 | sourced: Echidna |
| Janome | SQ10 | 100 x 100 | sourced: [The Sewing Studio](https://www.thesewingstudio.co.uk/products/janome-embroidery-hoop-sq10e-100m-x-100m-819401007) |
| Janome | SQ14 | 140 x 140 | sourced: [Embird hoop list](https://embird.net/sw/embird/hoops.htm) |
| Janome | RE20 | 140 x 200 | sourced: Embird |
| Janome | SQ20 | 200 x 200 | sourced: Embird |
| Janome | RE28 | 200 x 280 | sourced: Embird |
| Janome | GR (MC12000) | 230 x 300 | sourced: Embird (single source) |
| Janome (JEF header hoop code) | codes 0, 1, 2, 3, 4 | 110x110, 50x50, 140x200, 126x110, 200x200 | sourced: [EduTechWiki JEF](https://edutechwiki.unige.ch/en/Embroidery_format_JEF), [pystitch JefWriter](https://pypi.org/project/pystitch/) |
| Bernina | Small | 50 x 72 | sourced: one retailer listing found via search only; not confirmed on bernina.com |
| Bernina | Medium | 100 x 130 | sourced: one retailer listing (search only) |
| Bernina | Large Oval | 145 x 255 | sourced: one retailer listing (search only) |
| Bernina | Maxi | 210 x 400 | sourced: [BERNINA hoops](https://www.bernina.com/hoops) ("40 x 21 cm") |
| Bernina | Jumbo | 260 x 400 (7 Series: 210 x 400) | sourced: BERNINA product doc |
| Bernina | Midi | 265 x 165 listed; **unclear if field or frame** | sourced: [AllBrands](https://www.allbrands.com/categories/4044); sources disagree |
| Husqvarna Viking / Pfaff | Square | 120 x 120 | sourced: [Embird which hoop](https://www.embird.net/manual/0325whichhoop.htm) |
| Husqvarna Viking / Pfaff | Quilter's | 200 x 200 | sourced: [PFAFF hoops](https://www.singer.com/collections/pfaff-embroidery-hoops) |
| Husqvarna Viking | Large Metal / Jewel | 240 x 150 | sourced: [Singer.com](https://www.singer.com/products/husqvarnaviking-large-metal-embroidery-hoop-240-mm-x-150-mm) |
| Pfaff / Viking (Royal) | Deluxe | 360 x 200 | sourced: [Singer.com](https://www.singer.com/products/pfaff-creative-deluxe-hoop-360-x-200-mm) |
| Pfaff / Viking (Majestic) | Grand Dream | 360 x 350 | sourced: PFAFF hoops; Embird |
| Singer (SE9180/SE9150) | small / standard | 40 x 40; 100 x 100 | sourced: [Singer 40mm](https://www.singer.com/products/singer-40-x-40mm-embroidery-hoop), [Singer 100mm](https://www.singer.com/products/singer-100-x-100mm-embroidery-hoop) |
| Singer (SE9180) | max design | 170 x 100 | sourced: third-party listing only |
| Singer Quantum Futura | max field | 115 x 170 | sourced: [Emblibrary limits](https://emblibrary.com/page/help/embroidery-limits) |
| Tajima TMBR (commercial) | tubular field | approx. 355 x 495 (14 x 19.5 in) | sourced: AllBrands / zdigitizing; reseller data |
| Tajima SAI | tubular field | 200 x 300 | sourced: Embroidery Legacy |

**Measured usable fields can be smaller than nominal.** A user measured a
Brother 4x4 grid at 3.93 in (99.8 mm) and reported nominal 4-inch designs
being rejected ([Inkscape forum](https://inkscape.org/it/forums/embroidery/solving-the-pattern-is-too-large-for-frame)).
**Designers digitize right up to the nominal field:** designs sold as "4x4"
measured up to 98.6 mm and "6x10" up to 257.4 mm (**observed in our test
files**).

**Machine stitch-count limits.** Some machines refuse designs above a stitch
count: Baby Lock Destiny 700,000; Ellegante 500,000; Ellageo 200,000
([Emblibrary](https://emblibrary.com/page/help/embroidery-limits)). Brother
manuals say PES files exceeding the model's stitch, color or combined-pattern
limits "cannot be displayed", without giving numbers in the excerpt we could
read ([Brother manual](https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html)).

## 4. Stabilizers

| Fabric | Usual stabilizer | Basis |
|---|---|---|
| Knits, T-shirts, stretch | Cut-away (stays in garment) | sourced: [Linda's](https://lindas.com/blogs/tips-and-tricks/best-stabilizer-for-embroidery), [OESD guide](https://oesd.com/content/img/pages/stabilizer/OESD_stabilizers.pdf) |
| Stable wovens (quilting cotton, canvas, duck) | Tear-away | sourced: OESD guide |
| Dense designs on wovens | Cut-away ("holds more stitches") | sourced: OESD guide |
| Sheers, lace, free-standing lace | Wash-away (water soluble), often 2 layers | sourced: [Anita Goodesign](https://anitagoodesign.com/blogs/fundamentals/how-to-free-standing-lace-fundamentals) |
| Pile (towels, fleece, minky) | Wash-away topping on top + backing below | sourced: Linda's |

Software relevance: the stabilizer is not in the file, but design density and
type decide it. A printable worksheet can suggest one (**rule of thumb**).

## 5. Thread and needles

| Item | Typical value | Basis |
|---|---|---|
| Standard thread | 40 wt polyester or rayon; designs are digitized for it | sourced: [Madeira Polyneon](https://www.madeirausa.com/product-highlights/thread/polyneon.aspx), [Linda's Isacord guide](https://lindas.com/blogs/product-guides/isacord-40wt-embroidery-thread-guide) |
| Fine thread | 60 wt for small lettering and fine detail; 75 wt for the tiniest details | sourced: Madeira Polyneon |
| 60 wt vs 40 wt | satin letters about 25% smaller possible | sourced: [Graphics Pro](https://graphics-pro.com/education/what-can-embroiderers-do-to-execute-small-lettering-successfully/) |
| Bobbin thread | about 60 wt (lighter than top) | sourced: Linda's Isacord guide |
| Needle, general | 75/11 embroidery needle | sourced: Madeira (65/9–75/11), Linda's |
| Needle, heavy fabric | 90/14 | sourced: Linda's; eQuilter lists 90/14 for Isacord |
| Needle, 60 wt / tiny text | 70/10, 65/9 or 60/8 | sourced: Graphics Pro, [ABDigitizing](https://abdigitizing.com/how-to-digitize-small-text-for-embroidery-under-5mm-without-messing-up/) |

Thread weight is not stored in stitch files. Density in the file assumes 40 wt
unless the designer says otherwise (**rule of thumb**).

## 6. Getting designs onto the machine

| Route | Brands | Notes | Basis |
|---|---|---|---|
| USB stick | All modern home machines | Most common route. Brother: files in folders on "Removable Disk" may not be found; names with special characters may not display; stick to letters, digits, `-`, `_` | sourced: Brother manual excerpts ([support.brother.com](https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html), [PE-700 USB manual](https://download.brother.com/welcome/doch000417/nv700e2_pe700_2usb02endefrnltes.pdf)) |
| Brother Artspira app (Wi-Fi) | Brother Wi-Fi models | Transfer from phone; cloud quota ~20 files free, ~100 with Artspira+ | sourced: [Brother Artspira](https://www.brother-usa.com/apps/sewing-embroidery/artspira), [plans](https://support.brother.com/g/s/hf/mobileapp_info/artspira/plan/en.html) |
| Brother Design Database Transfer (WLAN, PC) | Brother WLAN models | Free PC program | sourced: Brother SE700 listings |
| mySewnet cloud / Connect | Husqvarna Viking, Pfaff | Send from desktop to cloud or directly to Wi-Fi machines; Direct USB on some models; subscription designs encrypted | sourced: [mySewnet transfer](https://mysewnet.com/en-il/studio/article/transferring-designs-via-mysewnet-cloud), [mySewnet Connect](https://softwarehelp.mysewnet.com/MSW/100/CrossStitcher/Topics/mySewnet™_Connect.htm) |
| BERNINA WiFi Device | BERNINA machines with USB | Plugs into USB port, machine sees it as a USB stick; software converts to the machine format before sending | sourced: [BERNINA help](https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/network/network-15.htm) |
| Wilcom WLAN send | Brother | From EmbroideryStudio | sourced: [Wilcom docs](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Production/output/output-7.htm) |
| Browser direct to USB | none | Chrome blocks USB mass storage from WebUSB, so a web app can only download a file | sourced: [Chromium blink-dev](https://groups.google.com/a/chromium.org/g/blink-dev/c/LZXocaeCwDw/m/GLfAffGLAAAJ) |

---

## Boundary conditions for EEganizer software

| # | Condition | Basis |
|---|---|---|
| M1 | Fit checks use the **published sewing field** per machine model, not the nominal hoop name or the outer frame size. | sourced (see table) |
| M2 | **No default safety margin** in fit checks: designers fill the nominal field (98.6 mm in "4x4", 257.4 mm in "6x10"). Offer margin only as an option. | observed in our test files |
| M3 | Treat a design within ~0.5 mm of the field edge as "fits, tight" rather than "too big"; some machines sew slightly less than nominal (99.8 mm measured on a Brother 4x4). | sourced (Inkscape forum) + rule of thumb |
| M4 | Always try 90° rotation before saying "does not fit" (portrait vs landscape hoops). | observed in our test files (designers rotate PES/JEF) |
| M5 | Stitch-time estimate = stitches / machine spm + per-stop allowance; use 400–1,000 spm for home machines, up to 1,200 spm commercial. Show as an estimate. | sourced speeds + rule of thumb |
| M6 | Count **color stops** (re-threads) separately from **unique colors**; single-needle users care about stops. | observed in our test files |
| M7 | Warn when a design exceeds the model's stitch-count limit where known (e.g. 200,000 / 500,000 / 700,000 on Baby Lock models). | sourced (Emblibrary) |
| M8 | USB export: plain file names (letters, digits, `-`, `_`), files in the stick root by default, one format per machine. | sourced (Brother manual) |
| M9 | Never decrypt or open encrypted vendor subscription designs (mySewnet). | sourced (mySewnet) + project policy |

## Sources

- Brother PE800 speed: https://zdigitizing.com/brother-pe800-embroidery-machine/
- Brother PR1055X speed: https://makerspace.rutgers.edu/equipment/brother-pr1055x-embroidery-machine
- Brother PR680W / business machines: https://www.brother.ca/en/business/c/had-bus
- Brother PR-600 multi-needle: https://www.brother-usa.com/products/pr-600
- Tajima TMBR speed/field: https://allbrands.com/categories/3396/printer_friendly ; https://zdigitizing.com/tajima-embroidery-machines/
- Tajima SAI: https://embroiderylegacy.com/tajima-embroidery-machines/sai/
- Brother hoop/field table: https://echidnasewing.com.au/article/machines/brother-machines-maximum-embroidery-field
- Hoop size vs field: https://www.sewingmachinefun.com/embroidery-hoop-sizes/
- Measured 3.93 in Brother 4x4: https://inkscape.org/it/forums/embroidery/solving-the-pattern-is-too-large-for-frame
- Janome SQ10: https://www.thesewingstudio.co.uk/products/janome-embroidery-hoop-sq10e-100m-x-100m-819401007
- Embird hoop lists: https://embird.net/sw/embird/hoops.htm ; https://www.embird.net/manual/0325whichhoop.htm
- JEF hoop codes: https://edutechwiki.unige.ch/en/Embroidery_format_JEF ; pystitch 1.0.1 `JefWriter.py` https://pypi.org/project/pystitch/
- BERNINA hoops: https://www.bernina.com/hoops ; Bernina retailer listings: https://www.qualitysewing.com/collections/bernina-embroidery-hoops ; https://www.allbrands.com/categories/4044
- PFAFF / Husqvarna Viking hoops: https://www.singer.com/collections/pfaff-embroidery-hoops ; https://www.singer.com/products/pfaff-creative-deluxe-hoop-360-x-200-mm ; https://www.singer.com/products/husqvarnaviking-large-metal-embroidery-hoop-240-mm-x-150-mm
- Singer hoops: https://www.singer.com/products/singer-40-x-40mm-embroidery-hoop ; https://www.singer.com/products/singer-100-x-100mm-embroidery-hoop
- Machine stitch limits: https://emblibrary.com/page/help/embroidery-limits
- Brother manual (USB, DST colors, limits): https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p6x/en/10_01.html ; https://download.brother.com/welcome/doch000417/nv700e2_pe700_2usb02endefrnltes.pdf
- Stabilizers: https://oesd.com/content/img/pages/stabilizer/OESD_stabilizers.pdf ; https://lindas.com/blogs/tips-and-tricks/best-stabilizer-for-embroidery ; https://anitagoodesign.com/blogs/fundamentals/how-to-free-standing-lace-fundamentals
- Thread/needles: https://www.madeirausa.com/product-highlights/thread/polyneon.aspx ; https://lindas.com/blogs/product-guides/isacord-40wt-embroidery-thread-guide ; https://graphics-pro.com/education/what-can-embroiderers-do-to-execute-small-lettering-successfully/ ; https://abdigitizing.com/how-to-digitize-small-text-for-embroidery-under-5mm-without-messing-up/
- Transfer: https://www.brother-usa.com/apps/sewing-embroidery/artspira ; https://support.brother.com/g/s/hf/mobileapp_info/artspira/plan/en.html ; https://mysewnet.com/en-il/studio/article/transferring-designs-via-mysewnet-cloud ; https://softwarehelp.mysewnet.com/MSW/100/CrossStitcher/Topics/mySewnet™_Connect.htm ; https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/network/network-15.htm ; https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Production/output/output-7.htm ; https://groups.google.com/a/chromium.org/g/blink-dev/c/LZXocaeCwDw/m/GLfAffGLAAAJ
- mySewnet encrypted designs: https://www.mySewnet.com/en-us/crafting/crafting-in-library
