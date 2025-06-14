from back_end.models.hull_structure.config import HULL_STRUCTURE_DB_PATH
from back_end.models.hull_structure.models.keel import Keel
from back_end.models.hull_structure.models.rudder import Rudder

from back_end.models.hull_structure.models.hulls.catamaran import Catamaran
from back_end.models.hull_structure.models.hulls.monohull import Monohull
from back_end.models.hull_structure.models.hulls.trimaran import Trimaran
from back_end.models.hull_structure.models.factory import HullStructureFactory


class HullStructureService:
    def __init__(self, db_path=HULL_STRUCTURE_DB_PATH):
        self.db_path = db_path
        self.db = None

    def initialize_from_base(self, yacht_id, base_id):
        """
        Initializes the hull structure service from a base yacht.
        This method should be called after the base yacht is created.
        """
        pass
        
    def save_keel(self, yacht_id, keel_type, draft, base_id=None):
        from back_end.models.hull_structure.models.database import KeelDatabase
        db = KeelDatabase(self.db_path)
        db.delete_keel_by_yacht(yacht_id)  # Ensure only one keel per yacht
        db.save_keel(yacht_id, base_id, keel_type, draft)
        db.close()

    def get_keel(self, yacht_id):
        from back_end.models.hull_structure.models.database import KeelDatabase
        db = KeelDatabase(self.db_path)
        row = db.get_keel_by_yacht(yacht_id)
        db.close()
        if row:
            _, yacht_id, base_id, keel_type, draft = row  # Unpack all columns
            return HullStructureFactory.create_keel(yacht_id, keel_type, draft)
        return None

    def save_rudder(self, yacht_id, rudder_type):
        from back_end.models.hull_structure.models.database import RudderDatabase
        db = RudderDatabase(self.db_path)
        db.delete_rudder_by_yacht(yacht_id)  # Ensure only one rudder per yacht
        db.save_rudder(yacht_id, rudder_type)
        db.close()

    def get_rudder(self, yacht_id):
        from back_end.models.hull_structure.models.database import RudderDatabase
        db = RudderDatabase(self.db_path)
        row = db.get_rudder_by_yacht(yacht_id)
        db.close()
        if row:
            _, yacht_id, base_id, rudder_type = row  # Unpack all columns
            return HullStructureFactory.create_rudder(yacht_id, rudder_type)
        return None

    def save_hull(self, hull):
        from back_end.models.hull_structure.models.database import HullDatabase
        db = HullDatabase(self.db_path)
        # Extract all required fields from the hull object
        yacht_id = getattr(hull, 'yacht_id', None)
        hull_type = getattr(hull, 'hull_type', None)
        loa = getattr(hull, 'loa', None)
        lwl = getattr(hull, 'lwl', None)
        beam = getattr(hull, 'beam', None)
        displacement = getattr(hull, 'displacement', None)
        ballast = getattr(hull, 'ballast', None)
        construction = getattr(hull, 'construction', None)
        db.delete_hull_by_yacht(yacht_id)  # Ensure only one hull per yacht
        db.save_hull(yacht_id, hull_type, loa, lwl, beam, displacement, ballast, construction)
        db.close()

    def get_hull(self, yacht_id):
        from back_end.models.hull_structure.models.database import HullDatabase
        db = HullDatabase(self.db_path)
        row = db.get_hull_by_yacht(yacht_id)
        db.close()
        if row:
            # Unpack all columns including construction
            _, yacht_id, base_id, hull_type, loa, lwl, beam, displacement, ballast, construction = row
            return {
                "yacht_id": yacht_id,
                "base_id": base_id,
                "hull_type": hull_type,
                "loa": loa,
                "lwl": lwl,
                "beam": beam,
                "displacement": displacement,
                "ballast": ballast,
                "construction": construction
            }
        return None

    def delete_all_by_yacht(self, yacht_id):
        from back_end.models.hull_structure.models.database import KeelDatabase, RudderDatabase, HullDatabase
        KeelDatabase(self.db_path).delete_keel_by_yacht(yacht_id)
        RudderDatabase(self.db_path).delete_rudder_by_yacht(yacht_id)
        HullDatabase(self.db_path).delete_hull_by_yacht(yacht_id)