"""
test_cli.py
End-to-end tests for the classify.py command line: run it as a subprocess
and check what a user would actually see.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "src" / "classify.py"

# A wide, colorless terminal so rich (if installed) doesn't wrap or add
# escape codes that would break simple substring checks.
ENV = {**os.environ, "COLUMNS": "200", "NO_COLOR": "1", "TERM": "dumb"}


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True, text=True, env=ENV,
    )


@pytest.mark.parametrize("text,symbol", [
    ("It is not raining.", "τ"),
    ("Not bad.", "ε"),
    ("I didn't say she stole the money.", "δ"),
])
def test_cli_prints_type_and_trigger(text, symbol):
    proc = run_cli("--text", text)
    assert proc.returncode == 0, proc.stderr
    assert symbol in proc.stdout
    assert "trigger" in proc.stdout or "'" in proc.stdout


def test_cli_reports_no_negation():
    proc = run_cli("--text", "It is raining.")
    assert proc.returncode == 0, proc.stderr
    assert "No negation detected." in proc.stdout


def test_cli_requires_text_argument():
    proc = run_cli()
    assert proc.returncode != 0
    assert "--text" in proc.stderr
