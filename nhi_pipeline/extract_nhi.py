"""
NHI extraction pipeline — main entry point.

REAL, LOCKED PIPELINE — ported verbatim from
notebooks/Mayo_Nancy_NLP_Analysis_v3.ipynb (cells 11, 13, 17), which is the
exact code used to produce the manuscript's NHI validation results
(kappa_w = 0.87, 95% CI 0.83-0.90; accuracy 85.6%; n = 799; see Table 4).

This file replaces an earlier placeholder scaffold that raised
NotImplementedError. See CHANGELOG / PR history for details.

Segmentation: reports are split at roman/arabic-numeral biopsy-site markers
(e.g. "I-", "1)"), matching the convention used in this centre's pathology
reports. Segments are NOT named by organ in the underlying algorithm (the
report text itself names the site within each segment); procedure-level NHI
is the maximum grade among evaluable segments, excluding polypectomy
specimens and terminal-ileal biopsies.

CLI:
    python -m nhi_pipeline.extract_nhi --input <csv> --output <csv>
"""

from __future__ import annotations
import argparse
from typing import Optional

from shared.text_normalisation import normalize
from nhi_pipeline.rules.ulceration import RE_ULCER, RE_NEG_ULCER
from nhi_pipeline.rules.acute_inflammation import (
    RE_CRYPT_ABS, RE_BASAL_PL, RE_SEV_ACTIVE, RE_ACTIVE, RE_MILD,
)
from nhi_pipeline.rules.chronic_inflammation import RE_CHRONIC, RE_NORMAL
from nhi_pipeline.rules.exclusions import RE_POLYP, RE_ILEUM

import re

_SEGMENT_SPLIT = re.compile(r'(?:^|\s)(?:I{1,4}V?|VI{0,3}|[0-9]+)[\-\)]\s*')


def split_segments(normalized_text: str) -> list[str]:
    """Split a normalized report into per-biopsy-site segments."""
    segs = re.split(_SEGMENT_SPLIT, normalized_text)
    segs = [s.strip() for s in segs if s.strip()]
    return segs if segs else [normalized_text]


def grade_segment(seg: str) -> int:
    """Deterministic hierarchical NHI grading for a single segment (0-4)."""
    is_polyp = bool(RE_POLYP.search(seg))
    is_ileum = bool(RE_ILEUM.search(seg))

    if (RE_ULCER.search(seg) and not RE_NEG_ULCER.search(seg)
            and not is_polyp and not is_ileum):
        return 4

    has_abs = bool(RE_CRYPT_ABS.search(seg))
    has_basal = bool(RE_BASAL_PL.search(seg))
    has_sev = bool(RE_SEV_ACTIVE.search(seg))
    has_active = bool(RE_ACTIVE.search(seg))
    has_mild = bool(RE_MILD.search(seg))

    if has_sev:
        return 3
    if has_abs and has_active and not has_mild:
        return 3
    if has_basal and has_active and not has_mild:
        return 3
    if has_abs and not is_polyp:
        return 3
    if has_active:
        return 2
    if RE_CHRONIC.search(seg) or 'ILTIHAP' in seg:
        return 1
    if RE_NORMAL.search(seg):
        return 0
    return 1  # default branch, matches the locked notebook exactly


def classify_report(report_text: Optional[str]) -> Optional[int]:
    """Procedure-level NHI = maximum grade among evaluable segments."""
    if not isinstance(report_text, str) or not report_text.strip():
        return None
    segs = split_segments(normalize(report_text))
    grades = [grade_segment(s) for s in segs]
    return max(grades) if grades else None


def extract_procedure_nhi(report_text: str) -> dict:
    """Main entry point — extract procedure-level NHI from a pathology report.

    Returns:
        {
            'procedure_nhi': int (0-4) or None,
            'segments': {segment_index: int (0-4)},  # positional, not named
            'flags': list[str]
        }
    """
    if not isinstance(report_text, str) or not report_text.strip():
        return {"procedure_nhi": None, "segments": {}, "flags": ["empty_report"]}

    segs = split_segments(normalize(report_text))
    if not segs:
        return {"procedure_nhi": None, "segments": {}, "flags": ["no_evaluable_segments"]}

    seg_grades = {f"segment_{i+1}": grade_segment(s) for i, s in enumerate(segs)}
    procedure_nhi = max(seg_grades.values())

    return {"procedure_nhi": procedure_nhi, "segments": seg_grades, "flags": []}


# ---- CLI ----

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-extract NHI from a CSV of pathology reports."
    )
    parser.add_argument("--input", required=True,
                        help="CSV with columns: procedure_id, report_text")
    parser.add_argument("--output", required=True,
                        help="Output CSV with extracted NHI per procedure")
    args = parser.parse_args()

    import pandas as pd
    df = pd.read_csv(args.input)
    if "procedure_id" not in df.columns or "report_text" not in df.columns:
        raise SystemExit("Input CSV must have 'procedure_id' and 'report_text' columns.")

    out_rows = []
    for _, row in df.iterrows():
        result = extract_procedure_nhi(str(row["report_text"]))
        out_rows.append({
            "procedure_id": row["procedure_id"],
            "procedure_nhi": result["procedure_nhi"],
            "n_segments_evaluated": len(result["segments"]),
            "flags": ";".join(result["flags"]),
        })

    pd.DataFrame(out_rows).to_csv(args.output, index=False)
    print(f"Wrote {len(out_rows)} rows to {args.output}")


if __name__ == "__main__":
    _cli()
