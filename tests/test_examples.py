"""
test_examples.py
Data-driven tests: every line in data/examples/<type>.txt must classify
to the negation type named by its file.

Run with:  pytest
"""

import sys
from pathlib import Path

import pytest

# The src modules import each other by bare name (e.g. `from taxonomy import ...`),
# so src/ must be on the path.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from patterns import classify  # noqa: E402
from taxonomy import NegationType  # noqa: E402

EXAMPLES_DIR = ROOT / "data" / "examples"

# Maps example filename stem -> expected NegationType.
FILE_TO_TYPE = {
    "tau": NegationType.TAU,
    "epsilon": NegationType.EPSILON,
    "delta": NegationType.DELTA,
}


def _load_cases():
    cases = []
    for stem, expected in FILE_TO_TYPE.items():
        path = EXAMPLES_DIR / f"{stem}.txt"
        for line in path.read_text(encoding="utf-8").splitlines():
            sentence = line.strip()
            if sentence:
                cases.append((sentence, expected))
    return cases


CASES = _load_cases()


@pytest.mark.parametrize("sentence,expected", CASES, ids=[c[0] for c in CASES])
def test_example_classifies_to_its_type(sentence, expected):
    result = classify(sentence)
    assert result is not None, f"no negation detected in: {sentence!r}"
    assert result.neg_type is expected, (
        f"{sentence!r} classified as {result.neg_type.value} "
        f"(trigger {result.trigger!r}), expected {expected.value}"
    )
