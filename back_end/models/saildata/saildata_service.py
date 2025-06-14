from back_end.models.saildata.models.saildata import SailData
from back_end.models.saildata.models.factory import SailDataFactory
from back_end.models.saildata.models.database import SailDataDatabase
from back_end.models.saildata.config import SAILDATA_DB_PATH
import requests

class SailDataService:
    def __init__(self, db_path=SAILDATA_DB_PATH, api_url=None):
        self.db = SailDataDatabase(db_path)
        self.api_url = api_url or "http://localhost:8001"  # Default saildata API URL

    def initialize_from_base(self, yacht_id, base_yacht):
        saildata = SailDataFactory.create(
            yacht_id,
            i=base_yacht.i,
            j=base_yacht.j,
            p=base_yacht.p,
            e=base_yacht.e,
            genoa_i=base_yacht.genoa_i,
            genoa_j=base_yacht.genoa_j,
            main_p=base_yacht.main_p,
            main_e=base_yacht.main_e,
            codezero_i=base_yacht.codezero_i,
            codezero_j=base_yacht.codezero_j,
            jib_i=base_yacht.jib_i,
            jib_j=base_yacht.jib_j,
            spin_i=base_yacht.spin_i,
            spin_j=base_yacht.spin_j,
            staysail_i=base_yacht.staysail_i,
            staysail_j=base_yacht.staysail_j,
            trisail_i=base_yacht.trisail_i,
            trisail_j=base_yacht.trisail_j,
        )
        self.save_saildata(saildata)
        print(f"Sail data initialized for yacht {yacht_id} based on base yacht {base_yacht.id}.")

    def save_saildata(self, saildata: SailData):
        # Ensure only one entry per yacht_id by deleting before saving
        self.db.delete_saildata_by_yacht(saildata.yacht_id)
        self.db.save_saildata(saildata)

    def save_saildata_from_dict(self, yacht_id, data: dict):
        saildata = SailDataFactory.from_dict(yacht_id, data)
        self.save_saildata(saildata)

    def get_saildata(self, yacht_id):
        # Try HTTP API first for microservice orchestration
        try:
            resp = requests.get(f"{self.api_url}/saildata/{yacht_id}", timeout=2)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            pass  # Fallback to DB if HTTP fails
        result = self.db.get_saildata_by_yacht(yacht_id)
        if result is None:
            return None
        if hasattr(result, "to_dict"):
            return result.to_dict()
        return result

    def close(self):
        self.db.close()
