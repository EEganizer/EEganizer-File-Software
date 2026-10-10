# Embroidery Stitch Files: Resizing, Format Properties, Machine Compatibility, and Customer Workflows

Research date: 2026-10-10. Method note: direct page fetches were blocked from the research sandbox (DNS/proxy refusals for embrilliance.com, edutechwiki.unige.ch, support.brother.com, hatchembroidery.com, kimberbell.com, inkstitch.org). Findings below come from web-search result extracts of the cited pages, not full-page reads. Where a figure appears only in a snippet, treat it as "verify before shipping UI copy." Quoted strings are as surfaced by search.

## 1. Why is resizing stitch files risky, what is a safe range, and how do tools do stitch-aware resizing?

### Takeaway
A stitch file (PES/DST/JEF/EXP/VP3) is a list of needle coordinates, so plain scaling stretches or squeezes stitch spacing without changing stitch count: enlarging leaves gaps and long stitches, shrinking packs density and causes thread breaks. Commercial tools either (a) "recalculate stitches" with a heuristic stitch processor (Embrilliance: 50–250%), (b) do density-preserving resize on the machine itself (Brother), or (c) reverse-engineer objects from stitches (Wilcom/Hatch). Free open-source libraries (pyembroidery) only do geometric scaling; Ink/Stitch regenerates stitches from SVG objects, not from stitch files. A "light" in-app tool should therefore limit itself to plain scaling within a small band (around ±10–20%), with warnings, rather than claim recalculation.

### Cited Findings
**Mechanics of the risk**
- Wilcom: if a .dst file is enlarged, "the stitch spacing increases without any adjustment to the stitch count"; objects avoid this because stitch properties "including stitch spacing, stitch length, and underlay are maintained when resized." — [Wilcom product blog](https://productblog.wilcom.com/?p=5321)
- Hatch: a saved stitch file keeps "only the individual stitch information, color stops, and a few machine commands," so it cannot retain the original digitized objects. — [Hatch Help: open stitch files with objects](https://help.hatchembroidery.com/portal/en/kb/articles/how-to-open-stitch-file-formats-with-objects-to-edit-hatch-v2-and-v3)
- Shrinking without adjusting stitch count makes stitches bunch up (bulky/uneven embroidery); enlarging leaves gaps that look sparse. — [Kimber Bell blog](https://kimberbell.com/blogs/thekimberbellablog/resizing-embroidery-designs-without-losing-quality)
- Doubling a design can push stitches past 12.1 mm; many machines then insert automatic trims, producing sections of missing ("invisible") embroidery; shrinking fine detail causes excessive density and thread breaks. — [zdigitizing: How to properly resize](https://zdigitizing.com/how-to-properly-resize-embroidery-designs/)
- DST's maximum stitch/jump value is 121 units (12.1 mm at 0.1 mm units), the origin of the commonly cited 12.1 mm ceiling. — [EduTechWiki: Embroidery format DST](https://edutechwiki.unige.ch/en/Embroidery_format_DST); unit inference also supported by [MIT Fab embroidery report](https://fab.cba.mit.edu/classes/863.18/EECS/people/dylan/E-embroidery-report.html) ("stitch deltas specified in units of 0.1mm")
- Designs resized larger tend to succeed more often than ones resized smaller; small adjustments (e.g. slightly smaller to fit a garment) may be fine by plain scaling, while larger changes need editing the original digitized file or re-digitizing. — [Embroidery Legacy: How much is too much?](https://embroiderylegacy.com/?p=403722); [Kimber Bell blog](https://kimberbell.com/blogs/thekimberbellablog/resizing-embroidery-designs-without-losing-quality)
- A digitizer's view is stricter: "leave the design at the size that you bought it at for best results," and do not resize free-standing lace (FSL) files at all. — [OML Embroidery: Resizing stitch files, yay or nay](https://omlembroidery.com/resizing-stitch-files-yay-or-nay)
- Recommended safeguards: proportional scaling only, keep a backup, check stitch count/density, and test-stitch on similar fabric. — [Kimber Bell blog](https://kimberbell.com/blogs/thekimberbellablog/resizing-embroidery-designs-without-losing-quality); [zdigitizing](https://zdigitizing.com/how-to-properly-resize-embroidery-designs/)

**How commercial tools handle it**
- Embrilliance Essentials: "sizing with stitch recalculation is included! You can re-size embroidery designs down to 50% and up to 250% of their original size"; the help describes a "stitch processor" that recalculates automatically, with sizing settings in Preferences. — [Embrilliance Essentials product page](https://embrilliance.com/product/essentials); [Embrilliance Help: Product Essentials](https://embrilliance.com/Help/Platform%20Win%201148/productessentials.htm)
- Embrilliance: holding Ctrl while dragging disables recalculation for that drag (i.e., plain scale). — [Embrilliance Help: Resizing](https://embrilliance.com/Help/Platform%20Mac%201169/resizing.htm)
- mySewnet (Husqvarna Viking/Pfaff software) separates "Resize" (changes size and "retain[s] constant density") from "Scale" (plain geometric scale). — [mySewnet Help: Resize and Scale](https://softwarehelp.mysewnet.com/MSW/100/Embroidery/Topics/Resize_and_Scale.htm)
- Brother machines (on-screen editing): with the density-maintaining option, the machine changes size while keeping thread density and recalculates stitch count; without it, enlarged patterns are less dense and reduced ones more dense; the manual warns there is a limit to how far a pattern can be enlarged or reduced (no percentage given in the extract). — [Brother operation manual: Changing the size and density](https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p5x/en/07_01_05.html)
- Wilcom EmbroideryStudio: "if you want to scale a design, edit an outline or change a stitch type, then the design or selected elements must be first converted into 'objects'"; recognition is partial — "not all objects will be restored... but the majority of objects will be re-vectorised," and DST colors cannot be recreated. — [Wilcom docs: Converting stitches to objects](https://docs.wilcom.com/embroiderystudio/28/en/OnlineHelp/Quality/functions/functions-9.htm); [Wilcom product blog](https://productblog.wilcom.com/?p=5321)
- Hatch: open with Options > "Convert stitches into object shapes" to get resizable objects; if outlines can't be determined and the design resizes badly, reopen as "Leave stitches as individual stitches," and save under a new name. — [Hatch Help: open stitch files with objects](https://help.hatchembroidery.com/portal/en/kb/articles/how-to-open-stitch-file-formats-with-objects-to-edit-hatch-v2-and-v3); [Hatch Help: stitch files do not resize correctly](https://help.hatchembroidery.com/portal/en/kb/articles/what-to-do-when-stitch-files-do-not-resize-correctly)
- Hatch Organizer (entry tier) is marketed to "resize designs accurately." — [Hatch pricing](https://www.hatchembroidery.com/pricing)
- SewWhat-Pro is described as supporting resizing, merging, density adjustment and splitting. — [Techjockey: SewWhat-Pro](https://www.techjockey.com/us/detail/sewwhat-pro); [hellosewing: SewWhat-Pro vs Embrilliance](https://hellosewing.com/sew-what-pro-vs-embrilliance/)
- Free resizers commonly recommended: Wilcom TrueSizer, BERNINA ARTlink, Embird Basic (trial-limited). — [toptut: free embroidery software](https://www.toptut.com/?p=14405)

**Open source**
- pyembroidery reads ~40 and writes ~10 formats (mandated: PES, DST, EXP, JEF, VP3) and states that reading/writing is "always lossy"; conversion reads into a pattern, normalizes jump/trim/color commands to middle-level commands, then re-encodes. — [pyembroidery on PyPI](https://pypi.org/project/pyembroidery/); [GitHub EmbroidePy/pyembroidery](https://github.com/EmbroidePy/pyembroidery)
- Early pyembroidery PES output (v1.0.0) showed blank in Brother software because of PES block handling (since addressed, but illustrates PES writer fidelity risk). — [pyembroidery 1.0.0 PyPI](https://pypi.org/project/pyembroidery/1.0.0/)
- Ink/Stitch can import and export DST, PES and other formats. — [Ink/Stitch File Formats](https://inkstitch.org/docs/file-formats/); imported stitch files become paths (a v1.22 bug fix concerned imported DST/PES paths with empty data). — [Ink/Stitch v1.22.0 release](https://inkstitch.org/de/2019-02-17-v1.22.0)
- Users describe Ink/Stitch as the only free Mac option but "not beginner friendly." — [r/Machine_Embroidery beginner software thread (mirror)](https://lr.us.psf.lt/r/Machine_Embroidery/comments/1kmf3tx/beginner_software)

### Inferences
- The ±10–20% "safe" band is folk wisdom; none of the sources I could reach state a fixed percentage. Sources agree risk depends on stitch type (satin columns, fine lettering, FSL most sensitive). A light tool should frame plain scaling as "small adjustments only" (suggest a soft warning past ~10% and a hard warning past ~20%), never as recalculation.
- Satin column behavior follows from the mechanics: plain scaling widens the satin and lengthens its stitches proportionally (wider than ~12 mm risks auto-trims/snagging); shrinking narrows satins and compresses spacing, and underlay/pull compensation are not adjusted. This is inference from the cited mechanics, not a sourced claim.
- Real recalculation (Embrilliance-style or Wilcom object recognition) is proprietary heuristics. There is no off-the-shelf open-source stitch-file recalculator; pyembroidery gives format I/O plus plain affine transforms, and Ink/Stitch needs vector objects as input. Building recalculation in-house is a large, quality-risky project.
- A low-risk, high-value check: after any scale, compute the longest stitch and flag any above 12.1 mm (DST limit) and estimate density change (stitch count / area) as a warning.

### Gaps
- No primary source found for a specific ±10/20% guideline; the Kimber Bell / Embroidery Legacy pages may contain one but could not be fully read.
- Brother PE-Design's specific resize-with-recalc behavior and limits could not be confirmed (manual not reachable).
- Exact algorithm details of Embrilliance's stitch processor are not published.
- No source checked on whether any open-source project (e.g., Embroidermodder) attempts stitch-to-object recognition.

## 2. Object/native formats vs stitch/expanded formats: what can be recovered?

### Takeaway
Native/object files (Wilcom EMB, Hatch EMB, Bernina ART, mySewnet EDO, Janome JAN/EMB, Embrilliance BE working files) store shapes, fills, underlay and properties and are meant for software, not machines; stitch files store only needle moves, trims and color changes. Going from stitch back to objects is lossy and only partially possible in high-end software; EEganizer should treat customer stitch files as the canonical artifact and not promise object-level edits.

### Cited Findings
- Native files are the digitizing software's editable working files (e.g., EMB for Wilcom, ART for Bernina) and keep object info like shapes and fills; DST/EXP are low-level stitch-only files; PES/JEF/VP3 are "hybrid" stitch files adding color sequence, hoop codes and previews. — [digit-it knowledge base: formats explained](https://knowledgebase.digit-it.com/knowledge-base/article/embroidery-file-formats-explained); [emborado glossary: embroidery file format](https://emborado.de/en/glossary/embroidery-file-format); [machineembroiderygeek: formats](https://machineembroiderygeek.com/what-are-machine-embroidery-file-formats/)
- Object-format design files "are not meant to run directly on machines." — [emborado glossary](https://www.emborado.de/en/glossary/embroidery-file-format)
- mySewnet Digitizing stores design outlines in .edo; its preferred export is .vp4, which preserves separate parts of multipart designs, hoop, background, appliqué info, thread colors and notes. — [mySewnet Help: File Formats](https://softwarehelp.mysewnet.com/MSW/120/Digitizing/Topics/File_Formats.htm)
- Janome: *.Jan was the master data file in Digitizer MBX V4.5 and earlier; newer versions use *.Emb; *.Jef is the stitch data format for all Janome/Elna machines; JEF+ is an editable stitch file from Horizon Link/Suite in which each included JEF can be moved/rotated/resized. — [Janome formats PDF (via SewingMachinesPlus)](https://www.sewingmachinesplus.com/media/products/Janome/j-500e/formats.pdf)
- Recovery is partial: Wilcom re-vectorizes "the majority" of objects from DST but cannot recreate colors. — [Wilcom product blog](https://productblog.wilcom.com/?p=5321)
- Embrilliance Express (free) builds lettering using BX fonts. — [hellosewing / machineembroiderygeek summary](https://www.machineembroiderygeek.com/what-is-embrilliance-software/)

### Inferences
- If a customer library contains native files (EMB/ART/EDO/BE), EEganizer can at most display/archive them; rendering them requires the vendor's engine. Prioritize stitch formats for preview/convert.
- BX is a keyboard-font package (Embrilliance), not a design format; worth recognizing in library tooling but not converting.

### Gaps
- Bernina ART's exact nature (ART is described both as native object format and as a machine format for some models) is inconsistent across sources; HUS's status (Husqvarna stitch format, not object) was not directly sourced here.
- No source on whether .EMB/.ART files embed a preview thumbnail extractable without the vendor engine.

## 3. Per-format properties: palettes, metadata, thumbnails, limits, hoops, which machines read what

### Takeaway
Brand mapping is stable: Brother/Baby Lock = PES (with embedded PEC), Janome = JEF, Husqvarna Viking/Pfaff = VP3 (older HUS/VIP/PCS), Bernina = EXP/ART, Singer = XXX, Melco = EXP, commercial/Tajima = DST. DST carries no colors and only a 512-byte header; PES carries palette indices into Brother's thread table plus a small monochrome PEC thumbnail and design name. Hoop limits are machine-specific and often slightly smaller than nominal (e.g., a "4x4" usable area ~3.93 in), so fit checks need per-model tables.

### Cited Findings
**Brand-to-format mapping**
- Brother/Baby Lock: PES (PEC noted); Janome: JEF; Husqvarna Viking/Pfaff: VP3 most common, with HUS, VIP, XXX for older/specific models (some sources add PCS/PCD for Pfaff); Bernina: ART or EXP depending on model/software; Melco: EXP; Singer: XXX; Tajima/commercial: DST, the most widely accepted exchange format. Sources partly disagree and advise checking the machine manual since model year changes accepted formats. — [My Girlfriend's Quilt Shoppe: formats by brand](https://mygirlfriendsquiltshoppe.com/blogs/tips-tricks/embroidery-file-formats-by-machine-brand); [SewingMachinesPlus: embroidery file formats](https://sewingmachinesplus.com/blogs/news/embroidery-file-formats); [digit-it machine compatibility guide](https://knowledgebase.digit-it.com/knowledge-base/article/machine-compatibility-guide); [Kimber Bell: formats](https://kimberbell.com/machine-embroidery-file-formats/)
- Embrilliance reads a long list of machine formats including DST, PES and VP3; SewWhat-Pro reads ~30 formats. — [Embrilliance Essentials page](https://embrilliance.com/product/essentials); [hellosewing comparison](https://hellosewing.com/sew-what-pro-vs-embrilliance/)

**PES / PEC**
- PES contains a PES section (design info for PE-Design) and a PEC section (design name, colors, machine commands and graphics); the PEC block is kept the same across versions for hardware backward compatibility. — [libpes wiki: PES format](https://github.com/frno7/libpes/wiki/PES-format); [EduTechWiki: PEC](https://edutechwiki.unige.ch/en/Embroidery_format_PEC)
- PEC header is 512 bytes; thumbnail is 1-bit, width stored in bytes (typically 6 bytes = 48 px) × typically 38 px tall; color count stored as n−1 (0xFF = none) followed by palette indices (indices into Brother's built-in thread table, not RGB). Standalone PEC files start with "#PEC0001". — [EduTechWiki: PEC](https://edutechwiki.unige.ch/en/Embroidery_format_PEC)
- Large PES files may fail on some machines depending on model/hoop; older machines may reject a design as not fitting even with correct dimensions. — [embpunch: PES file issues](https://www.embpunch.com/blog/major-pes-file-issues-and-their-solutions-a-comprehensive-guide)

**DST**
- DST stores no colors; Brother's manual: "Since Tajima (.dst) data does not contain specific thread color information, it is displayed with our default thread color sequence." — [EduTechWiki: DST](https://edutechwiki.unige.ch/en/Embroidery_format_DST); [Brother manual §10](https://support.brother.com/g/s/hf/htmldoc/hsm/om/888p5x/en/10_01.html)
- DST header always 512 bytes, only ~125 used (label/name, stitch count, color-change count, extents); body is 3-byte records with control bits; max stitch/jump 121 units. Extent-field units are inconsistent between sources (cm vs 0.1 mm). — [EduTechWiki: DST](https://edutechwiki.unige.ch/en/Embroidery_format_DST); [KDE Liberty: Tajima Ternary](https://community.kde.org/Projects/Liberty/File_Formats/Tajima_Ternary)

**VP3 / VP4**
- VP4 preserves multipart designs, hoop, background, appliqué info, thread colors and notes. — [mySewnet Help: File Formats](https://softwarehelp.mysewnet.com/MSW/120/Digitizing/Topics/File_Formats.htm)

**Hoops and fit**
- Hatch Organizer ships "522 hoop presets." — [Hatch pricing](https://www.hatchembroidery.com/pricing)
- Brother PE535 user: a 4"×4" hoop's usable area is about 3.93"×3.93"; designs at nominal 4" were rejected as too large. A Brother SE400 user reports a machine may simply ignore a file whose outer dimensions exceed its capability. — [Inkscape forum: pattern too large for frame](https://inkscape.org/it/forums/embroidery/solving-the-pattern-is-too-large-for-frame); [Inkscape forum: resizing error](https://inkscape.org/forums/embroidery/resizing-error)
- Brother SE400/SE600 are 4×4 machines; 5×7 max requires extra setup steps (lab note). — [Illinois CUC Fab Lab: SE600](https://cucfablab.web.illinois.edu/lab-tool/brother-se600-sewing-embroidery-machine/)

### Inferences
- PES color is a palette index into Brother's thread table; DST has no color at all, so a "thread chart" for DST must be user-assigned. Converting DST to PES/JEF will produce arbitrary default colors; the UI should say so.
- Hoop-fit checking needs a curated per-model sewing-field table (usable field, not nominal hoop), which is the main data asset of tools like Hatch (522 presets).
- Metadata worth extracting for EEganizer libraries: design name (PEC/DST label), stitch count, color count/sequence, extents, PEC thumbnail.

### Gaps
- No official Brother/Janome/Bernina spec sheet reachable for max stitch counts per machine or exact sewing fields; needs manufacturer manuals.
- The commonly cited Brother 64-color thread table size was not confirmed by sources found.
- JEF hoop-code field, VP3 metadata layout, EXP and XXX color handling not sourced here.

## 4. Typical customer workflows

### Takeaway
The everyday jobs are: convert to the machine's format, confirm it fits the hoop, see/print the color sequence and thread chart, make small resizes, merge/add lettering, split oversized designs, and move files to the machine (USB, or increasingly Wi-Fi via Brother Artspira / Bernina WiFi Device).

### Cited Findings
- Hatch Organizer core functions: view/manage designs, change color blocks, 522 hoop presets, resize, convert to popular formats and export to the machine format. — [Hatch pricing](https://www.hatchembroidery.com/pricing); [Hatch Organizer 3 overview video](https://hatchembroidery.com/videos/hatch-embroidery-organizer-3-overview)
- Embrilliance Essentials: merge designs, resize with recalc, remove overlapping stitches, colorize, print templates, add lettering, sewing-order control, thread palette and thread inventory, basting. — [Embrilliance Essentials page](https://embrilliance.com/product/essentials); [Embrilliance Help: Essentials](https://embrilliance.com/Help/Platform%20Win%201148/productessentials.htm)
- SewWhat-Pro: view, edit, convert, merge, adjust density, split large designs for smaller hoops, create SVG from appliqué files. — [Techjockey: SewWhat-Pro](https://www.techjockey.com/us/detail/sewwhat-pro); [machineembroiderygeek: SewWhat-Pro vs Embrilliance](https://www.machineembroiderygeek.com/?p=20167)
- Brother Artspira: cloud app to create, edit and wirelessly transfer designs to WLAN-enabled Brother machines; machine firmware must be updated to use it; paid Artspira+ announced in 2023 at $12.99/month. — [Brother USA: Artspira](https://www.brother-usa.com/apps/sewing-embroidery/artspira); [Artspira quick reference PDF](https://download.brother.com/welcome/doch102633/artspira_em_qrg03en.pdf); [Brother press release via Seeking Alpha](https://seekingalpha.com/pr/19482627-brother-expands-inspiration-with-the-introduction-of-artspira-a-subscription-plan-offering)
- Bernina WiFi Device: a USB-plugged adapter the machine sees as a USB stick; Embroidery Software 9.1+ generates machine files and sends them over the same Wi-Fi network. — [BERNINA Software Help: send designs to WiFi Device](https://softwarehelp.bernina.com/en/MainHelp/PART_Processing/network/network-15.htm); [BERNINA V9 WiFi Device](https://www.bernina.com/en-GB/Software-GB/Embroidery-Software/BERNINA-Embroidery-Software-9/BERNINA-V9-WiFi-Device)
- Janome AcuFil is a quilting (stipple/quilt-block placement) system with a dedicated hoop/template kit, not a wireless-transfer feature (contrary to the brief's assumption). — [Janome: Using the AcuFil Quilting Kit](https://www.janome.com/using-the-acufil-quilting-kit-on-your-embroidery-machine/)
- Users hitting "pattern too large for frame" is a recurring support problem. — [Inkscape forum thread](https://inkscape.org/it/forums/embroidery/solving-the-pattern-is-too-large-for-frame)

### Inferences
- For EEganizer (library/organizing service), the low-risk, high-value feature set is: preview + metadata, format conversion to the customer's machine, hoop-fit check against the customer's machine profile, color sequence/thread chart with printable worksheet, and USB/download packaging. Resize should be gated and warned; merge/split are second-tier and riskier.
- Wi-Fi transfer is vendor-locked (Artspira cloud, Bernina software + device); integration would require vendor APIs not evidently public, so "download for USB" is the realistic path.

### Gaps
- No quantitative data (surveys) on which workflow customers do most often; ranking is inferred from what tools emphasize.
- Janome's wireless transfer path (e.g., JanomeConnect / Artistic Edit) not researched in the extracted results.
- Printed worksheet contents (thread chart, stitch count, size, color stops) not confirmed by a primary source here.

## 5. Popular paid "light" tools: valued features and price points

### Takeaway
Light tools cluster at roughly $65–$180: SewWhat-Pro (~$65), Embrilliance Essentials (~$139 sale / $159 list), Hatch Organizer (~$149). Customers value conversion, resize with recalculation, merge/lettering, hoop presets and color management; free options (TrueSizer, ARTlink, My Editor, Ink/Stitch) cover viewing/convert/basic resize.

### Cited Findings
- Embrilliance Essentials: official page showed $139 sale (list $159), sales ending March 13 and August 12, 2026; one reseller listed $179; runs natively on macOS and Windows. — [Embrilliance Essentials product page](https://embrilliance.com/product/essentials); [Embrilliance (aff link, Aug 2026 sale)](https://embrilliance.com/product/essentials?aff=48764); [AllBrands](https://allbrands.com/categories/4619/printer_friendly)
- Hatch: Organizer $149, Personalizer $249, Composer $599 (third-party comparison); Hatch offers a 30-day free trial, 30-day money-back guarantee and FlexPay. — [Techjockey: SewIconz vs Hatch](https://www.techjockey.com/compare/sewiconz-vs-hatch-embroidery); [Hatch pricing](https://www.hatchembroidery.com/pricing)
- SewWhat-Pro: "just $65" per one review; CD version $83; 30-day free trial. — [machineembroiderygeek: SewWhat-Pro vs Embrilliance](https://www.machineembroiderygeek.com/?p=20167); [Techjockey: SewWhat-Pro](https://www.techjockey.com/us/detail/sewwhat-pro)
- Reddit sentiment: "the $150 is worth it for embrilliance"; advice to pick software you'll use long term rather than a "beginner" program. — [r/Machine_Embroidery thread (mirror)](https://lr.us.psf.lt/r/Machine_Embroidery/comments/1kmf3tx/beginner_software)
- Embrilliance Essentials described as "the module for resizing fonts or merging designs"; commonly recommended for Brother owners. — [machineembroiderygeek: what is Embrilliance](https://www.machineembroiderygeek.com/what-is-embrilliance-software/); [hellosewing](https://hellosewing.com/sew-what-pro-vs-embrilliance/)
- Free tools: Wilcom TrueSizer (resize/convert), BERNINA ARTlink (a "teaser" for the full software), Embird Basic (split/merge/resize, trial-limited). — [toptut free software list](https://www.toptut.com/?p=14405); [sewingmachinefun: free converters](https://www.sewingmachinefun.com/machine-embroidery-file-format-converters/)
- Artspira+ subscription $12.99/month (2023 announcement). — [Seeking Alpha press release](https://seekingalpha.com/pr/19482627-brother-expands-inspiration-with-the-introduction-of-artspira-a-subscription-plan-offering)

### Inferences
- An in-app EEganizer tool competes with free viewers/converters, not with $139 Essentials; resize-with-recalc and lettering are what people pay for. EEganizer's differentiation is library context (find, preview, convert, fit-check, send) rather than editing.

### Gaps
- Brother PE-Design Lite and Janome "My Editor" current pricing/status not found (PE-Design Lite may be discontinued; unverified).
- Hatch Organizer price is from a third-party aggregator; Hatch's own page could not be read.
- No review-volume or survey data ranking which features matter most.
