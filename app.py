"""
Main entry point for the yacht running rigging and sail management system.

This script demonstrates how to create a yacht, configure its sail wardrobe and running rigging,
override sail and rope configurations, and generate all sails and ropes using the registry system.
It also shows how to use the RopeConstructionType enum for robust rope construction overrides.

Example usage:
    $ python app.py
"""

from models.yacht.yacht import Yacht
from models.registry.rope_registry import ROPE_REGISTRY
from models.sails.sail_registry import SAIL_REGISTRY
from models.ropes.components.rope_construction import RopeConstructionType


def main():
    try:
        # Create a yacht with basic dimensions
        yacht = Yacht(i=20.0, j=5, p=11.0, e=3.5, boom_above_deck=1.0, boat_length=8.0)

        # --- SailWardrobe Example ---
        yacht.sailwardrobe.add_sail_type("Mainsail")
        yacht.sailwardrobe.add_sail_type("Genoa")
        yacht.sailwardrobe.add_sail_type("Jib")
        yacht.sailwardrobe.add_sail_type("AsymSpinnaker")
        # User can override any dimension if desired:
        yacht.sailwardrobe.set_sail_config("Genoa", {"luff": 15.2, "foot": 5.1})
        yacht.sailwardrobe.generate_sails(SAIL_REGISTRY)
        print("\n--- Generated Sails ---\n")
        for sail_type, sail in yacht.sailwardrobe.sails.items():
            print(f"{sail_type}: luff={sail.luff}, foot={sail.foot}, leech={sail.leech}, area={sail.area():.2f} m^2")

        # --- Running Rigging Example ---
        yacht.running_rigging.add_rope_type("MainHalyard", led_aft=True)
        yacht.running_rigging.add_rope_and_sheet("GenoaHalyard", led_aft=True)
        yacht.running_rigging.add_rope_and_sheet("SpinnakerHalyard", led_aft=True)
        # Use the new construction_type enum for overrides
        yacht.running_rigging.set_rope_config("MainHalyard", {"construction_type": RopeConstructionType.DYNEEMA_BRAID, "colour": "Red"})
        yacht.running_rigging.set_rope_config("GenoaSheet_Port", {"colour": "Blue", "construction_type": RopeConstructionType.BRAID_BRAID})
        yacht.running_rigging.generate_ropes(ROPE_REGISTRY)
        print("\n--- Generated Running Rigging ---\n")
        for rope_type, rope in yacht.running_rigging.ropes.items():
            print(f"{rope_type}:\n{rope}\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()