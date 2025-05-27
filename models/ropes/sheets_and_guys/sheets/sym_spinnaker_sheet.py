"""
SymSpinSheet module
------------------
Defines the SymSpinSheet class for the Running Rigging Management system.

The SymSpinSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

Classes:
    SymSpinSheet: Represents a symmetric spinnaker sheet with sensible defaults and calculation logic.
"""

from typing import Optional

from models.ropes.termination import Termination
from models.ropes.sheets_and_guys.sheets.base_sheet import Sheet

from utils.calculations import round_up_half_meter


class SymSpinSheet(Sheet):
    """
    Represents a symmetric spinnaker sheet for a yacht.

    Provides sensible defaults for colour and terminations, and implements length calculation logic.
    Designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

    Attributes:
        default_upper_termination (Termination): Default upper termination (spliced to snap shackle).
        default_lower_termination (Termination): Default lower termination (whipped).
        default_colour (str): Default rope colour.

    Args:
        yacht (Yacht): Yacht instance.
        colour (str, optional): Rope colour. Defaults to class default.
        construction (str, optional): Rope construction. Defaults to None.
        upper_termination (Termination, optional): Upper end termination. Defaults to class default.
        lower_termination (Termination, optional): Lower end termination. Defaults to class default.
        **kwargs: Additional keyword arguments for extensibility.
    """
    default_upper_termination = Termination(term_type="Splice", hardware="Small-Bail Snap Shackle")
    default_lower_termination = Termination(term_type="Whipping", hardware=None)
    default_colour = "Solid yellow"

    def __init__(self, yacht, 
                 colour: Optional[str] = None,
                 construction: Optional[str] = None,
                 upper_termination: Optional[Termination] = None,
                 lower_termination: Optional[Termination] = None,
                 **kwargs):
        """
        Initialize a Symetric Spin Sheet.

        Args:
            yacht (Yacht): Yacht instance.
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
        super().__init__(yacht, colour, construction, upper_termination, lower_termination)
        self.type = "Symetric Spinnaker Sheet"
    
    def calc_length(self) -> float:
        """
        Calculate the length of the symmetric spinnaker sheet.

        Returns:
            float: The calculated and rounded-up length in meters.
        """
        raw_length = (self.yacht.boat_length * 2) + self.safety_margin
        return round_up_half_meter(raw_length)
        

    def calc_diameter(self) -> float:
        """
        Calculate the diameter of the sheet.

        Returns:
            float: The calculated diameter in millimeters.

        Note:
            Not yet implemented. Raises NotImplementedError.
        """
        return  str(NotImplementedError("Diameter calculation not implemented yet."))
