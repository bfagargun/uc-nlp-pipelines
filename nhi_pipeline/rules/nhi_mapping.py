"""
Deterministic mapping of extracted features to NHI grade (0–4).

Reference:
    Marchal-Bressenot A, Salleron J, Boulagnon-Rombi C, et al.
    Development and validation of the Nancy histological index for UC.
    Gut. 2017;66(1):43–49.

Grade definitions:
    0 — no histologic significant disease
    1 — chronic inflammatory infiltrate (no acute inflammatory cells)
    2 — mild acute inflammatory cell infiltrate
    3 — moderate–severe acute inflammatory cell infiltrate
    4 — ulceration (overrides 0–3)

The mapping below is the canonical Nancy schema; do not modify the logic
when pasting the live code — only verify that the input feature codes
match the convention.
"""


def features_to_nhi(features: dict) -> int:
    """
    Args:
        features: {
            'acute': int in {0, 1, 2, 3},   # 0=absent, 1=mild, 2=moderate, 3=severe
            'chronic': int in {0, 1, 2, 3}, # 0=absent, 1=mild, 2=moderate, 3=severe
            'ulceration': bool,
        }

    Returns:
        int in {0, 1, 2, 3, 4}.
    """
    if features.get("ulceration"):
        return 4

    acute = features.get("acute", 0)
    if acute >= 2:           # moderate or severe acute
        return 3
    if acute == 1:           # mild acute
        return 2

    if features.get("chronic", 0) >= 1:
        return 1

    return 0
