"""
JibSheet module
---------------
Defines the JibSheet class for the Running Rigging Management system.

The JibSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility.

Classes:
    JibSheet: Represents a jib sheet with sensible defaults and calculation logic.
"""

from abc import ABC, abstractmethod
from typing import Optional

from models.ropes.models.ropes.rope import Rope
from models.ropes.models.components.termination import Termination
from models.ropes.models.ropes.sheets_and_guys.sheets.base_sheet import Sheet
from models.ropes.models.components.rope_construction import RopeConstructionType


class JibSheet(Sheet):
    """
    Represents a jib sheet for a yacht.

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
    default_upper_termination = Termination(term_type="Whipping", hardware=None)
    default_lower_termination = Termination(term_type="Whipping", hardware=None)
    default_colour = "Solid Blue"

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
        Initialize a JibSheet instance.
        Calculates length if not provided, and passes all arguments to the base Sheet class.

        Args:
            yacht (Yacht): Yacht instance.
            colour (str, optional): Rope colour.
            construction_type (RopeConstructionType, optional): Rope construction type.
            diameter (int, optional): Rope diameter.
            length (float, optional): Rope length.
            side (str, optional): Side designation (e.g., Port or Starboard).
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
        self.type = "Jib Sheet"
    
    def calc_length(self, yacht) -> float:
        """
        Calculate the length of the jib sheet based on yacht dimensions.

        Args:
            yacht (Yacht): Yacht instance.

        Returns:
            float: The calculated and rounded-up length in meters.
        """
        return self.round_up_half_meter(2.2 * yacht.saildata.jib_j + 1.8 * yacht.boat_length)
        

    def calc_diameter(self) -> float:
        """
        Calculate the diameter of the sheet.

        Returns:
            float: The calculated diameter in millimeters.

        Note:
            Not yet implemented. Raises NotImplementedError.
        """
        return  str(NotImplementedError("Diameter calculation not implemented yet."))
