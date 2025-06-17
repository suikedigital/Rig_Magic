class Rig:
    def __init__(
        self,
        yacht_id: int,
        rig_type: str,
        boom_above_deck: float = None,
        base_id: int = None,
    ):
        self.yacht_id = yacht_id
        self.base_id = base_id
        self.rig_type = rig_type
        self.boom_above_deck = boom_above_deck
