"""
NHI extraction pipeline — main entry point.

THIS IS A PLACEHOLDER FILE. Replace the body of `extract_procedure_nhi` and
the helper functions with the actual rule-based extraction code used in the
manuscript validation.

Expected interface (do not change without updating downstream code in
notebooks/01_nhi_validation.ipynb):

    extract_procedure_nhi(report_text: str) -> dict
        Returns:
            {
                'procedure_nhi': int (0-4) or None,
                'segments': {segment_name: int (0-4)},
                'features_per_segment': {
                    segment_name: {
                        'acute': int (0-3),
                        'chronic': int (0-3),
                        'ulceration': bool
                    }
                },
                'flags': list[str]  # any quality flags (e.g. 'no_segments_found')
            }

CLI:
    python -m nhi_pipeline.extract_nhi --input <csv> --output <csv>
"""

from __future__ import annotations
import argparse
import re
from typing import Optional

# ---- Segment headings used in our institution's pathology reports ----
# (Refine this list when you paste in the live code.)
SEGMENT_HEADINGS = [
    "rektum", "rectum",
    "sigmoid", "sigmoid kolon",
    "inen kolon", "descending",
    "transvers kolon", "transverse",
    "cikan kolon", "çıkan kolon", "ascending",
    "cekum", "çekum", "caecum",
]

EXCLUDED_SEGMENTS = [
    "terminal ileum", "ileum",
    "polip",  # polypectomy specimens
]


def segment_report(report_text: str) -> dict[str, str]:
    """Split a Turkish pathology report into per-segment substrings.

    PLACEHOLDER — replace with the locked rule set used in the manuscript.
    """
    raise NotImplementedError(
        "Paste the segmentation logic from your local pipeline here. "
        "Expected to return {segment_name: substring}."
    )


def extract_features_for_segment(segment_text: str) -> dict:
    """Extract acute / chronic / ulceration features from a segment substring.

    PLACEHOLDER — replace with the locked regex rules.
    """
    raise NotImplementedError(
        "Paste the per-segment feature extraction rules here. "
        "Expected to return {'acute': int, 'chronic': int, 'ulceration': bool}."
    )


def features_to_nhi(features: dict) -> int:
    """Map extracted features to an NHI grade (0–4) per the Nancy schema.

    Marchal-Bressenot et al., Gut 2017:
        Grade 0  : no histological significant disease
        Grade 1  : chronic inflammatory infiltrate, no acute inflammatory cells
        Grade 2  : mild acute inflammatory cell infiltrate
        Grade 3  : moderate-severe acute inflammatory cell infiltrate
        Grade 4  : ulceration

    PLACEHOLDER — replace with the locked mapping rules.
    """
    raise NotImplementedError("Paste the deterministic Nancy mapping here.")


def extract_procedure_nhi(report_text: str) -> dict:
    """Main entry point — extract procedure-level NHI from a pathology report.

    Returns the procedure-level NHI as the *maximum* segmental grade,
    excluding terminal-ileum and polypectomy segments.
    """
    segments = segment_report(report_text)
    segments = {
        name: text for name, text in segments.items()
        if not any(excl in name.lower() for excl in EXCLUDED_SEGMENTS)
    }

    if not segments:
        return {
            "procedure_nhi": None,
            "segments": {},
            "features_per_segment": {},
            "flags": ["no_evaluable_segments"],
        }

    features_per_segment = {}
    nhi_per_segment = {}
    flags: list[str] = []

    for name, text in segments.items():
        feats = extract_features_for_segment(text)
        features_per_segment[name] = feats
        nhi_per_segment[name] = features_to_nhi(feats)

    procedure_nhi = max(nhi_per_segment.values()) if nhi_per_segment else None

    return {
        "procedure_nhi": procedure_nhi,
        "segments": nhi_per_segment,
        "features_per_segment": features_per_segment,
        "flags": flags,
    }


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
