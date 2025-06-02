"""
trisail.py
----------
This module defines the Trisail class, representing a storm trisail for a yacht.

Classes:
    Trisail(BaseSail):
        Represents a storm trisail, with geometric properties and area calculation.

Typical Usage Example:
    trisail = Trisail(saildata)
    area = trisail.area
    force = trisail.aerodynamic_force(wind_speed_knots=12)

Class Details:
    - The luff and foot are taken from saildata (trisail_i and trisail_j) if not provided.
    - The leech is estimated as the hypotenuse of luff and foot if not provided.
    - Area is calculated as 0.5 * luff * foot.
    - Inherits aerodynamic_force() from BaseSail for force estimation.
"""
from math import sqrt
from .base_sail import BaseSail

class Trisail(BaseSail):
    """
    Represents a storm trisail.

    Args:
        saildata: Data source with geometric properties (trisail_i, trisail_j).
        luff (float, optional): Luff length in meters. Defaults to saildata.trisail_i.
        leech (float, optional): Leech length in meters. Estimated if not provided.
        foot (float, optional): Foot length in meters. Defaults to saildata.trisail_j.
        yacht_id: Optional identifier for the yacht.

    Attributes:
        luff (float): Length of the luff (meters).
        leech (float): Length of the leech (meters).
        foot (float): Length of the foot (meters).
        name (str): Name of the sail class ("Trisail").

    Methods:
        area (property): Returns the area of the sail in square meters.
        aerodynamic_force(wind_speed_knots, lift_coefficient=1.0, air_density=1.225):
            Returns the aerodynamic force (Newtons) on the sail for a given wind speed and coefficients.
    """
    def __init__(self, saildata, luff=None, leech=None, foot=None, yacht_id=None):
        luff = luff if luff is not None else saildata["trisail_i"]
        foot = foot if foot is not None else saildata["trisail_j"]
        leech = leech if leech is not None else sqrt(luff ** 2 + foot ** 2)
        super().__init__(saildata, luff, leech, foot, yacht_id=yacht_id)

    @property
    def area(self) -> float:
        """
        Calculate the area of the storm trisail in square meters.
        Returns:
            float: The area of the sail (m^2).
        """
        return 0.5 * self.luff * self.foot
