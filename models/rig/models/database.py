import sqlite3

class RigDatabase:
    def __init__(self, db_path="data/rigs.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS rigs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL UNIQUE,
                rig_type TEXT NOT NULL,
                boom_above_deck REAL
            )
        ''')
        self.conn.commit()

    def save_rig(self, yacht_id, rig_type, boom_above_deck):
        # Delete any existing rig for this yacht_id before saving
        self.conn.execute("DELETE FROM rigs WHERE yacht_id = ?", (yacht_id,))
        self.conn.execute(
            "INSERT INTO rigs (yacht_id, rig_type, boom_above_deck) VALUES (?, ?, ?)",
            (yacht_id, rig_type, boom_above_deck)
        )
        self.conn.commit()

    def get_rig_by_yacht(self, yacht_id):
        cursor = self.conn.execute("SELECT yacht_id, rig_type, boom_above_deck FROM rigs WHERE yacht_id = ?", (yacht_id,))
        return cursor.fetchone()

    def delete_rig_by_yacht(self, yacht_id):
        self.conn.execute("DELETE FROM rigs WHERE yacht_id = ?", (yacht_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
