from .cat_boat import CatBoat
from .cutter import Cutter
from .fractional_sloop import FractionalSloop
from .ketch import Ketch
from .sloop import Sloop
from .yawl import Yawl

class RigFactory:
    RIG_CLASSES = {
        "CatBoat": CatBoat,
        "Cutter": Cutter,
        "FractionalSloop": FractionalSloop,
        "Ketch": Ketch,
        "Sloop": Sloop,
        "Yawl": Yawl,
    }

    @staticmethod
    def create_rig(rig_type: str, yacht_id: int, boom_above_deck: float = None, base_id: int = None):
        rig_class = RigFactory.RIG_CLASSES.get(rig_type)
        if not rig_class:
            raise ValueError(f"Unknown rig type: {rig_type}")
        return rig_class(yacht_id=yacht_id, boom_above_deck=boom_above_deck, base_id=base_id)
