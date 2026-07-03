"""
Exclusion contexts — segments/mentions that must not drive NHI scoring.
Ported verbatim from notebooks/Mayo_Nancy_NLP_Analysis_v3.ipynb (cell 15).

NOTE: this file did not exist in the original repository scaffold. It was
added during the repair of the pipeline (see repo history / PR discussion)
because the real, locked decision tree (grade_segment in extract_nhi.py)
depends on these two patterns to exclude polypectomy specimens and
terminal-ileal biopsies from NHI scoring, per manuscript Methods 2.1/2.3.
"""

import re

RE_POLYP = re.compile(
    r'(PSODOPOLIP|PSEUDOPOLIP|POLIPEKTOMI|\bPOLIP\b|'
    r'ADENOMATOZ|ADENOM|INFLAMATUAR POLIP|IMMUNREAKSIYON)'
)
RE_ILEUM = re.compile(r'TERMINAL ILEUM')
