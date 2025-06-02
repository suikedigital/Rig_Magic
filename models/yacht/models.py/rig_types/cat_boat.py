from ..yacht import Yacht

class CatBoat(Yacht):
    """
    Represents a cat boat with specific sail and rigging configurations.

    Inherits from the Yacht class and provides default configurations for a cat boat rig.

    Defintion: A single sail on a single mast set well forward. No headsail. Very simple and traditional.

    Attributes:
        i (float): Height of the forestay (I).
        j (float): Base of the foretriangle (J).
        p (float): Height of the mainsail luff (P).
        e (float): Foot of the mainsail (E).
        boom_above_deck (float): Height of the boom above deck in meters.
        boat_length (float): Length of the boat in meters.
    """

    def __init__(self, i: float, j: float, p: float, e: float, boom_above_deck: float, boat_length: float):
        super().__init__(i, j, p, e, boom_above_deck, boat_length)