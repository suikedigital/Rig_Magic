# config.py for the saildata microservice
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAILDATA_DB_PATH = os.environ.get("SAILDATA_DB_PATH", os.path.join(BASE_DIR, "../data.db"))
