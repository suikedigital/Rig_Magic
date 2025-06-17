"""
sym_spinnaker.py
----------------
This module defines the SymSpinnaker class, representing a symmetric spinnaker sail for a yacht.

Classes:
    SymSpinnaker(BaseSail):
        Represents a symmetric spinnaker sail, with geometric properties and area calculation.

Typical Usage Example:
    sym_spin = SymSpinnaker(saildata)
    area = sym_spin.area
    force = sym_spin.aerodynamic_force(wind_speed_knots=12)

Class Details:
    - The luff and foot are taken from saildata (spin_i and spin_j) if not provided.
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


class SymSpinnaker(BaseSail):
    """
    Represents a symmetric spinnaker sail.

    Args:
        saildata: Data source with geometric properties (spin_i, spin_j).
        luff (float, optional): Luff length in meters. Defaults to saildata.spin_i.
        leech (float, optional): Leech length in meters. Estimated if not provided.
        foot (float, optional): Foot length in meters. Defaults to saildata.spin_j.
        yacht_id: Optional identifier for the yacht.

    Attributes:
        luff (float): Length of the luff (meters).
        leech (float): Length of the leech (meters).
        foot (float): Length of the foot (meters).
        name (str): Name of the sail class ("SymSpinnaker").

    Methods:
        area (property): Returns the area of the sail in square meters.
        aerodynamic_force(wind_speed_knots, lift_coefficient=1.0, air_density=1.225):
            Returns the aerodynamic force (Newtons) on the sail for a given wind speed and coefficients.
    """

    def __init__(self, saildata, luff=None, leech=None, foot=None, yacht_id=None):
        luff = luff if luff is not None else get_val(saildata, "spin_i")
        foot = foot if foot is not None else get_val(saildata, "spin_j")
        leech = leech if leech is not None else sqrt(luff**2 + foot**2)
        super().__init__(saildata, luff, leech, foot, yacht_id=yacht_id)

    @property
    def area(self) -> float:
        """
        Calculate the area of the symmetric spinnaker in square meters.
        Returns:
            float: The area of the sail (m^2).
        """
        luff_m = self._mm_to_m(self.luff)
        foot_m = self._mm_to_m(self.foot)
        return 0.5 * luff_m * foot_m

    @property
    def luff_length(self):
        """Return the luff length."""
        return self.luff_length
