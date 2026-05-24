# NHI mapping schema

Based on Marchal-Bressenot A, Salleron J, Boulagnon-Rombi C, et al.
*Development and validation of the Nancy histological index for UC.*
Gut. 2017;66(1):43–49.

| Grade | Definition |
|---|---|
| **0** | No histologically significant disease — normal mucosa, no chronic inflammatory infiltrate, no acute inflammation, no ulceration. |
| **1** | Chronic inflammatory infiltrate present, but **no** acute inflammatory cells. |
| **2** | **Mild** acute inflammatory cell infiltrate of the lamina propria. |
| **3** | **Moderate-to-severe** acute inflammatory cell infiltrate of the lamina propria, with or without cryptitis / crypt abscess. |
| **4** | **Ulceration / erosion** present, regardless of inflammatory grade. |

## Decision tree as implemented in the pipeline

```
IF ulceration:
    grade = 4
ELIF acute >= moderate:
    grade = 3
ELIF acute == mild:
    grade = 2
ELIF chronic >= mild:
    grade = 1
ELSE:
    grade = 0
```

Note: in routine adult UC pathology practice, a finding of fully normal mucosa (grade 0) is uncommon, because some baseline chronic inflammatory infiltrate typically remains even in deep remission. Grade 0 was absent from our cohort.

## Procedure-level aggregation

```
procedure_NHI = max(segment_NHI for segment in evaluable_segments)

Excluded segments:
    - terminal ileum
    - polypectomy specimens
```

## Histologic remission threshold

For binary analyses, **NHI 0–1 = histologic remission** (no acute inflammation, no ulceration). **NHI ≥ 2 = histologic activity**.
