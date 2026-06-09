"""
types.py
Core dataclasses for the τ/ε/δ negation taxonomy.
"""

from dataclasses import dataclass
from enum import Enum


class NegationType(Enum):
    TAU = "τ"          # truth-conditional
    EPSILON = "ε"      # expressive/evaluative
    DELTA = "δ"        # discourse/metalinguistic
    AMBIGUOUS = "?"    # underspecified


@dataclass
class NegationInstance:
    text: str
    neg_type: NegationType
    trigger: str
    rationale: str

    def __str__(self):
        return (
            f"[{self.neg_type.value}] '{self.trigger}' in: {self.text!r}\n"
            f"    → {self.rationale}"
        )
