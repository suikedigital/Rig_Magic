"""
mainsail.py
-----------
This module defines the Mainsail class, representing a mainsail for a yacht.

Classes:
    Mainsail(BaseSail):
        Represents a mainsail, with geometric properties and area calculation.

Typical Usage Example:
    mainsail = Mainsail(saildata)
    area = mainsail.area
    force = mainsail.aerodynamic_force(wind_speed_knots=12)

Class Details:
    - The luff and foot are taken from saildata (main_p and main_e) if not provided.
    - The leech is estimated as the hypotenuse of luff and foot if not provided.
    - Area is calculated as 0.5 * luff * foot.
    - Inherits aerodynamic_force() from BaseSail for force estimation.
"""
from .base_sail import BaseSail


def get_val(saildata, key):
    if isinstance(saildata, dict):
        return saildata.get(key)
    return getattr(saildata, key)


class Mainsail(BaseSail):
    """
    Represents a mainsail.

    Args:
        saildata: Data source with geometric properties (main_p, main_e).
        luff (float, optional): Luff length in meters. Defaults to saildata.main_p.
        leech (float, optional): Leech length in meters. Estimated if not provided.
        foot (float, optional): Foot length in meters. Defaults to saildata.main_e.
        yacht_id: Explicit ID of the yacht this sail belongs to.

    Attributes:
        luff (float): Length of the luff (meters).
        leech (float): Length of the leech (meters).
        foot (float): Length of the foot (meters).
        name (str): Name of the sail class ("Mainsail").

    Methods:
        area (property): Returns the area of the sail in square meters.
        aerodynamic_force(wind_speed_knots, lift_coefficient=1.0, air_density=1.225):
            Returns the aerodynamic force (Newtons) on the sail for a given wind speed and coefficients.
    """
    def __init__(self, saildata, luff=None, leech=None, foot=None, yacht_id=None):
        luff = luff if luff is not None else get_val(saildata, "main_p")
        foot = foot if foot is not None else get_val(saildata, "main_e")
        leech = leech if leech is not None else (luff ** 2 + foot ** 2) ** 0.5
        super().__init__(saildata, luff, leech, foot, yacht_id=yacht_id)

    @property
    def area(self) -> float:
        """
        Calculate the area of the mainsail in square meters.
        Returns:
            float: The area of the sail (m^2).
        """
        luff_m = self._mm_to_m(self.luff)
        foot_m = self._mm_to_m(self.foot)
        return 0.5 * luff_m * foot_m
