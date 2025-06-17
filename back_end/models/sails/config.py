# config.py for sails microservice
# Define the path to the sails database and any other settings here.

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAILS_DB_PATH = os.path.join(BASE_DIR, "sails.db")

# Saildata API URL for inter-service HTTP requests
SAILDATA_API_URL = os.environ.get("SAILDATA_API_URL", "http://saildata:8001")

# Add other sails-specific config variables here as needed.
