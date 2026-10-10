"""``eefile`` command line: a developer/ops tool over the library."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .convert import write_design
from .design import DesignError, load_design_file
from .formats import READABLE, WRITABLE
from .hoops import HOOPS, check_fit, smallest_hoop
from .inspect import analyze
from .render import render_png, render_svg
from .transform import transform


def _cmd_info(args) -> int:
    info = analyze(load_design_file(args.file))
    best = smallest_hoop(info)
    out = info.to_dict()
    out["smallest_hoop"] = best.hoop.key if best else None
    print(json.dumps(out, indent=2))
    return 0


def _cmd_convert(args) -> int:
    pattern = load_design_file(args.input)
    result = write_design(pattern, Path(args.output).suffix, pes_version=args.pes_version)
    Path(args.output).write_bytes(result.data)
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return 0


def _cmd_resize(args) -> int:
    pattern = load_design_file(args.input)
    new, report = transform(
        pattern,
        scale=args.scale,
        target_width_mm=args.width,
        target_height_mm=args.height,
        rotate_degrees=args.rotate,
        mirror_horizontal=args.mirror,
        target_extension=Path(args.output).suffix,
        free_standing_lace=args.lace,
        allow_large_resize=args.force,
    )
    print(json.dumps({k: v for k, v in vars(report).items()}, indent=2))
    if new is None:
        return 2
    result = write_design(new, Path(args.output).suffix)
    Path(args.output).write_bytes(result.data)
    return 0


def _cmd_preview(args) -> int:
    pattern = load_design_file(args.input)
    out = Path(args.output)
    out.write_bytes(render_svg(pattern) if out.suffix.lower() == ".svg" else render_png(pattern))
    return 0


def _cmd_fit(args) -> int:
    info = analyze(load_design_file(args.file))
    fit = check_fit(info, HOOPS[args.hoop])
    print(json.dumps({"hoop": args.hoop, "fits": fit.fits, "needs_rotation": fit.needs_rotation,
                      "scale_to_fit": fit.scale_to_fit}, indent=2))
    return 0 if fit.fits else 1


def _cmd_formats(_args) -> int:
    print(json.dumps({"read": READABLE, "write": WRITABLE}, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eefile", description="EEganizer embroidery file toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("info", help="show design properties")
    p.add_argument("file")
    p.set_defaults(func=_cmd_info)

    p = sub.add_parser("convert", help="convert to another format (by output extension)")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--pes-version", type=int, default=6, choices=[1, 6])
    p.set_defaults(func=_cmd_convert)

    p = sub.add_parser("resize", help="guarded scale/rotate/mirror")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--scale", type=float)
    p.add_argument("--width", type=float, help="target width in mm")
    p.add_argument("--height", type=float, help="target height in mm")
    p.add_argument("--rotate", type=float, default=0.0)
    p.add_argument("--mirror", action="store_true")
    p.add_argument("--lace", action="store_true", help="design is free-standing lace (resize blocked)")
    p.add_argument("--force", action="store_true", help="allow resizing beyond the warning limit")
    p.set_defaults(func=_cmd_resize)

    p = sub.add_parser("preview", help="render PNG or SVG preview")
    p.add_argument("input")
    p.add_argument("output")
    p.set_defaults(func=_cmd_preview)

    p = sub.add_parser("fit", help="check whether a design fits a hoop")
    p.add_argument("file")
    p.add_argument("--hoop", required=True, choices=sorted(HOOPS))
    p.set_defaults(func=_cmd_fit)

    p = sub.add_parser("formats", help="list readable/writable formats")
    p.set_defaults(func=_cmd_formats)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except DesignError as exc:
        print(f"error [{exc.code}]: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
