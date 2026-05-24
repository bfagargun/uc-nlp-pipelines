"""
MES extraction from the diagnosis (TANI) field of an endoscopy report.

PRIMARY PIPELINE — used in all primary analyses in the accompanying manuscript.

PLACEHOLDER FILE. Replace the body of `extract_mes_from_diagnosis` with the
locked regex pipeline used in the manuscript validation.

Expected return:
    {
        'mes': int (0-3) or None,
        'raw_match': str,                # the matched substring
        'is_range': bool,                # True if the report records a range (e.g. MAYO 1-2)
        'range': tuple[int, int] | None, # the captured range
    }
"""

from __future__ import annotations
import argparse
import re
from typing import Optional


# Replace with the locked rule set.
PATTERNS_INTEGER = [
    # r"\bMAYO\s*[:\-]?\s*([0-3])\b",
    # r"\bMAYO\s*SKORU\s*[:\-]?\s*([0-3])\b",
    # r"\bMAYO\s*(I{1,3})\b",  # Roman numerals
]

PATTERNS_RANGE = [
    # r"\bMAYO\s*[:\-]?\s*([0-3])\s*[-–]\s*([0-3])\b",
]


def _normalise_letter_o(text: str) -> str:
    """Normalise the typed letter 'O' to digit '0' inside Mayo expressions."""
    return re.sub(r"(MAYO\s*[:\-]?\s*)O\b", r"\g<1>0", text, flags=re.IGNORECASE)


def extract_mes_from_diagnosis(report_text: str) -> dict:
    """Extract MES from the diagnosis field of a Turkish endoscopy report.

    PLACEHOLDER — replace with the locked pipeline.
    """
    raise NotImplementedError(
        "Paste the locked diagnosis-field MES extraction code here."
    )


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-extract MES from a CSV of endoscopy reports (diagnosis field)."
    )
    parser.add_argument("--input", required=True,
                        help="CSV with columns: procedure_id, diagnosis_text")
    parser.add_argument("--output", required=True,
                        help="Output CSV with extracted MES per procedure")
    args = parser.parse_args()

    import pandas as pd
    df = pd.read_csv(args.input)
    out = []
    for _, row in df.iterrows():
        result = extract_mes_from_diagnosis(str(row["diagnosis_text"]))
        out.append({
            "procedure_id": row["procedure_id"],
            "mes": result["mes"],
            "is_range": result["is_range"],
            "raw_match": result["raw_match"],
        })
    pd.DataFrame(out).to_csv(args.output, index=False)
    print(f"Wrote {len(out)} rows to {args.output}")


if __name__ == "__main__":
    _cli()
