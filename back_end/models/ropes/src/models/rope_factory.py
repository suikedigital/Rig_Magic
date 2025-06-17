"""
rope_factory.py
---------------
Factory for creating rope objects based on type and configuration in the running rigging management system.

- Maps rope type names to rope classes
- Instantiates rope objects with correct parameters
- Used by RopeService and other modules to generate ropes dynamically
"""

"""
RunningRigging module
---------------------
This module defines the RunningRigging class, representing the running rigging system for a yacht.

The RunningRigging class manages dynamic rope instantiation, configuration overrides, automatic port/starboard pairing, and provides robust error handling for rope retrieval.

Classes:
    RunningRigging: Manages a yacht's running rigging system.
"""

from .database import RopeDatabase
from config import ROPES_DB_PATH
from .rope_utils import normalize_rope_type
from .ropes.halyards.main_halyard import MainHalyard
from .ropes.halyards.jib_halyard import JibHalyard
from .ropes.halyards.genoa_halyard import GenoaHalyard
from .ropes.halyards.staysail_halyard import StaysailHalyard
from .ropes.halyards.spinnaker_halyard import SpinnakerHalyard
from .ropes.halyards.code_zero_halyard import CodeZeroHalyard
from .ropes.halyards.topping_lift_halyard import ToppingLiftHalyard
from .ropes.halyards.trisail_halyard import TrisailHalyard
from .ropes.sheets_and_guys.sheets.mainsheet import Mainsheet
from .ropes.sheets_and_guys.sheets.jib_sheet import JibSheet
from .ropes.sheets_and_guys.sheets.genoa_sheet import GenoaSheet
from .ropes.sheets_and_guys.sheets.staysail_sheet import StaysailSheet
from .ropes.sheets_and_guys.sheets.sym_spinnaker_sheet import SymSpinSheet
from .ropes.sheets_and_guys.sheets.asym_spinnaker_sheet import AsymSpinSheet
from .ropes.sheets_and_guys.sheets.code_zero_sheet import CodeZeroSheet
from .ropes.sheets_and_guys.sheets.trisail_sheet import TrisailSheet
from .ropes.sheets_and_guys.guys.sym_spin_guy import SymSpinGuy


class Factory:
    """
    Manages a yacht's running rigging system.

    Attributes:
        yacht (Yacht): Yacht instance.
        sail_wardrobe (SailWardrobe): Sail wardrobe instance.
        ropes (dict): Dictionary of rope instances keyed by rope type.

    Args:
        yacht (Yacht): Yacht instance.
        sail_wardrobe (SailWardrobe): Sail wardrobe instance.
        rigging_config (dict, optional): Configuration overrides for ropes.
    """

    # Registry of available rope types for the Running Rigging Management system.
    # Maps class name strings to rope (halyard/sheet/guy) classes.
    _ROPE_REGISTRY = {
        # Halyard classes
        "MainsailHalyard": MainHalyard,
        "GenoaHalyard": GenoaHalyard,
        "JibHalyard": JibHalyard,
        "SpinnakerHalyard": SpinnakerHalyard,
        "CodeZeroHalyard": CodeZeroHalyard,
        "StaysailHalyard": StaysailHalyard,
        "ToppingLiftHalyard": ToppingLiftHalyard,
        "TrisailHalyard": TrisailHalyard,
        # Sheet classes
        "AsymSpinSheet": AsymSpinSheet,
        "CodeZeroSheet": CodeZeroSheet,
        "GenoaSheet": GenoaSheet,
        "JibSheet": JibSheet,
        "Mainsheet": Mainsheet,
        "StaysailSheet": StaysailSheet,
        "TrisailSheet": TrisailSheet,
        "SymSpinSheet": SymSpinSheet,
        # Guy classes
        "SymSpinGuy": SymSpinGuy,
        # Add more as needed
    }

    _SHEET_TO_SAIL = {
        "GenoaSheet": "Genoa",
        "MainSheet": "Mainsail",
        "JibSheet": "Jib",
        "SymSpinSheet": "Spinnaker",
        "AsymSpinSheet": "Spinnaker",
        "CodeZeroSheet": "CodeZero",
        "StormJibSheet": "StormJib",
        "TrisailSheet": "Trisail",
        # Add more as needed
    }

    _HALYARD_TO_SHEET = {
        "MainsailHalyard": ["MainSheet"],
        "GenoaHalyard": ["GenoaSheet"],
        "JibHalyard": ["JibSheet"],
        "SpinnakerHalyard": ["SymSpinSheet", "AsymSpinSheet", "SymSpinGuy"],
        "CodeZeroHalyard": ["CodeZeroSheet"],
        "StaysailHalyard": ["StaysailSheet"],
        "TrisailHalyard": ["TrisailSheet"],
        # Add more as needed
    }

    _HALYARD_TO_SAIL = {
        "GenoaHalyard": ["Genoa"],
        "MainHalyard": ["Mainsail"],
        "MainsailHalyard": ["Mainsail"],
        "JibHalyard": ["Jib"],
        "SpinnakerHalyard": ["AsymSpinnaker", "SymSpinnaker"],
        "CodeZeroHalyard": ["CodeZero"],
        "TrisailHalyard": ["Trisail"]
    }

    def __init__(self, yacht_id, saildata, sail_service, wind_speed_in_knots=30, halyard_load_safety_factor=1.25, dynamic_load_safety_factor=1.5, length_safety_factor=1.2):
        """
        Initialize RunningRigging for a yacht.

        Args:
            yacht: The Yacht instance this running rigging belongs to.
        """
        self.yacht_id = yacht_id

        self.saildata = saildata

        self.sail_service = sail_service

        self.rope_types = []      # List of rope type names (e.g., ["MainHalyard"])
        self.led_aft = {}         # Dict: rope_type (str) -> led aft length (float)
        self.rope_config = {}     # Dict: rope_type (str) -> config dict (construction, color, etc.)
        self.ropes = {}           # Dict: rope_type (str) -> Rope instance

        self.halyard_load_safety_factor = halyard_load_safety_factor  # Safety factor for halyard loads
        self.dynamic_load_safety_factor = dynamic_load_safety_factor  # Safety factor for dynamic loads

        self.length_safety_factor = length_safety_factor  # Safety factors for halyard length
        self.wind_speed_in_knots = wind_speed_in_knots

    def _to_classname(self, rope_type):
        # DEPRECATED: Use normalize_rope_type instead
        return normalize_rope_type(rope_type)

    def add_rope_type(self, rope_type, led_aft: float = 0.0):
        """
        Add a rope type to the yacht and specify its led aft length.

        Args:
            rope_type: RopeType enum or class name string (e.g., "MainHalyard").
            led_aft: Length (in meters) the rope is led aft. Default is 0.0.
        """
        rope_type_str = normalize_rope_type(rope_type)
        if rope_type_str not in self.rope_types:
            self.rope_types.append(rope_type_str)
        self.led_aft[rope_type_str] = led_aft

    def add_halyard_and_sheets(self, rope_type, led_aft):
        """
        Add a halyard and its corresponding sheets and guys (always as port and starboard pairs) to the yacht.

        Args:
            rope_type: RopeType enum or class name string (e.g., "GenoaHalyard").
            led_aft: Length (in meters) the halyard is led aft.
        """
        rope_type_str = self._to_classname(rope_type)
        self.add_rope_type(rope_type_str, led_aft=led_aft)
        for child in Factory._HALYARD_TO_SHEET.get(rope_type_str, []):
            # If it's a sheet or guy, add both port and starboard if needed
            if child.endswith("Sheet") or child.endswith("Guy"):
                for side in ["Port", "Starboard"]:
                    child_name = f"{child}_{side}" if f"{child}_{side}" in Factory._ROPE_REGISTRY else child
                    self.add_rope_type(child_name)
            else:
                self.add_rope_type(child)

    def load_possible_ropes_from_db(self):
        db = RopeDatabase(ROPES_DB_PATH)
        possible = db.get_possible_ropes(self.yacht_id)
        self.rope_types = []
        self.rope_config = {}
        self.led_aft = {}
        for rope_type_str, config_str in possible:
            rope_type_str = normalize_rope_type(rope_type_str)
            self.rope_types.append(rope_type_str)
            config = {}
            if config_str:
                try:
                    config = eval(config_str)
                except Exception:
                    config = {}
            self.rope_config[rope_type_str] = config

    def add_rope_type_to_possible_on_boat(self, rope_type, led_aft=0.0, config=None):
        rope_type_str = normalize_rope_type(rope_type)
        db = RopeDatabase(ROPES_DB_PATH)
        db.save_possible_rope(self.yacht_id, rope_type_str, config)
        self.load_possible_ropes_from_db()
        self.led_aft[rope_type_str] = led_aft

    def set_rope_config(self, rope_type, config: dict):
        rope_type_str = normalize_rope_type(rope_type)
        db = RopeDatabase(ROPES_DB_PATH)
        db.save_possible_rope(self.yacht_id, rope_type_str, config)
        self.load_possible_ropes_from_db()

    def generate_all_ropes_on_boat(self, rope_registry=None):
        self.load_possible_ropes_from_db()
        if rope_registry is None:
            rope_registry = Factory._ROPE_REGISTRY
        for rope_type in self.rope_types:
            rope_type_str = normalize_rope_type(rope_type)
            config = self.rope_config.get(rope_type_str, {})
            led_aft = self.led_aft.get(rope_type_str, 0.0)
            rope_class = rope_registry.get(rope_type_str)
            if rope_class is None:
                raise KeyError(f"Rope class for '{rope_type_str}' not found in registry.")
            rope = rope_class(
                yacht_id=self.yacht_id,
                saildata=self.saildata,
                HALYARD_TO_SAIL=Factory._HALYARD_TO_SAIL,
                wind_speed_in_knots=self.wind_speed_in_knots,
                led_aft=led_aft,
                halyard_load_safety_factor=self.halyard_load_safety_factor,
                dynamic_load_safety_factor=self.dynamic_load_safety_factor,
                sail_service=self.sail_service,
                **config
            )
            self.ropes[rope_type_str] = rope

    def get(self, rope_type):
        """
        Retrieve a rope by its type.

        Args:
            rope_type: RopeType enum or class name string.

        Returns:
            Rope: The requested rope instance.

        Raises:
            KeyError: If the rope type does not exist in the registry.
        """
        rope_type_str = normalize_rope_type(rope_type)
        print(f"[DEBUG] Factory.get: rope_type_str={rope_type_str}, available={list(self.ropes.keys())}")
        if rope_type_str not in self.ropes:
            # Try to regenerate ropes from DB if missing
            self.generate_all_ropes_on_boat()
            print(f"[DEBUG] Factory.get: After regeneration, available={list(self.ropes.keys())}")
            if rope_type_str not in self.ropes:
                raise KeyError(f"Rope type '{rope_type_str}' not found in running rigging.")
        return self.ropes[rope_type_str]
