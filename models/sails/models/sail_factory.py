from enum import Enum
from .sails.jib import Jib
from .sails.genoa import Genoa
from .sails.staysail import Staysail
from .sails.mainsail import Mainsail
from .sails.sym_spinnaker import SymSpinnaker
from .sails.asym_spinnaker import AsymSpinnaker
from .sails.code_zero import CodeZero
from .sails.trisail import Trisail

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
        SailType.TRISAIL: Trisail
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

    def add_sail_type_to_possible_on_boat(self, sail_type: SailType, config: dict = None):
        if sail_type not in self.sails_possible_on_boat:
            self.sails_possible_on_boat.append(sail_type)
        if config:
            self.sail_config[sail_type] = config

    def set_sail_config(self, sail_type: SailType, config: dict):
        self.sail_config[sail_type] = config

    def generate_all_sails_on_boat(self):
        for sail_type in self.sails_possible_on_boat:
            sail_type = SailType(sail_type)
            sail_class = self._registry[sail_type]
            config = self.sail_config.get(sail_type, {})
            self.sails[sail_type] = sail_class(self.saildata, yacht_id=self.yacht_id, **config)

    def get(self, sail_type: SailType | list[SailType]):
        if isinstance(sail_type, list):
            for st in sail_type:
                sail = self.sails.get(st)
                if sail is not None:
                    return sail
            return None
        else:
            return self.sails.get(sail_type, None)