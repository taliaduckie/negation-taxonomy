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

## Annotation Guidelines

Tag each negation instance with:
- Primary type (τ/ε/δ)
- Trigger token or expression
- Scope boundaries (for τ)
- Whether the negation cancels a presupposition (δ-subtype)
