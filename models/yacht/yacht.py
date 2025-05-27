"""
Yacht class for the Running Rigging Management system.

Represents a yacht and its key sail dimensions, as well as its running rigging.
"""

from models.yacht.saildata import SailData
from models.yacht.running_rigging import RunningRigging
from models.yacht.mainsheetsystem import MainsheetSystem

class Yacht:
    def __init__(self, i: float, j: float, p: float, e: float, boom_above_deck: float, boat_length):
        """
        Initialize a Yacht instance.

        Args:
            i (float): Height of the forestay (I).
            j (float): Base of the foretriangle (J).
            p (float): Height of the mainsail luff (P).
            e (float): Foot of the mainsail (E).
            boom_above_deck (float): Height of the boom above deck in meters.
            boat_length (float): Length of the boat in meters.

        """
        self.saildata = SailData(i, j, p, e)
        self.running_rigging = RunningRigging(self)
        self.boom_above_deck = boom_above_deck  # Default boom height above deck in meters
        self.boat_length = boat_length 
        self.mainsheet_system = MainsheetSystem(purchase_ratio=6, routing="traditional")  # Default mainsheet system