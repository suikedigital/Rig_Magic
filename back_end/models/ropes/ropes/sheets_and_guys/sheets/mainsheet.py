"""
MainSheet module
---------------
Defines the MainSheet class for the Running Rigging Management system.

The MainSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

Classes:
    MainSheet: Represents a mainsheet with sensible defaults and calculation logic.
"""

from typing import Optional

from ...components.termination import Termination
from .base_sheet import Sheet
from ...components.rope_construction import RopeConstructionType

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
                 construction_type: RopeConstructionType = None,
                 diameter: int = None,
                 length: float = None,
                 side: Optional[str] = None,
                 upper_termination: Optional[Termination] = None,
                 lower_termination: Optional[Termination] = None,
                 **kwargs):
        """
        Initialize a MainSheet instance.
        Calculates length if not provided, and passes all arguments to the base Sheet class.

        Args:
            yacht (Yacht): Yacht instance.
            colour (str, optional): Rope colour.
            construction_type (RopeConstructionType, optional): Rope construction type.
            diameter (int, optional): Diameter of the sheet.
            length (float, optional): Length of the sheet.
            side (str, optional): Side of the sheet.
            upper_termination (Termination, optional): Upper end termination.
            lower_termination (Termination, optional): Lower end termination.
        """
        if length is None:
            self.length = self.calc_length(yacht)
        else:
            self.length = length
        super().__init__(
            yacht=yacht,
            construction_type=construction_type or self.default_construction,
            diameter=diameter,
            length=self.length,
            side=side,
            colour=colour or self.default_colour,
            upper_termination=upper_termination or self.default_upper_termination,
            lower_termination=lower_termination or self.default_lower_termination,
            **kwargs
        )
        self.type = "Asymetric Spinnaker Sheet"
    
    def calc_diameter(self):
        """Return a sensible default or implement logic as needed."""
        return 10

    def calc_length(self, yacht) -> float:
        """
        Calculate the length of the mainsheet based on yacht dimensions.

        Args:
            yacht (Yacht): Yacht instance.

        Returns:
            float: The calculated and rounded-up length in meters.
        """
        # Example: 2.0 * E + 1.5 * LOA (can be adjusted as needed)
        return round_up_half_meter(2.0 * yacht.saildata.main_e + 1.5 * yacht.boat_length)
