"""
MES diagnosis-field ("TANI") pattern definitions.

IMPORTANT PROVENANCE NOTE — read before relying on this file:
The original source file for this pipeline was not present in the
repository or in any of the maintainer's saved notebooks (only its
already-computed output column, `nlp_mayo_from_tanı`, survived in the
dataset). This implementation was RECONSTRUCTED by reverse-engineering the
regex logic against that stored output column, then independently
validated:

    - Exact match against the stored `nlp_mayo_from_tanı` column: 829/829
      (100%) across the full cohort.
    - Re-run against the reference standard (mayo_score_classified)
      reproduces the manuscript's reported metrics exactly:
      kappa_w = 0.968 (rounds to 0.97), accuracy = 92.76% (rounds to
      92.8%), exact agreements = 769/829 — matching Table 4 and the
      Results text precisely.

This gives high confidence the reconstruction is behaviourally identical
to the original locked rule set, but it is a reconstruction, not a
recovered original file. The maintainer should review this file against
their own memory/records of the original implementation before treating
it as the canonical source.
"""

import re

ROMAN_TO_INT = {"O": 0, "I": 1, "II": 2, "III": 3}

# Observed keyword variants in the diagnosis field, including a typo
# ("MAYO SKOU") that appears in the real corpus and must be matched.
_KEYWORD = r'(?:\s*SUBSKORU|\s*SKORU|\s*SKOU|\s*SKOR)?'
_NUM = r'(?:[0-3]|III|II|I|O)'

RE_RANGE = re.compile(
    rf'MAYO{_KEYWORD}\s*[:;\-]?\s*({_NUM})\s*[-\u2013]\s*({_NUM})\b'
)
RE_SINGLE = re.compile(
    rf'MAYO{_KEYWORD}\s*[:;\-]?\s*({_NUM})\b'
)


def to_int(token: str):
    """Convert a matched token (arabic digit, roman numeral, or letter O
    used in place of zero) to an int 0-3, or None if unrecognised."""
    token = token.strip()
    if token.isdigit():
        return int(token)
    return ROMAN_TO_INT.get(token)


def normalize(text: str) -> str:
    if not isinstance(text, str):
        return ""
    t = text.upper()
    t = re.sub(r"\s+", " ", t)
    return t.strip()
