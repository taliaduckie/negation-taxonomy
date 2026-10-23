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

### Minimal pairs

`epsilon.txt` and `delta.txt` contain seven minimal pairs: an ε hedge on its
own, and the same hedge upgraded into a correction.

| ε | δ |
|---|---|
| It's not too hot in here. | It's not too hot, it's too cold. |
| I'm not thrilled. | I'm not thrilled, I'm ecstatic. |
| Not exactly. | Not exactly — more like a disaster. |
| That's not great. | That's not great, that's catastrophic. |

On the current 120 sentences, 10 are decided by stage ordering. Nine are
labeled δ and also carry an ε cue; the ε cue is the hedge the correction is
built on. In every one the δ reading is clearly right, so δ-before-ε holds.
The tenth is the known causal-comma false positive, "She did not attend the
meeting, she was sick" (see `data/examples/hard/tau.txt`).

### What this says about open question 1

Every ε-and-δ collision in the data runs the same way: an evaluative
negation is present, and a second clause or dash retracts or upgrades it.
There is no sentence where a δ cue is present and the ε reading should win.
That is consistent with ε being a layer δ can operate on, and says nothing
either way about ε being a *subtype* of δ, since pure-ε sentences ("Not
bad.") and pure-δ sentences ("I didn't say she stole it.") both exist and
neither needs the other.

The sentence that would actually press the question is one like

> I'm not saying it's bad.

It negates a speech act (δ in form) in order to perform a stance (ε in
function), and the two readings are not a correction built on a hedge; they
are the same negation described at two levels. It is deliberately *not* in
the example files, because labeling it would decide the question rather
than test it.

Twenty such sentences are in `data/probe/stance_vs_speech_act.txt`. Label
them with `python src/annotate.py <file> --annotator <name>` and compare
annotators with `--report`, which gives raw agreement and Cohen's kappa. If
annotators split between ε and δ, the dimensions look independent; if they
agree, one is primary. The report also shows the rule-based prediction per
sentence; on this set it says τ for most of them, which is itself a finding:
the rules have no cue for stance performed through a negated speech act.

### Known heuristic costs

- `not too X to VERB` is literal degree, not a hedge: "not too deep to wade
  in" is τ. The ε degree pattern now excludes it.
- A fragment restatement with no subject pronoun ("Not my favorite — my
  least favorite, if anything") is δ but the restatement rule cannot see it.
  It lives in `hard/delta.txt`.

## Annotation Guidelines

Tag each negation instance with:
- Primary type (τ/ε/δ)
- Trigger token or expression
- Scope boundaries (for τ)
- Whether the negation cancels a presupposition (δ-subtype)
