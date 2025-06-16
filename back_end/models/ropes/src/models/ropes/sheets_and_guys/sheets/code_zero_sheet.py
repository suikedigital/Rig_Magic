"""
CodeZeroSheet module
-------------------
Defines the CodeZeroSheet class for the Running Rigging Management system.

The CodeZeroSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

Classes:
    CodeZeroSheet: Represents a Code Zero sheet with sensible defaults and calculation logic.
"""

from typing import Optional

from ....components.rope_construction import RopeConstructionType
from ....components.termination import Termination
from .base_sheet import Sheet



class CodeZeroSheet(Sheet):
    """
    Represents a Code Zero sheet for a yacht.

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
    default_colour = "Purple"
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
        Initialize a CodeZeroSheet instance.
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
        Calculate the length of the Code Zero sheet based on yacht dimensions.
        """
        return self.round_up_half_meter(2.6 * yacht.saildata.codezero_j + 2.1 * yacht.boat_length)
        

    def calc_diameter(self):
        """Return a sensible default or implement logic as needed."""
        return 10
