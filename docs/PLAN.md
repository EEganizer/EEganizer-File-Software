# EEganizer File Software — Master Plan

**Goal:** customers who keep their embroidery design files in EEganizer can
open any design in their library, see what it is, check it fits their hoop,
make small safe adjustments, and download it in their machine's format —
without buying desktop software.

**Strategy:** reuse open source for file formats only (pystitch, MIT); build
everything customer-facing ourselves. Research: [`research/README.md`](research/README.md).

## Architecture

```
 EEganizer.com (WordPress)                    File service (this repo)
 ┌──────────────────────────┐   HTTPS + token  ┌───────────────────────────┐
 │ Library page / design    │ ───────────────► │ FastAPI  /v1/*            │
 │ detail page, "My         │                  │   │                       │
 │ Machines" profile        │ ◄─────────────── │   ▼  one child process    │
 └──────────────────────────┘  JSON / file     │ sandbox ► worker ► pystitch│
          │                                    └───────────────────────────┘
          ▼                                         (no network, read-only,
 object storage (design files, thumbnails)          memory/CPU/time limits)
```

- The service is **stateless**: bytes in, JSON/bytes out. Storage, accounts
  and billing stay in EEganizer.com.
- Every customer file is parsed in an isolated, resource-limited child process.
- The service is private (shared bearer token, internal network only).

## Phases and milestones

### Phase 1 — View & convert (MVP)

| # | Milestone | Status |
|---|---|---|
| 1.1 | Format library: read ~40 formats, properties, previews, conversion, guarded transforms, hoop fit, sandbox, CLI, tests | **Done** (`main`) |
| 1.2 | HTTP service: `/v1/formats`, `/inspect`, `/thumbnail`, `/convert` (by format or machine brand), `/fit`, `/transform`; upload size limit; token auth; Dockerfile; CI | **Done** (`claude/service-api`) |
| 1.3 | Real-file test corpus: 5+ real files per format (PES, DST, JEF, EXP, VP3, HUS, XXX), golden properties, round-trip checks | **Started**: 102 files / 6 formats pass ([CORPUS.md](CORPUS.md)); need XXX, SEW and more designers |
| 1.4 | Fuzz the parsers (malformed/truncated/random files) in the sandbox; fix or contain every crash and hang | Planned |
| 1.5 | WordPress integration: on upload, call `/inspect` + `/thumbnail` and store results; design detail page shows properties and thread list; "Download for my machine" button | Needs EEganizer.com owner sign-off |

**Exit criteria:** a customer uploads a PES, sees an accurate preview and
properties within seconds, and downloads a working JEF/VP3/DST that sews
correctly on a real machine (test stitch-outs on at least Brother, Janome,
Husqvarna/Pfaff).

### Phase 2 — Fit & light edit

| # | Milestone |
|---|---|
| 2.1 | Machine catalog: brand/model → formats, published sewing field per hoop, max stitch count |
| 2.2 | "My Machines" customer profile; fit badge on every design ("fits 5x7", "rotate to fit", "too big") |
| 2.3 | Guarded resize/rotate/mirror UI with the transform report (ok / caution / warning / blocked) |
| 2.4 | Printable thread chart / worksheet (color sequence, stitch counts, size, thumbnail) |
| 2.5 | Thread brand matching (convert hex colors to nearest Isacord / Madeira / Brother etc.) |
| 2.6 | Batch export: pick designs → one ZIP in the machine's format, ready for USB |
| 2.7 | **Combine designs + lettering** (library, CLI, `/v1/compose`) — **engine done**; needs a layout editor UI (drag to place, live preview) and real alphabet packs to test with |

### Phase 3 — Richer experience

| # | Milestone |
|---|---|
| 3.1 | In-browser interactive viewer (zoom, step through colors, stitch-out simulation) using the SVG/stitch data from the service |
| 3.2 | Lettering extras: arc/curved text, monogram templates, kerning tables per alphabet |
| 3.3 | Research spike: density-preserving resize for fill areas (our own algorithm), or license a commercial engine if customers ask for it |

## Decisions needed from EEganizer

1. **Hosting** for the service (same AWS account as EEganizer.com? container on ECS/Fargate or Lambda container?).
2. **Sample files** we're allowed to use for testing (our own purchased designs or free designs with permission).
3. **Who integrates** the WordPress side (Devin/team) and which plugin owns it.
4. **Pricing**: free for all customers, or part of a paid tier.
5. **License** for this repo's own code (currently unlicensed/proprietary).
6. **Legal review**: converting customer-owned designs, never decrypting vendor-encrypted designs, terms-of-service wording.

## Safety rules (apply to every phase)

- Never decrypt or strip protection from vendor-encrypted designs.
- Converted files belong to the customer's account only; never shared.
- Every untrusted file goes through `sandbox.run_isolated`.
- Only MIT/BSD/zlib/Apache-2.0 dependencies; no GPL/AGPL or unlicensed code.
- Resize never claims to recalculate stitches; the UI always shows the report.
