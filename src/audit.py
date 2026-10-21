"""
audit.py
Evidence for the stage ordering in patterns.py.

Runs every example sentence through every stage (not just the first that
matches) and reports:

  1. a confusion table of labeled vs. predicted type, and
  2. every sentence where more than one type's stage fires, i.e. where the
     answer depends on stage order rather than on a unique cue.

Usage:
    python src/audit.py            # main example files
    python src/audit.py --hard     # include data/examples/hard/
"""

import argparse
from collections import Counter
from pathlib import Path

from patterns import STAGES, classify, fire
from taxonomy import NegationType

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT / "data" / "examples"

LABELS = {
    "tau": NegationType.TAU,
    "epsilon": NegationType.EPSILON,
    "delta": NegationType.DELTA,
    "none": None,
}


def _sym(t):
    return t.value if t else "∅"


def load(include_hard: bool):
    cases = []
    for stem, label in LABELS.items():
        paths = [EXAMPLES_DIR / f"{stem}.txt"]
        if include_hard:
            paths.append(EXAMPLES_DIR / "hard" / f"{stem}.txt")
        for path in paths:
            if path.exists():
                for line in path.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        cases.append((line.strip(), label))
    return cases


def confusion(cases):
    counts = Counter()
    for sentence, label in cases:
        result = classify(sentence)
        counts[(label, result.neg_type if result else None)] += 1

    order = [NegationType.TAU, NegationType.EPSILON, NegationType.DELTA, None]
    print("Confusion (rows = labeled, cols = predicted)\n")
    print("        " + "".join(f"{_sym(c):>6}" for c in order) + "   total")
    for row in order:
        cells = [counts[(row, col)] for col in order]
        print(f"  {_sym(row):>4}  " + "".join(f"{n:>6}" for n in cells) + f"   {sum(cells):>5}")
    correct = sum(n for (l, p), n in counts.items() if l is p)
    print(f"\n  {correct}/{len(cases)} correct\n")


def order_dependent(cases):
    print("Order-dependent sentences (more than one type's stage fires)\n")
    print("  Each line: label | winning stage → type | other stages that also fired\n")
    n = 0
    flips = Counter()
    for sentence, label in cases:
        hits = fire(sentence)
        # Every negated sentence trips "τ token", so it is the default rather
        # than a contestant. A sentence is order-dependent when two different
        # non-default types fire, or when a τ-labeled sentence trips any
        # non-default stage (so τ can only win if that stage is removed).
        marked_types = {t for name, t, _ in hits if name != "τ token"}
        contested = len(marked_types) >= 2 or (
            label is NegationType.TAU and marked_types
        )
        if not contested:
            continue
        n += 1
        win_name, win_type, win_trig = hits[0]
        others = ", ".join(f"{name}:{trig!r}" for name, _, trig in hits[1:]
                           if name != "τ token")
        mark = " " if win_type is label else "✗"
        flips[(_sym(label), win_name)] += 1
        print(f"{mark} {_sym(label)} | {win_name} → {_sym(win_type)} {win_trig!r} | {others}")
        print(f"      {sentence}")
    print(f"\n  {n} of {len(cases)} sentences are decided by stage order")
    if flips:
        print("  by (label, winning stage):")
        for (label, stage), k in sorted(flips.items()):
            print(f"    {label}  {stage:16} {k}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hard", action="store_true", help="include data/examples/hard/")
    args = ap.parse_args()
    cases = load(args.hard)
    print(f"{len(cases)} sentences, {len(STAGES)} stages\n")
    confusion(cases)
    order_dependent(cases)
