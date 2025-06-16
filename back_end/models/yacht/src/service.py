from .models.base_yacht.database import BaseYachtDatabase
from .models.base_yacht.factory import BaseYachtFactory
from .models.base_yacht.base_yacht import BaseYacht

class BaseYachtService:
    def __init__(self, db_path="data/base_yachts.db"):
        self.db = BaseYachtDatabase(db_path)

    def save_base_yacht(self, base_yacht: BaseYacht):
        yacht_dict = base_yacht.__dict__
        columns = self._get_table_columns()
        yacht_data = {col: yacht_dict.get(col, None) for col in columns if col != 'id'}
        col_names = ', '.join(yacht_data.keys())
        placeholders = ', '.join(['?'] * len(yacht_data))
        values = list(yacht_data.values())
        self.db.conn.execute(f"INSERT INTO base_yachts ({col_names}) VALUES ({placeholders})", values)
        self.db.conn.commit()

    def update_base_yacht(self, yacht_id, base_yacht: BaseYacht):
        yacht_dict = base_yacht.__dict__
        columns = self._get_table_columns()
        yacht_data = {col: yacht_dict.get(col, None) for col in columns if col != 'id'}
        set_clause = ', '.join([f"{col} = ?" for col in yacht_data.keys()])
        values = list(yacht_data.values()) + [yacht_id]
        self.db.conn.execute(f"UPDATE base_yachts SET {set_clause} WHERE id = ?", values)
        self.db.conn.commit()

    def get_base_yacht_by_id(self, yacht_id):
        cursor = self.db.conn.execute("SELECT * FROM base_yachts WHERE id = ?", (yacht_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return BaseYachtFactory.from_row(row, columns)
        return None

    def list_base_yachts(self):
        cursor = self.db.conn.execute("SELECT * FROM base_yachts")
        columns = [desc[0] for desc in cursor.description]
        return [BaseYachtFactory.from_row(row, columns) for row in cursor.fetchall()]

    def delete_base_yacht(self, yacht_id):
        self.db.conn.execute("DELETE FROM base_yachts WHERE id = ?", (yacht_id,))
        self.db.conn.commit()

    def _get_table_columns(self):
        cursor = self.db.conn.execute('PRAGMA table_info(base_yachts)')
        return [row[1] for row in cursor.fetchall()]

    def close(self):
        self.db.close()
