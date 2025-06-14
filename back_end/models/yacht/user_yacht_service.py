from back_end.models.yacht.models.user_yacht.database import UserYachtDatabase
from back_end.models.yacht.models.user_yacht.user_yacht import UserYacht

class UserYachtService:
    def __init__(self, db_path="data/user_yachts.db"):
        self.db = UserYachtDatabase(db_path)

    def save_user_yacht(self, user_yacht):
        yacht_dict = {
            "base_yacht_id": user_yacht.base_yacht_id,
            "owner_id": user_yacht.owner_id,
            "name": user_yacht.name,
            "created_at": getattr(user_yacht, "created_at", None),
            "updated_at": getattr(user_yacht, "updated_at", None),
        }
        return self.db.insert(yacht_dict)

    def update_user_yacht(self, yacht_id, user_yacht):
        yacht_dict = {
            "base_yacht_id": user_yacht.base_yacht_id,
            "owner_id": user_yacht.owner_id,
            "name": user_yacht.name,
            "updated_at": getattr(user_yacht, "updated_at", None),
        }
        self.db.update(yacht_id, yacht_dict)

    def get_user_yacht_by_id(self, yacht_id, owner_id=None):
        if owner_id:
            row, columns = self.db.get_by_id_and_owner(yacht_id, owner_id)
        else:
            row, columns = self.db.get_by_id(yacht_id)
        if row:
            data = dict(zip(columns, row))
            return UserYacht(**data)
        return None

    def list_user_yachts(self, owner_id=None):
        rows, columns = self.db.list(owner_id)
        return [UserYacht(**dict(zip(columns, row))) for row in rows]

    def delete_user_yacht(self, yacht_id):
        self.db.delete(yacht_id)

    def close(self):
        self.db.close()