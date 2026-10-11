"""Printable thread chart / worksheet for one design.

Self-contained HTML (preview embedded as a data URI, inline CSS) that a
customer prints and keeps next to the machine: size, stitch count, sew time,
and the color stop sequence with each thread's color, name, stitches and
thread length. All text taken from the file is HTML-escaped: thread names
come from untrusted uploads.
"""

from __future__ import annotations

import base64
import html
import math

import pystitch

from .inspect import MAX_SEWN_STITCH_MM, DesignInfo, analyze, command_of
from .render import render_thumbnail

_STITCH = pystitch.STITCH
_JUMP = pystitch.JUMP
_TRIM = pystitch.TRIM
_COLOR_CHANGE = pystitch.COLOR_CHANGE
_END = pystitch.END


def block_stats(pattern: pystitch.EmbPattern) -> list[tuple[int, float]]:
    """(stitches, top-thread metres) per color stop; travel moves excluded."""
    totals: list[float] = [0.0]
    counts: list[int] = [0]
    prev = None
    sewing = False
    for stitch in pattern.stitches:
        cmd = command_of(stitch)
        if cmd == _COLOR_CHANGE:
            totals.append(0.0)
            counts.append(0)
            sewing = False
            continue
        if cmd == _STITCH:
            counts[-1] += 1
        if cmd in (_STITCH, _JUMP):
            point = (stitch[0], stitch[1])
            if cmd == _STITCH and prev is not None and sewing:
                length = math.dist(prev, point) / 10.0
                if length <= MAX_SEWN_STITCH_MM:
                    totals[-1] += length / 1000.0
            sewing = cmd == _STITCH
            prev = point
        elif cmd in (_TRIM, _END):
            sewing = False
    stats = list(zip(counts, totals))
    # A trailing color change before END leaves an empty last block.
    while len(stats) > 1 and stats[-1][0] == 0:
        stats.pop()
    return stats


def _swatch_text_color(hex_color: str) -> str:
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#000" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "#fff"


def worksheet_html(
    pattern: pystitch.EmbPattern,
    *,
    title: str = "Design",
    info: DesignInfo | None = None,
    has_colors: bool = True,
) -> str:
    """``has_colors=False`` for DST/EXP sources: their colors are placeholders."""
    info = info or analyze(pattern)
    stats = block_stats(pattern)
    thumb = base64.b64encode(render_thumbnail(pattern, 480)).decode()
    esc = html.escape

    has_colors = has_colors and bool(info.threads)
    rows = []
    for index, (stitches, length) in enumerate(stats):
        t = info.threads[index] if has_colors and index < len(info.threads) else None
        if t is not None:
            name = " ".join(x for x in (t.brand, t.catalog_number, t.description) if x) or "—"
            color_cell = (
                f'<span class="sw" style="background:{esc(t.hex_color)};color:{_swatch_text_color(t.hex_color)}">'
                f"{esc(t.hex_color)}</span>"
            )
        else:
            name, color_cell = "—", '<span class="sw none">your choice</span>'
        rows.append(
            f"<tr><td class=n>{index + 1}</td><td>{color_cell}</td><td>{esc(name)}</td>"
            f"<td class=n>{stitches:,}</td><td class=n>{length:.1f} m</td><td class=box></td></tr>"
        )

    unique = info.unique_color_count if has_colors else None
    note = ("" if has_colors else
            "<p class=note>This file format stores no thread colors. Pick colors from the designer's chart; "
            "the preview uses placeholder colors.</p>")
    summary = [
        ("Size", f"{info.width_mm:.1f} × {info.height_mm:.1f} mm ({info.width_in:.2f} × {info.height_in:.2f} in)"),
        ("Stitches", f"{info.stitch_count:,}"),
        ("Color stops", f"{len(stats)}" + (f" ({unique} colors)" if unique else "")),
        ("Est. sewing time", f"about {info.estimated_sew_minutes:.0f} min"),
        ("Top thread", f"about {info.thread_length_m:.0f} m"),
    ]
    summary_html = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in summary)

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{esc(title)} — thread chart</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font:14px/1.4 system-ui,-apple-system,Segoe UI,sans-serif;color:#1d1d1f;background:#fff;margin:24px;max-width:900px}}
h1{{font-size:22px;margin:0 0 4px}}
.top{{display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start}}
.prev{{border:1px solid #ddd;border-radius:8px;padding:8px;max-width:340px}}
.prev img{{max-width:100%;height:auto;display:block}}
dl{{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;margin:0}}
dt{{color:#666}} dd{{margin:0;font-weight:600}}
table{{border-collapse:collapse;width:100%;margin-top:20px}}
th,td{{border-bottom:1px solid #e5e5e5;padding:6px 8px;text-align:left}}
th{{font-size:12px;text-transform:uppercase;color:#666}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
td.box{{width:28px}} td.box::after{{content:"";display:inline-block;width:16px;height:16px;border:1.5px solid #999;border-radius:3px}}
.sw{{display:inline-block;min-width:84px;padding:2px 8px;border-radius:4px;border:1px solid #ccc;font-family:ui-monospace,monospace;font-size:12px}}
.sw.none{{background:#f3f3f3;color:#666}}
.note{{background:#fff8e1;border:1px solid #f0d58a;padding:8px 12px;border-radius:6px}}
footer{{margin-top:24px;color:#888;font-size:12px}}
@media print{{body{{margin:12mm}} .prev{{break-inside:avoid}} tr{{break-inside:avoid}}}}
</style></head><body>
<h1>{esc(title)}</h1>
<div class="top"><div class="prev"><img alt="Design preview" src="data:image/png;base64,{thumb}"></div>
<dl>{summary_html}</dl></div>
{note}
<table><thead><tr><th>Stop</th><th>Color</th><th>Thread</th><th>Stitches</th><th>Thread</th><th>Done</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<footer>Thread lengths are top thread only. Sewing time assumes 650 stitches/min plus thread changes.</footer>
</body></html>
"""
