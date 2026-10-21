"""
patterns.py
Heuristic pattern matching for negation type classification.

Not a complete system — designed as an annotation assist and
demonstration of the framework, not a production classifier.

Checks run in order of markedness: δ first, then ε, then τ as the default
whenever any negation token is present.
"""

import re
from taxonomy import NegationType, NegationInstance

# Pronouns that can open a clause.
_SUBJECT_PRONOUNS = r"(i|we|you|he|she|it|they|there|that|this)"
# ...plus negation, for telling a corrective "not X but Y" (Horn's classic,
# where Y replaces X) from a concessive "but" that starts a new clause
# ("not raining, but it is cold").
_CLAUSE_OPENERS = r"(" + _SUBJECT_PRONOUNS + r"|not|n't)\b"

# ---------------------------------------------------------------- δ ------

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

# Second clauses that are hedges on the first, not restatements of it:
# "The service was not terrible, I suppose." is ε, not a correction.
_PARENTHETICALS = (
    "i suppose", "i think", "i guess", "i mean", "i admit",
    "i believe", "i hope", "i'm afraid", "i'd say",
)

# ---------------------------------------------------------------- ε ------

# Affective/evaluative expressions that suggest ε. Ordered so the reported
# trigger is deterministic when a sentence contains more than one.
EPSILON_LEXICON = (
    "not bad", "not great", "not ideal",
    "not the best", "not terrible", "not thrilled",
    # attitude predicates
    "not a fan", "not loving", "not keen", "not impressed",
    "not crazy about", "not wild about", "n't mind", "n't hate", "not hate",
    # idioms
    "wouldn't say no", "not nothing",
)

# Productive ε constructions, as regexes over the lowercased text.
EPSILON_PATTERNS = [
    # Degree-hedged evaluation: "not too shabby", "not half bad", "not exactly ideal".
    r"\bnot (too|so|that|half|exactly|particularly|especially|entirely|altogether)\b",
    # Negated superlative: "not my finest hour", "not the sharpest tool".
    r"\bnot (my|the|his|her|their|our|your) (\w+est|favou?rite|best|worst|most)\b",
    # Litotes over a negative-prefixed adjective: "not unpleasant", "wasn't impossible".
    r"(\bnot|n't) (unpleasant|unreasonable|uncommon|unhappy|unkind|unwelcome|"
    r"unattractive|unimpressive|impossible|insignificant)\b",
]

# ---------------------------------------------------------------- τ ------

# Ordered so that the reported trigger is deterministic when several appear.
# Multi-word tokens come first so "no one" is reported rather than just "no".
NEGATION_TOKENS = (
    "no one",
    "not", "n't", "cannot", "no", "never", "neither", "nor",
    # negative quantifiers / pronouns
    "nothing", "nobody", "none", "nowhere",
)


def find_negation_token(text_lower: str) -> str | None:
    """Return the first negation token present in the text, or None."""
    for tok in NEGATION_TOKENS:
        # "n't" is a suffix ("isn't", "can't"), so there is no word boundary
        # in front of it; a leading \b would never match.
        prefix = "" if tok.startswith("n't") else r"\b"
        if re.search(prefix + re.escape(tok) + r"\b", text_lower):
            return tok
    return None


def _corrective_restatement(text_lower: str) -> str | None:
    """
    Detect asyndetic correction, the commonest shape of Horn's metalinguistic
    negation: a negated clause, a comma or dash, then a subject-led clause
    that restates it on a stronger or different term and contains no
    negation of its own.

        "I'm not hungry, I'm starving."
        "That's not a bug, that's a feature."

    Returns the negated first clause as the trigger, or None.
    """
    parts = re.split(r"[,;—–]|\s-\s", text_lower, maxsplit=1)
    if len(parts) != 2:
        return None
    first, second = parts[0].strip(), parts[1].strip()
    if find_negation_token(first) is None or find_negation_token(second) is not None:
        return None
    if not re.match(_SUBJECT_PRONOUNS + r"\b", second):
        return None
    if second.startswith(_PARENTHETICALS):
        return None
    return first


def _match_delta_pattern(text_lower: str) -> str | None:
    for pat in DELTA_PATTERNS:
        match = re.search(pat, text_lower, re.IGNORECASE)
        if match:
            return match.group().strip()
    return None


def _match_epsilon_lexicon(text_lower: str) -> str | None:
    for expr in EPSILON_LEXICON:
        if expr in text_lower:
            return expr
    return None


def _match_epsilon_pattern(text_lower: str) -> str | None:
    for pat in EPSILON_PATTERNS:
        match = re.search(pat, text_lower)
        if match:
            return match.group()
    return None


# The classifier, as an ordered list of stages. The first stage whose matcher
# returns a trigger decides the type. Order encodes markedness: δ cues beat
# ε cues, and any leftover negation token is τ.
Stage = tuple  # (name, NegationType, matcher, rationale)
STAGES: tuple[Stage, ...] = (
    ("δ pattern", NegationType.DELTA, _match_delta_pattern,
     "metalinguistic or corrective negation"),
    ("δ restatement", NegationType.DELTA, _corrective_restatement,
     "corrective restatement; the second clause replaces the first"),
    ("ε lexicon", NegationType.EPSILON, _match_epsilon_lexicon,
     "evaluative negation; encodes speaker stance"),
    ("ε construction", NegationType.EPSILON, _match_epsilon_pattern,
     "evaluative negation; hedged or understated stance"),
    ("τ token", NegationType.TAU, find_negation_token,
     "truth-conditional negation"),
)


def fire(text: str) -> list[tuple[str, NegationType, str]]:
    """
    Run every stage and return all that match, as (stage name, type, trigger),
    in stage order. classify() takes the first; this exposes the rest so the
    ordering decision can be audited (see audit.py).
    """
    text_lower = text.lower()
    hits = []
    for name, neg_type, matcher, _ in STAGES:
        trigger = matcher(text_lower)
        if trigger:
            hits.append((name, neg_type, trigger))
    return hits


def classify(text: str) -> NegationInstance | None:
    text_lower = text.lower()
    for _, neg_type, matcher, rationale in STAGES:
        trigger = matcher(text_lower)
        if trigger:
            return NegationInstance(text, neg_type, trigger, rationale)
    return None
