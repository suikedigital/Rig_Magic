from back_end.models.hull_structure.models.keel import Keel
from back_end.models.hull_structure.models.rudder import Rudder
from back_end.models.hull_structure.models.hulls.monohull import Monohull
from back_end.models.hull_structure.models.hulls.catamaran import Catamaran
from back_end.models.hull_structure.models.hulls.trimaran import Trimaran

class HullStructureFactory:
    @staticmethod
    def create_keel(yacht_id, keel_type, draft):
        return Keel(yacht_id, keel_type, draft)

    @staticmethod
    def create_rudder(yacht_id, rudder_type):
        return Rudder(yacht_id, rudder_type)

    @staticmethod
    def create_hull(hull_type, yacht_id, loa, lwl, beam, displacement, ballast):
        hull_type = str(hull_type).strip().lower()
        if hull_type == "monohull":
            return Monohull(yacht_id, loa, lwl, beam, displacement, ballast, construction="GRP")
        if hull_type == "trimaran":
            return Trimaran(yacht_id, loa, lwl, beam, displacement, ballast, construction="GRP")
        if hull_type == "catamaran":
            return Catamaran(yacht_id, loa, lwl, beam, displacement, ballast, construction="GRP")
        raise ValueError(f"Unknown hull type: {hull_type}")