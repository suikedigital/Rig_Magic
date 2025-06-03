from models.rig.models.rig import Rig

class Cutter(Rig):
    """
    Represents a cutter rigged yacht with specific sail and rigging configurations.

    Inherits from the Yacht class and provides default configurations for a cutter rig.

    Defintion: Like a sloop but with two headsails (e.g. jib + staysail) for versatility and better balance.

    Attributes:
        i (float): Height of the forestay (I).
        j (float): Base of the foretriangle (J).
        p (float): Height of the mainsail luff (P).
        e (float): Foot of the mainsail (E).
        boom_above_deck (float): Height of the boom above deck in meters.
        boat_length (float): Length of the boat in meters.
    """

    def __init__(self, yacht_id: int, boom_above_deck: float = None):
        super().__init__(yacht_id=yacht_id, rig_type=self.__class__.__name__, boom_above_deck=boom_above_deck)
