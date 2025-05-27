"""
Base class for all sheet rope types in the Running Rigging Management system.

This module defines the Sheet class, which serves as the abstract base for all sheet ropes (e.g., GenoaSheet, MainSheet, JibSheet, etc.).

Classes:
    Sheet: Abstract base class for sheet ropes, providing common initialization and interface for length/diameter calculation.
"""

from abc import ABC, abstractmethod
from typing import Optional
from models.ropes.rope import Rope
from models.ropes.termination import Termination



class Sheet(Rope, ABC):
    """
    Abstract base class for all sheet rope types.

    Provides common initialization logic and enforces implementation of length and diameter calculation methods.

    Args:
        yacht (Yacht): Yacht instance.
        colour (str, optional): Rope colour.
        construction (str, optional): Rope construction.
        upper_termination (Termination, optional): Upper end termination.
        lower_termination (Termination, optional): Lower end termination.
        **kwargs: Additional keyword arguments for extensibility.

    Attributes:
        safety_margin (float): Safety margin in meters (default: 1.5).
        yacht (Yacht): Reference to the yacht instance.
        length (float): Calculated length of the sheet (meters).
        diameter (float): Calculated diameter of the sheet (millimeters).
        colour (str): Colour of the rope.
        type (str): Rope type label (default: "Sheet").
    """
    def __init__(self, yacht, 
                 colour: Optional[str] = None,
                 construction: Optional[str] = None,
                 upper_termination: Optional[Termination] = None,
                 lower_termination: Optional[Termination] = None,
                 side: Optional[str] = None,
                 **kwargs):
        """
        Base class for sheet ropes.

        Args:
            yacht (Yacht): Yacht instance.
            led_aft (bool): Whether the sheet is led aft.
            colour (str, optional): Rope colour.
            construction (str, optional): Rope construction.
            upper_termination (Termination, optional): Upper end termination.
            lower_termination (Termination, optional): Lower end termination.
            side (str, optional): Sheet side ("Port" or "Starboard").
        """
        self.safety_margin = 1.5  # meters, safety margin
        self.yacht = yacht
        self.side = side
        self.length = self.calc_length()
        self.diameter = self.calc_diameter()
        self.colour = colour
        super().__init__(self.length, self.diameter, colour, construction, upper_termination, lower_termination)
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
