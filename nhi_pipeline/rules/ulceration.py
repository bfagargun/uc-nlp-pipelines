"""
NHI Grade 4 — ulceration / erosion rules.
Ported verbatim from notebooks/Mayo_Nancy_NLP_Analysis_v3.ipynb (cell 15),
locked and used in the manuscript validation (kappa_w = 0.87, n = 799).
"""

import re

RE_ULCER = re.compile(r'\b(ULSER|EROZYON)')
RE_NEG_ULCER = re.compile(r'ULSER\w*\s+(GOZLENMEDI|YOK|SAPTANMADI|IZLENMEDI)')
