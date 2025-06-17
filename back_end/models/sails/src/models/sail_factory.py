import inspect
from enum import Enum
from .sails.jib import Jib
from .sails.genoa import Genoa
from .sails.staysail import Staysail
from .sails.mainsail import Mainsail
from .sails.sym_spinnaker import SymSpinnaker
from .sails.asym_spinnaker import AsymSpinnaker
from .sails.code_zero import CodeZero
from .sails.trisail import Trisail
from .database import Database
from config import SAILS_DB_PATH
from .sail_utils import normalize_sail_type


class SailType(Enum):
    JIB = "Jib"
    GENOA = "Genoa"
    STAYSAIL = "Staysail"
    CODEZERO = "CodeZero"
    MAINSAIL = "Mainsail"
    SYMSPINNAKER = "SymSpinnaker"
    ASYMSPINNAKER = "AsymSpinnaker"
    TRISAIL = "Trisail"


class SailFactory:
    _registry = {
        SailType.JIB: Jib,
        SailType.GENOA: Genoa,
        SailType.STAYSAIL: Staysail,
        SailType.CODEZERO: CodeZero,
        SailType.MAINSAIL: Mainsail,
        SailType.SYMSPINNAKER: SymSpinnaker,
        SailType.ASYMSPINNAKER: AsymSpinnaker,
        SailType.TRISAIL: Trisail,
    }

    def __init__(self, saildata: dict, yacht_id):
        self.yacht_id = yacht_id
        self.saildata = saildata
        self.sails_possible_on_boat: list[SailType] = []
        self.sail_config: dict[SailType, dict] = {}
        self.sails: dict[SailType, object] = {}

    @classmethod
    def available_types(cls) -> list[SailType]:
        return list(cls._registry.keys())

    def _normalize_type(self, sail_type):
        return normalize_sail_type(sail_type)

    def load_possible_sails_from_db(self):
        db = Database(SAILS_DB_PATH)
        possible = db.get_possible_sails(self.yacht_id)
        self.sails_possible_on_boat = []
        self.sail_config = {}
        for sail_type_str, config_str in possible:
            sail_type_str = normalize_sail_type(sail_type_str)
            sail_type = SailType(sail_type_str)
            self.sails_possible_on_boat.append(sail_type)
            if config_str:
                try:
                    config = eval(config_str)
                except Exception:
                    config = {}
                self.sail_config[sail_type] = config

    def add_sail_type_to_possible_on_boat(self, sail_type, config: dict = None):
        sail_type_str = normalize_sail_type(sail_type)
        sail_type_enum = SailType(sail_type_str)
        db = Database(SAILS_DB_PATH)
        db.save_possible_sail(self.yacht_id, sail_type_enum.value, config)
        self.load_possible_sails_from_db()

    def set_sail_config(self, sail_type, config: dict):
        sail_type_str = normalize_sail_type(sail_type)
        sail_type_enum = SailType(sail_type_str)
        db = Database(SAILS_DB_PATH)
        db.save_possible_sail(self.yacht_id, sail_type_enum.value, config)
        self.load_possible_sails_from_db()

    def generate_all_sails_on_boat(self):
        self.load_possible_sails_from_db()
        if not isinstance(self.saildata, dict):
            raise ValueError(
                f"No saildata found for yacht_id={self.yacht_id}. Cannot generate sails."
            )
        for sail_type in self.sails_possible_on_boat:
            sail_class = self._registry[sail_type]
            config = self.sail_config.get(sail_type, {})
            # Filter config to only valid kwargs for the sail class
            sig = inspect.signature(sail_class.__init__)
            valid_keys = set(sig.parameters.keys()) - {"self"}
            filtered_config = {k: v for k, v in config.items() if k in valid_keys}
            # Validation for Genoa
            if sail_type.value == "Genoa":
                required = ["genoa_i", "genoa_j"]
                missing = [k for k in required if k not in self.saildata]
                if missing:
                    raise ValueError(f"Missing required saildata for Genoa: {missing}")
            # ...add similar checks for other sail types as needed...
            self.sails[sail_type] = sail_class(
                self.saildata, yacht_id=self.yacht_id, **filtered_config
            )

    def get(self, sail_type):
        sail_type_str = normalize_sail_type(sail_type)
        sail_type_enum = SailType(sail_type_str)
        print(
            f"[DEBUG] SailFactory.get called with sail_type={sail_type_enum} (type: {type(sail_type_enum)})"
        )
        print(f"[DEBUG] SailFactory.sails keys: {list(self.sails.keys())}")
        sail = self.sails.get(sail_type_enum, None)
        print(
            f"[DEBUG] SailFactory.get: trying sail_type={sail_type_enum}, found: {sail}"
        )
        if sail is not None:
            return sail
        # Try to reconstruct from DB if not in memory
        db = Database(SAILS_DB_PATH)
        row = db.get_sail_by_yacht_and_type(self.yacht_id, sail_type_enum.value)
        if row:
            keys = [
                "id",
                "yacht_id",
                "base_id",
                "sail_type",
                "luff",
                "leech",
                "foot",
                "area",
                "config",
            ]
            sail_dict = dict(zip(keys, row))
            sail_class = self._registry[sail_type_enum]
            config = (
                eval(sail_dict.get("config", "{}")) if sail_dict.get("config") else {}
            )
            sail_obj = sail_class(self.saildata, yacht_id=self.yacht_id, **config)
            self.sails[sail_type_enum] = sail_obj
            print(
                f"[DEBUG] SailFactory.get: reconstructed {sail_type_enum} from DB: {sail_obj}"
            )
            return sail_obj
        print(f"[DEBUG] SailFactory.get: could not find {sail_type_enum} in DB either")
        return None
