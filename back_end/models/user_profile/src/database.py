import sqlite3

DB_FILE = "user_profile.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        role TEXT NOT NULL,
        yacht_ids TEXT,
        telephone TEXT,
        address TEXT,
        subscription_status TEXT,
        payment_info TEXT,
        company_name TEXT
    )
    """)
    conn.commit()
    conn.close()
