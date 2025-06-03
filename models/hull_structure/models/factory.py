from models.hull_structure.models.keel import Keel
from models.hull_structure.models.rudder import Rudder
from models.hull_structure.models.hulls.monohull import Monohull
from models.hull_structure.models.hulls.catamaran import Catamaran
from models.hull_structure.models.hulls.trimaran import Trimaran

class HullStructureFactory:
    @staticmethod
    def create_keel(yacht_id, keel_type, draft):
        return Keel(yacht_id, keel_type, draft)

    @staticmethod
    def create_rudder(yacht_id, rudder_type):
        return Rudder(yacht_id, rudder_type)

    @staticmethod
    def create_hull(hull_type, yacht_id, loa, lwl, beam, displacement, ballast):
        if hull_type == "monohull":
            return Monohull(yacht_id, loa, lwl, beam, displacement, ballast)
        if hull_type == "trimaran":
            return Trimaran(yacht_id, loa, lwl, beam, displacement, ballast)
        if hull_type == "catamaran":
            return Catamaran(yacht_id, loa, lwl, beam, displacement, ballast)
        raise ValueError(f"Unknown hull type: {hull_type}")