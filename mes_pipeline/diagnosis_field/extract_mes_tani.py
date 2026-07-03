"""
MES extraction from the diagnosis (TANI) field of an endoscopy report.

PRIMARY PIPELINE — used in all primary analyses in the accompanying
manuscript (kappa_w = 0.97, accuracy 92.8%, 769/829 exact agreements;
see Table 4). See rules/mes_patterns.py for an important provenance note:
this file is a validated RECONSTRUCTION (see that module's docstring),
not a recovered original source file.

Resolution rules (all confirmed against the real cohort, see docstring
above):
    - When multiple MAYO mentions occur in one diagnosis line (e.g. one
      score per segment), the FIRST mention (by text position) wins —
      this matches the stored NLP output exactly and is presumed to
      reflect the convention that the first-stated score is the overall
      procedure impression, with subsequent mentions being per-segment
      detail.
    - A range (e.g. "MAYO 1-2") is resolved to its LOWER bound. Note this
      differs from the structured reference field, which resolves ranges
      via clinical adjudication against the narrative findings (Methods
      2.2) — this is the source of most disagreements between the NLP
      pipeline and the reference (see manuscript Results 3.3.2).
    - A letter "O" used in place of the numeral zero is recognised.
"""

from __future__ import annotations
import argparse
from typing import Optional

from mes_pipeline.diagnosis_field.rules.mes_patterns import (
    RE_RANGE, RE_SINGLE, to_int, normalize,
)


def extract_mes_from_diagnosis(diagnosis_text: str) -> dict:
    """
    Extract MES from a free-text diagnosis line.

    Returns:
        {
            'mes': int (0-3) or None,
            'raw_match': str,                 # matched substring
            'is_range': bool,
            'range': tuple[int, int] | None,
        }
    """
    if not isinstance(diagnosis_text, str) or not diagnosis_text.strip():
        return {"mes": None, "raw_match": "", "is_range": False, "range": None}

    t = normalize(diagnosis_text)

    m_range = RE_RANGE.search(t)
    m_single = RE_SINGLE.search(t)

    candidates = []  # (start_pos, mes_value, is_range, raw, range_tuple)

    if m_range:
        lo, hi = to_int(m_range.group(1)), to_int(m_range.group(2))
        if lo is not None and hi is not None:
            candidates.append((m_range.start(), min(lo, hi), True,
                                m_range.group(0), (min(lo, hi), max(lo, hi))))

    if m_single:
        # Skip if this single match is actually inside the range match
        # already captured above (avoid double-counting the same mention).
        overlaps_range = bool(
            m_range and m_range.start() <= m_single.start() < m_range.end()
        )
        if not overlaps_range:
            v = to_int(m_single.group(1))
            if v is not None:
                candidates.append((m_single.start(), v, False, m_single.group(0), None))

    if not candidates:
        return {"mes": None, "raw_match": "", "is_range": False, "range": None}

    # First mention (by text position) wins.
    candidates.sort(key=lambda c: c[0])
    _, mes, is_range, raw, rng = candidates[0]

    return {"mes": mes, "raw_match": raw, "is_range": is_range, "range": rng}


# ---- CLI ----

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-extract MES from a CSV of endoscopy diagnosis fields."
    )
    parser.add_argument("--input", required=True,
                        help="CSV with columns: procedure_id, diagnosis_text")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    import pandas as pd
    df = pd.read_csv(args.input)
    if "procedure_id" not in df.columns or "diagnosis_text" not in df.columns:
        raise SystemExit("Input CSV must have 'procedure_id' and 'diagnosis_text' columns.")

    out_rows = []
    for _, row in df.iterrows():
        result = extract_mes_from_diagnosis(str(row["diagnosis_text"]))
        out_rows.append({
            "procedure_id": row["procedure_id"],
            "mes": result["mes"],
            "is_range": result["is_range"],
            "raw_match": result["raw_match"],
        })

    pd.DataFrame(out_rows).to_csv(args.output, index=False)
    print(f"Wrote {len(out_rows)} rows to {args.output}")


if __name__ == "__main__":
    _cli()
