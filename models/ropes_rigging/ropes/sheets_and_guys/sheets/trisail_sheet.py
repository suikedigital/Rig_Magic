"""
TrisailSheet module
------------------
Defines the TrisailSheet class for the Running Rigging Management system.

The TrisailSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

Classes:
    TrisailSheet: Represents a trisail sheet with sensible defaults and calculation logic.
"""

from typing import Optional

from models.ropes_rigging.components.rope_construction import RopeConstructionType
from models.ropes_rigging.components.termination import Termination
from models.ropes.sheets_and_guys.sheets.base_sheet import Sheet

from utils.calculations import round_up_half_meter


class TrisailSheet(Sheet):
    """
    Represents a trisail sheet for a yacht.

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
    default_colour = "Solid Orange"

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
        Initialize a TrisailSheet instance.
        Calculates length if not provided, and passes all arguments to the base Sheet class.

        Args:
            yacht (Yacht): Yacht instance.
            colour (str, optional): Rope colour.
            construction_type (RopeConstructionType, optional): Rope construction type.
            diameter (int, optional): Diameter of the rope.
            length (float, optional): Length of the sheet.
            side (str, optional): Side of the yacht (e.g., "Port" or "Starboard").
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
        self.type = "Trisail Sheet"
    
    def calc_length(self, yacht) -> float:
        """
        Calculate the length of the trisail sheet based on yacht dimensions.

        Args:
            yacht (Yacht): Yacht instance.

        Returns:
            float: The calculated and rounded-up length in meters.
        """
        return round_up_half_meter(1.8 * yacht.saildata.trisail_j + 1.5 * yacht.boat_length)
        

    def calc_diameter(self) -> float:
        """
        Calculate the diameter of the sheet.

        Returns:
            float: The calculated diameter in millimeters.

        Note:
            Not yet implemented. Raises NotImplementedError.
        """
        return  str(NotImplementedError("Diameter calculation not implemented yet."))
