import sqlite3
from config import PROFILE_DB_PATH


class YachtProfileDatabase:
    def __init__(self, db_path=PROFILE_DB_PATH):
        self.db_path = db_path
        self.create_table()
 

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS yacht_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL,
                base_id INTEGER,
                yacht_class TEXT,
                model TEXT,
                version TEXT,
                builder TEXT,
                designer TEXT,
                year_introduced INTEGER,
                production_start INTEGER,
                production_end INTEGER,
                country_of_origin TEXT,
                notes TEXT
            )
            ''')
            conn.commit()

    def insert(self, profile: dict):
        col_names = ', '.join(profile.keys())
        placeholders = ', '.join(['?'] * len(profile))
        values = list(profile.values())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                f"INSERT OR REPLACE INTO yacht_profiles ({col_names}) VALUES ({placeholders})", values
            )
            conn.commit()

    def get_by_yacht_id(self, yacht_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM yacht_profiles WHERE yacht_id = ?", (yacht_id,))
            row = cursor.fetchone()
            columns = [desc[0] for desc in cursor.description]
            return row, columns

    def delete(self, yacht_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM yacht_profiles WHERE yacht_id = ?", (yacht_id,))
            conn.commit()

    def list_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM yacht_profiles")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]