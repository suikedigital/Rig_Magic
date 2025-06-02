"""
jib.py
------
This module defines the Jib class, representing a jib foresail for a yacht.

Classes:
    Jib(BaseSail):
        Represents a jib foresail, with geometric properties and area calculation.

Typical Usage Example:
    jib = Jib(saildata)
    area = jib.area
    force = jib.aerodynamic_force(wind_speed_knots=12)

Class Details:
    - The luff and foot are taken from saildata (jib_i and jib_j) if not provided.
    - The leech is estimated as the hypotenuse of luff and foot if not provided.
    - Area is calculated as 0.5 * luff * foot.
    - Inherits aerodynamic_force() from BaseSail for force estimation.
"""
from math import sqrt
from .base_sail import BaseSail

class Jib(BaseSail):
    """
    Represents a jib foresail.

    Args:
        saildata: Data source with geometric properties (jib_i, jib_j).
        luff (float, optional): Luff length in meters. Defaults to sqrt(jib_i^2 + jib_j^2).
        leech (float, optional): Leech length in meters. Estimated if not provided.
        foot (float, optional): Foot length in meters. Defaults to jib_j.
        yacht_id: Optional identifier for the yacht.

    Attributes:
        luff (float): Length of the luff (meters).
        leech (float): Length of the leech (meters).
        foot (float): Length of the foot (meters).
        name (str): Name of the sail class ("Jib").

    Methods:
        area (property): Returns the area of the sail in square meters.
        aerodynamic_force(wind_speed_knots, lift_coefficient=1.0, air_density=1.225):
            Returns the aerodynamic force (Newtons) on the sail for a given wind speed and coefficients.
    """
    def __init__(self, saildata, luff=None, leech=None, foot=None, yacht_id=None):
        # Default luff: hypotenuse of I and J
        default_luff = sqrt(saildata["jib_i"] ** 2 + saildata["jib_j"] ** 2)
        luff = luff if luff is not None else default_luff
        foot = foot if foot is not None else saildata["jib_j"]
        # Estimate leech as sqrt(luff^2 + foot^2) if not provided
        leech = leech if leech is not None else sqrt(luff ** 2 + foot ** 2)
        super().__init__(saildata, luff, leech, foot, yacht_id=yacht_id)

    @property
    def area(self) -> float:
        """
        Calculate the area of the jib foresail in square meters.
        Returns:
            float: The area of the sail (m^2).
        """
        return 0.5 * self.luff * self.foot