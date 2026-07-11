"""
classify.py
CLI entry point for negation classification.

Usage:
    python classify.py --text "Not bad."
    python classify.py --text "I didn't say she stole the money."
"""

import argparse

from patterns import classify
from taxonomy import NegationType

# One accent color per type. Falls back to plain text if rich isn't installed.
TYPE_COLOR = {
    NegationType.TAU: "cyan",
    NegationType.EPSILON: "magenta",
    NegationType.DELTA: "yellow",
    NegationType.AMBIGUOUS: "dim",
}


def render(result):
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
    except ImportError:
        print(result if result else "No negation detected.")
        return

    console = Console()
    if result is None:
        console.print("[dim]No negation detected.[/dim]")
        return

    color = TYPE_COLOR.get(result.neg_type, "white")
    body = Text()
    body.append(f"{result.neg_type.value}  ", style=f"bold {color}")
    body.append(f"trigger: {result.trigger!r}\n", style="bold")
    body.append(result.rationale, style="italic dim")
    console.print(Panel(body, title=Text(result.text, style="white"),
                        border_style=color, expand=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    render(classify(args.text))
