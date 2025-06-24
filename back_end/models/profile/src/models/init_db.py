"""
To initialize the database, run this file as a module from the 'profile' directory:
    python -m src.models.init_db
This ensures absolute imports work correctly for standalone usage.
"""
from src.models.database import YachtProfileDatabase

if __name__ == "__main__":
    db = YachtProfileDatabase()
    print(f"Database initialized at: {db.db_path}")
