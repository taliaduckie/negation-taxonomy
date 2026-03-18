# Negation Taxonomy: τ, ε, δ

A framework for classifying negation in natural language beyond the
syntactic/semantic binary. Distinguishes:

- **τ (truth-conditional negation)** — logical NOT; reverses truth value
- **ε (expressive/evaluative negation)** — speaker attitude, not truth reversal
- **δ (discourse negation)** — metalinguistic, corrective, or presupposition-canceling

Motivated by the observation that "Fine" in "Fine, I'll do it" is not truth-
conditionally equivalent to its uninverted form — it's performing something
closer to δ: negating the implicature of willingness, not the proposition.

## Usage

```bash
pip install -r requirements.txt
python src/classify.py --text "Not bad."
python src/classify.py --text "I didn't say she STOLE the money."
```

## Framework

| Type | Symbol | Core property | Example |
|------|--------|---------------|---------|
| Truth-conditional | τ | Reverses truth value | "It is not raining." |
| Expressive | ε | Encodes speaker stance | "That's not great." |
| Discourse | δ | Corrects or cancels | "I didn't say she *stole* it." |

## Project Structure
```
negation-taxonomy/
├── src/
│   ├── classify.py      # CLI classifier
│   ├── patterns.py      # rule-based pattern matching
│   └── types.py         # dataclass definitions
├── data/
│   └── examples/        # annotated example sentences per type
└── docs/
    └── framework.md     # extended theoretical notes
```
