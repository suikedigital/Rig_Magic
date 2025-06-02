"""Sloop Single mast, mainsail + one headsail (e.g., jib or genoa). Most common cruising and racing rig."""

from .hulls import Monohull, Trimaran, Catamaran
from .rig_types import CatBoat, FractionalSloop, Cutter, Ketch, Sloop, Yawl
from .yacht_profile import YachtProfile
from .saildata import SailData
from .yacht import Yacht

class YachtFactory:
    hull_types = {
        'monohull': Monohull,
        'trimaran': Trimaran,
        'catamaran': Catamaran,
        # Add more hulls as needed
    }
    rig_types = {
        'sloop': Sloop,
        'yawl': Yawl,
        'ketch': Ketch,
        'fractional_sloop': FractionalSloop,
        'cat_boat': CatBoat,
        'cutter': Cutter,
        # Add more rig types as needed
    }

    @staticmethod
    def create_yacht(hull_type: str, hull_kwargs: dict, rig_type: str, rig_profile_kwargs: dict, saildata_kwargs: dict):
        """
        Compose a yacht from hull, rig, rig profile, and sail data.
        """
        hull_class = YachtFactory.hull_types.get(hull_type)
        rig_class = YachtFactory.rig_types.get(rig_type)
        if not hull_class:
            raise ValueError(f"Unknown hull type: {hull_type}")
        if not rig_class:
            raise ValueError(f"Unknown rig type: {rig_type}")
        hull = hull_class(**hull_kwargs)
        rig_profile = YachtProfile(**rig_profile_kwargs)
        saildata = SailData(**saildata_kwargs)
        return Yacht(hull=hull, rig_type=rig_type, profile=rig_profile, saildata=saildata)