# Probe sets

Sentences chosen to *test* an open question in `docs/framework.md`, not to
train or check the classifier. They are unlabeled on purpose. Annotate them
with `src/annotate.py` and compare annotators with `--report`.

- `stance_vs_speech_act.txt` — open question 1. Each sentence negates a
  speech act or an assertion (δ in form) in order to perform an evaluative
  stance (ε in function), without correcting anything. If annotators split
  between ε and δ, the two look like independent dimensions; if they agree,
  one is primary.
