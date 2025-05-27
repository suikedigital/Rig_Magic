"""
Base Halyard class for the Running Rigging Management system.

Provides a template for all halyard rope types, including default safety margin,
core attributes, and string representation. Subclasses must implement length and diameter calculations.
"""

from typing import Optional
from models.ropes.rope import Rope
from models.ropes.termination import Termination
from math import sqrt
from abc import ABC, abstractmethod

class Halyard(Rope, ABC):
    def __init__(self, yacht, led_aft: bool,
                 colour: Optional[str] = None,
                 construction: Optional[str] = None,
                 upper_termination: Optional[Termination] = None,
                 lower_termination: Optional[Termination] = None):
        """
        Base class for halyard ropes.

        Args:
            yacht (Yacht): Yacht instance.
            led_aft (float): Additional length for leading aft (meters).
            construction (str, optional): Rope construction.
            upper_termination (Termination, optional): Upper end termination.
            lower_termination (Termination, optional): Lower end termination.
        """
        self.safety_margin = 1.5  # meters, safety margin
        self.yacht = yacht

         # Handle led_aft as bool
        if led_aft is True:
            # Use main boom as default, or override in subclasses if needed
            self.led_aft = self.yacht.boom_above_deck + yacht.saildata.main_e
        elif led_aft is False:
            led_aft = 0.0

        self.led_aft = led_aft
        self.length = self.calc_length()
        self.diameter = self.calc_diameter()
        self.colour = colour
        super().__init__(self.length, self.diameter, colour, construction, upper_termination, lower_termination)
        self.type = "Halyard"

    def __str__(self):
        return (
            f"{self.type}:\n"
            f"{self.length}m\n"
            f"{self.diameter} mm,\n"
            f"{self.construction},\n"
            f"Colour: {self.colour}\n"
            f"Upper: {self.upper_termination}\n"
            f"Lower: {self.lower_termination}\n"
        )

    @abstractmethod
    def calc_length(self) -> float:
        """Calculate the length of the halyard."""
        pass

    @abstractmethod
    def calc_diameter(self) -> float:
        """Default diameter calculation (can be overridden)."""
        return  str(NotImplementedError("Diameter calculation not implemented for this halyard."))