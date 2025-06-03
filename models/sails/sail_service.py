from models.sails.models.sail_factory import SailFactory, SailType
from models.sails.models.database import Database

class SailService:
    def __init__(self, saildata: dict, yacht_id, db_path="data/sails.db"):
        self.yacht_id = yacht_id
        self.sail_factory = SailFactory(saildata, yacht_id=yacht_id)
        self.db = Database(db_path)

    def add_sail_type(self, sail_type, config=None):
        sail_type = SailType(sail_type)
        self.sail_factory.add_sail_type_to_possible_on_boat(sail_type, config)
        print(f"{sail_type} added to possible sails on boat.")

    def set_sail_config(self, sail_type, config):
        sail_type = SailType(sail_type)
        self.sail_factory.set_sail_config(sail_type, config)

    def generate_sails(self):
        # Delete all existing sails for this yacht before generating new ones
        self.db.delete_sails_by_yacht(self.yacht_id)
        self.sail_factory.generate_all_sails_on_boat()
        for sail_type, sail in self.sail_factory.sails.items():
            print(f"{sail_type} generated with config: {self.sail_factory.sail_config.get(sail_type, {})}")
            self.db.save_sail(sail.to_dict())

    def get_sail(self,yacht_id, sail_type):
        sail_type = SailType(sail_type)
        # Try to get from DB first
        sail_row = self.db.get_sail_by_yacht_and_type(yacht_id, sail_type.value)
        if sail_row:
            keys = ["id", "yacht_id", "name", "luff", "leech", "foot", "area", "config"]
            sail_dict = dict(zip(keys, sail_row))
            return sail_dict
        # If not in DB, try to get from factory (in-memory)
        sail = self.sail_factory.get(sail_type)
        if sail:
            sail_dict = sail.to_dict()
            sail_dict["yacht_id"] = self.yacht_id
            return sail_dict
        return None

    def get_sails_from_db(self):
        rows = self.db.get_sails_by_yacht(self.yacht_id)
        keys = ["id", "yacht_id", "name", "luff", "leech", "foot", "area", "config"]
        return [dict(zip(keys, row)) for row in rows]

    def get_aero_force(self, sail_type, wind_speed):
        sail_type = SailType(sail_type)
        sail = self.sail_factory.get(sail_type)
        if sail:
            aero_force = sail.aerodynamic_force(wind_speed)
            print(f"Aero force for {sail_type} at {wind_speed} m/s: {aero_force:.2f} N (yacht_id: {self.yacht_id})")
            return aero_force
        else:
            print(f"Sail {sail_type} not found for yacht {self.yacht_id}")
            return None

    def close(self):
        self.db.close()