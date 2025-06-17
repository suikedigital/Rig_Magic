from .rig import Rig


class FractionalSloop(Rig):
    """
    Represents a fractional sloop rigged yacht with specific sail and rigging configurations.

    Inherits from the Rig class and provides default configurations for a fractional sloop rig.

    Defintion: A type of sloop where the forestay (jib) attaches below the masthead. Better sail control.

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
