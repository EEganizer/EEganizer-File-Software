"""Mutation fuzzer for the format readers.

Feeds damaged copies of seed files through everything a customer upload
touches (load, analyze, thumbnail, convert) and reports any outcome other
than success or a clean DesignError: unexpected exceptions, hangs and memory
blow-ups. Run it before trusting a new pystitch version or reader change:

    python scripts/fuzz.py --cases 2000 [--seeds DIR] [--seed 1]

Seeds default to synthetic designs in every writable format; add a folder of
real files with --seeds. Findings are printed with the seed, mutation and a
case id that reproduces them.
"""

from __future__ import annotations

import argparse
import collections
import io
import random
import resource
import signal
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests"))

from eeganizer_files import DesignError, analyze, load_design, write_design  # noqa: E402
from eeganizer_files.formats import READABLE  # noqa: E402
from eeganizer_files.render import render_thumbnail  # noqa: E402

CASE_TIMEOUT_S = 3


class Timeout(Exception):
    pass


def _alarm(_signum, _frame):
    raise Timeout()


def mutate(data: bytes, rng: random.Random) -> tuple[bytes, str]:
    buf = bytearray(data)
    kind = rng.choice(["flip", "bytes", "insert", "delete", "truncate", "header", "dup", "extreme"])
    n = len(buf)
    if n == 0:
        return bytes(rng.randbytes(64)), "random"
    if kind == "flip":
        for _ in range(rng.randint(1, 8)):
            i = rng.randrange(n)
            buf[i] ^= 1 << rng.randrange(8)
    elif kind == "bytes":
        for _ in range(rng.randint(1, 16)):
            buf[rng.randrange(n)] = rng.randrange(256)
    elif kind == "insert":
        i = rng.randrange(n)
        buf[i:i] = rng.randbytes(rng.randint(1, 8))
    elif kind == "delete":
        i = rng.randrange(n)
        del buf[i:i + rng.randint(1, 8)]
    elif kind == "truncate":
        buf = buf[: rng.randrange(n)]
    elif kind == "header":  # corrupt length/offset fields near the start
        for _ in range(rng.randint(1, 4)):
            i = rng.randrange(min(n, 600))
            buf[i] = rng.choice([0x00, 0xFF, 0x7F, 0x80, rng.randrange(256)])
    elif kind == "dup":
        i = rng.randrange(n)
        j = min(n, i + rng.randint(1, 256))
        buf[i:i] = buf[i:j] * rng.randint(2, 20)
    elif kind == "extreme":  # large offsets/counts in 32-bit fields
        i = rng.randrange(max(1, min(n - 4, 600)))
        buf[i:i + 4] = rng.choice([b"\xff\xff\xff\x7f", b"\x00\x00\x00\x80", b"\xff\xff\xff\xff"])
    return bytes(buf), kind


class Implausible(Exception):
    pass


def exercise(data: bytes, ext: str) -> None:
    pattern = load_design(data, ext)
    info = analyze(pattern)
    if max(info.width_mm, info.height_mm) > 1200:
        raise Implausible(f"{info.width_mm}x{info.height_mm}")
    render_thumbnail(pattern, 96)
    write_design(pattern, "dst")


def synthetic_seeds() -> list[tuple[str, bytes]]:
    from conftest import make_pattern

    pattern = make_pattern()
    seeds = []
    for ext in ["pes", "pec", "dst", "exp", "jef", "vp3", "xxx", "sew", "u01", "tbf"]:
        seeds.append((f"synthetic.{ext}", write_design(pattern, ext).data))
    return seeds


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=1000)
    parser.add_argument("--seeds", help="folder of real design files to mutate as well")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--memory-mb", type=int, default=2048)
    args = parser.parse_args()

    limit = args.memory_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    signal.signal(signal.SIGALRM, _alarm)

    seeds = synthetic_seeds()
    if args.seeds:
        files = [p for p in Path(args.seeds).rglob("*") if p.suffix.lower()[1:] in READABLE and p.is_file()]
        rng = random.Random(args.seed)
        rng.shuffle(files)
        seeds += [(p.name, p.read_bytes()) for p in files[:200]]

    rng = random.Random(args.seed)
    outcomes = collections.Counter()
    findings = []
    for case in range(args.cases):
        name, data = rng.choice(seeds)
        ext = name.rsplit(".", 1)[-1].lower()
        mutated, kind = mutate(data, rng)
        signal.alarm(CASE_TIMEOUT_S)
        try:
            exercise(mutated, ext)
            outcomes["ok"] += 1
        except DesignError as exc:
            outcomes[f"rejected:{exc.code}"] += 1
        except Implausible:
            outcomes["IMPLAUSIBLE_SIZE"] += 1
            findings.append((case, name, kind, "implausible", ""))
        except Timeout:
            outcomes["HANG"] += 1
            findings.append((case, name, kind, "hang", ""))
        except MemoryError:
            outcomes["MEMORY"] += 1
            findings.append((case, name, kind, "memory", ""))
        except Exception as exc:  # anything else is a bug: it must become a DesignError
            outcomes["CRASH"] += 1
            tb = traceback.extract_tb(exc.__traceback__)[-1]
            findings.append((case, name, kind, type(exc).__name__, f"{Path(tb.filename).name}:{tb.lineno}"))
        finally:
            signal.alarm(0)

    print(dict(sorted(outcomes.items())))
    by_site = collections.Counter((f[3], f[4]) for f in findings)
    for (what, where), count in by_site.most_common():
        example = next(f for f in findings if f[3] == what and f[4] == where)
        print(f"{count:5d}  {what:16s} {where:28s} e.g. case {example[0]} ({example[1]}, {example[2]})")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
