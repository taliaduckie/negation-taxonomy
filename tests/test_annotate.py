"""
test_annotate.py
The annotation tool, driven with a fake stdin and a temporary annotations dir.
"""

import io
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import annotate  # noqa: E402


@pytest.fixture
def probe(tmp_path, monkeypatch):
    monkeypatch.setattr(annotate, "ANNOTATIONS_DIR", tmp_path / "annotations")
    p = tmp_path / "probe.txt"
    p.write_text("Not bad.\nI'm not saying it's bad.\nIt is not raining.\n")
    return p


def test_annotate_records_labels_and_skips_done(probe):
    annotate.annotate(probe, "ann", stream=io.StringIO("e\nd\nt\n"))
    table = annotate.load_annotations(probe)
    assert table["Not bad."]["ann"] == "ε"
    assert table["I'm not saying it's bad."]["ann"] == "δ"
    assert table["It is not raining."]["ann"] == "τ"

    # Second session for the same annotator has nothing to do and writes nothing.
    annotate.annotate(probe, "ann", stream=io.StringIO("t\nt\nt\n"))
    assert annotate.load_annotations(probe) == table


def test_annotate_skip_and_quit(probe):
    annotate.annotate(probe, "ann", stream=io.StringIO("s\nx\ne\nq\n"))
    table = annotate.load_annotations(probe)
    assert "Not bad." not in table                      # skipped
    assert table["I'm not saying it's bad."]["ann"] == "ε"   # 'x' ignored, then 'e'
    assert "It is not raining." not in table            # quit before it


def test_cohen_kappa():
    assert annotate.cohen_kappa(["τ", "ε", "δ"], ["τ", "ε", "δ"]) == pytest.approx(1.0)
    assert annotate.cohen_kappa(["τ", "τ"], ["τ", "τ"]) is None   # expected == 1
    assert annotate.cohen_kappa([], []) is None
    # Half agreement on two balanced labels: observed .5, expected .5 -> kappa 0
    assert annotate.cohen_kappa(["ε", "δ", "ε", "δ"], ["ε", "ε", "δ", "δ"]) == pytest.approx(0.0)


def test_report_two_annotators(probe):
    annotate.annotate(probe, "a", stream=io.StringIO("e\nd\nt\n"))
    annotate.annotate(probe, "b", stream=io.StringIO("e\ne\nt\n"))
    out = io.StringIO()
    annotate.report(probe, out=out)
    text = out.getvalue()
    assert "a vs b: 3 shared, raw agreement 67%" in text
    assert "1 sentences with disagreement" in text
    assert "I'm not saying it's bad." in text


def test_report_without_annotations(probe):
    out = io.StringIO()
    annotate.report(probe, out=out)
    assert "No annotations yet" in out.getvalue()
