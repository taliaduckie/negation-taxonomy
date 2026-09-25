"""
patterns.py
Heuristic pattern matching for negation type classification.

Not a complete system at all at all. it's designed as an annotation assist and
demonstration of the framework, not a production classifier.
"""

import re
from taxonomy import NegationType, NegationInstance

# Pronouns that can open a clause. Used to tell a corrective "not X but Y"
# (Horn's classic blunder (not a blunder just funny to say that hohohoh), where Y replaces X) from a merely concessive "but" that
# starts a new clause ("not raining, but it is cold").
_CLAUSE_OPENERS = r"(i|we|you|he|she|it|they|there|that|this|not|n't)\b"

# Patterns that suggest δ (metalinguistic/discourse negation).
# Matched case-insensitively (see re.IGNORECASE in classify), so keep them lowercase.
DELTA_PATTERNS = [
    r"\bdidn't say\b",
    # "not X but Y": Y must be a direct replacement, not a new negated or
    # subject-led clause. Rejects "Not bad, but not great either." (ε).
    r"\bnot\b.{0,20}\bbut (?!" + _CLAUSE_OPENERS + ")",
    # "it's not that <clause>": "that" as complementizer ("it's not that I
    # don't care"), not as degree adverb ("it's not that bad", which is ε).
    r"\bit's not that " + _CLAUSE_OPENERS,
    r"\bi'm not saying\b",
    # Negation retracted/upgraded across a dash: "Not bad — actually, it's excellent."
    r"\bnot\b.*[—-]\s*(actually|instead|rather|i (said|mean|just))",
]

# Affective/evaluative terms that suggest ε. Ordered so the reported trigger
# is deterministic when a sentence contains more than one.
EPSILON_LEXICON = (
    "not bad", "not great", "not ideal", "not exactly",
    "not the best", "not terrible", "not thrilled",
    "not that bad", "not so bad",
)

# Ordered so that the reported trigger is deterministic when several appear.
# Multi-word tokens come first so "no one" is reported rather than just "no".
NEGATION_TOKENS = (
    "no one",
    "not", "n't", "no", "never", "neither", "nor",
    # negative quantifiers / pronouns
    "nothing", "nobody", "none", "nowhere",
)


def classify(text: str) -> NegationInstance | None:
    text_lower = text.lower()

    # Check for δ patterns first (most marked)
    for pat in DELTA_PATTERNS:
        match = re.search(pat, text_lower, re.IGNORECASE)
        if match:
            return NegationInstance(text, NegationType.DELTA, match.group().strip(),
                                    "metalinguistic or corrective negation")

    # Check for ε multi-word expressions
    for expr in EPSILON_LEXICON:
        if expr in text_lower:
            return NegationInstance(text, NegationType.EPSILON, expr,
                                    "evaluative negation; encodes speaker stance")

    # Default to τ if a negation token is present
    for tok in NEGATION_TOKENS:
        # "n't" is a suffix ("isn't", "can't"), so there is no word boundary
        # in front of it; a leading \b would never match.
        prefix = "" if tok.startswith("n't") else r"\b"
        if re.search(prefix + re.escape(tok) + r"\b", text_lower):
            return NegationInstance(text, NegationType.TAU, tok,
                                    "truth-conditional negation")

    return None
