"""
CodeZeroHalyard class for the Running Rigging Management system.

Represents a Code Zero halyard with sensible defaults for terminations and colour.
Calculates length based on yacht sail data and allows per-instance overrides.
"""

from typing import Optional
from math import sqrt

from .base_halyard import Halyard
from ...components.termination import Termination
from ...components.rope_construction import RopeConstructionType


class CodeZeroHalyard(Halyard):
    default_upper_termination = Termination(
        term_type="Covered Splice", hardware="Swivel Shackle"
    )
    default_lower_termination = Termination(
        term_type="Pull Through Whipping", hardware=None
    )
    default_colour = "Black Fleck"
    default_construction = RopeConstructionType.BRAID_BRAID
    halyard_angle_deg = 20

    def __init__(
        self,
        yacht_id,
        saildata,
        HALYARD_TO_SAIL,
        wind_speed_in_knots,
        led_aft: float,
        length_safety_margin: float = 1.0,
        construction_type: RopeConstructionType = None,
        diameter: int = None,
        length: float = None,
        colour: str = None,
        upper_termination: Optional[Termination] = None,
        lower_termination: Optional[Termination] = None,
        halyard_load_safety_factor: float = 1.25,
        dynamic_load_safety_factor: float = 1.5,
        sail_service=None,
        **kwargs
    ):
        if colour is None:
            colour = self.default_colour
        if upper_termination is None:
            upper_termination = self.default_upper_termination
        if lower_termination is None:
            lower_termination = self.default_lower_termination
        if construction_type is None:
            construction_type = self.default_construction
        self.led_aft = led_aft
        self.length_safety_margin = length_safety_margin
        # Call base class init first to set safety factors
        super().__init__(
            yacht_id=yacht_id,
            construction_type=construction_type,
            diameter=None,  # Will set after
            length=None,  # Will set after
            colour=colour,
            upper_termination=upper_termination,
            lower_termination=lower_termination,
            halyard_load_safety_factor=halyard_load_safety_factor,
            dynamic_load_safety_factor=dynamic_load_safety_factor,
            sail_service=sail_service,
            **kwargs
        )
        # Now calculate diameter and length using the correct safety factors
        self.length = self.calc_length(saildata, led_aft, length_safety_margin)
        self.diameter = self.calc_diameter(HALYARD_TO_SAIL, wind_speed_in_knots)
        self.sync_construction_diameter()

    def calc_length(self, saildata, led_aft, length_safety_margin) -> float:
        """
        Calculate the length of the Code Zero halyard.

        Returns:
            float: The halyard length, rounded up to the nearest 0.5 meter.
        """
        raw_length = (
            saildata.codezero_i
            + sqrt(saildata.codezero_i**2 + saildata.codezero_j**2)
            + led_aft
            + length_safety_margin
        )
        return self.round_up_half_meter(raw_length)

    def is_complete(self):
        """
        Check if the halyard instance has all the necessary attributes set.

        Returns:
            bool: True if the instance is complete, False otherwise.
        """
        return all(
            attr is not None
            for attr in (
                self.length,
                self.diameter,
                self.material,
                self.cover,
                self.core,
                self.termination,
                self.construction,
                self.breaking_load,
                self.stretch,
                self.weight,
                self.price,
                self.notes,
            )
        )
