"""
test_examples.py
Data-driven tests: every line in data/examples/<type>.txt must classify
to the negation type named by its file, and every line in
data/examples/none.txt must not be detected as negation at all.

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


def _load_sentences(stem):
    path = EXAMPLES_DIR / f"{stem}.txt"
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def _load_cases():
    return [(sentence, expected)
            for stem, expected in FILE_TO_TYPE.items()
            for sentence in _load_sentences(stem)]


CASES = _load_cases()
NONE_CASES = _load_sentences("none")


@pytest.mark.parametrize("sentence,expected", CASES, ids=[c[0] for c in CASES])
def test_example_classifies_to_its_type(sentence, expected):
    result = classify(sentence)
    assert result is not None, f"no negation detected in: {sentence!r}"
    assert result.neg_type is expected, (
        f"{sentence!r} classified as {result.neg_type.value} "
        f"(trigger {result.trigger!r}), expected {expected.value}"
    )


@pytest.mark.parametrize("sentence", NONE_CASES)
def test_non_negation_is_not_detected(sentence):
    result = classify(sentence)
    assert result is None, (
        f"{sentence!r} classified as {result.neg_type.value} "
        f"(trigger {result.trigger!r}), expected no negation"
    )
