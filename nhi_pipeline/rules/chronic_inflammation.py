"""
NHI Grade 0-1 — chronic inflammatory infiltrate and normal-mucosa rules.
Ported verbatim from notebooks/Mayo_Nancy_NLP_Analysis_v3.ipynb (cell 15),
locked and used in the manuscript validation (kappa_w = 0.87, n = 799).
"""

import re

# GRADE 1: Chronic only
RE_CHRONIC = re.compile(r'KRONIK\s+(ILTIHAP|INFLAMASYON|KOLIT|REKTIT)')

# GRADE 0: Normal
RE_NORMAL = re.compile(r'\bNORMAL\b|BELIRGIN\s+DEGISIKLIK\s+YOK')
