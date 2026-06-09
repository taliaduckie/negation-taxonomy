"""
patterns.py
Heuristic pattern matching for negation type classification.

Not a complete system — designed as an annotation assist and
demonstration of the framework, not a production classifier.
"""

import re
from taxonomy import NegationType, NegationInstance

# Patterns that suggest δ (metalinguistic/discourse negation)
DELTA_PATTERNS = [
    r"\bdidn't say\b",
    r"\bnot .{0,20} but\b",
    r"\bit's not that\b",
    r"\bI'm not saying\b",
]

# Affective/evaluative terms that suggest ε
EPSILON_LEXICON = {
    "not bad", "not great", "not ideal", "not exactly",
    "not the best", "not terrible", "not thrilled",
}

NEGATION_TOKENS = {"not", "n't", "no", "never", "neither", "nor"}


def classify(text: str) -> NegationInstance | None:
    text_lower = text.lower()

    # Check for δ patterns first (most marked)
    for pat in DELTA_PATTERNS:
        if re.search(pat, text_lower):
            trigger = re.search(pat, text_lower).group()
            return NegationInstance(text, NegationType.DELTA, trigger,
                                    "metalinguistic or corrective negation")

    # Check for ε multi-word expressions
    for expr in EPSILON_LEXICON:
        if expr in text_lower:
            return NegationInstance(text, NegationType.EPSILON, expr,
                                    "evaluative negation; encodes speaker stance")

    # Default to τ if a negation token is present
    for tok in NEGATION_TOKENS:
        if re.search(r'\b' + tok + r'\b', text_lower):
            return NegationInstance(text, NegationType.TAU, tok,
                                    "truth-conditional negation")

    return None
