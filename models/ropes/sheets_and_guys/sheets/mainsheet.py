"""
MainSheet module
---------------
Defines the MainSheet class for the Running Rigging Management system.

The MainSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

Classes:
    MainSheet: Represents a mainsheet with sensible defaults and calculation logic.
"""

from typing import Optional

from models.ropes.termination import Termination
from models.ropes.sheets_and_guys.sheets.base_sheet import Sheet

from utils.calculations import round_up_half_meter


class MainSheet(Sheet):
    """
    Represents a mainsheet for a yacht.

    Provides sensible defaults for colour and terminations, and implements length calculation logic.
    Designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

    Attributes:
        default_upper_termination (Termination): Default upper termination (spliced).
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
    default_upper_termination = Termination(term_type="Splice", hardware=None)
    default_lower_termination = Termination(term_type="Whipping", hardware=None)
    default_colour = "White"

    def __init__(self, yacht, 
                 colour: Optional[str] = None,
                 construction: Optional[str] = None,
                 upper_termination: Optional[Termination] = None,
                 lower_termination: Optional[Termination] = None,
                 **kwargs):
        """
        Initialize a MainSheet.

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
        self.type = "Asymetric Spinnaker Sheet"
    
    def calc_length(self) -> float:
        """
        Calculate the length of the mainsheet.

        Returns:
            float: The calculated and rounded-up length in meters.
        """
        raw_length = (self.yacht.saildata * 2 * self.yacht.mainsheet_purchase) + self.safety_margin
        if self.yacht.mainsheet.type == "German":
            raw_length *= 2
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
