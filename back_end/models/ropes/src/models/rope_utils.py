"""
Rope utilities for normalization and mapping.
"""


def normalize_rope_type(rope_type):
    """
    Normalize any rope type input (enum, string, etc.) to the canonical registry key.
    """
    if hasattr(rope_type, "value"):
        rope_type = rope_type.value
    s = str(rope_type).replace(" ", "").replace("_", "").title().lower()
    mapping = {
        "mainhalyard": "MainsailHalyard",
        "mainsailhalyard": "MainsailHalyard",
        "codezerohalyard": "CodeZeroHalyard",
        "codezero": "CodeZeroHalyard",
        "genoahalyard": "GenoaHalyard",
        "genoa": "GenoaHalyard",
        "jibhalyard": "JibHalyard",
        "jib": "JibHalyard",
        "spinnakerhalyard": "SpinnakerHalyard",
        "spinnaker": "SpinnakerHalyard",
        "staysailhalyard": "StaysailHalyard",
        "staysail": "StaysailHalyard",
        "toppinglifthalyard": "ToppingLiftHalyard",
        "toppinglift": "ToppingLiftHalyard",
        "trisailhalyard": "TrisailHalyard",
        "trisail": "TrisailHalyard",
        # Add more as needed
    }
    return mapping.get(s, rope_type if isinstance(rope_type, str) else str(rope_type))
