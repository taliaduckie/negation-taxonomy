# τ/ε/δ Negation Framework — Extended Notes

## Motivation

Standard NLP treatments of negation focus on scope and truth conditions (τ).
But natural language negation is richer:

- "Not bad" does not mean "bad is false" — it performs a positive evaluation
  with distancing. This is ε.
- "I didn't say she *stole* it" doesn't negate the proposition about theft
  — it corrects the conversational record. This is δ (Horn's metalinguistic
  negation).

## Theoretical Grounding

- **τ**: Frege, Russell, standard compositional semantics
- **ε**: Expressivism (Gibbard, Blackburn); scalar evaluative language
- **δ**: Horn (1985, 1989) — metalinguistic negation; Gricean maxim
  exploitation; Sperber & Wilson relevance theory

## Open Questions

1. Is ε a subtype of δ, or a genuinely independent dimension?
2. How does prosody interact with type assignment? (Focus stress on "NOT" vs
   "not" suggests different types in spoken language)
3. Does "Fine" in affirmative non-compliance (e.g. "Fine, I'll do it") belong
   to δ — negating the implicature of willingness — or is it a separate class?

## Evidence from the Example Set

`python src/audit.py --hard` runs every example through every rule, not just
the first that fires, so the stage ordering in `patterns.py` can be checked
against the data rather than asserted.

On the current 104 sentences, 4 are decided by ordering alone:

- 3 are labeled δ and carry an ε cue as well: "not bad" inside "Not bad —
  actually, it's excellent", and the degree-hedge reading of "not that"
  inside "It's not that I don't care". In each the δ reading is clearly
  right, which supports δ-before-ε. It also shows that the ε cue is
  *present*: the correction is built on top of an evaluative negation. That
  is weak evidence for open question 1 in the direction of ε being a layer
  δ can operate on, rather than a sibling.
- 1 is labeled τ and misfires as δ: "She did not attend the meeting, she was
  sick" has the surface shape of a corrective restatement but is causal.
  This is the known cost of the restatement heuristic (see
  `data/examples/hard/tau.txt`).

No sentence in the set has an ε cue and a δ cue that point to *different*
plausible readings, so the data does not yet discriminate between "ε is a
subtype of δ" and "ε and δ are independent". Sentences that would: an
evaluative hedge that is *not* also a correction but still carries a δ cue,
or a correction with no evaluative content at all that the ε rules catch.

## Annotation Guidelines

Tag each negation instance with:
- Primary type (τ/ε/δ)
- Trigger token or expression
- Scope boundaries (for τ)
- Whether the negation cancels a presupposition (δ-subtype)
