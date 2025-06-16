from config import ROPES_DB_PATH
from .models.rope_factory import Factory
from .models.database import RopeDatabase
from .models.rope_utils import normalize_rope_type
import requests
import threading

SAILDATA_API_URL = "http://127.0.0.1:8001"
SAILS_API_URL = "http://127.0.0.1:8002"
PROFILE_API_URL = "http://127.0.0.1:8003"
HULL_API_URL = "http://127.0.0.1:8004"


class RopeService:
    _thread_local = threading.local()

    def __init__(self, db_path=ROPES_DB_PATH):
        self.db = RopeDatabase(db_path)

    def _fetch_saildata(self, yacht_id):
        # Use a thread-local cache to avoid repeated HTTP requests for the same yacht_id within a request
        if not hasattr(self._thread_local, 'saildata_cache'):
            self._thread_local.saildata_cache = {}
        cache = self._thread_local.saildata_cache
        if yacht_id in cache:
            return cache[yacht_id]
        try:
            resp = requests.get(f"{SAILDATA_API_URL}/saildata/{yacht_id}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data and isinstance(data, dict) and data.get("i") is not None:
                    cache[yacht_id] = data
                    return data
        except Exception as e:
            pass  # Optionally log error
        return None

    def _fetch_sails(self, yacht_id):
        try:
            resp = requests.get(f"{SAILS_API_URL}/sails/{yacht_id}", timeout=2)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return []

    def _fetch_hull(self, yacht_id):
        try:
            resp = requests.get(f"{HULL_API_URL}/hull/hull/{yacht_id}", timeout=2)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return None

    def _get_factory(self, yacht_id, wind_speed_in_knots=30, halyard_load_safety_factor=4, dynamic_load_safety_factor=2, length_safety_factor=2):
        saildata_dict = self._fetch_saildata(yacht_id)
        saildata = saildata_dict  # Use dict directly or refactor as needed
        if saildata is None:
            raise ValueError(f"No saildata found for yacht_id={yacht_id}. Cannot create ropes.")
        return Factory(
            yacht_id=yacht_id,
            saildata=saildata,
            wind_speed_in_knots=wind_speed_in_knots,
            halyard_load_safety_factor=halyard_load_safety_factor,
            dynamic_load_safety_factor=dynamic_load_safety_factor,
            length_safety_factor=length_safety_factor,
        )

    def add_rope_type(self, yacht_id, rope_type, led_aft=0.0, **kwargs):
        rope_type = normalize_rope_type(rope_type)
        known_factory_args = [
            'wind_speed_in_knots', 'halyard_load_safety_factor', 'dynamic_load_safety_factor', 'length_safety_factor'
        ]
        factory_kwargs = {k: v for k, v in kwargs.items() if k in known_factory_args}
        config = {k: v for k, v in kwargs.items() if k not in known_factory_args}
        factory = self._get_factory(yacht_id, **factory_kwargs)
        factory.add_rope_type_to_possible_on_boat(rope_type, led_aft, config)
        return f"{rope_type} added to possible ropes on boat."

    def set_rope_config(self, yacht_id, rope_type, config):
        rope_type = normalize_rope_type(rope_type)
        factory = self._get_factory(yacht_id)
        factory.set_rope_config(rope_type, config)
        return f"Config for {rope_type} set."

    def generate_ropes(self, yacht_id, **kwargs):
        factory = self._get_factory(yacht_id, **kwargs)
        factory.generate_all_ropes_on_boat()
        self.db.save_ropes(factory.ropes)

    def get_rope(self, yacht_id, rope_type, **kwargs):
        rope_type = normalize_rope_type(rope_type)
        factory = self._get_factory(yacht_id, **kwargs)
        return factory.get(rope_type)

    def delete_ropes_by_yacht(self, yacht_id):
        self.db.delete_ropes_by_yacht(yacht_id)
        self.db.delete_possible_ropes(yacht_id)

    def close(self):
        self.db.close()
        print("Rope database connection closed.")
