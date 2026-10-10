# Open-source in-browser embroidery file viewers/converters (JS/TS/WASM)

Research date: 2026-10-10. Star counts, licenses and "last push" dates come from the GitHub repository-search API, queried 2026-10-10 (each entry links to its repo). Several sites could not be fetched from the research environment because of DNS failures: embroideryviewer.xyz, discourse.threejs.org, producthunt.com, zdigitizing.com and developer.mozilla.org. Claims about those sites come from search-result snippets only and are flagged as such.

## Which JS/TS libraries/projects exist on GitHub/npm (license, stars, last commit, formats, rendering, maintenance)?

### Takeaway
No mature, widely adopted JS/TS embroidery I/O library exists. The JS ecosystem is small, mostly single-maintainer, and low in stars (all under 70). The format knowledge lives in pyembroidery/pystitch (Python, MIT) and libembroidery (C, Zlib). The most promising embeddable candidates found are:
- **Ricuci / embroidery-converter-kit** (TS, MIT core, zero-deps, reads 13 and writes 10 formats, very new);
- **leomurca/embroidery-viewer** (Svelte, MIT, archived on GitHub);
- **redteam316/html5-embroidery** (MIT, many readers, abandoned in 2015);
- **manthrax/dst-format** (three.js, DST only, textured-thread rendering, no license shown).

### Cited Findings

**Format/IO reference libraries (non-JS, but the source of truth that JS projects port from)**

- **EmbroidePy/pyembroidery** — Python, MIT, 312 stars, last push 2024-05-24 ([GitHub](https://github.com/EmbroidePy/pyembroidery)).
  - The README lists 40 embroidery read formats, including .pes, .dst, .exp, .jef, .vp3, .xxx, .hus, .sew, .pec, .u01, .zhs and .gcode.
  - It writes .pes, .dst, .exp, .jef, .vp3, .u01, .pec, .xxx, .tbf and .gcode, plus .csv, .json, .png, .txt and .svg ([GitHub](https://github.com/EmbroidePy/pyembroidery)).
  - It supports translate, scale and rotate through write settings and MATRIX_* commands. Mirroring is achievable via negative scale; the README does not present it as a named feature ([GitHub](https://github.com/EmbroidePy/pyembroidery)).
  - Its newest release is 1.5.1 (2024-03-27) per piwheels, which lists "Dependencies: None" ([piwheels](https://www.piwheels.org/project/pyembroidery/)).
- **inkstitch/pystitch** — Python, MIT, 112 stars, last push 2026-09-08 ([GitHub](https://github.com/inkstitch/pystitch)).
  - It describes itself as "an updated fork of the original" pyembroidery, maintained by the Ink/Stitch org, with the same read/write coverage (about 40 formats read, about 10 embroidery formats written). It requires Python 3.9 or later ([GitHub](https://github.com/inkstitch/pystitch)).
  - It is the actively maintained successor; pyembroidery itself has had no push since May 2024.
- **Embroidermodder/libembroidery** — C, Zlib, 82 stars, last push 2026-10-08 ([GitHub](https://github.com/Embroidermodder/libembroidery)).
  - The README claims it "handles over 45 different embroidery specific formats". It does not list formats individually or mention WebAssembly/Emscripten ([GitHub](https://github.com/Embroidermodder/libembroidery)).
  - The parent repo Embroidermodder/Embroidermodder is C, Zlib, 634 stars, last push 2026-10-07 ([GitHub](https://github.com/Embroidermodder/Embroidermodder)).
  - A search snippet reports an open issue where the CMake build fails with an implicit declaration of `emb_fwrite`, a native build problem ([ecosyste.ms issue index](https://opencollective.ecosyste.ms/projects/23720/issues)). Not verified directly.
- **EmbroidePy/EmbroideryIO** — Java/Android port, MIT, 39 stars, last push 2024-04-19 ([GitHub](https://github.com/EmbroidePy/EmbroideryIO)). Not browser-usable, but a further reference implementation.

**JavaScript / TypeScript projects**

- **Federicokalik/embroidery-converter-kit ("Ricuci")** — TypeScript, 1 star, created 2026-07-05, last push 2026-09-19, site https://ricuci.app/ ([GitHub](https://github.com/Federicokalik/embroidery-converter-kit)).
  - Stack: a pnpm monorepo with a "TS, zero deps" core built with tsup, an Astro web app, an Electron desktop app, and Vitest tests.
  - Reads 13 formats: vip, zhs, dst, exp, jef, pec, pes, vp3, hus, xxx, sew, shv, pcs.
  - Writes 10 formats: zhs, dst, exp, jef, pec, pes, vp3, hus, vip, xxx.
  - It uses a shared intermediate representation (stitches, commands and threads in 0.1 mm units).
  - It claims the web studio is client-side and that "files never leave your computer". It offers hoop presets for 109 machines and a "thread preview with real colors".
  - Lineage: EmbCompress, HUS and VIP logic was ported from pyembroidery, and the VIP color keystream was transcoded from libembroidery.
  - License: code is MIT; docs are CC BY 4.0; fonts (OFL) and GSAP keep their own terms; the "Ricuci" name is trademarked ([GitHub](https://github.com/Federicokalik/embroidery-converter-kit)).
  - Overall it is the closest thing found to an embeddable TS read/write core, but it has very little adoption.
- **leomurca/embroidery-viewer** — JavaScript/Svelte + Vite, MIT, 24 stars, 6 forks, 80 commits, live demo embroideryviewer.xyz ([GitHub](https://github.com/leomurca/embroidery-viewer)).
  - The GitHub repo was archived read-only on 2025-04-13. The owner says development moved to a self-hosted git at git.leomurca.xyz ([GitHub](https://github.com/leomurca/embroidery-viewer)).
  - Formats and rendering approach are not stated on the GitHub page ([GitHub](https://github.com/leomurca/embroidery-viewer)).
- **redteam316/html5-embroidery** — JavaScript, MIT, 63 stars, 8 commits, last push 2015-01-07. Described as "View embroidery designs directly in your HTML5 browser with no other software required" ([GitHub](https://github.com/redteam316/html5-embroidery)).
  - Its source files suggest readers for DST, EXP, EXY, JEF, PCS, PEC, PES, SEW, VP3, XXX and ZSK (inferred from `*format.js` filenames, not documented). It uses jDataView for binary parsing ([GitHub](https://github.com/redteam316/html5-embroidery)).
  - Read-only viewer, effectively abandoned.
- **manthrax/dst-format** — JavaScript three.js loader for .dst only, 31 stars, last push 2024-03-05, no license shown on the page. Demo: https://manthrax.github.io/dst-format/index.html ([GitHub](https://github.com/manthrax/dst-format)).
  - Stitches render as lines or textured quads (`threadThickness`, separate `jumpThreadThickness`). The example applies a thread texture plus normal map, and there is a `toTexture()` render-target option.
  - A draw-range control animates the sewing progress.
  - Colors come from a manual `palette` array; missing entries get random colors, because DST carries no colors ([GitHub](https://github.com/manthrax/dst-format)).
  - A three.js forum thread (snippet only) has the author saying it "isn't guaranteed to work", with colors specified manually ([three.js forum](https://discourse.threejs.org/t/load-file-in-dst-format/60325?page=2)).
- **jhbruhn/respira** — TypeScript, Apache-2.0, 104 stars, last push 2026-03-29. Controller software for the Brother PP-1 SKiTCH that sends .PES patterns to the machine via WebBluetooth in Chrome/Edge, with Electron desktop builds ([GitHub](https://github.com/jhbruhn/respira)).
  - It uses Ink/Stitch's pystitch to import PES and has a live pattern preview with a color-block list.
  - The page does not say whether pystitch runs in-browser through Pyodide. Unverified; the repo could not be accessed from this session. If it does, it is a working pystitch-in-browser precedent.
  - The author says about 99% of the code was written with LLMs ([GitHub](https://github.com/jhbruhn/respira)).
- **akjabay/jef2img** — JS, MIT, 4 stars, last push 2023-09-12. A Node.js module that converts JEF to an image ([GitHub search result](https://github.com/akjabay/jef2img)).
- **Generative/creation libraries (write-oriented, not viewers):**
  - **stitchables/stitch.js** — MIT, 23 stars, last push 2024-08-01, "computational embroidery with Javascript" ([GitHub](https://github.com/stitchables/stitch.js)).
  - **nkymut/p5.embroider** — 15 stars, last push 2026-09-02, a p5.js library for creating digital embroidery patterns ([GitHub](https://github.com/nkymut/p5.embroider)).
  - **carlsapp/grizzly-stitch** — LGPL-3.0, 18 stars, last push 2023-03-03, a "Web-Based Embroidery Digitizer" ([GitHub](https://github.com/carlsapp/grizzly-stitch)).
  - **GabrielRalph/Embroidery** — "SVG Embroidery DST file cam", 4 stars ([GitHub](https://github.com/GabrielRalph/Embroidery)).
- **Very new or low-signal repos (2026, 0–2 stars):**
  - **Frankyface/satin-studio** — "Free browser-based embroidery digitizer… export machine-ready" files, TS, last push 2026-07-20 ([GitHub](https://github.com/Frankyface/satin-studio)).
  - **abhineetunreal/loom-studio** — "embroidery design viewer and yarn recolor tool", TS, last push 2026-10-09 ([GitHub](https://github.com/abhineetunreal/loom-studio)).
  - **scxf666/EDVC_Embroidery-Design** — "Embroidery Design Viewer and Converter", JS, MIT, last push 2026-03-09 ([GitHub](https://github.com/scxf666/EDVC_Embroidery-Design)).
  - **D-git-boom/Embroidery-Design-Viewer** — "view designs in 3d model", JS, last push 2025-12-28 ([GitHub](https://github.com/D-git-boom/Embroidery-Design-Viewer)).
  - **HoangEditor/embroidery-converter** — "convert between DST, PES, JEF, EXP and 40+ formats", HTML, no license, last push 2026-07-27 ([GitHub](https://github.com/HoangEditor/embroidery-converter)).
  - **Achraf921/twineconvert** — a multi-format in-browser converter including DST/PES/JEF/EXP, TS, no license ([GitHub](https://github.com/Achraf921/twineconvert)).
- **Non-JS viewers (reference only):**
  - **njcrawford/EmbroideryReader** — C#, GPL-2.0, 44 stars, PES viewer ([GitHub](https://github.com/njcrawford/EmbroideryReader)).
  - **quentin452/Catz-Embroidery** — "Rust embroidery suite" (PES/DST/SVG), MIT, 1 star ([GitHub](https://github.com/quentin452/Catz-Embroidery)).
  - **bobbymarko/StitchPeek** — macOS Quick Look for DST ([GitHub](https://github.com/bobbymarko/StitchPeek)).
- A three.js forum post (snippet only) describes a React embroidery viewer with camera try-on. Its showcased images were rendered by Wilcom Embroidery Studio, not by the viewer, and no code license was visible ([three.js forum](https://discourse.threejs.org/t/embroidery-viewer/64392)).

### Inferences
- Rendering quality across the open JS projects is mostly **flat 2D polylines on canvas**, colored per thread block. The one notable exception is manthrax/dst-format, which uses textured quads with normal maps in three.js to approximate thread. None of the projects reviewed offer a documented "realistic 3D thread shading" renderer comparable to commercial tools (Wilcom/Embrilliance). EEganizer would likely need to build a shaded renderer itself (e.g., three.js or a canvas stroke-with-gradient technique on top of a parser).
- **Format coverage for writing is the hard part.** Only Ricuci (TS) and the Python/C libraries write PES/JEF/VP3/XXX. PES writing in particular needs the PEC thumbnail/graphics section and a thread-palette mapping. A safe path is either (a) adopting or forking Ricuci's MIT TS core after an audit, or (b) running pystitch in Pyodide.
- License-wise, MIT (pyembroidery, pystitch, Ricuci core, html5-embroidery, leomurca) and Zlib (libembroidery) are all compatible with embedding in a commercial site. Avoid GPL code such as Ink/Stitch (GPL-3.0) and EmbroideryReader (GPL-2.0) for client-shipped code. Also avoid repos with no license (dst-format, HoangEditor, twineconvert) unless the author grants one.
- Maintenance risk is high for every JS option: single maintainers, archived repos, or projects only months old.

### Gaps
- **npm:** I did not query the npm registry directly (no npm search tool reachable). Whether packages like "pes.js", "dst-parser" or "embroidery" with meaningful download counts exist is unverified.
- **leomurca/embroidery-viewer:** Formats, rendering approach, and whether the self-hosted repo is still active could not be verified, because embroideryviewer.xyz did not resolve.
- **"Josh Varga":** I found no source tying a "Josh Varga" or "Jason" to a specific embroidery-viewer repo. The author of html5-embroidery (GitHub user redteam316) is not named on the page, and attributing it to anyone is unverified.
- **No embroideryviewer by "Ruby" was found;** the only Ruby repo surfaced was cloudhausllc/emb-editor, a CSV viewer from 2017.
- **Ricuci:** Rendering technology and the per-format quality of its writers have not been tested.

## Feasibility of pyembroidery in-browser via Pyodide, or libembroidery to WASM via Emscripten — any existing demos?

### Takeaway
Running pyembroidery/pystitch in Pyodide looks technically straightforward, since piwheels lists no dependencies. The cost is a roughly 5–7 MB Brotli first-load Pyodide runtime with about 0.5–1.3 s initialization (based on Pyodide 0.23-era benchmarks). I found no public demo of either Pyodide+pyembroidery or a libembroidery Emscripten build. Respira uses pystitch, but whether it does so in-browser is unconfirmed.

### Cited Findings
- **Pyodide runtime:** Pyodide is "a Python distribution for the browser and Node.js based on WebAssembly" ([Pyodide docs](https://pyodide.org/en/0.26.3/_sources/project/about.md)).
  - Pure-Python packages with a wheel on PyPI can be installed with micropip. C-extension packages work only if ported ([Pyodide usage](https://pyodide.org/en/0.21.3/usage/index.html)).
- **pyembroidery dependencies:** pyembroidery declares no dependencies on piwheels ([piwheels](https://www.piwheels.org/project/pyembroidery/)).
  - The README explicitly describes its HUS decompressor as "written from the ground up in pure python… does not require any compiled element or dll file" ([GitHub](https://github.com/EmbroidePy/pyembroidery)).
- **Load cost:** The Pyodide 0.23 release notes give about 5.3 MB Brotli-compressed for core plus stdlib, with load and init of 1.3 s in Firefox and 0.9 s in Chrome.
  - A py-compiled build is 6.9 MB and loads in 0.9 s / 0.5 s, measured on 100 Mbps with the cache disabled ([Pyodide blog 0.23](https://blog.pyodide.org/posts/0.23-release/)).
  - The older roadmap says a 6.4 MB first download and 4–5 s init; repeat loads are faster because they are cached ([Pyodide roadmap](https://pyodide.org/en/stable/project/roadmap.html)).
  - The 0.23 notes caution that size gains have been offset by stdlib growth ([Pyodide blog 0.23](https://blog.pyodide.org/posts/0.23-release/)).
- **libembroidery to WASM:** The libembroidery README makes no mention of WebAssembly, Emscripten or JS bindings ([GitHub](https://github.com/Embroidermodder/libembroidery)). Emscripten compiles C/C++ to WebAssembly, so it is the obvious route, but no existing build or demo was found ([search](https://inkstitch.org/developers/pyembroidery/)).
  - Only Rust FFI bindings exist (hakasec/libembroidery-sys, last push 2024-09-16) ([GitHub](https://github.com/hakasec/libembroidery-sys)).
- **History:** Ink/Stitch originally used libembroidery, and pyembroidery was later created as a Python port ([Ink/Stitch developer docs](https://inkstitch.org/developers/pyembroidery/)).
- **Respira:** Respira imports PES with pystitch and runs in the browser via WebBluetooth. The page does not state the Python runtime used in the web build ([GitHub](https://github.com/jhbruhn/respira)).

### Inferences
- **Recommended approach if write support for many formats is needed:** load Pyodide plus a pystitch wheel lazily, in a Web Worker, only when the user opens "Convert/Export". Viewing stays in a light JS parser.
  - Expected first-use payload is roughly 6–8 MB including the pystitch wheel. This is an estimate: the wheel size and the current Pyodide release size were not measured. The payload caches thereafter.
  - Pyodide's micropip can install pure-Python wheels, and pystitch/pyembroidery appear to be pure Python, so no porting should be required. This needs a quick proof-of-concept to confirm (e.g., PNG writing might need extra modules such as zlib, which is in the stdlib).
- A libembroidery Emscripten build would likely be smaller (C compiled to a few hundred KB of WASM is typical), but that figure is an estimate. No one appears to have done the build, and the repo has had recent native build issues. It is higher effort and less proven than Pyodide.
- Porting pyembroidery to TS (as Ricuci partially did) produces the smallest bundle but carries the highest maintenance cost.

### Gaps
- No measured size for the current (2026) Pyodide release or for the pystitch wheel was found.
- No confirmed public demo of pyembroidery/pystitch running in Pyodide was found. Respira's mechanism remains unverified because the repo was not accessible from this session for file inspection.
- No confirmed Emscripten build of libembroidery exists. The libembroidery.org site was not checked.

## Existing free web tools and what open source they're built on

### Takeaway
Free browser viewers exist, but most do not disclose their engine. Only embroideryviewer.xyz (leomurca, MIT) and Ricuci (ricuci.app, MIT core) are verifiably open source. The Chrome/Google Workspace "Embroidery Viewer and Converter" and the Product Hunt "Embroidery Viewer" are closed or of unknown provenance.

### Cited Findings
- **embroideryviewer.xyz** — the live demo of leomurca/embroidery-viewer (MIT, Svelte), archived on GitHub 2025-04-13 ([GitHub](https://github.com/leomurca/embroidery-viewer)). The site itself could not be fetched (DNS failure in this environment).
- **ricuci.app** — the web studio of embroidery-converter-kit. It claims client-side conversion where files never leave the computer, and has MIT core code ([GitHub](https://github.com/Federicokalik/embroidery-converter-kit)).
- **"Embroidery Viewer and Converter"** (Chrome extension / Google Workspace add-on):
  - Views pes, dst, exp, jef, vp3, u01 and pec (the Chrome listing also mentions gcode) and converts between formats.
  - Opens files from local storage, a URL, Google Drive, Dropbox or Box. The listing dates are 2019 and 2022.
  - One reviewer reports the free daily conversion limit. Source code is not indicated. All details come from search snippets ([Google Workspace Marketplace](https://workspace.google.com/marketplace/app/embroidery_viewer_and_converter/397239404956); [Chrome Web Store](https://chromewebstore.google.com/detail/dhecljdbpaninichncjocoljjihkfacj)).
  - Its format list (u01, pec, gcode) closely matches pyembroidery's set, but that is an inference, not confirmed.
- **"Embroidery Viewer" on Product Hunt** — a browser-only viewer for pes, dst, jef, pec and exp that says it processes files locally. The maker, URL and source could not be retrieved (search snippet only) ([Product Hunt](https://www.producthunt.com/products/embroidery-viewer/makers)).
- **Ink/Stitch** — GPL-3.0, 1,363 stars, last push 2026-10-08. It is an Inkscape (desktop) extension, not a web app ([GitHub](https://github.com/inkstitch/inkstitch)). Its I/O layer is pystitch ([GitHub](https://github.com/inkstitch/pystitch)).
- **Desktop free viewers often recommended instead of web tools:** BERNINA ArtLink, Embrilliance Express, Embroidery Reader (from a zdigitizing article, per search snippet) ([zdigitizing](https://zdigitizing.com/what-is-a-pes-file/)).
- The "8 FREE Machine Embroidery File Format Converters" article exists, but its content could not be fetched ([zdigitizing](https://zdigitizing.com/embroidery-file-format-converter/)).

### Inferences
- "myembroideries" and an "Ink/Stitch web" product were not found in any source. Ink/Stitch remains desktop-only as far as the evidence shows.
- The space is fragmented enough that EEganizer would be competing with small hobby tools, not an established open-source web standard.

### Gaps
- The myembroideries site and its tech stack were not found or verified.
- I found no Reddit r/MachineEmbroidery or Hacker News threads; searches returned none.
- The engines behind the Chrome extension and the Product Hunt viewer are unknown.

## How do these handle export/download to USB for machines?

### Takeaway
Browser tools cannot write directly to a USB stick through WebUSB, because browsers block the mass-storage class. Web tools therefore just trigger a normal file download, or a save dialog on Chromium via the File System Access API, and the user saves or copies the file onto the USB drive. The only "direct to machine" browser path found is wireless: Respira uses WebBluetooth for the Brother SKiTCH.

### Cited Findings
- **WebUSB blocks mass storage:** Chrome's Blink explicitly blocks protected USB interface classes, including Mass Storage, from WebUSB ([Chromium blink-dev](https://groups.google.com/a/chromium.org/g/blink-dev/c/LZXocaeCwDw/m/GLfAffGLAAAJ)).
  - Web-platform tests expect claiming a protected mass-storage interface to fail with SecurityError ([WPT via Searchfox](https://searchfox.org/firefox-main/source/testing/web-platform/tests/webusb/protected-interface-classes.https.any.js)).
  - The protected list covers audio, HID, mass storage, smart card, video, audio/video and wireless controllers ([BleepingComputer](https://www.bleepingcomputer.com/news/google/google-chrome-to-let-isolated-web-app-access-sensitive-usb-devices/amp/)).
  - Only Chrome Isolated Web Apps with the `usb-unrestricted` policy can claim protected classes ([Chromium intent to ship](https://groups.google.com/a/chromium.org/g/blink-dev/c/hXgwRCYta-k/m/NsLkciF1BwAJ); [WICG explainer](https://github.com/WICG/webusb/blob/main/unrestricted-usb-explainer.md)).
  - Electron apps can override the protected-class list ([Electron commit mirror](https://ayakael.net/mirrors/electron/commit/b4ec363b3ddfccc094e9ff2016b66a87294e0e84?files=docs)).
- **Respira:** sends .PES patterns to the Brother PP-1 SKiTCH over WebBluetooth in Chromium browsers, with Electron desktop builds as an alternative ([GitHub](https://github.com/jhbruhn/respira)).
- **Ricuci:** offers a browser studio plus Electron desktop and CLI builds. Its hoop presets for 109 machines suggest export is targeted per machine, but the save mechanism is not described ([GitHub](https://github.com/Federicokalik/embroidery-converter-kit)).

### Inferences
- **Recommended UX for EEganizer:** convert client-side, then offer a standard `<a download>` Blob download, named with the machine's expected extension (and 8.3-style or short filenames for older machines). On Chromium, optionally use the File System Access API `showSaveFilePicker` so the user can pick the USB drive directly. Pair this with help text on copying the file to the USB root or the machine's expected folder.
  - `showSaveFilePicker` is Chromium-only in my understanding (unverified here; the MDN fetch failed). It must be feature-detected, with a fallback to plain download.
- Machine-specific constraints matter more than transport: hoop size limits, max stitch count, color-count limits, and PES version compatibility. These should be validated before export.

### Gaps
- Browser support for `showSaveFilePicker` could not be confirmed (MDN unreachable).
- No source documented how embroideryviewer.xyz or the Chrome extension deliver files (download vs. cloud save). This is assumed to be standard download.
- Per-machine USB folder and filename conventions were not researched (out of scope here).
