import sqlite3


class UserYachtDatabase:
    def __init__(self, db_path="data/user_yachts.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute(
            """
        CREATE TABLE IF NOT EXISTS user_yachts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_yacht_id INTEGER,
            owner_id INTEGER,
            name TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        """
        )
        self.conn.commit()

    def insert(self, yacht_data):
        col_names = ", ".join(yacht_data.keys())
        placeholders = ", ".join(["?"] * len(yacht_data))
        values = list(yacht_data.values())
        cursor = self.conn.execute(
            f"INSERT INTO user_yachts ({col_names}) VALUES ({placeholders})", values
        )
        self.conn.commit()
        return cursor.lastrowid

    def update(self, yacht_id, yacht_data):
        set_clause = ", ".join([f"{col} = ?" for col in yacht_data.keys()])
        values = list(yacht_data.values()) + [yacht_id]
        self.conn.execute(f"UPDATE user_yachts SET {set_clause} WHERE id = ?", values)
        self.conn.commit()

    def get_by_id(self, yacht_id):
        cursor = self.conn.execute(
            "SELECT * FROM user_yachts WHERE id = ?", (yacht_id,)
        )
        return cursor.fetchone(), [desc[0] for desc in cursor.description]

    def get_by_id_and_owner(self, yacht_id, owner_id):
        cursor = self.conn.execute(
            "SELECT * FROM user_yachts WHERE id = ? AND owner_id = ?",
            (yacht_id, owner_id),
        )
        return cursor.fetchone(), [desc[0] for desc in cursor.description]

    def list(self, owner_id=None):
        if owner_id:
            cursor = self.conn.execute(
                "SELECT * FROM user_yachts WHERE owner_id = ?", (owner_id,)
            )
        else:
            cursor = self.conn.execute("SELECT * FROM user_yachts")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return rows, columns

    def delete(self, yacht_id):
        self.conn.execute("DELETE FROM user_yachts WHERE id = ?", (yacht_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
