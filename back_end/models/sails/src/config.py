# config.py for sails microservice
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAILS_DB_PATH = os.environ.get("SAILS_DB_PATH", os.path.join(BASE_DIR, "../data.db"))
SAILDATA_API_URL = os.environ.get("SAILDATA_API_URL", "http://saildata:8001")
