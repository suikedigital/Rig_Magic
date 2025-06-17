"""
Rope module
-----------
This module defines the Rope class, representing the base class for all ropes in the running rigging system.

The Rope class now uses RopeConstructionType and diameter for all strength and construction logic, following the new preset-based design.

Classes:
    Rope: Abstract base class for all running rigging ropes.
"""

import math

from ..components.termination import Termination
from ..components.rope_construction import RopeConstruction, RopeConstructionType


class Rope:
    """
    Abstract base class for all running rigging ropes.

    Attributes:
        yacht (Yacht): Yacht instance.
        construction_type (RopeConstructionType): Rope construction type (preset).
        diameter (int): Rope diameter in mm.
        length (float): Rope length in meters.
        construction (RopeConstruction): Rope construction object.
        type (str): Rope type.

    Args:
        yacht (Yacht): Yacht instance.
        construction_type (RopeConstructionType): Rope construction type.
        diameter (int): Rope diameter in mm.
        length (float): Rope length in meters.
        colour (str, optional): Rope colour.
        upper_termination (Termination, optional): Upper termination object.
        lower_termination (Termination, optional): Lower termination object.
        **kwargs: Additional keyword arguments for extensibility.
    """

    def __init__(
        self,
        yacht_id,
        construction_type: RopeConstructionType,
        diameter: int,
        length: float,
        colour: str = None,
        upper_termination: Termination = None,
        lower_termination: Termination = None,
        **kwargs,
    ):
        self.yacht = yacht_id
        self.construction_type = construction_type
        self.diameter = diameter
        self.length = length
        self.colour = colour
        self.upper_termination = upper_termination
        self.lower_termination = lower_termination
        self.construction = RopeConstruction(
            construction_type=construction_type, diameter=diameter
        )
        self.type = getattr(self, "type", self.__class__.__name__)

    def break_strength(self):
        """
        Returns the breaking strain (kg) for this rope, using the preset table.
        """
        return self.construction.total_break_strength()

    def __str__(self):
        return (
            f"{self.type}: {self.length}m x {self.diameter} mm,\n"
            f"{self.construction}, Colour: {self.colour}\n"
            f"Upper: {self.upper_termination}\n  Lower: {self.lower_termination}"
        )

    def calc_length(self):
        """
        Placeholder for rope length calculation logic.
        Returns:
            float: The rope's length.
        """
        return self.length

    def calc_diameter(self):
        """
        Placeholder for rope diameter calculation logic.
        Returns:
            float: The rope's diameter.
        """
        return self.diameter

    def round_up_half_meter(self, value: float) -> float:
        """
        Round up a value to the nearest half meter.

        Args:
            value (float): The value to round up.

        Returns:
            float: The value rounded up to the nearest 0.5 meter.
        """
        return math.ceil(value * 2) / 2
