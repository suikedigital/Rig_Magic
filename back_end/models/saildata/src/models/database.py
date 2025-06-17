import sqlite3
from .saildata import SailData
from config import SAILDATA_DB_PATH
import json
from back_end.logger import get_logger

logger = get_logger(__name__)


class SailDataDatabase:
    def __init__(self, db_path=SAILDATA_DB_PATH):
        self.db_path = db_path
        logger.info(f"SAILDATA DB PATH: {self.db_path}")
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saildata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    yacht_id INTEGER NOT NULL,
                    base_id INTEGER,
                    i INTEGER,
                    j INTEGER,
                    p INTEGER,
                    e INTEGER,
                    data TEXT NOT NULL
                )
            """
            )
            conn.commit()

    def delete_saildata_by_yacht(self, yacht_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM saildata WHERE yacht_id = ?", (yacht_id,))
            conn.commit()

    def save_saildata(self, saildata: SailData, base_id=None):
        # Only store kwargs in the data column
        base_keys = {"yacht_id", "i", "j", "p", "e"}
        kwargs = {k: v for k, v in saildata.to_dict().items() if k not in base_keys}
        data_json = json.dumps(kwargs)
        self.delete_saildata_by_yacht(saildata.yacht_id)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO saildata (yacht_id, base_id, i, j, p, e, data) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    saildata.yacht_id,
                    base_id,
                    saildata.i,
                    saildata.j,
                    saildata.p,
                    saildata.e,
                    data_json,
                ),
            )
            conn.commit()

    def get_saildata_by_yacht(self, yacht_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, yacht_id, i, j, p, e, data FROM saildata WHERE yacht_id = ?",
                (yacht_id,),
            )
            row = cursor.fetchone()
            if row:
                id_, yacht_id, i, j, p, e, data_json = row
                kwargs = json.loads(data_json) if data_json else {}
                kwargs.pop("yacht_id", None)
                saildata = SailData(yacht_id, i, j, p, e, **kwargs)
                return saildata
            return None

    def list_yacht_ids(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT yacht_id FROM saildata")
            return [row[0] for row in cursor.fetchall()]
