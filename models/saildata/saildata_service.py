from models.saildata.models.saildata import SailData
from models.saildata.models.factory import SailDataFactory
from models.saildata.models.database import SailDataDatabase

class SailDataService:
    def __init__(self, db_path="data/saildata.db"):
        self.db = SailDataDatabase(db_path)

    def save_saildata(self, saildata: SailData):
        self.db.save_saildata(saildata)

    def save_saildata_from_dict(self, yacht_id, data: dict):
        saildata = SailDataFactory.from_dict(yacht_id, data)
        self.save_saildata(saildata)

    def get_saildata(self, yacht_id):
        return self.db.get_saildata_by_yacht(yacht_id)

    def close(self):
        self.db.close()
