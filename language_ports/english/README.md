# English-language adaptation template

**Status: proof-of-concept / adaptation template — NOT independently validated.**

This folder is a companion to the validated Turkish-language NLP pipeline
described in [manuscript citation]. It exists to help centres with
English-language endoscopy and pathology reporting adapt the same
**rule-based architecture** to their own reports, and to document the
adaptation process transparently.

## What this is

- A line-by-line translation of the *rule categories and grading logic*
  from the locked, validated Turkish rule set into English, using
  terminology drawn from the published Nancy Histological Index
  descriptors (Marchal-Bressenot et al., *Gut* 2017) and standard Mayo
  Endoscopic Score conventions.
- Tested against a small set of **hand-written synthetic example
  sentences** (`example_reports_en.py`) to confirm the rules fire as
  intended on clearly-worded text.

## What this is NOT

- **Not validated on real English-language reports.** No pathologist- or
  endoscopist-scored English cohort was used to tune or test these
  rules. The kappa/accuracy figures reported in the manuscript apply
  only to the Turkish pipeline on the Turkish cohort (n = 830 procedures,
  see Table 4).
- **Not a drop-in tool.** Reporting conventions vary substantially
  between centres, pathologists, and countries — including within
  English-language reporting. Site-segmentation conventions, hedging
  language, and negation phrasing in particular are known to differ (see
  below).

## A finding from building this template

While translating the rule set we found a concrete difference in
reporting style: in the original Turkish cohort, pathologists almost
never explicitly negate a finding (e.g. writing the equivalent of "no
crypt abscess" or "no active inflammation" when a feature is simply
absent) — the corresponding negation rule fired 0 times across the
entire cohort (Supplementary Table S2 in the manuscript). Hand-written
English example sentences, by contrast, very commonly use explicit
negation ("no ulceration identified", "no active inflammation"). Early
versions of this template pipeline mis-graded such reports upward
because the underlying keyword ("ulceration", "active", "crypt
abscess") was present in a negated sentence. We added explicit negation
guards for this reason (see `RE_NEG_*` patterns).

This is exactly the kind of centre- and language-specific reporting
convention that requires local, blinded validation before deployment —
it is not something that can be assumed to generalise from one
language, or even one centre, to another.

## How to validate this for your own centre

Follow the same process described in the manuscript (Methods 2.3–2.4):

1. Draft/adapt rules against a **development set** of your own
   de-identified reports, working with a pathologist and/or
   gastroenterologist to encode your local reporting terminology.
2. Refine rules by **error-driven development** against a
   blinded reference standard (independent pathologist/endoscopist
   re-scoring), reviewing confusion-matrix error cells.
3. Lock the rule set and evaluate on a **temporally independent
   held-out set** collected after rule-locking, to check for
   over-fitting (see Supplementary Table S2 for the per-rule
   provenance-audit approach used in the original study).
4. Report quadratic-weighted Cohen's kappa and accuracy against the
   blinded reference standard, both overall and for the operationally
   relevant binary activity/remission classification.

## Files

| File | Purpose |
|---|---|
| `nhi_pipeline_en.py` | English adaptation of the Nancy Histological Index rule-based pipeline |
| `mes_pipeline_en.py` | English adaptation of the diagnosis-field Mayo Endoscopic Score pipeline |
| `example_reports_en.py` | Synthetic example reports used to sanity-check the two pipelines above |

Run either pipeline's demo directly:

```bash
python3 nhi_pipeline_en.py
python3 mes_pipeline_en.py
```

## Contributing external validation results

If you validate this template (or your own adaptation of it) on a
local English-language cohort, we would welcome hearing about your
results — see the corresponding author contact in the manuscript, or
open an issue/pull request on this repository. External validation
across centres and languages is the intended next step for this line
of work.
