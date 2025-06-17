"""
rope_construction.py
-------------------
Defines RopeConstruction class and RopeConstructionType enums for rope construction logic in the running rigging management system.

- RopeConstructionType: Enum for construction types (e.g., Braid/Braid, Dyneema/Braid)
- RopeConstruction: Data class for construction type and diameter, with break strength calculation
"""

from dataclasses import dataclass
from enum import Enum


class RopeConstructionType(Enum):
    BRAID_BRAID = "Braid/Braid"
    DYNEEMA_BRAID = "Dyneema/Braid"
    DYNEEMA_DYNEEMA = "Dyneema/Dyneema"


CONSTRUCTION_MAP = {
    RopeConstructionType.BRAID_BRAID: ("braid", "braid"),
    RopeConstructionType.DYNEEMA_BRAID: ("dyneema", "braid"),
    RopeConstructionType.DYNEEMA_DYNEEMA: ("dyneema", "dyneema"),
}

# Preset breaking strains (kg) for each construction type and diameter
# These are example values; adjust as needed for your application or vendor data.
PRESET_BREAK_STRAINS = {
    RopeConstructionType.BRAID_BRAID: {6: 820, 8: 2400, 10: 2400, 12: 3200, 14: 4500},
    RopeConstructionType.DYNEEMA_BRAID: {4: 1600, 5: 2300, 6: 3100, 7: 4100, 8: 5200, 10: 7700, 12: 10500, 14: 13500},
    RopeConstructionType.DYNEEMA_DYNEEMA: {4: 2000, 5: 3000, 6: 4000, 7: 5200, 8: 6500, 10: 9500, 12: 13000, 14: 17000},
}


@dataclass
class RopeConstruction:
    construction_type: RopeConstructionType
    diameter: int  # mm

    @property
    def base_diameter(self):
        """
        Returns the diameter to use for this rope (just the set diameter).
        """
        return self.diameter

    def total_break_strength(self):
        """
        Returns the preset breaking strain (kg) for this construction type and diameter.
        """
        try:
            return PRESET_BREAK_STRAINS[self.construction_type][self.diameter]
        except KeyError:
            return 0  # Return 0 if no preset found, or handle as needed
