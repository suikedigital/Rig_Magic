import sqlite3
from typing import List, Optional, Dict, Any

import os   
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data.db'))

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Facnor_Selection_Criteria (     
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            min_loa INTEGER NOT NULL,
            max_loa INTEGER NOT NULL,
            min_dia REAL NOT NULL,
            max_dia REAL NOT NULL
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Facnor_Requires_Eye_Turnbuckle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            stay_diameter REAL NOT NULL
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS  Furlex_Selection_Criteria(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            stay_diameter REAL NOT NULL,
            rod_diameter TEXT,
            righting_moment TEXT,
            displacement TEXT
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS furlex_parts_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            stay_diameter REAL NOT NULL,
            stay_length INTEGER NOT NULL,
            sta_lok_part_number TEXT NOT NULL,
            rigging_screw_part_number TEXT NOT NULL,
            stud_terminal_part_number TEXT NOT NULL
            )''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Furlex_Link_plates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stay_diameter REAL,
            link_plate_part_number TEXT NOT NULL
            )''')
            
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Harken_Selection_Criteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            min_loa INTEGER NOT NULL,
            max_loa INTEGER NOT NULL,
            stay_diameters TEXT,
            rod_diameters TEXT,
            clevis_pin_diameters TEXT
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Harken_Base_Unit_Part_Numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            base_unit_part_number TEXT NOT NULL,
            stay_length INTEGER NOT NULL,
            additional_foil_part_number TEXT,
            additional_connector_part_number TEXT
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Harken_Toggles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            toggle_part_number TEXT NOT NULL,
            clevis_pin_diameter REAL NOT NULL,
            type TEXT
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Harken_Rod_Adapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_number TEXT NOT NULL,
            rod_diameter REAL NOT NULL,
            thread TEXT NOT NULL
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profurl_Selection_Criteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            min_loa INTEGER NOT NULL,
            max_loa INTEGER NOT NULL,
            max_sa REAL NOT NULL,
            max_wire_diameter REAL NOT NULL,
            max_rod_diameter REAL,
            clevis_pin_size_range TEXT NOT NULL
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profurl_Requires_Swageless_Eye (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            stay_diameter REAL NOT NULL
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profurl_Part_Numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            stay_length INTEGER NOT NULL,
            part_number TEXT NOT NULL
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profurl_Turnbuckle_Cylinders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            part_number TEXT NOT NULL
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profurl_Link_Plates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            part_number TEXT NOT NULL
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profurl_Prefeeders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_name TEXT NOT NULL,
            part_number TEXT NOT NULL
            )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profurl_Reefing_Kits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_number TEXT NOT NULL,
            models TEXT NOT NULL,
            description TEXT NOT NULL
            )''')

def get_facnor_selection_criteria():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT unit_name, min_loa, max_loa, min_dia, max_dia FROM Facnor_Selection_Criteria')
        results = []
        for row in cursor.fetchall():
            results.append({
                'unit_name': row[0],
                'min_loa': int(row[1]),
                'max_loa': int(row[2]),
                'min_dia': float(row[3]),
                'max_dia': float(row[4])
            })
    return results

def get_facnor_requires_eye_turnbuckle():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Facnor_Requires_Eye_Turnbuckle')
        results = cursor.fetchall()
    return results

def get_furlex_selection_criteria():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT unit_name, stay_diameter, rod_diameter, righting_moment, displacement FROM Furlex_Selection_Criteria')
        results = []
        for unit_name, stay_diameter, rod_diameter, righting_moment, displacement in cursor.fetchall():
            rod_diameter_list = [float(x) for x in rod_diameter.split(',') if x] if rod_diameter else []
            righting_moment_list = [float(x) for x in righting_moment.split(',') if x] if righting_moment else []
            displacement_list = [float(x) for x in displacement.split(',') if x] if displacement else []
            results.append((unit_name, stay_diameter, rod_diameter_list, righting_moment_list, displacement_list))
    return results

def get_furlex_parts_numbers():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM furlex_parts_numbers')
        results = []
        for unit_name, stay_diameter, stay_length, sta_lok_part_number, rigging_screw_part_number, stud_terminal_part_number in cursor.fetchall():
            results.append({
                'unit_name': unit_name,
                'stay_diameter': stay_diameter,
                'stay_length': stay_length,
                'sta_lok_part_number': sta_lok_part_number,
                'rigging_screw_part_number': rigging_screw_part_number,
                'stud_terminal_part_number': stud_terminal_part_number
            })
    return results

def get_furlex_link_plates():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Furlex_Link_plates')
        results = cursor.fetchall()
    return results

def find_furlex_part(unit_name, stay_diameter, requested_stay_length):
    """
    Find the furlex part with the smallest stay_length >= requested_stay_length for the given unit_name and stay_diameter.
    Returns a dict with part numbers and the matched stay_length, or None if not found.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT stay_length, sta_lok_part_number, rigging_screw_part_number, stud_terminal_part_number
            FROM furlex_parts_numbers
            WHERE unit_name = ? AND stay_diameter = ? AND stay_length >= ?
            ORDER BY stay_length ASC
            LIMIT 1
            ''',
            (unit_name, stay_diameter, requested_stay_length)
        )
        row = cursor.fetchone()
        if row:
            return {
                'stay_length': row[0],
                'sta_lok_part_number': row[1],
                'rigging_screw_part_number': row[2],
                'stud_terminal_part_number': row[3]
            }
        else:
            return None

def find_furlex_link_plate(stay_diameter):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT link_plate_part_number FROM Furlex_Link_plates WHERE stay_diameter = ?",
            (stay_diameter,)
        )
        row = cursor.fetchone()
        return row[0] if row else None
    
def get_harken_selection_criteria():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT unit_name, min_loa, max_loa, stay_diameters, rod_diameters, clevis_pin_diameters FROM Harken_Selection_Criteria')
        results = []
        for unit_name, min_loa, max_loa, stay_diameters, rod_diameters, clevis_pin_diameters in cursor.fetchall():
            stay_diameters_list = [float(x) for x in stay_diameters.split(',') if x] if stay_diameters else []
            rod_diameters_list = [float(x) for x in rod_diameters.split(',') if x] if rod_diameters else []
            clevis_pin_diameters_list = [float(x) for x in clevis_pin_diameters.split(',') if x] if clevis_pin_diameters else []
            results.append({
                'unit_name': unit_name,
                'min_loa': int(min_loa),
                'max_loa': int(max_loa),
                'stay_diameters': stay_diameters_list,
                'rod_diameters': rod_diameters_list,
                'clevis_pin_diameters': clevis_pin_diameters_list
            })
    return results

def get_harken_toggles(unit_name=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        if unit_name:
            cursor.execute('SELECT toggle_part_number, clevis_pin_diameter, type FROM Harken_Toggles WHERE unit_name = ?', (unit_name,))
        else:
            cursor.execute('SELECT unit_name, toggle_part_number, clevis_pin_diameter, type FROM Harken_Toggles')
        results = []
        for row in cursor.fetchall():
            if unit_name:
                results.append({'toggle_part_number': row[0], 'clevis_pin_diameter': row[1], 'type': row[2]})
            else:
                results.append({'unit_name': row[0], 'toggle_part_number': row[1], 'clevis_pin_diameter': row[2], 'type': row[3]})
    return results

def get_harken_rod_adapters():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT part_number, rod_diameter, thread FROM Harken_Rod_Adapters')
        results = []
        for row in cursor.fetchall():
            results.append({'part_number': row[0], 'rod_diameter': row[1], 'thread': row[2]})
    return results

def get_profurl_selection_criteria():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT unit_name, min_loa, max_loa, max_sa, max_wire_diameter, max_rod_diameter, clevis_pin_size_range FROM Profurl_Selection_Criteria')
        results = []
        for unit_name, min_loa, max_loa, max_sa, max_wire_diameter, max_rod_diameter, clevis_pin_size_range in cursor.fetchall():
            clevis_pin_list = [float(x) for x in clevis_pin_size_range.split(',') if x] if clevis_pin_size_range else []
            results.append({
                'unit_name': unit_name,
                'min_loa': int(min_loa),
                'max_loa': int(max_loa),
                'max_sa': float(max_sa),
                'max_wire_diameter': float(max_wire_diameter),
                'max_rod_diameter': float(max_rod_diameter) if max_rod_diameter is not None else None,
                'clevis_pin_size_range': clevis_pin_list
            })
    return results

# Profurl part numbers

def find_profurl_part(unit_name, requested_stay_length):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT stay_length, part_number FROM Profurl_Part_Numbers WHERE unit_name = ? AND stay_length >= ? ORDER BY stay_length ASC LIMIT 1''',
            (unit_name, requested_stay_length)
        )
        row = cursor.fetchone()
        if row:
            return {'stay_length': row[0], 'part_number': row[1]}
        else:
            return None

def get_profurl_link_plate(unit_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT part_number FROM Profurl_Link_Plates WHERE unit_name = ?', (unit_name,))
        return [row[0] for row in cursor.fetchall()]

def get_profurl_turnbuckle_cylinder(unit_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT part_number FROM Profurl_Turnbuckle_Cylinders WHERE unit_name = ?', (unit_name,))
        row = cursor.fetchone()
        return row[0] if row else None

def get_profurl_reefing_kit(unit_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT part_number, description FROM Profurl_Reefing_Kits WHERE models LIKE ?', (f'%{unit_name}%',))
        return [{'part_number': row[0], 'description': row[1]} for row in cursor.fetchall()]

def get_profurl_prefeeder(unit_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT part_number FROM Profurl_Prefeeders WHERE unit_name = ?', (unit_name,))
        row = cursor.fetchone()
        return row[0] if row else None

def requires_profurl_swageless_eye(unit_name, stay_diameter):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT 1 FROM Profurl_Requires_Swageless_Eye WHERE unit_name = ? AND stay_diameter = ?',
            (unit_name, stay_diameter)
        )
        return cursor.fetchone() is not None