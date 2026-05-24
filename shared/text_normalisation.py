"""
Shared Turkish-language text preprocessing utilities.

PLACEHOLDER — replace function bodies with the locked preprocessing
routines used in the manuscript validation.
"""

import re
import unicodedata


def normalise_turkish(text: str) -> str:
    """Lowercase + diacritic normalisation (preserving Turkish-specific characters).

    Note: standard NFKD normalisation will incorrectly strip dots from 'ı' / 'i'.
    This routine should preserve them.
    """
    if text is None:
        return ""
    # Replace as needed when pasting the live code.
    text = text.replace("İ", "i").replace("I", "ı")
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    """Naive sentence boundary detection."""
    return [s.strip() for s in re.split(r"[.!?]+\s+", text) if s.strip()]


def strip_punct(text: str) -> str:
    return re.sub(r"[^\w\s]", " ", text)
