from models.yacht.yacht import Yacht
from models.ropes.termination import Termination
from models.ropes.rope_registry import ROPE_REGISTRY

def main():
    try:
        yacht = Yacht(i=20.0, j=5, p=11.0, e=3.5, boom_above_deck=1.0, boat_length=8.0)

        # Test 1: Add halyards only (no sheets)
        yacht.running_rigging.add_rope_type("MainHalyard", led_aft=True)
        yacht.running_rigging.add_rope_type("JibHalyard", led_aft=False)

        # Test 2: Add halyard and corresponding sheet(s) in one go
        yacht.running_rigging.add_rope_and_sheet("GenoaHalyard", led_aft=True)
        yacht.running_rigging.add_rope_and_sheet("SpinnakerHalyard", led_aft=True)

        # Custom configs
        yacht.running_rigging.set_rope_config("MainHalyard", {"construction": "Dyneema Core", "colour": "Red"})
        yacht.running_rigging.set_rope_config("JibHalyard", {"construction": "Polyester", "colour": "Green"})
        yacht.running_rigging.set_rope_config("SpinnakerHalyard", {"colour": "Purple Fleck"})
        yacht.running_rigging.set_rope_config("MainSheet", {"colour": "Black", "construction": "Polyester"})
        yacht.running_rigging.set_rope_config("GenoaSheet", {"colour": "Blue", "construction": "Polyester"})

        # Generate and print
        yacht.running_rigging.generate_ropes(ROPE_REGISTRY)
        print("\n--- Generated Running Rigging ---\n")
        for rope_type, rope in yacht.running_rigging.ropes.items():
            print(f"{rope_type}:\n{rope}\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()