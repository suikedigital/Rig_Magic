"""
rope_service.py
---------------
Main service for rope generation, management, and regeneration in the running rigging management system.

- Generates all ropes for a yacht based on configuration and sail data
- Handles safety factor propagation and rope recalculation
- Integrates with RopeFactory and RopeDatabase
- Provides API for retrieving and updating ropes
"""

from models.ropes_rigging.models.rope_factory import Factory
from models.ropes_rigging.models.database import RopeDatabase

class RopeService:
    """
    Service class for managing ropes on a yacht.
    """
    def __init__(self, saildata: dict, sail_service, wind_speed_in_knots=30, halyard_load_safety_factor=4, dynamic_load_safety_factor=2, length_safety_factor=2):
        self.factory = Factory(
            yacht_id=saildata['yacht_id'],
            saildata=saildata,
            sail_service=sail_service,
            wind_speed_in_knots=wind_speed_in_knots,
            halyard_load_safety_factor=halyard_load_safety_factor,
            dynamic_load_safety_factor=dynamic_load_safety_factor,
            length_safety_factor=length_safety_factor,
        )
        self.db = RopeDatabase()

    def add_rope_type(self, rope_type, led_aft=0.0):
        self.factory.add_rope_type(rope_type, led_aft)
        return f"{rope_type} added to possible ropes on boat."

    def add_halyard_and_sheets(self, halyard_type, led_aft):
        self.factory.add_halyard_and_sheets(halyard_type, led_aft)
        return f"{halyard_type} and its sheets added with led aft length {led_aft}."

    def set_rope_config(self, rope_type, config):
        self.factory.set_rope_config(rope_type, config)
        return f"Configuration for {rope_type} set to {config}."

    def generate_ropes(self):
        self.factory.generate_all_ropes_on_boat()
        # Force recalculation of diameter for all ropes (in case safety factors changed)
        for rope_type, rope in self.factory.ropes.items():
            # Only recalculate if the rope has a calc_diameter method
            if hasattr(rope, 'calc_diameter'):
                # This will also update required_wl_kg
                try:
                    # Use the current safety factors and wind speed
                    diameter = rope.calc_diameter(self.factory._HALYARD_TO_SAIL, self.factory.wind_speed_in_knots)
                    rope.diameter = diameter
                except Exception as e:
                    print(f"Warning: Could not recalculate diameter for {rope_type}: {e}")
            print(f"{rope_type} generated with config: {self.factory.rope_config.get(rope_type, {})} and diameter: {getattr(rope, 'diameter', None)}")
        # Save all ropes to the database after generation using RopeDatabase class
        self.db.save_ropes(self.factory.ropes)
        self.db.conn.commit()

    def get_rope(self, rope_type):
        return self.factory.get(rope_type)

def close(self):
    """
    Close the database connection.
    """
    RopeDatabase.close()
    print("Rope database connection closed.")