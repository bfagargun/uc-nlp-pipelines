# NHI extraction pipeline

Rule-based extraction of the **Nancy Histological Index** (grades 0–4) from Turkish free-text pathology reports.

## How it works

The pipeline executes four deterministic stages:

1. **Report segmentation** — splits the pathology narrative into per-segment biopsy descriptions (rectum, sigmoid, descending, transverse, ascending, caecum). Polypectomy specimens and terminal ileal biopsies are excluded.
2. **Turkish-language preprocessing** — lowercasing, diacritic normalisation, sentence boundary detection (`shared/text_normalisation.py`).
3. **Feature extraction** — three NHI constituent features are extracted by regex layers:
   - **Acute inflammatory infiltrate** (`rules/acute_inflammation.py`) — including cryptitis, crypt abscess, neutrophilic infiltrate of the lamina propria. Graded: absent / mild / moderate / severe.
   - **Chronic inflammatory infiltrate** (`rules/chronic_inflammation.py`) — graded: absent / mild / moderate / severe.
   - **Ulceration / erosion** (`rules/ulceration.py`) — present / absent.
4. **NHI mapping** (`rules/nhi_mapping.py`) — extracted features are deterministically mapped to NHI grades 0–4 per the published Nancy schema (Marchal-Bressenot et al., *Gut* 2017).

## Procedure-level aggregation

Segment-level NHI grades are aggregated to a procedure-level NHI by taking the **maximum** across all evaluable segments, mirroring the convention used by the reference pathologists.

## Usage

```python
from nhi_pipeline.extract_nhi import extract_procedure_nhi

text = """
TANI: Ülseratif kolit aktivasyonu
...
REKTUM BIOPSISI: Mukozada belirgin kronik aktif iltihap...
SIGMOID BIOPSISI: Kronik aktif kolit, ülserasyon (+)...
"""
result = extract_procedure_nhi(text)
# {
#   'procedure_nhi': 4,
#   'segments': {'rektum': 3, 'sigmoid': 4},
#   'features_per_segment': {...},
#   'flags': []
# }
```

## Batch mode

```bash
python -m nhi_pipeline.extract_nhi --input pathology_reports.csv --output nhi_extracted.csv
```

Input CSV should have at minimum two columns: `procedure_id`, `report_text`.

## Validation

See `validation_results/nhi_confusion_matrix.csv` and `notebooks/01_nhi_validation.ipynb`.

| Metric | Value |
|---|---|
| Multi-class κw | 0.87 |
| Multi-class accuracy | 85.6% |
| Macro-F1 | 0.86 |
| Binary (≥ 2 vs 0–1) accuracy | 97.1% |

n = 799 paired procedures; reference standard = blinded gastrointestinal pathologist.
