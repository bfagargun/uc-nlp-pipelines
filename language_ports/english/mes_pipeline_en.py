"""
Mayo Endoscopic Score (MES) — diagnosis-field pipeline
English-language adaptation template
=======================================================

STATUS: PROOF-OF-CONCEPT / ADAPTATION TEMPLATE — NOT INDEPENDENTLY VALIDATED

Mirrors the architecture of the validated Turkish diagnosis-field MES
pipeline described in the manuscript (Methods 2.4; kappa_w = 0.97,
accuracy 92.8% against endoscopist-assigned MES, n = 829). That pipeline
parses the structured diagnosis line of the endoscopy report and
recognises:
    - Arabic numerals (0-3)
    - Roman numerals (I-III)
    - Hyphenated notation (e.g. MAYO-2)
    - Keyword-based entries (e.g. MAYO SCORE 3)
    - Score ranges (e.g. MAYO 1-2)
    - A letter "O" used in place of the numeral zero

This module reproduces the same recognition categories for English-
language diagnosis lines (e.g. "ULCERATIVE COLITIS, MAYO 2",
"MAYO SCORE 3, SEVERE ACTIVITY", "MAYO I-II"). It has only been tested
against synthetic examples (see example_reports_en.py) and must be
validated locally before use on real reports.
"""

import re
import numpy as np

ROMAN_TO_INT = {"0": 0, "I": 1, "II": 2, "III": 3}


def _normalize_o_as_zero(text):
    """A letter 'O' used where a numeral zero was intended, immediately
    after MAYO / MAYO SCORE / a hyphen, is normalized to '0'."""
    text = re.sub(r"\bMAYO(\s*SCORE)?\s*[-:]?\s*O\b", lambda m: m.group(0)[:-1] + "0", text)
    return text


def normalize(text):
    if not isinstance(text, str):
        return ""
    t = text.upper()
    t = re.sub(r"\s+", " ", t)
    t = _normalize_o_as_zero(t)
    return t.strip()


# Range entry, e.g. "MAYO 1-2", "MAYO SCORE 0-1", "MAYO I-II"
RE_RANGE = re.compile(
    r"MAYO(?:\s*SCORE)?[\s\-:]*([0-3]|I{1,3})\s*[-–]\s*([0-3]|I{1,3})\b"
)

# Single value with optional keyword / hyphen, e.g.:
#   "MAYO 2", "MAYO-2", "MAYO SCORE 3", "MAYO SCORE: 2", "MAYO III"
RE_SINGLE = re.compile(
    r"MAYO(?:\s*SCORE)?\s*[\-:]?\s*([0-3]|I{1,3})\b"
)


def _val(token):
    """Convert a matched token (arabic or roman numeral) to an int 0-3."""
    if token.isdigit():
        return int(token)
    return ROMAN_TO_INT.get(token, np.nan)


def extract_mes(diagnosis_text, range_resolution="dominant_descriptor"):
    """
    Extract MES from a free-text diagnosis line.

    range_resolution:
        "dominant_descriptor" - caller supplies resolved integer via
            resolve_range() using narrative findings (mirrors the
            manuscript's predefined adjudication rule, Methods 2.2).
            Here, as a template default, the LOWER bound of the range
            is returned, and the raw range is also returned so the
            caller can apply their own adjudication rule.
        "raw" - returns a string like "1-2" instead of an integer.

    Returns:
        dict with keys: 'mes' (int, np.nan if unparseable),
                         'is_range' (bool),
                         'range_raw' (str or None)
    """
    if not isinstance(diagnosis_text, str) or not diagnosis_text.strip():
        return {"mes": np.nan, "is_range": False, "range_raw": None}

    t = normalize(diagnosis_text)

    m_range = RE_RANGE.search(t)
    if m_range:
        lo, hi = _val(m_range.group(1)), _val(m_range.group(2))
        raw = f"{m_range.group(1)}-{m_range.group(2)}"
        if range_resolution == "raw":
            return {"mes": np.nan, "is_range": True, "range_raw": raw}
        # Template default: lower bound. Replace with a narrative-based
        # adjudication rule for production use (see manuscript Methods 2.2).
        return {"mes": lo, "is_range": True, "range_raw": raw}

    m_single = RE_SINGLE.search(t)
    if m_single:
        return {"mes": _val(m_single.group(1)), "is_range": False, "range_raw": None}

    return {"mes": np.nan, "is_range": False, "range_raw": None}


if __name__ == "__main__":
    from example_reports_en import MES_EXAMPLES

    print("=" * 70)
    print("MES (diagnosis-field) English adaptation template — synthetic run")
    print("(NOT a validation — see module docstring)")
    print("=" * 70)
    correct = 0
    for text, expected in MES_EXAMPLES:
        result = extract_mes(text)
        pred = result["mes"]
        ok = "OK" if pred == expected else "MISMATCH"
        correct += (pred == expected)
        flag = " [RANGE]" if result["is_range"] else ""
        print(f"[{ok:8s}] expected={expected}  predicted={pred}{flag}  | {text}")
    print(f"\n{correct}/{len(MES_EXAMPLES)} synthetic examples matched expected value.")
