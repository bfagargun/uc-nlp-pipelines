"""
MES extraction from the BULGULAR (findings) section of an endoscopy report,
without access to the structured diagnosis field.

EXPLORATORY PIPELINE — presented as a benchmark for settings where the
structured diagnosis field is absent or non-standardised. Not used in any
primary analysis in the accompanying manuscript.

PLACEHOLDER FILE. Replace the body of `extract_mes_from_findings` with the
locked rule set used in the manuscript validation.

Expected return:
    {
        'mes': int (0-3) or None,
        'descriptors_found': list[str],  # which Turkish descriptors matched
        'reasoning': str,                # short trace of which rule fired
    }
"""

from __future__ import annotations
import argparse
import re
from typing import Optional


# Replace with the locked rule set. Below is a non-exhaustive sketch of the
# descriptor categories mapped to Mayo criteria.

DESCRIPTORS = {
    "vascular_loss": [
        # r"damarlanma\s+(silik|yok|kaybolm)",
    ],
    "vascular_preserved": [
        # r"damarlanma\s+(normal|korunmuş)",
    ],
    "friability_present": [
        # r"friabil",
        # r"frajilite\s*\(\s*\+\s*\)",
    ],
    "erosion_present": [
        # r"erozyon",
    ],
    "ulceration_focal": [
        # r"nokta\s+ülseras?yon",
    ],
    "ulceration_widespread": [
        # r"yaygın\s+ülseras?yon",
        # r"derin\s+ülseras?yon",
    ],
    "exudate": [
        # r"eksuda",
    ],
    "terminal_ileum_section": [
        # r"terminal\s+ileum",  # used for masking
    ],
}


def extract_mes_from_findings(report_text: str) -> dict:
    """Predict MES from the free-text findings section.

    PLACEHOLDER — replace with the locked pipeline.
    """
    raise NotImplementedError(
        "Paste the locked findings-section MES extraction code here."
    )


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-extract MES from the findings section of endoscopy reports."
    )
    parser.add_argument("--input", required=True,
                        help="CSV with columns: procedure_id, findings_text")
    parser.add_argument("--output", required=True,
                        help="Output CSV with extracted MES per procedure")
    args = parser.parse_args()

    import pandas as pd
    df = pd.read_csv(args.input)
    out = []
    for _, row in df.iterrows():
        result = extract_mes_from_findings(str(row["findings_text"]))
        out.append({
            "procedure_id": row["procedure_id"],
            "mes": result["mes"],
            "descriptors_found": ";".join(result["descriptors_found"]),
        })
    pd.DataFrame(out).to_csv(args.output, index=False)
    print(f"Wrote {len(out)} rows to {args.output}")


if __name__ == "__main__":
    _cli()
