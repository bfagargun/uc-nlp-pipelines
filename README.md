# uc-nlp-pipelines

Rule-based natural language processing pipelines for the automated extraction of the **Nancy Histological Index (NHI)** from free-text pathology reports and the **Mayo Endoscopic Score (MES)** from free-text endoscopy reports, in Turkish, for ulcerative colitis (UC).

This repository accompanies the manuscript:

> **Hidden histologic activity in endoscopic remission and the histologic dissociation of Mayo 0 and Mayo 1 strata: a real-world ulcerative colitis cohort enabled by NLP-based automated pathology grading.**
> Ağargün BF, Işık B, Kızıltaş C, Güner AÇ, et al. (submitted, 2026).

If you use this code, please cite the manuscript above.

---

## Overview

The repository contains two independent, deterministic, rule-based pipelines:

### 1. `nhi_pipeline/`
Extracts the **Nancy Histological Index** (grades 0–4) from Turkish free-text pathology reports. Operates at segment level (per biopsied colon segment) and aggregates to procedure level by taking the maximum across evaluable segments. Polypectomy specimens and terminal ileal biopsies are excluded by design.

### 2. `mes_pipeline/`
Extracts the **Mayo Endoscopic Score** (grades 0–3) from Turkish free-text endoscopy reports. Two variants are provided:

- **`diagnosis_field/`** — parses the structured diagnosis (`TANI`) line. Primary pipeline used in all manuscript analyses.
- **`narrative_findings/`** — exploratory pipeline that predicts the MES from the free-text findings (`BULGULAR`) section, without access to the diagnosis line.

---

## Validation summary (from the accompanying manuscript)

### NHI pipeline (against blinded reference pathologist, n = 799 procedures)
| Metric | Value |
|---|---|
| Quadratic-weighted Cohen's κ (multi-class) | **0.87** |
| Overall accuracy (multi-class) | 85.6% |
| Macro-F1 (multi-class) | 0.86 |
| Inter-pathologist κw (human ceiling) | 0.99 |
| Binary (NHI ≥ 2 vs NHI 0–1) accuracy | **97.1%** |
| Binary simple Cohen's κ | 0.89 |
| Binary sensitivity / specificity | 98.5% / 89.3% |
| Binary PPV / NPV | 98.1% / 91.5% |

### MES pipeline — diagnosis field (against endoscopist-assigned integer MES, n = 829)
| Metric | Value |
|---|---|
| Quadratic-weighted Cohen's κ | **0.97** |
| Accuracy (exact agreement) | 92.8% (770/829) |

### MES pipeline — blind narrative findings (exploratory, n = 829)
| Metric | Value |
|---|---|
| Quadratic-weighted Cohen's κ | 0.66 |
| Accuracy (exact agreement) | 57.8% |
| Agreement within ± 1 grade | 90.6% |
| Binary remission/active accuracy | 80.3% |

---

## Repository structure

```
uc-nlp-pipelines/
├── README.md                       <- this file
├── LICENSE                         <- MIT
├── CITATION.cff                    <- machine-readable citation
├── requirements.txt
├── .gitignore
│
├── nhi_pipeline/
│   ├── README.md
│   ├── extract_nhi.py              <- main entry point
│   ├── rules/
│   │   ├── acute_inflammation.py
│   │   ├── chronic_inflammation.py
│   │   ├── ulceration.py
│   │   └── nhi_mapping.py
│   ├── preprocessing.py
│   └── tests/
│       └── test_extract_nhi.py
│
├── mes_pipeline/
│   ├── README.md
│   ├── diagnosis_field/
│   │   ├── extract_mes_tani.py     <- main entry point (primary pipeline)
│   │   └── rules/
│   │       └── mes_patterns.py
│   ├── narrative_findings/
│   │   ├── extract_mes_bulgular.py <- exploratory pipeline
│   │   └── rules/
│   │       └── descriptor_patterns.py
│   └── tests/
│       └── test_extract_mes.py
│
├── shared/
│   ├── text_normalisation.py       <- shared Turkish-language preprocessing
│   └── segment_split.py
│
├── language_ports/
│   └── english/                    <- English adaptation template (NOT independently validated)
│       ├── README.md
│       ├── nhi_pipeline_en.py
│       ├── mes_pipeline_en.py
│       └── example_reports_en.py
│
├── notebooks/
│   ├── 01_nhi_validation.ipynb
│   ├── 02_mes_validation.ipynb
│   └── 03_concordance_analysis.ipynb
│
├── validation_results/
│   ├── nhi_confusion_matrix.csv
│   ├── mes_tani_confusion_matrix.csv
│   ├── mes_bulgular_confusion_matrix.csv
│   └── summary_metrics.json
│
└── docs/
    ├── nhi_schema.md               <- mapping rules from features to NHI grade
    ├── mes_schema.md               <- mapping rules to MES grade
    └── data_dictionary.md          <- variable definitions
```

---

## Quick start

```bash
git clone https://github.com/bfagargun/uc-nlp-pipelines.git
cd uc-nlp-pipelines
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Extract NHI from a single pathology report
```python
from nhi_pipeline.extract_nhi import extract_procedure_nhi

report_text = open("example_pathology_report.txt").read()
result = extract_procedure_nhi(report_text)
print(result)
# {'procedure_nhi': 3, 'segments': {'rektum': 3, 'sigmoid': 2, ...},
#  'features': {...}, 'flags': []}
```

### Extract MES from a single endoscopy report
```python
from mes_pipeline.diagnosis_field.extract_mes_tani import extract_mes_from_diagnosis

report_text = open("example_endoscopy_report.txt").read()
result = extract_mes_from_diagnosis(report_text)
print(result)
# {'mes': 1, 'raw_match': 'MAYO 1', 'is_range': False}
```

### Run on a batch
```bash
python -m nhi_pipeline.extract_nhi --input data/pathology.csv --output out/nhi.csv
python -m mes_pipeline.diagnosis_field.extract_mes_tani --input data/endoscopy.csv --output out/mes.csv
```

---

## Reproducing the manuscript analyses

The notebooks in `notebooks/` reproduce the manuscript's validation tables and figures from a confidential cohort of 830 procedures (499 patients). The de-identified individual-level dataset cannot be released for data-protection reasons; however, the rule sets are fully released here, and the notebooks can be re-run on any institutional dataset structured in the same way (see `docs/data_dictionary.md`).

Aggregate validation outputs that *can* be shared (confusion matrices, summary metrics) are checked into `validation_results/`.

---

## Limitations and portability

- **Language-specific.** Regex rules target Turkish source text. Porting to another language requires re-specifying the regex layer; the NHI / MES schemas themselves are language-independent.
- **Template-specific.** Rules were calibrated on reports from a single tertiary IBD referral centre. External validation in other centres is encouraged before clinical deployment elsewhere.
- **Rule-based, not learned.** No supervised model weights, no statistical training. All decisions are deterministic and inspectable. This is a design choice for transparency.

---

## English-language adaptation template

`language_ports/english/` contains an **English-language adaptation template** that re-implements the same rule architecture (segment splitting → hierarchical grading → procedure-level aggregation) using terminology drawn from the published Nancy Histological Index descriptors and standard Mayo Endoscopic Score conventions.

**This template is a proof-of-concept, not a validated pipeline.** It has been checked only against a small set of hand-written synthetic example sentences; it has not been evaluated against a pathologist- or endoscopist-scored English cohort. See `language_ports/english/README.md` for full details, including a documented reporting-convention difference (explicit negation phrasing) discovered while building the template — a concrete illustration of why local, blinded validation is required before adapting these rules to a new language or centre.

Centres with English-language reports are welcome to use this as a starting point and to contribute validation results back via pull request (see Contributing, below).

---

## Locked rule set

The rule sets used in the manuscript validation are tagged as **`v1.0-manuscript`** in this repository. Any subsequent edits to the rules will not affect the validation reported in the paper.

```bash
git checkout v1.0-manuscript
```

---

## Contributing

External pull requests are welcome for:
- Bug fixes in regex rules,
- Additional language ports (e.g. English, Spanish, Arabic) — see `language_ports/english/` for an example port and validation checklist,
- New histologic-index extensions (e.g. Robarts Histopathology Index).

Please open an issue to discuss methodological changes before submitting a PR.

---

## License

MIT — see `LICENSE`.

## Contact

Besim Fazıl Ağargün, MD
Department of Gastroenterohepatology
Istanbul University, Istanbul Faculty of Medicine
bfagargun@istanbul.edu.tr

## Acknowledgements

Independent histopathologic re-scoring used as the reference standard was performed by Burce Işık and Alper Çağatay Güner.
