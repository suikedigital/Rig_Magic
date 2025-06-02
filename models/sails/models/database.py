import sqlite3

class Database:
    def __init__(self, db_path="data/sails.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            yacht_id INTEGER NOT NULL,
            sail_type TEXT NOT NULL,
            luff REAL,
            leech REAL,
            foot REAL,
            area REAL,
            config TEXT
        )
        """)
        self.conn.commit()

    def save_sail(self, sail_dict):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO sails (yacht_id, sail_type, luff, leech, foot, area, config)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            sail_dict["yacht_id"],
            sail_dict["name"],
            sail_dict["luff"],
            sail_dict["leech"],
            sail_dict["foot"],
            sail_dict["area"],
            str(sail_dict.get("kwargs", {}))
        ))
        self.conn.commit()

    def get_sails_by_yacht(self, yacht_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sails WHERE yacht_id = ?", (yacht_id,))
        return cursor.fetchall()
    
    def get_sails_by_type(self, sail_type):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sails WHERE sail_type = ?", (sail_type,))
        return cursor.fetchall()

    def get_sail_by_yacht_and_type(self, yacht_id, sail_type):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM sails WHERE yacht_id = ? AND sail_type = ?",
            (yacht_id, sail_type)
        )
        return cursor.fetchone()

    def close(self):
        self.conn.close()