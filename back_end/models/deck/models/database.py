import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS deck (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL,
                base_id INTEGER,
                -- ...existing columns...
            )
        """
        )
        # ...create other tables...

    def save_deck(self, yacht_id, base_id=None, **kwargs):
        # Example: add your deck fields as needed
        self.conn.execute(
            "INSERT OR REPLACE INTO deck (yacht_id, base_id) VALUES (?, ?)",
            (yacht_id, base_id),
        )
        self.conn.commit()


db = Database("yachts.db")
