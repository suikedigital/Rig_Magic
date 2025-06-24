"""
Database initialization script for hull_structure microservice.
Creates the SQLite database and tables if they do not exist.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.database import KeelDatabase, RudderDatabase, HullDatabase


def main():
    print("Initializing database...")
    keel_db = KeelDatabase()
    rudder_db = RudderDatabase()
    hull_db = HullDatabase()
    # Close connections
    keel_db.close()
    rudder_db.close()
    hull_db.close()
    print("Database initialized.")


if __name__ == "__main__":
    main()
