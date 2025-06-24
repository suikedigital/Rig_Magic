# db_init.py for initializing the saildata database
import sys
import os

# Add the src directory to sys.path so both database and config can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from models.database import SailDataDatabase

if __name__ == "__main__":
    db = SailDataDatabase()
    print(f"Database initialized at: {db.db_path}")
