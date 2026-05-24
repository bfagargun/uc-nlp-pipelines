# How to publish this repo to GitHub

This document is for the repository maintainer (Besim). Delete it before making the repo public if you prefer.

## Step 1 — create the empty repo on GitHub

Go to https://github.com/new and create a new **empty** repository:

- **Name:** `uc-nlp-pipelines`
- **Description:** *"Rule-based NLP for Nancy Histological Index and Mayo Endoscopic Score extraction from Turkish free-text reports (ulcerative colitis)."*
- **Visibility:** Public
- **Do NOT** initialise with a README, .gitignore, or license (this folder already has them).

## Step 2 — push this folder

```bash
cd uc-nlp-pipelines/

# replace any placeholder files with your live code (see below)

git init
git add .
git commit -m "Initial release accompanying the UC NLP manuscript (v1.0-manuscript)"
git branch -M main
git remote add origin https://github.com/bfagargun/uc-nlp-pipelines.git
git push -u origin main

# tag the locked rule set as used in the manuscript
git tag -a v1.0-manuscript -m "Locked rule sets used in the manuscript validation"
git push origin v1.0-manuscript
```

## Step 3 — replace placeholders with your live code

The following files are scaffolds and must be replaced with the actual code from your local pipeline before the repo is publishable. Each raises `NotImplementedError` to make this obvious.

- `nhi_pipeline/extract_nhi.py`
  - `segment_report()`
  - `extract_features_for_segment()`
- `nhi_pipeline/rules/acute_inflammation.py` — `grade_acute()`
- `nhi_pipeline/rules/chronic_inflammation.py` — `grade_chronic()`
- `nhi_pipeline/rules/ulceration.py` — `has_ulceration()`
- `mes_pipeline/diagnosis_field/extract_mes_tani.py` — `extract_mes_from_diagnosis()`
- `mes_pipeline/narrative_findings/extract_mes_bulgular.py` — `extract_mes_from_findings()`

The `rules/nhi_mapping.py` file (deterministic Nancy schema) is **not** a placeholder — it is the canonical mapping and can be used as is.

## Step 4 — fill in manuscript link

Once the paper is accepted / a DOI is assigned, update:

- `README.md` — the citation block under "If you use this code, please cite the manuscript above."
- `CITATION.cff` — the `preferred-citation.journal` and add `doi:` field.

## Step 5 — add a Zenodo DOI (optional but recommended for journals)

Many IBD journals expect software cited in a manuscript to have a DOI. After the repo is public:
1. Sign in at https://zenodo.org with your GitHub account
2. Enable the `uc-nlp-pipelines` repo in the Zenodo GitHub integration
3. Create a GitHub release matching the `v1.0-manuscript` tag — Zenodo will mint a DOI automatically
4. Add the DOI badge to the top of `README.md`

## Step 6 — link from the manuscript

The manuscript currently has two `[HOCAM: GitHub URL]` placeholders (Methods 2.3 and 2.4). Replace both with:

```
https://github.com/bfagargun/uc-nlp-pipelines
```

(or the Zenodo DOI for the locked tagged release, which is preferable for archival citation).
