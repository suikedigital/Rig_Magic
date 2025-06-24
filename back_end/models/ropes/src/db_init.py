"""
db_init.py
----------
Initializes the SQLite database and creates required tables for the running rigging management system.
"""

from models.database import RopeDatabase

def initialize_database():
    RopeDatabase()  # This will create tables if they don't exist

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
