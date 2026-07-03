"""
MES narrative-findings ("BULGULAR") descriptor patterns.
Ported verbatim from notebooks/mayo_nlp_from_bulgular.ipynb (cell 5), the
exploratory blind pipeline (kappa_w = 0.66, n = 829; not used in any
primary or replication analysis in the manuscript — see Table 4 and
Supplementary Figure S1).
"""

import re

NEGATION = re.compile(
    r'(yok|görülmedi|izlenmedi|saptanmadı|tespit\s+edilmedi|bulunmadı)',
    re.IGNORECASE)

TI_SENTENCE = re.compile(
    r'[^.!?]*\b(terminal\s+ileum|t[\. ]?ileum)\b[^.!?]*[.!?]',
    re.IGNORECASE)

PATTERNS = {
    # Mayo 3 -- definite severe-disease markers
    'spontaneous_bleed': re.compile(
        r'\b(spontan\s+kanama|aktif\s+kanama|serbest\s+kanama)\b', re.I),
    'no_intact_mucosa': re.compile(
        r'(sağlam\s+mukoza\s+kalma(?:yacak|mış)|'
        r'arada\s+normal\s+mukoza\s+(?:kalma|olmay))', re.I),
    'severe_ulcer': re.compile(
        r'\b(yaygın|derin|büyük|geniş)\s+ülser', re.I),
    'very_friable': re.compile(r'\boldukça\s+frajil\b', re.I),

    # Ulceration severity discrimination
    'focal_ulcer': re.compile(     # mild -> Mayo 2
        r'\b(yer\s+yer|milimetrik|küçük|seyrek|tek|nadir)\s+ülser', re.I),
    'general_ulcer': re.compile(   # not focal -> Mayo 3
        r'\bülser(?:asyon|e|ler|li)?\b', re.I),

    # Mayo 2 markers
    'erosion': re.compile(r'\beroz(?:yon|yonlu|yonlar)\b', re.I),
    'friable': re.compile(r'\bfrajil(?:ite|di|dir)?\b', re.I),
    'exudate': re.compile(
        r'\beksüda(?:syon|syonlu|tif|t|li)?\b|eksuday?\b', re.I),
    'contact_bleeding': re.compile(
        r'(temas\s+kanam|kanamaya\s+eğilimli)', re.I),
    'granular': re.compile(r'\bgranüler\b', re.I),
    'vascular_absent': re.compile(
        r'vasküler\s+(?:(?:patern[ıi]|yapı(?:lar)?)\s+)?'
        r'(?:silinm|kaybolm|bozulm|seçilem|görülem)', re.I),

    # Mayo 1 markers
    'erythema': re.compile(
        r'\b(?:eritemli|eritem|hiperemik|hiperemi)\b', re.I),
    'edema': re.compile(r'\bödem(?:li)?\b', re.I),
    'vascular_decreased': re.compile(
        r'vasküler\s+(?:patern[ıi]\s+)?(?:azalm|belirsizleşm)', re.I),
}


def is_negated(text: str, start: int, window: int = 70) -> bool:
    """Is there a negation cue within `window` characters of the match?"""
    return bool(NEGATION.search(text[max(0, start - window): start + window]))


def mask_terminal_ileum(text: str) -> str:
    """Blank out sentences mentioning the terminal ileum (irrelevant to UC
    Mayo scoring, which only covers colonic segments)."""
    return TI_SENTENCE.sub(' ', text)


def has_feature(key: str, text: str) -> bool:
    """Does feature `key` occur in `text` in a non-negated context?"""
    m = PATTERNS[key].search(text)
    return bool(m) and not is_negated(text, m.start())
