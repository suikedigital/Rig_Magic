"""
Sheet module
------------
This module defines the Sheet class, representing the base class for all sheets in the running rigging system.

The Sheet class provides common logic for sheet construction, default terminations, and extensibility for specific sheet types.

Classes:
    Sheet: Abstract base class for sheet ropes.
"""

from abc import ABC, abstractmethod
from typing import Optional
from models.ropes_rigging.models.ropes.rope import Rope
from models.ropes_rigging.models.components.termination import Termination
from models.ropes_rigging.models.components.rope_construction import RopeConstructionType



class Sheet(Rope, ABC):
    """
    Abstract base class for sheet ropes.

    Attributes:
        default_upper_termination (Termination): Default upper termination (spliced to shackle or snap shackle).
        default_lower_termination (Termination): Default lower termination (whipped).
        default_colour (str): Default rope colour.

    Args:
        yacht (Yacht): Yacht instance.
        colour (str, optional): Rope colour. Defaults to class default.
        construction (str, optional): Rope construction. Defaults to None.
        upper_termination (Termination, optional): Upper end termination. Defaults to class default.
        lower_termination (Termination, optional): Lower end termination. Defaults to class default.
        side (str, optional): Side of the yacht (port/starboard). Defaults to None.
        **kwargs: Additional keyword arguments for extensibility.
    """
    def __init__(self, yacht, 
                 construction_type: RopeConstructionType, 
                 diameter: int, 
                 length: float, 
                 side: Optional[str] = None,
                 colour: str = None, 
                 upper_termination: Termination = None, 
                 lower_termination: Termination = None, 
                 **kwargs):
        """
        Base class for sheet ropes.

        Args:
            yacht (Yacht): Yacht instance.
            construction_type (RopeConstructionType): The construction type of the rope.
            diameter (int): The diameter of the rope.
            length (float): The length of the rope.
            side (str, optional): Sheet side ("Port" or "Starboard").
        """
        self.safety_margin = 1.5  # meters, safety margin
        self.yacht = yacht
        self.construction_type = construction_type
        self.diameter = diameter
        self.length = length
        self.side = side
        self.colour = colour
        self.upper_termination = upper_termination
        self.lower_termination = lower_termination
        super().__init__(yacht=yacht, construction_type=construction_type, diameter=diameter, length=length, colour=colour, upper_termination=upper_termination, lower_termination=lower_termination, **kwargs)
        self.type = "Sheet"

    def __str__(self):
        """
        Return a string representation of the sheet rope, including type, length, diameter, construction, colour, and terminations.
        """
        side_str = f" ({self.side})" if self.side else ""
        return (
            f"{self.type}{side_str}:\n"
            f"{self.length}m\n"
            f"{self.diameter} mm,\n"
            f"{self.construction},\n"
            f"Colour: {self.colour}\n"
            f"Upper: {self.upper_termination}\n"
            f"Lower: {self.lower_termination}\n"
        )
    
    @abstractmethod
    def calc_length(self) -> float:
        """
        Abstract method to calculate the length of the sheet.

        Returns:
            float: The calculated length in meters.
        """
        pass

    @abstractmethod
    def calc_diameter(self) -> float:
        """
        Abstract method to calculate the diameter of the sheet.

        Returns:
            float: The calculated diameter in millimeters.
        """
        return  str(NotImplementedError("Diameter calculation not implemented yet."))

    def break_strength(self):
        """
        Calculate the break strength of the sheet based on its construction.

        Returns:
            The total break strength.
        """
        return self.construction.total_break_strength()
