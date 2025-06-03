from models.rig.models.factory import RigFactory
from models.rig.models.database import RigDatabase

class RigService:
    def __init__(self, db_path="data/rigs.db"):
        self.db_path = db_path

    def create_rig(self, rig_type: str, yacht_id: int, boom_above_deck: float = None):
        return RigFactory.create_rig(rig_type, yacht_id, boom_above_deck)

    def save_rig(self, rig):
        db = RigDatabase(self.db_path)
        db.save_rig(rig.yacht_id, rig.rig_type, rig.boom_above_deck)
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