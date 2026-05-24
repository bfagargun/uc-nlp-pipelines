# MES mapping schema

Based on Schroeder KW, Tremaine WJ, Ilstrup DM. *Coated oral 5-aminosalicylic acid therapy for mildly to moderately active ulcerative colitis.* N Engl J Med. 1987;317(26):1625–1629.

| Grade | Definition |
|---|---|
| **0** | Normal or inactive disease — intact vascular pattern, no friability, no erosion. |
| **1** | Mild disease — erythema, decreased vascular pattern, mild friability. |
| **2** | Moderate disease — marked erythema, absent vascular pattern, friability, erosions. |
| **3** | Severe disease — spontaneous bleeding, frank ulceration. |

## Endoscopic remission threshold

Per STRIDE-II (Turner et al., *Gastroenterology* 2021), endoscopic remission is operationalised as **MES 0–1**. Endoscopic activity is **MES ≥ 2**.

> The accompanying manuscript demonstrates that this MES 0–1 grouping conflates two histologically distinct populations (Mayo 0 vs Mayo 1), and discusses the implications for treat-to-target monitoring.

## Pipeline 1 — diagnosis-field extraction

Operates on the structured `TANI` line of the endoscopy report. Matches:
- Integer notation (`MAYO 2`, `Mayo:3`)
- Roman numerals (`MAYO II`)
- Hyphenated notation (`MAYO-2`)
- Keyword-prefixed (`MAYO SKORU 3`)
- Range entries (`MAYO 0-1`, `MAYO 1-2`, `MAYO 2-3`)
- Letter-`O`-for-zero typos (`MAYO O` → `MAYO 0`)

Range entries are not silently averaged — they are flagged and either resolved by review of the narrative findings or excluded from analyses that require an integer.

## Pipeline 2 — blind narrative-findings extraction (exploratory)

Predicts MES from the `BULGULAR` section only. Descriptor → MES mapping:

| Descriptors | MES |
|---|---|
| Normal mucosa, normal vascular pattern | 0 |
| Mild erythema, decreased vascular pattern, mild friability | 1 |
| Marked erythema, absent vascular pattern, friability, erosions, focal ulcers | 2 |
| Spontaneous bleeding, frank / widespread / deep ulceration | 3 |

Terminal ileal findings are masked, as they are not part of UC scoring.
