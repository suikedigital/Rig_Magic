import sqlite3
from back_end.models.hull_structure.config import HULL_STRUCTURE_DB_PATH

class KeelDatabase:
    def __init__(self, db_path=HULL_STRUCTURE_DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS keels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL,
                base_id INTEGER,
                keel_type TEXT NOT NULL,
                draft REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def save_keel(self, yacht_id, base_id, keel_type, draft):
        self.conn.execute(
            "INSERT OR REPLACE INTO keels (yacht_id, base_id, keel_type, draft) VALUES (?, ?, ?, ?)",
            (yacht_id, base_id, keel_type, draft)
        )
        self.conn.commit()

    def get_keel_by_yacht(self, yacht_id):
        cursor = self.conn.execute("SELECT * FROM keels WHERE yacht_id = ?", (yacht_id,))
        return cursor.fetchone()

    def delete_keel_by_yacht(self, yacht_id):
        self.conn.execute("DELETE FROM keels WHERE yacht_id = ?", (yacht_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

class RudderDatabase:
    def __init__(self, db_path=HULL_STRUCTURE_DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS rudders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL,
                base_id INTEGER,
                rudder_type TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def save_rudder(self, yacht_id, rudder_type, base_id=None):
        self.conn.execute(
            "INSERT OR REPLACE INTO rudders (yacht_id, base_id, rudder_type) VALUES (?, ?, ?)",
            (yacht_id, base_id, rudder_type)
        )
        self.conn.commit()

    def get_rudder_by_yacht(self, yacht_id):
        cursor = self.conn.execute("SELECT * FROM rudders WHERE yacht_id = ?", (yacht_id,))
        return cursor.fetchone()

    def delete_rudder_by_yacht(self, yacht_id):
        self.conn.execute("DELETE FROM rudders WHERE yacht_id = ?", (yacht_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

class HullDatabase:
    def __init__(self, db_path=HULL_STRUCTURE_DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS hulls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL,
                base_id INTEGER,
                hull_type TEXT NOT NULL,
                loa REAL,
                lwl REAL,
                beam REAL,
                displacement REAL,
                ballast REAL,
                construction TEXT
            )
        ''')
        self.conn.commit()

    def save_hull(self, yacht_id, hull_type, loa, lwl, beam, displacement, ballast, construction, base_id=None):
        self.conn.execute(
            "INSERT OR REPLACE INTO hulls (yacht_id, base_id, hull_type, loa, lwl, beam, displacement, ballast, construction) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (yacht_id, base_id, hull_type, loa, lwl, beam, displacement, ballast, construction)
        )
        self.conn.commit()

    def get_hull_by_yacht(self, yacht_id):
        cursor = self.conn.execute("SELECT * FROM hulls WHERE yacht_id = ?", (yacht_id,))
        return cursor.fetchone()

    def delete_hull_by_yacht(self, yacht_id):
        self.conn.execute("DELETE FROM hulls WHERE yacht_id = ?", (yacht_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
