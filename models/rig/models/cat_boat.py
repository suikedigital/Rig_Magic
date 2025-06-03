from models.rig.models.rig import Rig

class CatBoat(Rig):
    """
    Represents a cat boat with specific sail and rigging configurations.

    Inherits from the Yacht class and provides default configurations for a cat boat rig.

    Defintion: A single sail on a single mast set well forward. No headsail. Very simple and traditional.

    Attributes:
        boom_above_deck (float): Height of the boom above deck in meters.
        boat_length (float): Length of the boat in meters.
    """

    def __init__(self, yacht_id: int, boom_above_deck: float = None):
        super().__init__(yacht_id=yacht_id, rig_type=self.__class__.__name__, boom_above_deck=boom_above_deck)
        self.boom_above_deck = boom_above_deck