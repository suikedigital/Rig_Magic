"""
AsymSpinSheet module
-------------------
This module defines the AsymSpinSheet class, representing an asymmetric spinnaker sheet for a yacht's running rigging system.

The AsymSpinSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed to be instantiated dynamically via the rope registry, supporting configuration overrides and extensibility.

Classes:
    AsymSpinSheet: Represents an asymmetric spinnaker sheet with sensible defaults and calculation logic.
"""

from typing import Optional

from models.ropes.models.components.termination import Termination
from models.ropes.models.ropes.sheets_and_guys.guys.base_guy import Guy


class SymSpinGuy(Guy):
    """
    Represents an asymmetric spinnaker sheet for a yacht.

    This class provides sensible defaults for colour and terminations, and implements length calculation logic.
    It is designed to be instantiated dynamically via the rope registry, supporting configuration overrides and extensibility.

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
    default_colour = "Solid Green"

    def __init__(self, yacht, 
                 colour: Optional[str] = None,
                 construction: Optional[str] = None,
                 upper_termination: Optional[Termination] = None,
                 lower_termination: Optional[Termination] = None,
                 side: Optional[str] = None,
                 **kwargs):
        """
        Initialize an SymSpinSheet instance.

        Args:
            yacht (Yacht): Yacht instance.
            colour (str, optional): Rope colour. If None, uses default_colour.
            construction (str, optional): Rope construction.
            upper_termination (Termination, optional): Upper end termination. If None, uses default_upper_termination.
            lower_termination (Termination, optional): Lower end termination. If None, uses default_lower_termination.
            side (str, optional): Side of the yacht (e.g., 'port' or 'starboard'). Defaults to None.
            **kwargs: Additional keyword arguments for extensibility.
        """
        if colour is None:
            colour = self.default_colour
        if upper_termination is None:
            upper_termination = self.default_upper_termination
        if lower_termination is None:
            lower_termination = self.default_lower_termination
        super().__init__(yacht, colour, construction, upper_termination, lower_termination, side=side, **kwargs)
        self.type = "Asymetric Spinnaker Sheet"
    
    def calc_length(self) -> float:
        """
        Calculate the length of the asymmetric spinnaker sheet.

        Returns:
            float: The calculated and rounded-up length in meters.
        """
        raw_length = (self.yacht.boat_length * 2.5) + self.safety_margin
        return self.round_up_half_meter(raw_length)
        
    def calc_diameter(self) -> float:
        """
        Calculate the diameter of the sheet.

        Returns:
            float: The calculated diameter in millimeters.

        Note:
            Not yet implemented. Raises NotImplementedError.
        """
        return  str(NotImplementedError("Diameter calculation not implemented yet."))
