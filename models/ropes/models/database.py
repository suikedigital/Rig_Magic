"""
database.py
-----------
Handles SQLite database integration for rope storage and retrieval in the running rigging management system.

- Creates and manages the ropes table
- Provides upsert (insert or replace) logic for rope records
- Supports retrieval of ropes by yacht or type
"""

import sqlite3
from pathlib import Path

class RopeDatabase:
    def __init__(self, db_path="data/ropes.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ropes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                yacht_id INTEGER,
                rope_type TEXT,
                construction TEXT,
                colour TEXT,
                length REAL,
                diameter INTEGER,
                upper_term_type TEXT,
                upper_hardware TEXT,
                lower_term_type TEXT,
                lower_hardware TEXT,
                led_aft REAL,
                required_wl_kg REAL,
                config TEXT,
                UNIQUE(yacht_id, rope_type) ON CONFLICT REPLACE
            )
        ''')
        self.conn.commit()

    def save_rope(self, rope_type, rope):
        cursor = self.conn.cursor()
        yacht_id = getattr(rope, 'yacht_id', None)
        construction = getattr(rope, 'construction_type', None) or getattr(rope, 'construction', None)
        colour = getattr(rope, 'colour', None)
        length = getattr(rope, 'length', None)
        diameter = getattr(rope, 'diameter', None)
        upper_termination = getattr(rope, 'upper_termination', None)
        lower_termination = getattr(rope, 'lower_termination', None)
        upper_term_type = getattr(upper_termination, 'term_type', None)
        upper_hardware = getattr(upper_termination, 'hardware', None)
        lower_term_type = getattr(lower_termination, 'term_type', None)
        lower_hardware = getattr(lower_termination, 'hardware', None)
        led_aft = getattr(rope, 'led_aft', None)
        required_wl_kg = getattr(rope, 'required_wl_kg', None)
        config = getattr(rope, 'config', None)
        cursor.execute('''
            INSERT OR REPLACE INTO ropes (
                yacht_id, rope_type, construction, colour, length, diameter,
                upper_term_type, upper_hardware, lower_term_type, lower_hardware,
                led_aft, required_wl_kg, config
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            yacht_id, rope_type, str(construction), colour, length, diameter,
            upper_term_type, upper_hardware, lower_term_type, lower_hardware,
            led_aft, required_wl_kg, str(config)
        ))
        self.conn.commit()

    def save_ropes(self, ropes: dict):
        for rope_type, rope in ropes.items():
            self.save_rope(rope_type, rope)

    def get_ropes_by_yacht(self, yacht_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM ropes WHERE yacht_id = ?", (yacht_id,))
        return cursor.fetchall()

    def get_rope_by_type(self, rope_type):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM ropes WHERE rope_type = ?", (rope_type,))
        return cursor.fetchall()

    def close(self):
        self.conn.close()
