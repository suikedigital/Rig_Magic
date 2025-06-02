"""
base_halyard.py
---------------
Abstract base class for all halyard rope types in the running rigging management system.

Provides shared logic for:
- Load calculation (including safety factors)
- Length calculation (abstract method)
- Diameter calculation and RopeConstruction synchronization
- Default terminations and color

All halyard subclasses should inherit from this class and implement their own calc_length method.
"""

"""
BaseHalyard module
-----------------
This module defines the BaseHalyard class, representing the base class for all halyards in the running rigging system.

The BaseHalyard class provides common logic for halyard construction, default terminations, and dynamic diameter calculation based on sail load and yacht configuration.

Classes:
    BaseHalyard: Abstract base class for halyard ropes.
"""

from typing import Optional
from math import radians, sin

from models.ropes.models.ropes.rope import Rope
from models.ropes.models.components.termination import Termination
from abc import ABC, abstractmethod
from models.ropes.models.components.rope_construction import RopeConstruction, RopeConstructionType


class Halyard(Rope, ABC):
    """
    Abstract base class for halyard ropes.

    Attributes:
        default_upper_termination (Termination): Default upper termination (spliced to shackle).
        default_lower_termination (Termination): Default lower termination (whipped).
        default_colour (str): Default rope colour.
        halyard_angle_deg (float): Default halyard angle in degrees.

    Args:
        yacht (Yacht): Yacht instance.
        colour (str, optional): Rope colour. Defaults to class default.
        construction (str, optional): Rope construction. Defaults to None.
        upper_termination (Termination, optional): Upper end termination. Defaults to class default.
        lower_termination (Termination, optional): Lower end termination. Defaults to class default.
        **kwargs: Additional keyword arguments for extensibility.
    """
    halyard_angle_deg = 15  # Default angle, can be overridden in subclasses
    def __init__(self, yacht_id, construction_type: RopeConstructionType, diameter: int, length: float, 
                 halyard_load_safety_factor: float, dynamic_load_safety_factor: float, sail_service, colour: str = None, 
                 upper_termination: Termination = None, lower_termination: Termination = None, **kwargs):
        """
        Base class for halyard ropes.

        Args:
            yacht (Yacht): Yacht instance.
            led_aft (float): Additional length for leading aft (meters).
            construction (str, optional): Rope construction.
            upper_termination (Termination, optional): Upper end termination.
            lower_termination (Termination, optional): Lower end termination.
            length (float): Rope length in meters.
        """
        
        self.yacht_id = yacht_id
        self.halyard_angle_deg = getattr(self, 'halyard_angle_deg', 15)
        self.construction_type = construction_type
        self.diameter = diameter
        self.colour = colour
        self.upper_termination = upper_termination
        self.lower_termination = lower_termination
        self.halyard_load_safety_factor = halyard_load_safety_factor
        self.dynamic_load_safety_factor = dynamic_load_safety_factor
        self.sail_service = sail_service
        if 'length' in kwargs:
            kwargs.pop('length')
        super().__init__(yacht_id=yacht_id, construction_type=construction_type, diameter=diameter, length=length, colour=colour, upper_termination=upper_termination, lower_termination=lower_termination, **kwargs)

    def __str__(self):
        return (
            f"{self.type}:\n"
            f"{self.length}m\n"
            f"{self.diameter} mm,\n"
            f"{self.construction},\n"
            f"Colour: {self.colour}\n"
            f"Upper: {self.upper_termination}\n"
            f"Lower: {self.lower_termination}\n"
        )

    @abstractmethod
    def calc_length(self) -> float:
        """Calculate the length of the halyard."""
        pass

    def calc_load(self, HALYARD_TO_SAIL, wind_speed_knots):
        sail_names = HALYARD_TO_SAIL[self.__class__.__name__]
        max_load = 0
        for sail_name in sail_names:
            sail = self.sail_service.get_sail(self.yacht_id, sail_name)
            if sail is None:
                continue
            aero_force_newtons = self.sail_service.get_aero_force(sail["name"], wind_speed_knots)
            load_n = ((aero_force_newtons * sin(radians(self.halyard_angle_deg))) * self.halyard_load_safety_factor) * self.dynamic_load_safety_factor
            load_kg = load_n / 9.80665
            if load_kg > max_load:
                max_load = load_kg
        if max_load == 0:
            raise ValueError(f"No valid sails found for {self.__class__.__name__} on yacht {self.yacht_id}")
        return max_load

    def calc_diameter(self, HALYARD_TO_SAIL, wind_speed_knots) -> int:
        """
        Calculate the minimum rope diameter that meets the required working load for this halyard.
        Also sets self.required_wl_kg for database export.
        Returns:
            int: The calculated diameter in millimeters.
        """
        required_wl = self.calc_load(HALYARD_TO_SAIL, wind_speed_knots)
        self.required_wl_kg = required_wl  # Expose for database
        print(f"[DEBUG] {self.__class__.__name__}: required working load = {required_wl:.2f} kg")
        diameters = [6, 7, 8, 10, 12, 14]
        for d in diameters:
            if self.construction_type:
                construction = RopeConstruction(self.construction_type, d)
                break_strength = construction.total_break_strength()
                print(f"[DEBUG] {self.__class__.__name__}: diameter {d} mm, break strength = {break_strength:.2f} kg")
                if break_strength >= required_wl:
                    self.diameter = d
                    self.construction = construction
                    self.sync_construction_diameter()
                    return d
        raise ValueError(f"No suitable diameter found for {self.type} with required working load {required_wl:.1f} kg.")

    def _get_materials_from_construction(self):
        """
        Helper to map the construction string to core and cover materials.
        Returns (core_material, cover_material)
        """
        # Default logic: if 'dyneema' in construction, use dyneema core, else braid
        # If 'polyester' or 'braid' in construction, use braid cover, else None
        cstr = (self.construction or '').lower()
        if 'dyneema' in cstr:
            core_material = 'dyneema'
        else:
            core_material = 'braid'
        if 'polyester' in cstr or 'braid' in cstr:
            cover_material = 'braid'
        elif 'dyneema' in cstr:
            cover_material = 'dyneema'
        else:
            cover_material = None
        return core_material, cover_material

    def sync_construction_diameter(self):
        """
        Ensure the RopeConstruction object reflects the current diameter.
        """
        if hasattr(self, 'construction') and self.construction is not None:
            self.construction.diameter = self.diameter
