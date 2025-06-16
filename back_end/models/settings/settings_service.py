from .models.settings import Settings
from .models.factory import SettingsFactory
from .models.database import SettingsDatabase

class SettingsService:
    def __init__(self, db_path="data/settings.db"):
        self.db = SettingsDatabase(db_path)

    def save_settings(self, settings: Settings):
        self.db.delete_settings_by_yacht(settings.yacht_id)  # Ensure only one entry per yacht
        self.db.save_settings(settings)

    def save_settings_from_dict(self, data: dict):
        settings = SettingsFactory.from_dict(data)
        self.save_settings(settings)

    def get_settings(self, yacht_id):
        row = self.db.get_settings_by_yacht(yacht_id)
        if row:
            return SettingsFactory.from_row(row)
        return None

    def delete_settings(self, yacht_id):
        self.db.delete_settings_by_yacht(yacht_id)

    def close(self):
        self.db.close()
