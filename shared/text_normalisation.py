"""
Shared Turkish-language text normalisation.

Ported verbatim from the validated pipeline notebook
(notebooks/Mayo_Nancy_NLP_Analysis_v3.ipynb, cell "normalize"). Used by the
NHI pipeline. The MES pipelines use their own lighter-weight uppercase +
whitespace normalisation (they do not depend on Turkish diacritic folding),
defined locally in mes_pipeline/diagnosis_field/rules/mes_patterns.py.
"""

import re


def normalize(text: str) -> str:
    """Uppercase, fold Turkish diacritics to ASCII, collapse whitespace."""
    if not isinstance(text, str):
        return ""
    t = text.upper()
    t = t.replace('\u0130', 'I')  # İ -> I
    for src, dst in [('\u00dc', 'U'), ('\u00d6', 'O'), ('\u00c7', 'C'),
                      ('\u015e', 'S'), ('\u011e', 'G')]:
        t = t.replace(src, dst)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()
