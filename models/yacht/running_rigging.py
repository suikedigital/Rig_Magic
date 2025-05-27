from models.ropes.rope_registry import ROPE_REGISTRY, HALYARD_TO_SHEET

class RunningRigging:
    """
    Manages all running rigging (ropes) for a yacht.

    Responsibilities:
        - Stores which rope types the yacht has (e.g., MainHalyard, GenoaHalyard).
        - Tracks whether each rope is led aft and by how much.
        - Stores configuration details for each rope (construction, color, terminals, etc.).
        - Generates and stores actual rope instances using a rope registry.

    Attributes:
        yacht: The Yacht instance this running rigging belongs to.
        rope_types: List of rope type names present on the yacht.
        led_aft: Dict mapping rope type to led aft length (float, in meters).
        rope_config: Dict mapping rope type to configuration dictionary.
        ropes: Dict mapping rope type to the generated Rope instance.
    """

    def __init__(self, yacht):
        """
        Initialize RunningRigging for a yacht.

        Args:
            yacht: The Yacht instance this running rigging belongs to.
        """
        self.yacht = yacht
        self.rope_types = []      # List of rope type names (e.g., ["MainHalyard"])
        self.led_aft = {}         # Dict: rope_type -> led aft length (float)
        self.rope_config = {}     # Dict: rope_type -> config dict (construction, color, etc.)
        self.ropes = {}           # Dict: rope_type -> Rope instance

    def add_rope_type(self, rope_type: str, led_aft: float = 0.0):
        """
        Add a rope type to the yacht and specify its led aft length.

        Args:
            rope_type: Name of the rope type (e.g., "MainHalyard").
            led_aft: Length (in meters) the rope is led aft. Default is 0.0.
        """
        if rope_type not in self.rope_types:
            self.rope_types.append(rope_type)
        self.led_aft[rope_type] = led_aft

    def add_rope_and_sheet(self, rope_type, led_aft):
        """
        Add a halyard and its corresponding sheets and guys (always as port and starboard pairs) to the yacht.

        Args:
            rope_type: Name of the halyard type (e.g., "GenoaHalyard").
            led_aft: Length (in meters) the halyard is led aft.
        """
        self.add_rope_type(rope_type, led_aft=led_aft)
        for child in HALYARD_TO_SHEET.get(rope_type, []):
            # If it's a sheet or guy, add both port and starboard
            if child.endswith("Sheet") or child.endswith("Guy"):
                for side in ["Port", "Starboard"]:
                    child_name = f"{child}_{side}"
                    self.add_rope_type(child_name)
            else:
                self.add_rope_type(child)

    def set_rope_config(self, rope_type: str, config: dict):
        """
        Set the configuration dictionary for a specific rope type.

        Args:
            rope_type: Name of the rope type.
            config: Dictionary of configuration parameters (e.g., construction, color, terminals).
        """
        self.rope_config[rope_type] = config

    def generate_ropes(self, rope_registry):
        """
        Generate Rope instances for all rope types using the provided registry.

        Args:
            rope_registry: Dictionary mapping rope type names to Rope classes.

        Side Effects:
            Populates self.ropes with Rope instances for each rope type.
        """
        for rope_type in self.rope_types:
            # Check for port/starboard sheet or guy naming
            if rope_type.endswith("_Port") or rope_type.endswith("_Starboard"):
                base_type, side = rope_type.rsplit('_', 1)
                rope_class = rope_registry[base_type]
                config = self.rope_config.get(rope_type, self.rope_config.get(base_type, {}))
                led_aft = self.led_aft.get(rope_type, self.led_aft.get(base_type, 0.0))
                rope = rope_class(self.yacht, led_aft=led_aft, side=side, **config)
                self.ropes[rope_type] = rope
            else:
                rope_class = rope_registry[rope_type]
                config = self.rope_config.get(rope_type, {})
                led_aft = self.led_aft.get(rope_type, 0.0)
                rope = rope_class(self.yacht, led_aft=led_aft, **config)
                self.ropes[rope_type] = rope
