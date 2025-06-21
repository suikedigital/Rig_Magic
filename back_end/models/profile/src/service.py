from config import PROFILE_DB_PATH

from .models.database import YachtProfileDatabase
from .models.factory import YachtProfileFactory
from src.logger import get_logger


logger = get_logger(__name__)


class YachtProfileService:
    def __init__(self, db_path=PROFILE_DB_PATH):
        self.db = YachtProfileDatabase(db_path)

    def initialize_from_base(self, yacht_id, base_yacht, base_id=None):
        profile_data = {
            "yacht_id": yacht_id,
            "base_id": base_id,
            "yacht_class": base_yacht.yacht_class,
            "model": base_yacht.model,
            "version": base_yacht.version,
            "builder": base_yacht.builder,
            "designer": base_yacht.designer,
            "year_introduced": base_yacht.year_introduced,
            "production_start": base_yacht.production_start,
            "production_end": base_yacht.production_end,
            "country_of_origin": base_yacht.country_of_origin,
            "notes": base_yacht.notes,
        }

        profile = YachtProfileFactory.from_dict(profile_data)
        self.save_profile(profile)
        logger.info(
            f"Profile initialized for yacht {yacht_id} based on base yacht {base_id}."
        )

    def save_profile(self, profile, base_id=None):
        # Accepts a YachtProfile object or dict, and optional base_id
        profile_dict = (
            profile.__dict__ if hasattr(profile, "__dict__") else dict(profile)
        )
        if base_id is not None:
            profile_dict["base_id"] = base_id
        elif "base_id" not in profile_dict:
            profile_dict["base_id"] = None
        self.db.insert(profile_dict)

    def get_profile(self, yacht_id):
        row, columns = self.db.get_by_yacht_id(yacht_id)
        if row:
            return YachtProfileFactory.from_row(row, columns)
        return None

    def delete_profile(self, yacht_id):
        self.db.delete(yacht_id)

    def close(self):
        self.db.close()
