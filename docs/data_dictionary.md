# Data dictionary

This document defines the variables used by the pipelines and the validation
notebooks. Use it as a contract when running the pipelines on a new dataset.

## Pathology input — required columns

| Column | Type | Description |
|---|---|---|
| `procedure_id` | str / int | Unique identifier of the endoscopic procedure. |
| `report_text` | str | Full free-text pathology report (Turkish). |

## Endoscopy input — required columns

| Column | Type | Description |
|---|---|---|
| `procedure_id` | str / int | Unique identifier of the endoscopic procedure. |
| `diagnosis_text` | str | Content of the `TANI` field. |
| `findings_text` | str | Content of the `BULGULAR` field (only needed for the exploratory pipeline). |

## Output of `extract_procedure_nhi`

| Key | Type | Description |
|---|---|---|
| `procedure_nhi` | int (0–4) or None | Procedure-level NHI = max of evaluable segment NHIs. |
| `segments` | dict[str, int] | Segment name → segment NHI. |
| `features_per_segment` | dict[str, dict] | Segment name → {acute, chronic, ulceration}. |
| `flags` | list[str] | Quality flags (e.g. `no_evaluable_segments`). |

## Output of `extract_mes_from_diagnosis`

| Key | Type | Description |
|---|---|---|
| `mes` | int (0–3) or None | Single integer MES if extracted; None if range or no match. |
| `raw_match` | str | The substring that matched. |
| `is_range` | bool | True if the report records a range (e.g. `MAYO 1-2`). |
| `range` | tuple[int, int] or None | The captured range, if any. |

## Reference variables (for validation)

| Variable | Used as reference for |
|---|---|
| `nancy_index_cagatay` | Reference-standard NHI (gastrointestinal pathologist 2) |
| `nancy_index_burce` | Independent NHI (pathologist 1), used for inter-pathologist agreement only |
| `mayo_score_classified` | Reference-standard endoscopist-assigned integer MES |

## Histologic / endoscopic remission thresholds

| Concept | Definition |
|---|---|
| Histologic remission | NHI ≤ 1 |
| Histologic activity | NHI ≥ 2 |
| Hidden histologic activity | NHI ≥ 2 in a procedure with endoscopic remission (MES ≤ 1) |
| Endoscopic remission | MES ≤ 1 |
| Endoscopic activity | MES ≥ 2 |
