from back_end.models.sails.config import SAILS_DB_PATH
from back_end.models.sails.models.sail_factory import SailFactory, SailType
from back_end.models.sails.models.database import Database
from back_end.models.saildata.saildata_service import SailDataService
from back_end.models.sails.models.sail_utils import normalize_sail_type

class SailService:
    def __init__(self, db_path=SAILS_DB_PATH):
        self.db = Database(db_path)
        self.saildata_service = SailDataService()

    def initialize_from_base(self, yacht_id, base_yacht):
        if base_yacht.mainsail is True:
            self.add_sail_type(yacht_id, "mainsail")
        if base_yacht.jib is True:
            self.add_sail_type(yacht_id, "jib")
        if base_yacht.genoa is True:
            self.add_sail_type(yacht_id, "genoa")
        if base_yacht.symmetric_spinnaker is True:
            self.add_sail_type(yacht_id, "symmetric_spinnaker")
        if base_yacht.asymmetric_spinnaker is True:
            self.add_sail_type(yacht_id, "asymmetric_spinnaker")
        if base_yacht.code_zero is True:
            self.add_sail_type(yacht_id, "codezero")
        if base_yacht.staysail is True:
            self.add_sail_type(yacht_id, "staysail")
        if base_yacht.trisail is True:
            self.add_sail_type(yacht_id, "trisail")
        if base_yacht.stormjib is True:
            self.add_sail_type(yacht_id, "storm_jib")
        self.generate_sails(yacht_id)
        print(f"Sails initialized for yacht {yacht_id} based on base yacht {base_yacht.id}.")
        
    def _get_factory(self, yacht_id):
        saildata = self.saildata_service.get_saildata(yacht_id)
        if saildata is None:
            raise ValueError(f"No saildata found for yacht_id={yacht_id}. Cannot create SailFactory.")
        return SailFactory(saildata, yacht_id)

    def add_sail_type(self, yacht_id, sail_type, config=None):
        factory = self._get_factory(yacht_id)
        sail_type_str = normalize_sail_type(sail_type)
        factory.add_sail_type_to_possible_on_boat(sail_type_str, config)
        print(f"{sail_type_str} added to possible sails on boat.")

    def set_sail_config(self, yacht_id, sail_type, config):
        factory = self._get_factory(yacht_id)
        sail_type_str = normalize_sail_type(sail_type)
        factory.set_sail_config(sail_type_str, config)

    def generate_sails(self, yacht_id):
        factory = self._get_factory(yacht_id)
        self.db.delete_sails_by_yacht(yacht_id)
        factory.generate_all_sails_on_boat()
        for sail_type, sail in factory.sails.items():
            print(f"{sail_type} generated with config: {factory.sail_config.get(sail_type, {})}")
            self.db.save_sail(sail.to_dict())

    def get_sail(self, yacht_id, sail_type):
        print(f"[DEBUG] get_sail called with yacht_id={yacht_id}, sail_type={sail_type}")
        sail_type_str = normalize_sail_type(sail_type)
        factory = self._get_factory(yacht_id)
        print(f"[DEBUG] SailFactory.sails_possible_on_boat: {factory.sails_possible_on_boat}")
        print(f"[DEBUG] SailFactory.sails: {factory.sails}")
        sail = factory.get(sail_type_str)
        print(f"[DEBUG] SailFactory.get({sail_type_str}) returned: {sail}")
        if sail:
            sail_dict = sail.to_dict()
            sail_dict["yacht_id"] = yacht_id
            return sail_dict
        return None

    def get_sails_from_db(self, yacht_id):
        rows = self.db.get_sails_by_yacht(yacht_id)
        keys = ["id", "yacht_id", "base_id", "sail_type", "luff", "leech", "foot", "area", "config"]
        result = []
        for row in rows:
            d = dict(zip(keys, row))
            d["name"] = d["sail_type"]  # Add a name field for API compatibility
            result.append(d)
        return result

    def get_aero_force(self, yacht_id, sail_type, wind_speed):
        factory = self._get_factory(yacht_id)
        sail_type_str = normalize_sail_type(sail_type)
        sail = factory.get(sail_type_str)
        if sail:
            aero_force = sail.aerodynamic_force(wind_speed)
            print(f"Aero force for {sail_type_str} at {wind_speed} m/s: {aero_force:.2f} N (yacht_id: {yacht_id})")
            return aero_force
        else:
            print(f"Sail {sail_type_str} not found for yacht {yacht_id}")
            return None