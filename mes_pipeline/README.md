# MES extraction pipeline

Rule-based extraction of the **Mayo Endoscopic Score** (grades 0–3) from Turkish free-text endoscopy reports.

Two pipelines are provided:

## 1. `diagnosis_field/` — primary pipeline

Parses the structured **TANI** (diagnosis) line of the endoscopy report. This pipeline is used in **all primary analyses** in the accompanying manuscript.

### Patterns recognised
| Pattern type | Example matches |
|---|---|
| Arabic numerals (0–3) | `MAYO 2`, `Mayo:3` |
| Roman numerals (I–III) | `MAYO II`, `MAYO III` |
| Hyphenated notation | `MAYO-2` |
| Keyword-prefixed | `MAYO SKORU 3`, `Mayo score: 1` |
| Range entries | `MAYO 0–1`, `MAYO 1-2`, `MAYO 2–3` |
| Letter "O" typed for zero | `MAYO O` → normalised to `MAYO 0` |

### Range entries
Range entries are flagged and resolved to a single integer by review of the corresponding narrative findings, **not** silently averaged or rounded.

### Validation (n = 829)
| Metric | Value |
|---|---|
| Quadratic-weighted κ | **0.97** |
| Accuracy (exact agreement) | 92.8% (769/829) |

### Usage
```python
from mes_pipeline.diagnosis_field.extract_mes_tani import extract_mes_from_diagnosis

report_text = "TANI: Ülseratif kolit, Mayo 1"
result = extract_mes_from_diagnosis(report_text)
# {'mes': 1, 'raw_match': 'MAYO 1', 'is_range': False, 'range': None}
```

---

## 2. `narrative_findings/` — exploratory pipeline

Predicts the MES from the free-text **BULGULAR** (findings) section, without access to the diagnosis line. Used as an exploratory benchmark for settings where a structured diagnosis field is unavailable or non-standardised.

### Approach
Rule-based extraction of Turkish endoscopic descriptors mapped to Mayo criteria:
- Ulceration severity (focal vs widespread)
- Vascular pattern (loss / preserved / partially preserved)
- Friability
- Erosions
- Exudate

Terminal ileal findings irrelevant to UC scoring are masked.

### Validation (n = 829)
| Metric | Value |
|---|---|
| Quadratic-weighted κ | 0.66 |
| Accuracy (exact agreement) | 57.8% |
| Agreement within ± 1 grade | 90.6% |
| Binary remission/active accuracy | 80.3% (sens 75.4%, spec 84.1%) |

The reduced performance relative to the diagnosis-field pipeline reflects the intrinsic difficulty of inferring an ordinal score from descriptive narrative text and is consistent with the well-documented inter-observer variability in Mayo scoring (approximately 70–80% exact agreement between trained endoscopists).

### Usage
```python
from mes_pipeline.narrative_findings.extract_mes_bulgular import extract_mes_from_findings

report_text = "BULGULAR: Mukozada eritem, ödem, frajilite, eroziv değişiklikler izlendi."
result = extract_mes_from_findings(report_text)
# {'mes': 2, 'descriptors_found': ['erythema', 'edema', 'friable']}
```

---

## Batch mode
```bash
python -m mes_pipeline.diagnosis_field.extract_mes_tani --input endoscopy.csv --output mes_tani.csv
python -m mes_pipeline.narrative_findings.extract_mes_bulgular --input endoscopy.csv --output mes_bulgular.csv
```
