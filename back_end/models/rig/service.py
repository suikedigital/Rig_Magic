from back_end.models.rig.config import RIG_DB_PATH
from back_end.models.rig.models.factory import RigFactory
from back_end.models.rig.models.database import RigDatabase

class RigService:
    def __init__(self, db_path=RIG_DB_PATH):
        self.db_path = db_path

    def create_rig(self, rig_type: str, yacht_id: int, boom_above_deck: float = None, base_id: int = None):
        return RigFactory.create_rig(rig_type, yacht_id, boom_above_deck, base_id)

    def save_rig(self, rig):
        db = RigDatabase(self.db_path)
        db.save_rig(rig.yacht_id, rig.rig_type, rig.boom_above_deck, rig.base_id)
        db.close()

    def get_rig(self, yacht_id):
        db = RigDatabase(self.db_path)
        row = db.get_rig_by_yacht(yacht_id)
        db.close()
        if row:
            yacht_id, rig_type, boom_above_deck = row
            return RigFactory.create_rig(rig_type, yacht_id, boom_above_deck)
        return None

    def delete_rig(self, yacht_id):
        db = RigDatabase(self.db_path)
        db.delete_rig_by_yacht(yacht_id)
        db.close()