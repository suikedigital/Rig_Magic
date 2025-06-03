"""
GenoaSheet module
-----------------
Defines the GenoaSheet class for the Running Rigging Management system.

The GenoaSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

Classes:
    GenoaSheet: Represents a genoa sheet with sensible defaults and calculation logic.
"""

from typing import Optional

from models.ropes_rigging.models.ropes.rope import Rope
from models.ropes_rigging.models.components.termination import Termination
from models.ropes_rigging.models.ropes.sheets_and_guys.sheets.base_sheet import Sheet
from models.ropes_rigging.models.components.rope_construction import RopeConstructionType



class GenoaSheet(Sheet):
    """
    Represents a genoa sheet for a yacht.

    Provides sensible defaults for colour and terminations, and implements length calculation logic.
    Designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

    Attributes:
        default_upper_termination (Termination): Default upper termination (whipped).
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
    default_colour = "Red"
    default_construction = RopeConstructionType.BRAID_BRAID
    default_upper_termination = Termination(term_type="Covered Splice", hardware="Snap Shackle")
    default_lower_termination = Termination(term_type="Pull Through Whipping", hardware=None)

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
        Initialize a GenoaSheet instance.
        Calculates length if not provided, and passes all arguments to the base Sheet class.
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

    def calc_length(self, yacht):
        """
        Calculate the length of the genoa sheet based on yacht dimensions.

        Args:
            yacht (Yacht): The yacht instance to calculate the sheet length for.

        Returns:
            float: The calculated and rounded-up length in meters.
        """
        # Use yacht.saildata.j and yacht.saildata.boat_length
        return self.round_up_half_meter(2.5 * yacht.saildata.genoa_j + 2.0 * yacht.boat_length)
        

    def calc_diameter(self):
        """
        Calculate the diameter of the sheet.

        Returns:
            float: The calculated diameter in millimeters.

        Note:
            Not yet implemented. Raises NotImplementedError.
        """
        return  str(NotImplementedError("Diameter calculation not implemented yet."))
