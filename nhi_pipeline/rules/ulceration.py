"""
Ulceration / erosion detection.

PLACEHOLDER — paste the locked regex rules used in the manuscript validation.

Output convention:
    True  = ulceration / erosion present
    False = absent
"""

import re

ULCERATION_PATTERNS = [
    # r"ülseras?yon",
    # r"erozyon",
    # Replace with the locked rule set, including negation handling
    # (e.g. "ülserasyon (-)").
]


def has_ulceration(segment_text: str) -> bool:
    raise NotImplementedError("Paste locked ulceration rules.")
