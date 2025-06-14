"""
code_zero.py
------------
This module defines the CodeZero class, representing a Code Zero hybrid sail for a yacht.

Classes:
    CodeZero(BaseSail):
        Represents a Code Zero sail, with geometric properties and area calculation.

Typical Usage Example:
    code_zero = CodeZero(saildata)
    area = code_zero.area
    force = code_zero.aerodynamic_force(wind_speed_knots=12)

Class Details:
    - The luff and foot are taken from saildata (codezero_i and codezero_j) if not provided.
    - The leech is estimated as the hypotenuse of luff and foot if not provided.
    - Area is calculated as 0.5 * luff * foot.
    - Inherits aerodynamic_force() from BaseSail for force estimation.
"""
from math import sqrt
from .base_sail import BaseSail

def get_val(saildata, key):
    if isinstance(saildata, dict):
        return saildata.get(key)
    return getattr(saildata, key)

class CodeZero(BaseSail):
    """
    Represents a Code Zero hybrid sail.

    Args:
        saildata: Data source with geometric properties (codezero_i, codezero_j).
        luff (float, optional): Luff length in meters. Defaults to saildata.codezero_i.
        leech (float, optional): Leech length in meters. Estimated if not provided.
        foot (float, optional): Foot length in meters. Defaults to saildata.codezero_j.
        yacht_id: Optional identifier for the yacht.

    Attributes:
        luff (float): Length of the luff (meters).
        leech (float): Length of the leech (meters).
        foot (float): Length of the foot (meters).
        name (str): Name of the sail class ("CodeZero").

    Methods:
        area (property): Returns the area of the sail in square meters.
        aerodynamic_force(wind_speed_knots, lift_coefficient=1.0, air_density=1.225):
            Returns the aerodynamic force (Newtons) on the sail for a given wind speed and coefficients.
    """
    def __init__(self, saildata, luff=None, leech=None, foot=None, yacht_id=None):
        # Convert mm to meters if values are > 100 (assume mm if so)
        def mm_to_m(val):
            return val / 1000 if val and val > 100 else val
        luff = mm_to_m(luff if luff is not None else get_val(saildata, "codezero_i"))
        foot = mm_to_m(foot if foot is not None else get_val(saildata, "codezero_j"))
        leech = mm_to_m(leech if leech is not None else (sqrt(luff ** 2 + foot ** 2) if luff and foot else None))
        super().__init__(saildata, luff, leech, foot, yacht_id=yacht_id)

    @property
    def area(self) -> float:
        """
        Calculate the area of the Code Zero sail in square meters.
        Returns:
            float: The area of the sail (m^2).
        """
        luff_m = self._mm_to_m(self.luff)
        foot_m = self._mm_to_m(self.foot)
        return 0.5 * luff_m * foot_m