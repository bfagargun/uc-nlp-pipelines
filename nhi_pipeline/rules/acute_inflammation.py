"""
Acute inflammatory infiltrate detection.

PLACEHOLDER — paste the locked regex rules used in the manuscript validation.

Output convention:
    0 = absent
    1 = mild
    2 = moderate
    3 = severe

Typical Turkish trigger phrases (non-exhaustive; refine when pasting real rules):
    - "kript abse(si)?" / "crypt abscess"
    - "kriptit(is)?" / "cryptitis"
    - "nötrofil(ik)? infiltrasyon"
    - "akut iltihab(i|î|i)? aktivit(e|esi) (hafif|orta|şiddetli)"
"""

import re

# Replace with the locked rule set.
ACUTE_PATTERNS = {
    # 3: severe
    # 2: moderate
    # 1: mild
    # 0: absent (default)
}


def grade_acute(segment_text: str) -> int:
    raise NotImplementedError("Paste locked acute-infiltrate rules.")
