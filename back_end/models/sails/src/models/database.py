import sqlite3
from config import SAILS_DB_PATH
from .sail_utils import normalize_sail_type


class Database:
    def __init__(self, db_path=SAILS_DB_PATH):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL,
                base_id INTEGER,
                sail_type TEXT NOT NULL,
                luff REAL,
                leech REAL,
                foot REAL,
                area REAL,
                config TEXT
            )
            """)    
            # New table for possible sails on a yacht
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sails_possible (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL,
                sail_type TEXT NOT NULL,
                config TEXT,
                UNIQUE(yacht_id, sail_type) ON CONFLICT REPLACE
            )
            """)
            conn.commit()

    def save_sail(self, sail_dict, base_id=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            sail_type = normalize_sail_type(sail_dict["name"] if sail_dict.get("name") else None)
            cursor.execute("""
            INSERT INTO sails (yacht_id, base_id, sail_type, luff, leech, foot, area, config)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sail_dict["yacht_id"],
                base_id,
                sail_type,
                sail_dict["luff"],
                sail_dict["leech"],
                sail_dict["foot"],
                sail_dict["area"],
                str(sail_dict.get("kwargs", {}))
            ))
            conn.commit()

    def get_sails_by_yacht(self, yacht_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sails WHERE yacht_id = ?", (yacht_id,))
            return cursor.fetchall()
    
    def get_sails_by_type(self, sail_type):
        sail_type = normalize_sail_type(sail_type)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sails WHERE sail_type = ?", (sail_type,))
            return cursor.fetchall()

    def get_sail_by_yacht_and_type(self, yacht_id, sail_type):
        sail_type = normalize_sail_type(sail_type)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM sails WHERE yacht_id = ? AND sail_type = ?",
                (yacht_id, sail_type)
            )
            return cursor.fetchone()

    def delete_sails_by_yacht(self, yacht_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sails WHERE yacht_id = ?", (yacht_id,))
            conn.commit()

    def save_possible_sail(self, yacht_id, sail_type, config=None):
        sail_type = normalize_sail_type(sail_type)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO sails_possible (yacht_id, sail_type, config) VALUES (?, ?, ?)",
                (yacht_id, sail_type, str(config) if config else None)
            )
            conn.commit()

    def get_possible_sails(self, yacht_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT sail_type, config FROM sails_possible WHERE yacht_id = ?",
                (yacht_id,)
            )
            # Normalize all sail_type values on load
            sails = [(normalize_sail_type(row[0]), row[1]) for row in cursor.fetchall()]
        return sails

    def delete_possible_sails(self, yacht_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sails_possible WHERE yacht_id = ?", (yacht_id,))
            conn.commit()

    """
    Additional methods for sail management can be added here.
    """