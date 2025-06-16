"""
base_sail.py
------------
This module defines the BaseSail abstract base class, representing the base for all sails in the running rigging system.

Classes:
    BaseSail(ABC):
        Abstract base class for sails, providing common logic for area calculation and aerodynamic force estimation.

Typical Usage Example:
    class MySail(BaseSail):
        @property
        def area(self):
            return ...
    sail = MySail(saildata, luff, leech, foot)
    area = sail.area
    force = sail.aerodynamic_force(wind_speed_knots=12)

Class Details:
    - Subclasses must implement the area property.
    - Provides aerodynamic_force() for force estimation.
"""

from abc import ABC, abstractmethod


class BaseSail(ABC):
    """
    Abstract base class for sails.

    Attributes:
        saildata: Arbitrary data or configuration for the sail (often from the yacht).
        luff (float): Length of the luff (meters).
        leech (float): Length of the leech (meters).
        foot (float): Length of the foot (meters).
        name (str): Name of the sail class (defaults to class name).

    Methods:
        area (property): Abstract property. Returns the area of the sail in square meters. Must be implemented by subclasses.
        aerodynamic_force(wind_speed_knots, lift_coefficient=1.0, air_density=1.225):
            Returns the aerodynamic force (Newtons) on the sail for a given wind speed and coefficients.
    """

    def __init__(self, saildata, luff: float, leech: float, foot: float, yacht_id=None, **kwargs):
        """
        Initialize a sail with its geometric properties.

        Args:
            saildata: Arbitrary data or configuration for the sail (often from the yacht).
            luff (float): Length of the luff (meters).
            leech (float): Length of the leech (meters).
            foot (float): Length of the foot (meters).
        """
        self.saildata = saildata
        self.name = self.__class__.__name__
        self.luff = luff
        self.leech = leech
        self.foot = foot
        self.yacht_id = yacht_id
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    @abstractmethod
    def area(self) -> float:
        """
        Calculate the sail area in square meters.
        Must be implemented by all subclasses.
        """
        pass

    def aerodynamic_force(self, wind_speed_knots: float, lift_coefficient: float = 1.0, air_density: float = 1.225) -> float:
        """
        Estimate the aerodynamic force (in Newtons) acting on a sail.

        Args:
            wind_speed_knots (float): Apparent wind speed in knots (required, user-supplied).
            lift_coefficient (float): Aerodynamic lift coefficient (default 1.0).
            air_density (float): Air density in kg/m³ (default 1.225 at sea level).

        Returns:
            float: Force on sail in Newtons (N).

        Formula:
            F = 0.5 * rho * A * C_L * V^2
            where:
                rho = air_density (kg/m³)
                A = sail area (m²)
                C_L = lift_coefficient
                V = wind speed (m/s)
        """
        wind_speed_mps = wind_speed_knots * 0.514444  # Convert knots to m/s
        return 0.5 * air_density * self.area * lift_coefficient * (wind_speed_mps ** 2)

    def to_dict(self):
        # Standard fields
        result = {
            "yacht_id": self.yacht_id,
            "name": getattr(self, "name", self.__class__.__name__),
            "luff": self.luff,
            "leech": self.leech,
            "foot": self.foot,
            "area": self.area,
        }
        # Collect extra kwargs (exclude standard fields and saildata)
        exclude = {"name", "luff", "leech", "foot", "area", "saildata", "yacht_id"}
        kwargs = {k: v for k, v in self.__dict__.items() if k not in exclude}
        result["kwargs"] = kwargs
        return result

    def _mm_to_m(self, val):
        """Convert mm to meters if value is likely in mm (val > 100)."""
        return val / 1000 if val and val > 100 else val