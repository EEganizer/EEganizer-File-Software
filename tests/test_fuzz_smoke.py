"""A short fuzz run on every test run; scripts/fuzz.py does the long runs."""

import importlib.util
import random
from pathlib import Path

from eeganizer_files import DesignError

_spec = importlib.util.spec_from_file_location("fuzz", Path(__file__).resolve().parents[1] / "scripts" / "fuzz.py")
fuzz = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fuzz)


def test_damaged_files_never_crash():
    rng = random.Random(20261011)
    seeds = fuzz.synthetic_seeds()
    for _ in range(400):
        name, data = rng.choice(seeds)
        mutated, _kind = fuzz.mutate(data, rng)
        try:
            fuzz.exercise(mutated, name.rsplit(".", 1)[-1])
        except DesignError:
            pass  # clean rejection is the expected outcome for damaged files
