from models.hull_structure.models.keel import Keel
from models.hull_structure.models.rudder import Rudder

from models.hull_structure.models.hulls.catamaran import Catamaran
from models.hull_structure.models.hulls.monohull import Monohull
from models.hull_structure.models.hulls.trimaran import Trimaran
from models.hull_structure.models.factory import HullStructureFactory


class HullStructureService:
    def __init__(self, db_path="data/hull_structure.db"):
        self.db_path = db_path
        self.db = None

    def save_keel(self, yacht_id, keel_type, draft):
        from models.hull_structure.models.database import KeelDatabase
        db = KeelDatabase()
        db.delete_keel_by_yacht(yacht_id)  # Ensure only one keel per yacht
        db.save_keel(yacht_id, keel_type, draft)
        db.close()

    def get_keel(self, yacht_id):
        from models.hull_structure.models.database import KeelDatabase
        db = KeelDatabase()
        row = db.get_keel_by_yacht(yacht_id)
        db.close()
        if row:
            _, yacht_id, keel_type, draft = row
            return HullStructureFactory.create_keel(yacht_id, keel_type, draft)
        return None

    def save_rudder(self, yacht_id, rudder_type):
        from models.hull_structure.models.database import RudderDatabase
        db = RudderDatabase()
        db.delete_rudder_by_yacht(yacht_id)  # Ensure only one rudder per yacht
        db.save_rudder(yacht_id, rudder_type)
        db.close()

    def get_rudder(self, yacht_id):
        from models.hull_structure.models.database import RudderDatabase
        db = RudderDatabase()
        row = db.get_rudder_by_yacht(yacht_id)
        db.close()
        if row:
            _, yacht_id, rudder_type = row
            return HullStructureFactory.create_rudder(yacht_id, rudder_type)
        return None

    def save_hull(self, hull_type, yacht_id, loa, lwl, beam, displacement, ballast):
        from models.hull_structure.models.database import HullDatabase
        db = HullDatabase()
        db.delete_hull_by_yacht(yacht_id)  # Ensure only one hull per yacht
        db.save_hull(yacht_id, hull_type, loa, lwl, beam, displacement, ballast)
        db.close()

    def get_hull(self, yacht_id):
        from models.hull_structure.models.database import HullDatabase
        db = HullDatabase()
        row = db.get_hull_by_yacht(yacht_id)
        db.close()
        if row:
            _, yacht_id, hull_type, loa, lwl, beam, displacement, ballast = row
            return HullStructureFactory.create_hull(hull_type, yacht_id, loa, lwl, beam, displacement, ballast)
        return None

    def delete_all_by_yacht(self, yacht_id):
        from models.hull_structure.models.database import KeelDatabase, RudderDatabase, HullDatabase
        KeelDatabase().delete_keel_by_yacht(yacht_id)
        RudderDatabase().delete_rudder_by_yacht(yacht_id)
        HullDatabase().delete_hull_by_yacht(yacht_id)