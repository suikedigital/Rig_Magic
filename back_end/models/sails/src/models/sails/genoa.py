"""
genoa.py
--------
This module defines the Genoa class, representing a genoa foresail for a yacht.

Classes:
    Genoa(BaseSail):
        Represents a genoa foresail, with geometric properties and area calculation.

Typical Usage Example:
    genoa = Genoa(saildata, overlap_percent=120)
    area = genoa.area
    force = genoa.aerodynamic_force(wind_speed_knots=12)

Class Details:
    - The luff and foot are taken from saildata (genoa_i and genoa_j) if not provided.
    - The leech is estimated as the hypotenuse of luff and foot if not provided.
    - Area is calculated as 0.5 * luff * foot (foot includes overlap).
    - Inherits aerodynamic_force() from BaseSail for force estimation.
"""

from math import sqrt
from .base_sail import BaseSail


def get_val(saildata, key):
    if isinstance(saildata, dict):
        return saildata.get(key)
    return getattr(saildata, key)


class Genoa(BaseSail):
    """
    Represents a genoa foresail.

    Args:
        saildata: Data source with geometric properties (genoa_i, genoa_j).
        luff (float, optional): Luff length in meters. Defaults to sqrt(genoa_i^2 + genoa_j^2).
        leech (float, optional): Leech length in meters. Estimated if not provided.
        foot (float, optional): Foot length in meters. Defaults to genoa_j * (overlap_percent / 100).
        overlap_percent (float, optional): Overlap percentage. Defaults to 100.
        yacht_id: Optional identifier for the yacht. Passed to the BaseSail constructor.

    Attributes:
        luff (float): Length of the luff (meters).
        leech (float): Length of the leech (meters).
        foot (float): Length of the foot (meters).
        overlap_percent (float): Overlap percentage used in foot calculation.
        name (str): Name of the sail class ("Genoa").

    Methods:
        area (property): Returns the area of the sail in square meters.
        aerodynamic_force(wind_speed_knots, lift_coefficient=1.0, air_density=1.225):
            Returns the aerodynamic force (Newtons) on the sail for a given wind speed and coefficients.
    """

    def __init__(
        self,
        saildata,
        luff=None,
        leech=None,
        foot=None,
        overlap_percent=None,
        yacht_id=None,
    ):
        # Default luff: hypotenuse of I and J
        default_luff = sqrt(
            get_val(saildata, "genoa_i") ** 2 + get_val(saildata, "genoa_j") ** 2
        )
        luff = luff if luff is not None else default_luff
        overlap = overlap_percent if overlap_percent is not None else 100
        foot = (
            foot if foot is not None else get_val(saildata, "genoa_j") * (overlap / 100)
        )
        leech = leech if leech is not None else sqrt(luff**2 + foot**2)
        self.overlap_percent = overlap
        super().__init__(saildata, luff, leech, foot, yacht_id=yacht_id)

    @property
    def area(self) -> float:
        """
        Calculate the area of the genoa in square meters.
        Returns:
            float: The area of the sail (m^2).
        """
        luff_m = self._mm_to_m(self.luff)
        foot_m = self._mm_to_m(self.foot)
        return 0.5 * luff_m * foot_m

    @property
    def luff_length(self):
        """
        Returns the luff length of the genoa.
        """
        return self.luff_length
