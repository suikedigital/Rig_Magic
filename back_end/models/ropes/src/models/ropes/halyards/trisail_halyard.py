"""
TrisailHalyard class for the Running Rigging Management system.

Represents a trisail halyard with sensible defaults for terminations and colour.
Calculates length based on yacht sail data and allows per-instance overrides.
"""

from typing import Optional
from math import sqrt

from .base_halyard import Halyard
from ...components.termination import Termination
from ...components.rope_construction import RopeConstructionType

class TrisailHalyard(Halyard):
    default_upper_termination = Termination(term_type="Covered Splice", hardware="Shackle")
    default_lower_termination = Termination(term_type="Pull Through Whipping", hardware=None)
    default_colour = "Purple Fleck"
    default_construction = RopeConstructionType.BRAID_BRAID
    halyard_angle_deg = 10

    def __init__(self, yacht_id, saildata, HALYARD_TO_SAIL, wind_speed_in_knots, led_aft: float,
                 length_safety_margin: float = 1.0,
                 construction_type: RopeConstructionType = None,
                 diameter: int = None,
                 length: float = None,
                 colour: Optional[str] = None,
                 upper_termination: Optional[Termination] = None,
                 lower_termination: Optional[Termination] = None,
                 halyard_load_safety_factor: float = 1.25,
                 dynamic_load_safety_factor: float = 1.5,
                 sail_service=None,
                 **kwargs):
        self.type = self.__class__.__name__
        """
        Initialize a Trisail Halyard.

        If diameter is not provided, it is automatically calculated based on sail load, construction, and safety factors.

        Args:
            yacht (Yacht): Yacht instance.
            led_aft (float): Additional length for leading aft (meters).
            construction_type (RopeConstructionType, optional): Rope construction type.
            diameter (int, optional): Rope diameter.
            colour (str, optional): Rope colour.
            upper_termination (Termination, optional): Upper end termination.
            lower_termination (Termination, optional): Lower end termination.
            halyard_load_safety_factor (float, optional): Safety factor for halyard load.
            dynamic_load_safety_factor (float, optional): Safety factor for dynamic load.
            sail_service (optional): Sail service information.
        """
        if colour is None:
            colour = self.default_colour
        if upper_termination is None:
            upper_termination = self.default_upper_termination
        if lower_termination is None:
            lower_termination = self.default_lower_termination
        if construction_type is None:
            construction_type = self.default_construction

        self.yacht_id = yacht_id
        self.sail_service = sail_service
        self.saildata = saildata
        self.halyard_load_safety_factor = halyard_load_safety_factor
        self.dynamic_load_safety_factor = dynamic_load_safety_factor
        self.led_aft = led_aft
        self.length_safety_margin = length_safety_margin 
        self.construction_type = construction_type
        if diameter is None:
            diameter = self.calc_diameter(HALYARD_TO_SAIL, wind_speed_in_knots)
        
        length = self.calc_length(saildata, led_aft, self.length_safety_margin) if length is None else length

        super().__init__(
            yacht_id=yacht_id,
            saildata=saildata,
            led_aft=led_aft,
            construction_type=construction_type,
            diameter=diameter,
            length=length,
            colour=colour,
            upper_termination=upper_termination,
            lower_termination=lower_termination,
            halyard_load_safety_factor=halyard_load_safety_factor,
            dynamic_load_safety_factor=dynamic_load_safety_factor,
            sail_service=sail_service,
            **kwargs
        )
        self.sync_construction_diameter()

    def calc_length(self, saildata, led_aft, length_safety_margin) -> float:
        """
        Calculate the length of the trisail halyard.

        Returns:
            float: The halyard length, rounded up to the nearest 0.5 meter.
        """
        raw_length = (
            saildata["trisail_i"]
            + sqrt(saildata["trisail_i"] ** 2 + saildata["trisail_j"] ** 2)
            + led_aft
            + length_safety_margin
        )
        return self.round_up_half_meter(raw_length)