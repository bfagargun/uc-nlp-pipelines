"""
NHI Grade 2-3 — acute inflammatory infiltrate rules.
Ported verbatim from notebooks/Mayo_Nancy_NLP_Analysis_v3.ipynb (cell 15),
locked and used in the manuscript validation (kappa_w = 0.87, n = 799).
"""

import re

# GRADE 3: Severe active markers
RE_CRYPT_ABS = re.compile(r'KRIPT\s*ABSE')
RE_BASAL_PL = re.compile(r'BAZAL\s+(LENFOPLAZMASITOZ|PLAZMOSITOZ|LENFOPLAZM)')
RE_SEV_ACTIVE = re.compile(r'SIDDETLI\s+AKTIF')

# GRADE 2-3 discrimination
RE_ACTIVE = re.compile(r'\bAKTIF\b')
RE_MILD = re.compile(r'(HAFIF|MINIMAL|SEYREK|FOKAL|ODAKSAL)\s+(AKTIF|KRIPTIT)')
