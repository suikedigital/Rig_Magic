"""
Base Rope class for the Running Rigging Management system.

Defines default construction, terminations, and colour for all ropes.
Provides string representation and placeholder calculation methods.
"""

from typing import Optional
from models.ropes.termination import Termination

class Rope:
    default_upper_termination = Termination(term_type="Whipping", hardware="None")
    default_lower_termination = Termination(term_type="Whipping", hardware="None")
    default_construction = "Braid on Braid"

    def __init__(self, length: float, diameter: float, colour: str,
                 construction: Optional[str]=None,
                 upper_termination: Optional[Termination] = None,
                 lower_termination: Optional[Termination] = None):
        """
        Initialize a Rope instance.

        Args:
            length (float): Rope length in meters.
            diameter (float): Rope diameter in mm.
            colour (str): Rope colour.
            construction (str, optional): Rope construction type (e.g., 'Braid on Braid').
            upper_termination (Termination, optional): Upper rope end termination.
            lower_termination (Termination, optional): Lower rope end termination.
        """
        if construction is None:
            construction = self.default_construction
        self.length = length
        self.diameter = diameter
        self.construction = construction
        self.upper_termination = upper_termination
        self.lower_termination = lower_termination
        self.colour = colour

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