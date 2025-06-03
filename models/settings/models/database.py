import sqlite3

class SettingsDatabase:
    def __init__(self, db_path="data/settings.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER NOT NULL UNIQUE,
                wind_speed_in_knots INTEGER NOT NULL,
                length_safety_factor REAL NOT NULL,
                halyard_load_safety_factor REAL NOT NULL,
                dynamic_load_safety_factor REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def save_settings(self, settings):
        self.conn.execute(
            "INSERT OR REPLACE INTO settings (yacht_id, wind_speed_in_knots, length_safety_factor, halyard_load_safety_factor, dynamic_load_safety_factor) VALUES (?, ?, ?, ?, ?)",
            (
                settings.yacht_id,
                settings.wind_speed_in_knots,
                settings.length_safety_factor,
                settings.halyard_load_safety_factor,
                settings.dynamic_load_safety_factor
            )
        )
        self.conn.commit()

    def get_settings_by_yacht(self, yacht_id):
        cursor = self.conn.execute("SELECT yacht_id, wind_speed_in_knots, length_safety_factor, halyard_load_safety_factor, dynamic_load_safety_factor FROM settings WHERE yacht_id = ?", (yacht_id,))
        return cursor.fetchone()

    def delete_settings_by_yacht(self, yacht_id):
        self.conn.execute("DELETE FROM settings WHERE yacht_id = ?", (yacht_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
