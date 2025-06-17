"""
AsymSpinSheet module
-------------------
This module defines the AsymSpinSheet class, representing an asymmetric spinnaker sheet for a yacht's running rigging system.

The AsymSpinSheet class provides sensible defaults for construction, colour, and terminations, and implements logic for calculating sheet length. It is designed to be instantiated dynamically via the rope registry, supporting configuration overrides and extensibility.

Classes:
    AsymSpinSheet: Represents an asymmetric spinnaker sheet with sensible defaults and calculation logic.
"""

from typing import Optional

from ....components.rope_construction import RopeConstructionType
from ....components.termination import Termination
from .base_sheet import Sheet


class AsymSpinSheet(Sheet):
    """
    Represents an asymmetric spinnaker sheet for a yacht's running rigging system.

    This class provides sensible defaults for rope colour and end terminations, and implements logic for calculating the sheet's length. It is designed for dynamic instantiation via the rope registry, supporting configuration overrides and extensibility for different yacht setups.

    Attributes:
        default_upper_termination (Termination): Default upper termination (spliced to snap shackle).
        default_lower_termination (Termination): Default lower termination (whipped).
        default_colour (str): Default rope colour (solid red).

    Args:
        yacht (Yacht): The yacht instance this sheet is associated with.
        colour (str, optional): Rope colour. If None, uses default_colour.
        construction (str, optional): Rope construction type. If None, uses default.
        upper_termination (Termination, optional): Upper end termination. If None, uses default_upper_termination.
        lower_termination (Termination, optional): Lower end termination. If None, uses default_lower_termination.
        side (str, optional): Side of the yacht (port/starboard). Used for automatic pairing. Defaults to None.
        **kwargs: Additional keyword arguments for extensibility.
    """

    default_colour = "Solid Red"
    default_construction = RopeConstructionType.BRAID_BRAID
    default_upper_termination = Termination(
        term_type="Covered Splice", hardware="Snap Shackle"
    )
    default_lower_termination = Termination(
        term_type="Pull Through Whipping", hardware=None
    )

    def __init__(
        self,
        yacht,
        colour: Optional[str] = None,
        construction_type: RopeConstructionType = None,
        diameter: int = None,
        length: float = None,
        side: Optional[str] = None,
        upper_termination: Optional[Termination] = None,
        lower_termination: Optional[Termination] = None,
        **kwargs
    ):
        """
        Initialize an AsymSpinSheet instance.
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
        Calculate the length of the asymmetric spinnaker sheet based on yacht dimensions.

        The length is typically twice the yacht's length plus a safety margin, then rounded up to the nearest half meter.

        Args:
            yacht (Yacht): The yacht instance this sheet is associated with.

        Returns:
            float: The calculated and rounded-up length in meters.
        """
        # Example: 2.8 * J + 2.2 * LOA (can be adjusted as needed)
        return self.round_up_half_meter(
            2.8 * yacht.saildata.spin_j + 2.2 * yacht.boat_length
        )

    def calc_diameter(self):
        """
        Calculate the diameter of the sheet.

        Returns:
            float: The calculated diameter in millimeters.

        Note:
            Not yet implemented. Raises NotImplementedError.
        """
        return str(NotImplementedError("Diameter calculation not implemented yet."))
