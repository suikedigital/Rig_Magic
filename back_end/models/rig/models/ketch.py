from back_end.models.rig.models.rig import Rig


class Ketch(Rig):
    """
    Represents a ketch rigged yacht with specific sail and rigging configurations.

    Inherits from the Rig class and provides default configurations for a ketch rig.

    Definition: Two masts: mainmast forward, smaller mizzen mast aft but in front of the rudder post. Good balance and sail area distribution.

    Attributes:
        boom_above_deck (float): Height of the boom above deck in meters.
    """

    def __init__(self, yacht_id: int, boom_above_deck: float = None):
        super().__init__(
            yacht_id=yacht_id,
            rig_type=self.__class__.__name__,
            boom_above_deck=boom_above_deck,
        )
        self.boom_above_deck = boom_above_deck
