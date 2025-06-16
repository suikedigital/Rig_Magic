"""
Sail utilities for normalization and mapping.
"""

def normalize_sail_type(sail_type):
    """
    Normalize any sail type input (enum, string, etc.) to the canonical registry key.
    """
    if hasattr(sail_type, 'value'):
        sail_type = sail_type.value
    s = str(sail_type).replace(" ", "").replace("_", "").title().lower()
    mapping = {
        "mainsail": "Mainsail",
        "main": "Mainsail",
        "jib": "Jib",
        "genoa": "Genoa",
        "staysail": "Staysail",
        "codezero": "CodeZero",
        "codezer": "CodeZero",
        "symspinnaker": "SymSpinnaker",
        "symmetricspinnaker": "SymSpinnaker",
        "asymspinnaker": "AsymSpinnaker",
        "asymmetricspinnaker": "AsymSpinnaker",
        "trisail": "Trisail",
        # Add more as needed
    }
    return mapping.get(s, sail_type if isinstance(sail_type, str) else str(sail_type))
