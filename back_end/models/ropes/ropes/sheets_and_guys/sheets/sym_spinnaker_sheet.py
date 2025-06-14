"""
SymSpinSheet module
------------------
Defines the SymSpinSheet class for the Running Rigging Management system.

The SymSpinSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

Classes:
    SymSpinSheet: Represents a symmetric spinnaker sheet with sensible defaults and calculation logic.
"""

from typing import Optional

from models.ropes.components.rope_construction import RopeConstructionType
from models.ropes.components.termination import Termination
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
    default_colour = "Solid yellow"
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
        Initialize a SymSpinSheet instance.
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

    def calc_diameter(self):
        """Return a sensible default or implement logic as needed."""
        return 10

    def calc_length(self, yacht):
        """
        Calculate the length of the symmetric spinnaker sheet based on yacht dimensions.
        """
        return round_up_half_meter(3.0 * yacht.saildata.spin_j + 2.5 * yacht.boat_length)
