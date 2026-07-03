"""
Synthetic example reports for the English adaptation template.
================================================================

IMPORTANT: These are HAND-WRITTEN SYNTHETIC sentences constructed from
published Nancy Histological Index descriptors (Marchal-Bressenot et al.,
Gut 2017) and standard Mayo Endoscopic Score conventions. They are NOT
real patient data and do NOT constitute a validation cohort. They exist
only to demonstrate that the rule architecture fires as intended on
clearly-worded example text.

A genuine validation requires a blinded pathologist/endoscopist-scored
cohort of REAL English-language reports from the adopting centre,
following the methodology in the manuscript (Methods 2.3/2.4, and the
per-rule provenance-audit approach in Supplementary Table S2).
"""

# ---------------------------------------------------------------------
# NHI examples: (pathology report text, expected NHI grade)
# ---------------------------------------------------------------------
NHI_EXAMPLES = [
    (
        "I- RECTUM: Colonic mucosa with normal architecture, no significant "
        "histologic abnormality. No active or chronic inflammation identified.",
        0,
    ),
    (
        "I- SIGMOID COLON: Mild increase in chronic inflammatory infiltrate "
        "in the lamina propria. No acute inflammation. No ulceration.",
        1,
    ),
    (
        "I- RECTUM: Chronic active colitis with mild active inflammation "
        "(occasional cryptitis). No crypt abscess. No ulceration.",
        2,
    ),
    (
        "I- DESCENDING COLON: Chronic active colitis with crypt abscess "
        "formation and active inflammation. No ulceration identified.",
        3,
    ),
    (
        "I- RECTUM: Severe active chronic colitis with basal plasmacytosis "
        "and diffuse crypt abscesses.",
        3,
    ),
    (
        "I- RECTUM: Chronic active colitis with ulceration and extensive "
        "crypt abscess formation.",
        4,
    ),
    (
        "I- TERMINAL ILEUM: Ulceration noted.\n"
        "II- RECTUM: Mild chronic inflammation only, no acute inflammation, "
        "no ulceration.",
        1,  # terminal ileum segment excluded; only rectum segment scored
    ),
    (
        "I- SIGMOID COLON: Inflammatory polyp with associated chronic "
        "inflammation; underlying mucosa shows no ulceration.\n"
        "II- RECTUM: Chronic inflammation, mild focal active cryptitis.",
        2,
    ),
]

# ---------------------------------------------------------------------
# MES examples: (diagnosis-field text, expected MES integer)
# ---------------------------------------------------------------------
MES_EXAMPLES = [
    ("ULCERATIVE COLITIS, MAYO 2", 2),
    ("ULCERATIVE COLITIS (MAYO SCORE 3, SEVERE ACTIVITY)", 3),
    ("ULCERATIVE COLITIS MAYO-1", 1),
    ("ULCERATIVE COLITIS, MAYO III", 3),
    ("ULCERATIVE COLITIS, MAYO O", 0),          # letter O -> 0
    ("ULCERATIVE COLITIS, MAYO 1-2", 1),        # range -> template default: lower bound
    ("ULCERATIVE COLITIS IN ENDOSCOPIC REMISSION, MAYO 0", 0),
    ("ULCERATIVE COLITIS, MAYO SCORE: 2", 2),
]
