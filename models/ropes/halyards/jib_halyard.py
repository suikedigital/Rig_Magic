"""
JibHalyard class for the Running Rigging Management system.

Represents a Jib halyard with sensible defaults for terminations and colour.
Calculates length based on yacht sail data and allows per-instance overrides.
"""

from typing import Optional
from math import sqrt
from utils.calculations import round_up_half_meter

from models.ropes.halyards.base_halyard import Halyard
from models.ropes.termination import Termination

class JibHalyard(Halyard):
    default_upper_termination = Termination(term_type="Covered Splice", hardware="Snap Shackle")
    default_lower_termination = Termination(term_type="Pull Through Whipping", hardware=None)
    default_colour = "Blue Fleck"

    def __init__(self, yacht, led_aft: float, 
                 colour: Optional[str] = None, 
                 construction: Optional[str] = None, 
                 upper_termination: Optional[Termination] = None,
                 lower_termination: Optional[Termination] = None):
        """
        Initialize a Jib Halyard.

        Args:
            yacht (Yacht): Yacht instance.
            led_aft (float): Additional length for leading aft (meters).
            colour (str, optional): Rope colour.
            construction (str, optional): Rope construction.
            upper_termination (Termination, optional): Upper end termination.
            lower_termination (Termination, optional): Lower end termination.
        """
        if colour is None:
            colour = self.default_colour
        if upper_termination is None:
            upper_termination = self.default_upper_termination
        if lower_termination is None:
            lower_termination = self.default_lower_termination
        super().__init__(yacht, led_aft, colour, construction, upper_termination, lower_termination)
        self.type = "Jib Halyard"

    def calc_length(self) -> float:
        """
        Calculate the length of the Jib halyard.

        Returns:
            float: The halyard length, rounded up to the nearest 0.5 meter.
        """
        raw_length = (
            self.yacht.saildata.jib_i
            + sqrt(self.yacht.saildata.jib_i ** 2 + self.yacht.saildata.jib_j ** 2)
            + self.led_aft
            + self.safety_margin
        )
        return round_up_half_meter(raw_length)

    def calc_diameter(self):
        """
        Placeholder for diameter calculation.
        Returns:
            str: NotImplementedError message.
        """
        return str(NotImplementedError("Diameter calculation not implemented yet"))