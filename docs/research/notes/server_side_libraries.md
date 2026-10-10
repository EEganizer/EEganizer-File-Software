# Open-source server-side / native libraries for embroidery design files (state as of 2026-10-10)

Method note: GitHub API access was blocked in this session, so stars and commit dates come from rendered GitHub pages fetched on 2026-10-10. Package dates come from the PyPI, npm and crates.io registry APIs. Where a page did not show a value, it is listed under Gaps rather than estimated. inkstitch.org and git.narl.io did not resolve from this environment.

## Q1. Candidate libraries: license, runtime, stars, recency, maintainers, activity

### Takeaway
Only three candidates are both permissively licensed and actively maintained in 2026: **pystitch** (MIT, Python; the Ink/Stitch team's fork of pyembroidery), **libembroidery** (zlib, C; still `v1.0-alpha`) and a group of young TypeScript and Rust ports. The ports have almost no adoption yet. Upstream **pyembroidery** (MIT) is effectively dormant: its last commit and release were in March 2024. **Ink/Stitch** is GPL-3 and an Inkscape extension, not a library. **Embroidery Reader** (C#) is GPL-2 and reads PES only.

### Cited Findings
**pyembroidery (EmbroidePy)**: Python, MIT.
- MIT license; 312 stars, 70 forks, 43 open issues, 4 open PRs; the GitHub Releases section is empty — [GitHub](https://github.com/EmbroidePy/pyembroidery)
- Last commits are dated **Mar 27, 2024** (merge of PR #171 "tbf-write-flip"), preceded by Nov 6, 2023 (PR #167 "silent-pass"). All recent commits are by **tatarize** (Tatarize, the sole maintainer) — [GitHub commits](https://github.com/EmbroidePy/pyembroidery/commits/main)
- PyPI: latest version **1.5.1** (2024-03-27); before that 1.5.0 (2023-11-06) and 1.4.36 (2022-04-26) — [PyPI](https://pypi.org/pypi/pyembroidery/json)
- EmbroideryIO is a Java/Android "honest transcription of pyembroidery." It is MIT-licensed, has 39 stars and 77 commits, and its install examples reference v0.0.7. It writes .pes .dst .exp .jef .vp3 .u01 .pec .xxx .csv .emm and omits gcode/png/svg/txt — [GitHub](https://github.com/EmbroidePy/EmbroideryIO)

**pystitch (inkstitch/pystitch)**: Python ≥3.9, MIT.
- MIT; 112 stars, 49 forks, 435 commits. The README calls it "an updated fork of the original" pyembroidery — [GitHub](https://github.com/inkstitch/pystitch)
- Recent commits: **Sep 8, 2026** "fix(pec): do not use reserved machine function from thread catalog (#140)" by emerzn; **Jun 19, 2026** "bump to v1.0.1" by kaalleen (an Ink/Stitch maintainer); a cleanup PR #136 from tcyrus in June 2026 — [GitHub commits](https://github.com/inkstitch/pystitch/commits/main)
- PyPI: **1.0.0** (2025-07-26), **1.0.1** (2026-06-19) — [PyPI](https://pypi.org/pypi/pystitch/json)

**Ink/Stitch**: Inkscape extension, GPL-3.0.
- GPL-3.0; ~1.4k stars, 254 forks. The README says it produces "embroidery pattern files (PES, DST, and many more)." The README does not mention a CLI or library API — [GitHub](https://github.com/inkstitch/inkstitch)
- Latest stable release is **v3.3.0, 2026-07-31**. Dev-build pre-releases continue into Sep–Oct 2026 — [GitHub releases/latest](https://github.com/inkstitch/inkstitch/releases/latest), [releases](https://github.com/inkstitch/inkstitch/releases)

**libembroidery (Embroidermodder)**: C single-header library, zlib.
- zlib licence; the license comment in `embroidery.h` must be kept. 82 stars, 27 forks, 31 open issues, no releases. The README is labelled **`v1.0-alpha` "(Under construction, please wait for v1.0 release.)"** and the copyright line reads 2018–2025 — [GitHub](https://github.com/Embroidermodder/libembroidery), [README raw](https://raw.githubusercontent.com/Embroidermodder/libembroidery/main/README.md)
- It claims to handle "over 45 different embroidery specific formats" plus vector formats. The CLI is named `sew` in one place and `embroider` in another (the README is inconsistent). It builds with CMake and has `ctest` diagnostics — [README](https://raw.githubusercontent.com/Embroidermodder/libembroidery/main/README.md)
- Latest commits are dated **Jul 4, 2026** by robin-swift ("moving to fixed types: uint8_t etc", "sew --test", PR #245) — [GitHub commits](https://github.com/Embroidermodder/libembroidery/commits/main)
- The Rust FFI crate `libembroidery-sys` 0.1.2 has not been updated since 2019-04-13 (stale) — [crates.io](https://crates.io/api/v1/crates?q=embroidery)

**Embroidery Reader (njcrawford/EmbroideryReader)**: C#, GPL-2.0.
- GPL-2.0; 44 stars, 289 commits, 6 open issues, no releases. It is described as an "open source .PES file viewer written in C#" (PES only) — [GitHub](https://github.com/njcrawford/EmbroideryReader)

**TypeScript/JS ports (all MIT)**
- **@guillaumemmm/tsembroidery**: MIT, "Based on pyembroidery." 17 versions since 2025-05-29; latest **2.9.0**, modified 2026-10-10, so very active. It has 3 deps (colord, clipper2-ts, svg-pathdata). It reads and writes .pes .dst .jef .exp .vp3 .xxx, writes SVG previews, and converts SVG to stitches. Coordinates are in 0.1 mm — [npm registry](https://registry.npmjs.org/@guillaumemmm/tsembroidery), [GitHub](https://github.com/GuillaumeMMM/tsembroidery)
- **ricuci / embroidery-converter-kit** (Federicokalik): code is MIT and docs are CC BY 4.0. Format logic is ported from pyembroidery (MIT) and libembroidery (zlib). It has 1 star and 43 commits, and the npm CLI `ricuci` 0.4.0 dates from 2026-09-19 (first published 2026-07-05). "Ricuci"/"embconv" are trademarks — [GitHub](https://github.com/Federicokalik/embroidery-converter-kit), [npm registry](https://registry.npmjs.org/ricuci)
- **jef2img**: MIT, JEF→PNG/JPEG via node-canvas; a single 1.0.0 release from 2020 (stale) — [npm registry](https://registry.npmjs.org/jef2img)

**Rust crates**
- **oxideav-embroidery**: MIT, pure Rust. 1 star, 39 commits, no releases on GitHub; crates.io 0.0.3, updated 2026-09-01, 249 downloads — [GitHub](https://github.com/OxideAV/oxideav-embroidery), [crates.io](https://crates.io/api/v1/crates?q=embroidery)
- **rustitch** 0.2.2 ("PES embroidery file parser and thumbnail renderer") and **stitch-peek** 0.1.4 (Nautilus thumbnailer). Both updated 2026-04-03, with 225 and 55 downloads; hosted on git.narl.io — [crates.io](https://crates.io/api/v1/crates?q=embroidery)
- **embroidery_tools** 0.2.0 (2025-08-09; "PES/PEC" tools; part of Wandalen/cgtools), 1,121 downloads — [crates.io](https://crates.io/api/v1/crates?q=embroidery)
- No crate named "embroidery-rs" turned up in a crates.io search for "embroidery" — [crates.io](https://crates.io/api/v1/crates?q=embroidery)

**Other**
- PEmbroider (CMU Creative Inquiry) is a Java/Processing library for *generating* embroidery, not a viewer or parser — [GitHub](https://github.com/CreativeInquiry/PEmbroider) (via search result)
- p5.embroider (LGPL-2.1+, 2026-09-02) is a p5.js generative library, not a file parser — [npm search](https://registry.npmjs.org/-/v1/search?text=embroidery)

### Inferences
- For a Python back end, **pystitch** is the better-maintained choice. It is API-compatible in spirit (same EmbPattern model), is MIT, and has active maintainers (the Ink/Stitch team). Upstream pyembroidery has had no commits for about 2.5 years.
- GPL-3 (Ink/Stitch) and GPL-2 (Embroidery Reader) are usable server-side without distribution obligations, because the GPL lacks AGPL's network clause. Copying their code into anything distributed (desktop helper, on-prem) would trigger copyleft. MIT and zlib carry no such issue.
- Every TS/Rust port is roughly 0–1 year old with negligible adoption (1–2 stars, hundreds of downloads). Treat them as experimental. Most are derivatives of pyembroidery logic anyway.

### Gaps
- Star counts for tsembroidery, rustitch/stitch-peek and libembroidery's parent Embroidermodder repo were not retrieved (blocked or not fetched).
- The last commit dates for EmbroideryIO and Embroidery Reader are not shown on the rendered pages. Both look dormant, but this is unverified.
- The SourceForge-era "Embroidery Reader" Windows freeware on Softpedia could not be confirmed as the same codebase.
- Whether the current Ink/Stitch v3.3.0 bundles pystitch rather than pyembroidery was not confirmed from a fetched source. The inkstitch.org docs were unreachable. The pystitch repo living in the inkstitch org and the Ink/Stitch maintainer's commits strongly suggest it does.

## Q2. Format coverage (read vs write) and known quality issues

### Takeaway
The pyembroidery family reads about 40 formats (including PES v1–v10 headers, HUS via a pure-Python EmbCompress decoder, and ZHS) and writes about 10–11 (PES, DST, EXP, JEF, VP3, PEC, XXX, U01, TBF, GCODE; pystitch adds SEW). It writes PES only as version 1 or 6. **No open-source library reads ART (Bernina).** The only open writers of VIP/HUS found are the young projects ricuci and oxideav-embroidery.

### Cited Findings
- **pyembroidery writes**: .pes, .dst, .exp, .jef, .vp3 (the "mandated" set) plus .u01, .pec, .xxx, .tbf, .gcode. **Reads**: .pes .dst .exp .jef .vp3 .10o .100 .bro .dat (Barudan & Sunstar) .dsb .dsz .emd .exy .fxy .gt .hus .inb .jpx .ksm .max .mit .new .pcd .pcm .pcq .pcs .pec .phb .phc .sew .shv .stc .stx .tap .tbf .u01 .xxx .zhs .zxy .gcode. Colour companions .col/.edr/.inf/.pmv are read and written. CSV and JSON are read/write. PNG, TXT and SVG are write-only — [pyembroidery README](https://github.com/EmbroidePy/pyembroidery)
- In the pyembroidery source, the ART format entry is **commented out** (`#     "extension": "art"`). Entries for hus and zhs are present — [EmbPattern.py](https://raw.githubusercontent.com/EmbroidePy/pyembroidery/main/pyembroidery/EmbPattern.py)
- PES read: PesReader branches on `#PES0100` (v10), 0090, 0080, 0070, 0060, 0050, 0055, 0056, 0040, 0030, and so on. Its comment reads "Ignoring several known PES versions, just abort and read PEC block," meaning it falls back to the PEC stitch block — [PesReader.py](https://raw.githubusercontent.com/EmbroidePy/pyembroidery/main/pyembroidery/PesReader.py)
- PES write supports only **VERSION_1 (`#PES0001`) and VERSION_6 (`#PES0060`)**, with an optional "truncated" mode (e.g. version `"6t"`) — [PesWriter.py](https://raw.githubusercontent.com/EmbroidePy/pyembroidery/main/pyembroidery/PesWriter.py)
- Issue #97 "PES file version 7 8 9 10 header" was closed on 2020-07-27 — [issues](https://github.com/EmbroidePy/pyembroidery/issues?q=is%3Aissue+crash+OR+hang+OR+infinite+OR+exception)
- **pystitch** writes .dst .exp .gcode .jef .pec .pes .sew .tbf .u01 .vp3 .xxx (11 entries, although the README says "10"). It reads 40 formats. It also adds quilting formats (reads iqp/plt/qcc, writes plt/qcc) and includes a pure-Python HUS decompressor (EmbCompress) — [pystitch](https://github.com/inkstitch/pystitch)
- pystitch's Sep 2026 fix: "fix(pec): do not use reserved machine function from thread catalog (#140)" — [commits](https://github.com/inkstitch/pystitch/commits/main)
- **libembroidery**: the README gives no per-format table. An old Embroidermodder wiki table (last updated January 2017) marks .art "No" for read/write and .dst/.col/.csv "Unstable." HUS/VIP rows were not captured. Treat this table as **stale** — [everybodywiki Embroidermodder](https://en.everybodywiki.com/Embroidermodder) (search snippet only)
- **oxideav-embroidery**: DST, PEC (writes 48×38 thumbnails), JEF, EXP (+.inf/.col/.edr), HUS and VIP are all read/write. PES is read, with a "minimal `#PES0001`" write. PHC/PHB/PTN/JEF+/JPX are decode-only. PHX is partial and unvalidated. VP3 is "header probe only; stitch section undocumented." XXX is header-only. ART is "extension recognition only." VIP's "colour-table scale [is] undocumented" — [GitHub](https://github.com/OxideAV/oxideav-embroidery)
- **ricuci**: reads vip zhs dst exp jef pec pes vp3 hus xxx sew shv pcs and writes zhs dst exp jef pec pes vp3 hus vip xxx. EmbCompress is ported from pyembroidery. It calls itself "the first open implementation of a ZHS writer." Multi-colour/trim-heavy ZHS writing is "deliberately conservative," and the project notes that "physical stitch-out remains the final acceptance test" — [GitHub](https://github.com/Federicokalik/embroidery-converter-kit), [npm](https://registry.npmjs.org/ricuci)
- **tsembroidery**: reads and writes .pes .dst .jef .exp .vp3 .xxx — [npm README](https://registry.npmjs.org/@guillaumemmm/tsembroidery)
- **Embroidery Reader**: .PES only — [GitHub](https://github.com/njcrawford/EmbroideryReader)
- Thread colour handling, DST: pyembroidery issue #149 "Dst Reader Thread values" is open (since 2022-06-06), and #142 "Help needed, color change macros" is open — [issues](https://github.com/EmbroidePy/pyembroidery/issues?q=is%3Aissue+crash+OR+hang+OR+infinite+OR+exception)
- JEF: issue #115 "Janome JEF Stop may indicate corruption on some machines" is closed — [issues](https://github.com/EmbroidePy/pyembroidery/issues?q=is%3Aissue+crash+OR+hang+OR+infinite+OR+exception)
- Commercial context: Wilcom treats ART (Bernina) as read-only up to V6, and Hatch reads ART V1–V4. This shows that ART support exists only in proprietary tools — [Wilcom](https://help.wilcom.com/portal/en/kb/articles/supported-formats), [Hatch](https://help.hatchembroidery.com/portal/en/kb/articles/what-file-formats-does-hatch-embroidery-v2-v3-read-and-write)

### Inferences
- PES v7–v10 support is read-oriented and relies on the embedded PEC block, so PES-specific objects (hoop, editable objects) beyond the header metadata are likely lost on round-trip. Output is always v1 or v6.
- DST and EXP carry no real thread colours. Previews of these formats need a default palette or the companion .inf/.col/.edr file.
- For a storage SaaS, the ART gap is the main uncovered format. VIP and EMB (Wilcom native) also appear in no mature open-source reader's list: pyembroidery's reader list has no .vip or .emb.
- VP3 is solid in pyembroidery-family libraries but only partial in oxideav-embroidery.

### Gaps
- No current per-format read/write table for libembroidery was retrievable (the main source is a single header in literate style, and raw fetches of `embroidery.h` returned empty or 404).
- No source was found for Wilcom .EMB support in any open-source library. Assume it is unsupported.
- No authoritative statement was found on HUS decode accuracy in pyembroidery (beyond the existence of EmbCompress).
- PEC thumbnail *reading* (the embedded 48×38 monochrome icons) in pyembroidery was not confirmed from source here.

## Q3. Extractable properties

### Takeaway
pyembroidery and pystitch expose everything EEganizer needs for a properties panel: bounds/extents, stitch count, colour-change count, thread list with hex colours and brand/catalog metadata, trims/jumps via command counting, and file metadata such as PES version. Hoop size and estimated stitch time are not built-in features. They must be computed or read from format-specific metadata.

### Cited Findings
- `EmbPattern` methods include `bounds()`, `count_stitch_commands(command)`, `count_color_changes()`, `count_needle_sets()`, `count_stitches()`, `count_threads()`, `get_match_commands()`, `get_unique_threadlist()`, `get_metadata(name)`, `transform(matrix)`, `fix_color_count()`, and `interpolate_trims(...)` — [EmbPattern.py](https://raw.githubusercontent.com/EmbroidePy/pyembroidery/main/pyembroidery/EmbPattern.py)
- Pattern data consists of `stitches` (`[x, y, command]`), `threadlist` (EmbThread with `.color`, `set_hex_color()`) and `extras` (metadata) — [README](https://github.com/EmbroidePy/pyembroidery)
- PesReader records the PES version into metadata (`out.metadata("version", 10)` and so on) — [PesReader.py](https://raw.githubusercontent.com/EmbroidePy/pyembroidery/main/pyembroidery/PesReader.py)
- ricuci `info` reports "stitches, colors, size, hoop fit" (with `--brand janome`). It ships hoop presets for 109 machines — [npm](https://registry.npmjs.org/ricuci), [GitHub](https://github.com/Federicokalik/embroidery-converter-kit)
- oxideav-embroidery derives extents, stitch/colour counts and absolute-position helpers — [GitHub](https://github.com/OxideAV/oxideav-embroidery)

### Inferences
- Trim and jump counts can be computed with `count_stitch_commands(TRIM)` / `(JUMP)`.
- Stitch time can be estimated as stitch count ÷ machine SPM plus a per-colour-change overhead. No library provides this, so it is an application-level formula.
- Hoop fit can be computed by comparing `bounds()` to a hoop table. ricuci's 109-machine hoop data (MIT code, CC BY docs) could be a reference.

### Gaps
- No library was found that reads the hoop size stored in PES/JEF headers as a first-class property. pyembroidery may store some in metadata, but this was not verified.
- No built-in stitch-time estimator was found in any candidate.

## Q4. Transforms, stitch-aware scaling, and max-stitch-length handling

### Takeaway
All candidates apply transforms by **naive coordinate math** (matrix translate/scale/rotate). None re-densifies fills or satins when resizing; pystitch explicitly puts high-level shape/fill processing out of scope. pyembroidery and pystitch do handle **long stitches on write**: they split stitches that exceed per-format `max_stitch`/`max_jump` limits (DST is 12.1 mm) according to a `long_stitch_contingency` policy.

### Cited Findings
- Writer settings include `translate`, `scale` and `rotate`, applied in that order, plus the middle-level commands `MATRIX_TRANSLATE`, `MATRIX_SCALE`, `MATRIX_SCALE_ORIGIN`, `MATRIX_ROTATE`, `MATRIX_ROTATE_ORIGIN` and `MATRIX_RESET`. There is also `move_center_to_origin()` — [README](https://github.com/EmbroidePy/pyembroidery)
- Max stitch: the `max_stitch` and `max_jump` settings are per format (DST max stitch 12.1 mm). The `OPTION_MAX_STITCH_LENGTH` and `OPTION_MAX_JUMP_LENGTH` commands change them on the fly. `long_stitch_contingency` can be needle jump (default), sew-to, or none. Other encoder settings: `full_jump`, `round`, `needle_count`, `thread_change_command`, `sequin_contingency`, `tie_on`, `tie_off`, `explicit_trim`, `writes_speeds`, `encode` — [README](https://github.com/EmbroidePy/pyembroidery)
- pystitch has a stated philosophy of minimising information loss, with low/middle/high-level command layers, and "High-level shape and fill processing is explicitly out of scope." Its encoder normalises patterns before writing — [pystitch](https://github.com/inkstitch/pystitch)
- ricuci offers `--center` and `--hoop WxH` but no resize-with-density option in its README — [npm](https://registry.npmjs.org/ricuci)

### Inferences
- Resizing a stitch file by more than about ±10–20% with these libraries changes stitch density and satin widths proportionally, because scaling is a coordinate multiply. A SaaS "resize" feature built on them should cap the scale range and warn users. True stitch-aware resizing requires object/outline data, which only native digitizing formats (and Ink/Stitch SVG sources) contain.
- Ink/Stitch can regenerate fills at any size, but only from its SVG source objects, not from imported machine files.

### Gaps
- No source was found documenting any open-source "stitch-aware" (re-densifying) resize of machine stitch files.

## Q5. Rendering to PNG/SVG

### Takeaway
pyembroidery and pystitch render natively to PNG and SVG with no external dependencies (a pure-Python PNG encoder), so they are good enough for server thumbnails. tsembroidery renders SVG, oxideav renders vector polylines, rustitch renders PES thumbnails, and jef2img renders JEF via node-canvas.

### Cited Findings
- pyembroidery `PngWriter` contains a self-contained `write_png` (zlib PNG packing), `draw_line`, gradient shading, `draw_text`, and `draw_guides`. Its settings are `guides`, `fancy`, `background` and `linewidth` — [PngWriter.py](https://raw.githubusercontent.com/EmbroidePy/pyembroidery/main/pyembroidery/PngWriter.py)
- `write_png` / `write_svg` are listed in the README — [README](https://github.com/EmbroidePy/pyembroidery)
- Issue #100 "PNGWriter automatically align to center the Pattern" was closed on 2020-09-15 — [issues](https://github.com/EmbroidePy/pyembroidery/issues?q=is%3Aissue+crash+OR+hang+OR+infinite+OR+exception)
- tsembroidery: `writeSvg(readPes(bytes))` gives an SVG preview — [npm README](https://registry.npmjs.org/@guillaumemmm/tsembroidery)
- oxideav-embroidery: `design_to_vector` gives a `Frame::Vector` with one stroked polyline per colour block, using thread RGB — [GitHub](https://github.com/OxideAV/oxideav-embroidery)
- rustitch: "PES embroidery file parser and thumbnail renderer" — [crates.io](https://crates.io/api/v1/crates?q=embroidery)
- jef2img: JEF→PNG/JPEG via `canvas` — [npm](https://registry.npmjs.org/jef2img)

### Inferences
- pyembroidery's "fancy" PNG mode gives a shaded, thread-like look. For higher-quality previews, render SVG and rasterise it with a separate tool (e.g. resvg or cairosvg), or draw stitches yourself with Pillow/Skia using the stitch list.

### Gaps
- No benchmark of render speed or memory for large designs (500k+ stitches) was found for any library.

## Q6. Security and robustness for untrusted uploads

### Takeaway
No candidate except oxideav-embroidery (a 1-star, pre-1.0 Rust crate) shows fuzzing. pyembroidery historically swallowed errors silently until v1.5.0 (Nov 2023) made them raise `IOError`. libembroidery is alpha C code. Parsing untrusted uploads with any of these libraries should be done in a sandboxed, resource-limited worker.

### Cited Findings
- oxideav-embroidery has a libFuzzer suite in `fuzz/` covering every public decode entry point plus a structured HUS/VIP container target. Its corpus-gated tests skip without a private commercial sample corpus — [GitHub](https://github.com/OxideAV/oxideav-embroidery)
- pystitch/pyembroidery: "Since 1.5.0, it raises explicit `IOError`s instead of silently passing errors" — [pystitch](https://github.com/inkstitch/pystitch); see also PR #167 "silent-pass" merged on Nov 6, 2023 — [pyembroidery commits](https://github.com/EmbroidePy/pyembroidery/commits/main)
- Historic crash and open bugs: issue #109 "Vintage fixed crash bug notification -- Inkstitch Version Issue" (closed 2021-03-20); issue #96 "DST Open Bug." (closed 2020-09-15); issue #8 "Transcode (object, object) malforms." (closed 2018) — [issues search](https://github.com/EmbroidePy/pyembroidery/issues?q=is%3Aissue+crash+OR+hang+OR+infinite+OR+exception)
- libembroidery is self-described as `v1.0-alpha`, "Under construction." A July 2026 commit was "moving to fixed types: uint8_t etc" — [README](https://raw.githubusercontent.com/Embroidermodder/libembroidery/main/README.md), [commits](https://github.com/Embroidermodder/libembroidery/commits/main)
- ricuci has 658 Vitest tests including byte-identical round-trips, but golden files are not in the repo, and the README does not mention fuzzing — [GitHub](https://github.com/Federicokalik/embroidery-converter-kit)

### Inferences
- Python and TypeScript parsers are memory-safe, but they can still hang or exhaust memory on crafted inputs. Examples are huge declared stitch counts, and decompression loops in HUS/VIP EmbCompress or in PES header offsets that seek elsewhere. Run them with CPU-time, memory and output-size limits plus per-file timeouts.
- C libembroidery carries memory-corruption risk on untrusted inputs. It is not recommended for internet-facing parsing without fuzzing it yourself and process isolation.
- A cheap hardening step is to fuzz pystitch's readers in-house (e.g. with Atheris) before launch.

### Gaps
- No CVEs, OSS-Fuzz integration, or published fuzzing results were found for pyembroidery, pystitch, libembroidery, tsembroidery or ricuci.
- No reports of infinite loops in HUS/VIP decoding were found (the issue search returned none). This is absence of evidence, not proof of robustness.
