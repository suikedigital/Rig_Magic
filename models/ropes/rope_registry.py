"""
Registry of available rope types for the Running Rigging Management system.

Maps string keys to rope (halyard) classes, allowing dynamic rope creation
based on configuration or user input.
"""

from models.ropes.halyards import (
    MainHalyard, GenoaHalyard, JibHalyard, SpinnakerHalyard,
    CodeZeroHalyard, StaysailHalyard, ToppingLiftHalyard, TrisailHalyard
)
from models.ropes.sheets_and_guys.sheets import (
    MainSheet, GenoaSheet, JibSheet, SymSpinSheet,
    CodeZeroSheet, StaysailSheet, TrisailSheet, AsymSpinSheet
)
from models.ropes.sheets_and_guys.guys import SymSpinGuy

ROPE_REGISTRY = {
    # Halyard classes
    "MainHalyard": MainHalyard,
    "GenoaHalyard": GenoaHalyard,
    "JibHalyard": JibHalyard,
    "SpinnakerHalyard": SpinnakerHalyard,
    "CodeZeroHalyard": CodeZeroHalyard,  # Fixed typo here
    "StaysailHalyard": StaysailHalyard,
    "ToppingLiftHalyard": ToppingLiftHalyard,
    "TrisailHalyard": TrisailHalyard,
    # Sheet classes
    "AsymSpinSheet": AsymSpinSheet,
    "CodeZeroSheet": CodeZeroSheet,
    "GenoaSheet": GenoaSheet,
    "JibSheet": JibSheet,
    "MainSheet": MainSheet,
    "StaysailSheet": StaysailSheet,
    "TrisailSheet": TrisailSheet,
    "SymSpinSheet": SymSpinSheet,
     # Guy classes
    "SymSpinGuy": SymSpinGuy,
    # Add more as needed
}

# In app.py or a config file
HALYARD_TO_SHEET = {
    "MainHalyard": ["MainSheet"],
    "GenoaHalyard": ["GenoaSheet"],
    "JibHalyard": ["JibSheet"],
    "SpinnakerHalyard": ["SymSpinSheet", "AsymSpinSheet", "SymSpinGuy"],
    "CodeZeroHalyard": ["CodeZeroSheet"],
    "StaysailHalyard": ["StaysailSheet"],
    "TrisailHalyard": ["TrisailSheet"],
    # Add more as needed
}