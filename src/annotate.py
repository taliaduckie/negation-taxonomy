"""
annotate.py
Label probe sentences by hand and measure inter-annotator agreement.

    python src/annotate.py data/probe/stance_vs_speech_act.txt --annotator talia
    python src/annotate.py data/probe/stance_vs_speech_act.txt --report

Labels are appended to data/annotations/<probe stem>.csv as
(sentence, annotator, label). Re-running for the same annotator skips
sentences they have already labeled. The report lists each sentence with
every annotator's label and the classifier's prediction, then gives raw
agreement and Cohen's kappa for each pair of annotators.
"""

import argparse
import csv
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from patterns import classify

ROOT = Path(__file__).resolve().parent.parent
ANNOTATIONS_DIR = ROOT / "data" / "annotations"

LABELS = {"t": "τ", "e": "ε", "d": "δ", "?": "?"}
PROMPT = "  [t]au  [e]psilon  [d]elta  [?] unsure  [s]kip  [q]uit > "


def load_sentences(probe):
    return [line.strip() for line in probe.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")]


def annotations_path(probe):
    return ANNOTATIONS_DIR / f"{probe.stem}.csv"


def load_annotations(probe):
    """{sentence: {annotator: label}}"""
    table = defaultdict(dict)
    path = annotations_path(probe)
    if path.exists():
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                table[row["sentence"]][row["annotator"]] = row["label"]
    return table


def annotate(probe, annotator, stream=sys.stdin):
    existing = load_annotations(probe)
    todo = [s for s in load_sentences(probe) if annotator not in existing.get(s, {})]
    if not todo:
        print(f"{annotator} has labeled every sentence in {probe.name}.")
        return
    path = annotations_path(probe)
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["sentence", "annotator", "label"])
        for i, sentence in enumerate(todo, 1):
            print(f"\n({i}/{len(todo)}) {sentence}")
            while True:
                print(PROMPT, end="", flush=True)
                key = stream.readline()
                if not key:            # EOF
                    return
                key = key.strip().lower()
                if key == "q":
                    return
                if key == "s":
                    break
                if key in LABELS:
                    writer.writerow([sentence, annotator, LABELS[key]])
                    f.flush()
                    break


def cohen_kappa(a, b):
    """Kappa over two parallel label lists. None if undefined."""
    n = len(a)
    if n == 0:
        return None
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    if expected == 1.0:
        return None
    return (observed - expected) / (1 - expected)


def report(probe, out=sys.stdout):
    table = load_annotations(probe)
    sentences = load_sentences(probe)
    annotators = sorted({a for labels in table.values() for a in labels})
    if not annotators:
        print(f"No annotations yet for {probe.name}.", file=out)
        return

    print(f"{probe.name}: {len(sentences)} sentences, "
          f"annotators: {', '.join(annotators)}\n", file=out)
    header = "  ".join(f"{a[:8]:>8}" for a in annotators)
    print(f"{'clf':>4}  {header}  sentence", file=out)
    for sentence in sentences:
        labels = table.get(sentence, {})
        result = classify(sentence)
        clf = result.neg_type.value if result else "∅"
        row = "  ".join(f"{labels.get(a, '·'):>8}" for a in annotators)
        print(f"{clf:>4}  {row}  {sentence}", file=out)

    # Distribution per annotator
    print("\nLabel counts", file=out)
    for a in annotators:
        counts = Counter(labels[a] for labels in table.values() if a in labels)
        print(f"  {a:12} " + "  ".join(f"{k}:{v}" for k, v in sorted(counts.items())),
              file=out)

    # Pairwise agreement
    if len(annotators) >= 2:
        print("\nPairwise agreement (shared sentences only, '?' excluded)", file=out)
        for a, b in combinations(annotators, 2):
            pairs = [(l[a], l[b]) for l in table.values()
                     if a in l and b in l and "?" not in (l[a], l[b])]
            if not pairs:
                print(f"  {a} vs {b}: no shared sentences", file=out)
                continue
            xs, ys = zip(*pairs)
            raw = sum(x == y for x, y in pairs) / len(pairs)
            kappa = cohen_kappa(xs, ys)
            k = f"{kappa:.2f}" if kappa is not None else "n/a"
            print(f"  {a} vs {b}: {len(pairs)} shared, "
                  f"raw agreement {raw:.0%}, kappa {k}", file=out)

    # Which sentences split the annotators
    split = [s for s in sentences
             if len({l for l in table.get(s, {}).values() if l != "?"}) > 1]
    if split:
        print(f"\n{len(split)} sentences with disagreement:", file=out)
        for s in split:
            print(f"  {s}", file=out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("probe", type=Path, help="a file in data/probe/")
    ap.add_argument("--annotator", help="your name; starts an annotation session")
    ap.add_argument("--report", action="store_true", help="print the agreement report")
    args = ap.parse_args()
    if args.report:
        report(args.probe)
    elif args.annotator:
        annotate(args.probe, args.annotator)
    else:
        ap.error("pass --annotator NAME to label, or --report to compare")
