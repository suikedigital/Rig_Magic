"""
Script to initialize the sails SQLite database and create required tables.
Run this before starting the Docker container if you want to pre-create the DB file.
"""

import os
from models.database import Database
from config import SAILS_DB_PATH

if __name__ == "__main__":
    # Ensure the directory exists
    db_dir = os.path.dirname(SAILS_DB_PATH)
    os.makedirs(db_dir, exist_ok=True)
    # This will create the DB and tables if they don't exist
    db = Database()
    print(f"Initialized sails DB at {SAILS_DB_PATH}")
