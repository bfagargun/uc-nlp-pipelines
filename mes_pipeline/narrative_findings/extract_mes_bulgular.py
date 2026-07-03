"""
MES prediction from the free-text findings ("BULGULAR") section of an
endoscopy report, WITHOUT access to the diagnosis (TANI) line — a blind,
exploratory benchmark.

Ported verbatim from notebooks/mayo_nlp_from_bulgular.ipynb.

STATUS: exploratory only. Performance: kappa_w = 0.66, exact agreement
57.8%, agreement within +/-1 grade 90.6%, binary remission/active accuracy
80.3% (n = 829). NOT used in any primary or replication analysis in the
manuscript (see Table 4, Supplementary Figure S1). Provided as a benchmark
for settings where a structured diagnosis field is unavailable or
non-standardised.
"""

from __future__ import annotations
import argparse
from typing import Optional

from mes_pipeline.narrative_findings.rules.descriptor_patterns import (
    has_feature, mask_terminal_ileum, PATTERNS, is_negated,
)


def extract_mes_from_findings(findings_text: str) -> dict:
    """
    Predict MES from the free-text findings section (blind to diagnosis).

    Returns:
        {'mes': int (0-3) or None, 'descriptors_found': list[str]}
    """
    if not findings_text or len(str(findings_text).strip()) < 20:
        return {"mes": None, "descriptors_found": []}

    text = mask_terminal_ileum(str(findings_text))
    h = has_feature
    found = []

    def hf(key):
        ok = h(key, text)
        if ok:
            found.append(key)
        return ok

    focal = hf('focal_ulcer')
    ulc_m = PATTERNS['general_ulcer'].search(text)
    gen_ulc = bool(ulc_m) and not is_negated(text, ulc_m.start()) if ulc_m else False
    if gen_ulc:
        found.append('general_ulcer')
    nonfocal = gen_ulc and not focal

    # -- Mayo 3 --
    if (hf('spontaneous_bleed') or
            hf('severe_ulcer') or
            (hf('no_intact_mucosa') and gen_ulc) or
            (hf('very_friable') and gen_ulc) or
            nonfocal):
        return {"mes": 3, "descriptors_found": found}

    ery = hf('erythema')
    edm = hf('edema')
    fri = hf('friable')
    vasc = hf('vascular_absent')

    # -- Mayo 2 --
    if (hf('erosion') or
            hf('exudate') or
            hf('contact_bleeding') or
            focal or
            (fri and (ery or edm)) or
            (vasc and fri) or
            (hf('granular') and fri)):
        return {"mes": 2, "descriptors_found": found}

    # -- Mayo 1 --
    if (ery or edm or
            hf('vascular_decreased') or vasc or
            hf('granular') or fri):
        return {"mes": 1, "descriptors_found": found}

    # -- Mayo 0 --
    return {"mes": 0, "descriptors_found": found}


# ---- CLI ----

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Batch-predict MES from a CSV of endoscopy findings text."
    )
    parser.add_argument("--input", required=True,
                        help="CSV with columns: procedure_id, findings_text")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    import pandas as pd
    df = pd.read_csv(args.input)
    if "procedure_id" not in df.columns or "findings_text" not in df.columns:
        raise SystemExit("Input CSV must have 'procedure_id' and 'findings_text' columns.")

    out_rows = []
    for _, row in df.iterrows():
        result = extract_mes_from_findings(str(row["findings_text"]))
        out_rows.append({
            "procedure_id": row["procedure_id"],
            "mes": result["mes"],
            "descriptors_found": ";".join(result["descriptors_found"]),
        })

    pd.DataFrame(out_rows).to_csv(args.output, index=False)
    print(f"Wrote {len(out_rows)} rows to {args.output}")


if __name__ == "__main__":
    _cli()
