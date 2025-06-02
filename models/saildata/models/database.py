import sqlite3
from models.saildata.models.saildata import SailData

class SailDataDatabase:
    def __init__(self, db_path="data/saildata.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS saildata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL,
                i INTEGER,
                j INTEGER,
                p INTEGER,
                e INTEGER,
                data TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def save_saildata(self, saildata: SailData):
        import json
        # Only store kwargs in the data column
        base_keys = {"yacht_id", "i", "j", "p", "e"}
        kwargs = {k: v for k, v in saildata.to_dict().items() if k not in base_keys}
        data_json = json.dumps(kwargs)
        self.conn.execute(
            "INSERT OR REPLACE INTO saildata (yacht_id, i, j, p, e, data) VALUES (?, ?, ?, ?, ?, ?)",
            (
            saildata.yacht_id,
            saildata.i,
            saildata.j,
            saildata.p,
            saildata.e,
            data_json
            )
        )
        self.conn.commit()

    def get_saildata_by_yacht(self, yacht_id):
        import json
        cursor = self.conn.execute(
            "SELECT id, yacht_id, i, j, p, e, data FROM saildata WHERE yacht_id = ?", (yacht_id,)
        )
        row = cursor.fetchone()
        if row:
            id_, yacht_id, i, j, p, e, data_json = row
            kwargs = json.loads(data_json) if data_json else {}
            # Remove yacht_id from kwargs to avoid duplicate argument error
            kwargs.pop("yacht_id", None)
            saildata = SailData(yacht_id, i, j, p, e, **kwargs)
            return saildata
        return None
    
    def close(self):
        self.conn.close()