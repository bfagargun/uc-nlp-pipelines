# NHI extraction pipeline

Rule-based extraction of the **Nancy Histological Index** (grades 0–4) from Turkish free-text pathology reports.

## How it works

1. **Text normalisation** (`shared/text_normalisation.py`) — uppercasing and Turkish diacritic folding (İ/Ü/Ö/Ç/Ş/Ğ -> ASCII), whitespace collapse.
2. **Report segmentation** (`extract_nhi.py::split_segments`) — splits the normalised report at roman/arabic-numeral biopsy-site markers (e.g. `I-`, `1)`). Segments are positional (`segment_1`, `segment_2`, ...); the report text itself, not the segmentation step, records which colon site each segment corresponds to.
3. **Per-segment grading** (`extract_nhi.py::grade_segment`) — a single hierarchical, rule-priority decision tree, evaluated top-down: ulceration (grade 4, unless negated or in an excluded polyp/terminal-ileum context) → severe/crypt-abscess/basal-plasmacytosis markers (grade 3) → active inflammation (grade 2) → chronic inflammation (grade 1) → normal (grade 0). It draws its regex constants from `rules/ulceration.py`, `rules/acute_inflammation.py`, `rules/chronic_inflammation.py`, and `rules/exclusions.py`.
4. **Procedure-level aggregation** — the procedure-level NHI is the **maximum** grade across all segments (`extract_nhi.py::classify_report` / `extract_procedure_nhi`).

This is a single deterministic function per segment, not a "score three sub-features independently, then map to a grade" pipeline — see the note on `rules/nhi_mapping.py` below.

## Usage

```python
from nhi_pipeline.extract_nhi import extract_procedure_nhi

text = """
I- REKTUM: Mukozada belirgin kronik aktif iltihap...
II- SIGMOID: Kronik aktif kolit, ulserasyon izlendi...
"""
result = extract_procedure_nhi(text)
# {
#   'procedure_nhi': 4,
#   'segments': {'segment_1': 2, 'segment_2': 4},
#   'flags': []
# }
```

## Batch mode

```bash
python -m nhi_pipeline.extract_nhi --input pathology_reports.csv --output nhi_extracted.csv
```

Input CSV should have at minimum two columns: `procedure_id`, `report_text`.

## Validation

See `validation_results/nhi_confusion_matrix.csv`, `notebooks/Mayo_Nancy_NLP_Analysis_v3.ipynb` (development validation) and `notebooks/NHI_heldout_validation.ipynb` (temporal held-out validation + per-rule provenance audit).

**Note on `rules/nhi_mapping.py`:** that file documents the canonical Nancy grade definitions (Marchal-Bressenot et al.) as a *reference table*. The actual implemented decision tree in `extract_nhi.py::grade_segment()` is a single hierarchical rule-priority function (ported verbatim from the validated notebook) rather than a two-step "score sub-features, then map to grade" pipeline — it does not import or call `nhi_mapping.py`. Both describe the same grade semantics; only `grade_segment()` is what actually ran to produce the manuscript's validation numbers.

| Metric | Value |
|---|---|
| Multi-class κw | 0.87 |
| Multi-class accuracy | 85.6% |
| Macro-F1 | 0.86 |
| Binary (≥ 2 vs 0–1) accuracy | 97.1% |

n = 799 paired procedures; reference standard = blinded gastrointestinal pathologist.
