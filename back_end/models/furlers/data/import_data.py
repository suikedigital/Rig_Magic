from back_end.models.furlers.src.database import create_tables
create_tables()

import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'data.db'))
from back_end.models.furlers.data.temp_data import (
    FURLEX_PART_NUMBERS,
    FURLEX_LINK_PLATES,
    PROFURL_SELECTION_CRITERIA,
    PROFURL_REQUIRES_SWAGELES_EYE,
    PROFURL_PART_NUMBERS,
    PROFURL_TURNBUCKLE_CYLINDERS,
    PROFURL_LINK_PLATES,
    PROFURL_PREFEEDER_PART_NUMBERS,
    PROFURL_REEFING_KIT_PART_NUMBERS,
    FACNOR_SELECTION_CRITERIA,
    MKIV_PART_NUMBERS,
    MKIV_OCEAN_PART_NUMBERS,
    MKIV_UNDERDECK_PART_NUMBERS
)

def import_facnor_selection_criteria():
    with sqlite3.connect(DB_PATH) as conn:
        for row in FACNOR_SELECTION_CRITERIA:
            conn.execute(
                """
                INSERT INTO Facnor_Selection_Criteria (unit_name, min_loa, max_loa, min_dia, max_dia)
                VALUES (?, ?, ?, ?, ?)
                """,
                row
            )
        conn.commit()

def import_furlex_selection_criteria():
    def to_str(val):
        if isinstance(val, (tuple, list)):
            return ','.join(str(x) for x in val if x is not None)
        elif val is None:
            return ''
        else:
            return str(val)
    try:
        from temp_data import FURLEX_SELECTION_CRITERIA
    except ImportError:
        return
    if not FURLEX_SELECTION_CRITERIA:
        return
    with sqlite3.connect(DB_PATH) as conn:
        count = 0
        for row in FURLEX_SELECTION_CRITERIA:
            unit_name = row[0]
            stay_diameter = row[1]
            rod_diameter = row[2]
            righting_moment = row[3]
            displacement = row[4]
            rod_diameter_str = to_str(rod_diameter)
            righting_moment_str = to_str(righting_moment)
            displacement_str = to_str(displacement)
            conn.execute(
                """
                INSERT INTO Furlex_Selection_Criteria (unit_name, stay_diameter, rod_diameter, righting_moment, displacement)
                VALUES (?, ?, ?, ?, ?)
                """,
                (unit_name, stay_diameter, rod_diameter_str, righting_moment_str, displacement_str)
            )
            count += 1
        conn.commit()
        print(f"Inserted {count} rows into Furlex_Selection_Criteria.")

def import_harken_base_unit_part_numbers():
    with sqlite3.connect(DB_PATH) as conn:
        # Extract from all three dicts
        for d in [MKIV_PART_NUMBERS, MKIV_OCEAN_PART_NUMBERS, MKIV_UNDERDECK_PART_NUMBERS]:
            for unit_name, data in d.items():
                base = data.get("Base")
                foil = data.get("Foil")
                stay_length = foil[1] if foil and isinstance(foil, tuple) else None
                additional_foil_part_number = foil[0] if foil and isinstance(foil, tuple) else None
                additional_connector_part_number = data.get("Connector")
                # Handle all possible base structures
                if isinstance(base, tuple):
                    # If tuple of tuples (e.g., (('7413.11 3/4', 19.1), ('7413.11 7/8', 22.2)))
                    if all(isinstance(x, tuple) for x in base):
                        for b in base:
                            base_unit_part_number = b[0]
                            conn.execute(
                                """
                                INSERT INTO Harken_Base_Unit_Part_Numbers (unit_name, base_unit_part_number, stay_length, additional_foil_part_number, additional_connector_part_number)
                                VALUES (?, ?, ?, ?, ?)
                                """,
                                (unit_name, base_unit_part_number, stay_length, additional_foil_part_number, additional_connector_part_number)
                            )
                    else:
                        base_unit_part_number = base[0]
                        conn.execute(
                            """
                            INSERT INTO Harken_Base_Unit_Part_Numbers (unit_name, base_unit_part_number, stay_length, additional_foil_part_number, additional_connector_part_number)
                            VALUES (?, ?, ?, ?, ?)
                            """,
                            (unit_name, base_unit_part_number, stay_length, additional_foil_part_number, additional_connector_part_number)
                        )
                elif isinstance(base, str):
                    conn.execute(
                        """
                        INSERT INTO Harken_Base_Unit_Part_Numbers (unit_name, base_unit_part_number, stay_length, additional_foil_part_number, additional_connector_part_number)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (unit_name, base, stay_length, additional_foil_part_number, additional_connector_part_number)
                    )
        conn.commit()

def import_harken_rod_adapters():
    with sqlite3.connect(DB_PATH) as conn:
        for d in [MKIV_PART_NUMBERS, MKIV_OCEAN_PART_NUMBERS, MKIV_UNDERDECK_PART_NUMBERS]:
            for unit_name, data in d.items():
                rod_adapters = data.get("Rod_adapter")
                if rod_adapters:
                    for part_number, rod_diameter, thread in rod_adapters:
                        conn.execute(
                            """
                            INSERT INTO Harken_Rod_Adapters (part_number, rod_diameter, thread)
                            VALUES (?, ?, ?)
                            """,
                            (part_number, rod_diameter, thread)
                        )
        conn.commit()

def import_harken_selection_criteria():
    from back_end.models.furlers.data.temp_data import HARKEN_SELECTION_CRITERIA
    if not HARKEN_SELECTION_CRITERIA:
        return
    with sqlite3.connect(DB_PATH) as conn:
        count = 0
        for row in HARKEN_SELECTION_CRITERIA:
            unit_name = row[0]
            min_loa = row[1]
            max_loa = row[2]
            stay_diameters = row[3]
            rod_diameters = row[4]
            clevis_pin_diameters = row[5]
            def to_str(val):
                if isinstance(val, (tuple, list)):
                    return ','.join(str(x) for x in val if x is not None)
                elif val is None:
                    return ''
                else:
                    return str(val)
            stay_diameters_str = to_str(stay_diameters)
            rod_diameters_str = to_str(rod_diameters)
            clevis_pin_diameters_str = to_str(clevis_pin_diameters)
            conn.execute(
                """
                INSERT INTO Harken_Selection_Criteria (unit_name, min_loa, max_loa, stay_diameters, rod_diameters, clevis_pin_diameters)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (unit_name, min_loa, max_loa, stay_diameters_str, rod_diameters_str, clevis_pin_diameters_str)
            )
            count += 1
        conn.commit()
        print(f"Inserted {count} rows into Harken_Selection_Criteria.")

def import_harken_toggles():
    with sqlite3.connect(DB_PATH) as conn:
        for d in [MKIV_PART_NUMBERS, MKIV_OCEAN_PART_NUMBERS]:
            for unit_name, data in d.items():
                toggles = data.get("Toggles")
                if toggles:
                    for clevis_pin_diameter, toggle_list in toggles.items():
                        for toggle in toggle_list:
                            part_number = toggle.get("part_number")
                            toggle_type = toggle.get("type")
                            conn.execute(
                                """
                                INSERT INTO Harken_Toggles (unit_name, toggle_part_number, clevis_pin_diameter, type)
                                VALUES (?, ?, ?, ?)
                                """,
                                (unit_name, part_number, clevis_pin_diameter, toggle_type)
                            )
        conn.commit()

def import_furlex_parts_numbers():
    with sqlite3.connect(DB_PATH) as conn:
        for unit_name, wire_dict in FURLEX_PART_NUMBERS.items():
            for stay_diameter, length_dict in wire_dict.items():
                for stay_length, part_numbers in length_dict.items():
                    sta_lok, rigging_screw, stud_terminal = part_numbers
                    conn.execute(
                        """
                        INSERT INTO furlex_parts_numbers (unit_name, stay_diameter, stay_length, sta_lok_part_number, rigging_screw_part_number, stud_terminal_part_number)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (unit_name, stay_diameter, stay_length, sta_lok, rigging_screw, stud_terminal)
                    )
        conn.commit()

def import_furlex_link_plates():
    with sqlite3.connect(DB_PATH) as conn:
        for stay_diameter, part_number in FURLEX_LINK_PLATES:
            conn.execute(
                """
                INSERT INTO Furlex_Link_plates (stay_diameter, link_plate_part_number)
                VALUES (?, ?)
                """,
                (stay_diameter, part_number)
            )
        conn.commit()

def import_profurl_selection_criteria():
    with sqlite3.connect(DB_PATH) as conn:
        count = 0
        for row in PROFURL_SELECTION_CRITERIA:
            row = list(row)
            if row[-1] is None:
                row[-1] = ''
            else:
                row[-1] = ','.join(str(x) for x in row[-1] if x is not None)
            conn.execute(
                """
                INSERT INTO Profurl_Selection_Criteria (unit_name, min_loa, max_loa, max_sa, max_wire_diameter, max_rod_diameter, clevis_pin_size_range)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                tuple(row)
            )
            count += 1
        conn.commit()
        print(f"Inserted {count} rows into Profurl_Selection_Criteria.")

def import_profurl_requires_swageless_eye():
    with sqlite3.connect(DB_PATH) as conn:
        for unit_name, stay_diameter in PROFURL_REQUIRES_SWAGELES_EYE:
            conn.execute(
                """
                INSERT INTO Profurl_Requires_Swageless_Eye (unit_name, stay_diameter)
                VALUES (?, ?)
                """,
                (unit_name, stay_diameter)
            )
        conn.commit()

def import_profurl_part_numbers():
    with sqlite3.connect(DB_PATH) as conn:
        for unit_name, length_dict in PROFURL_PART_NUMBERS.items():
            for stay_length, part_number in length_dict.items():
                conn.execute(
                    """
                    INSERT INTO Profurl_Part_Numbers (unit_name, stay_length, part_number)
                    VALUES (?, ?, ?)
                    """,
                    (unit_name, stay_length, part_number)
                )
        conn.commit()

def import_profurl_turnbuckle_cylinders():
    with sqlite3.connect(DB_PATH) as conn:
        for unit_name, part_number in PROFURL_TURNBUCKLE_CYLINDERS.items():
            conn.execute(
                """
                INSERT INTO Profurl_Turnbuckle_Cylinders (unit_name, part_number)
                VALUES (?, ?)
                """,
                (unit_name, part_number)
            )
        conn.commit()

def import_profurl_link_plates():
    with sqlite3.connect(DB_PATH) as conn:
        for part_number, unit_names in PROFURL_LINK_PLATES.items():
            for unit_name in unit_names:
                conn.execute(
                    """
                    INSERT INTO Profurl_Link_Plates (unit_name, part_number)
                    VALUES (?, ?)
                    """,
                    (unit_name, part_number)
                )
        conn.commit()

def import_profurl_prefeeders():
    with sqlite3.connect(DB_PATH) as conn:
        for part_number, unit_names in PROFURL_PREFEEDER_PART_NUMBERS.items():
            for unit_name in unit_names:
                conn.execute(
                    """
                    INSERT INTO Profurl_Prefeeders (unit_name, part_number)
                    VALUES (?, ?)
                    """,
                    (unit_name, part_number)
                )
        conn.commit()

def import_profurl_reefing_kits():
    with sqlite3.connect(DB_PATH) as conn:
        for part_number, info in PROFURL_REEFING_KIT_PART_NUMBERS.items():
            models = ','.join(info["models"])
            description = info["description"]
            conn.execute(
                """
                INSERT INTO Profurl_Reefing_Kits (part_number, models, description)
                VALUES (?, ?, ?)
                """,
                (part_number, models, description)
            )
        conn.commit()

def import_facnor_requires_eye_turnbuckle():
    from back_end.models.furlers.data.temp_data import FACNOR_REQUIRES_EYE_TURNBUCKLE
    with sqlite3.connect(DB_PATH) as conn:
        count = 0
        for unit_name, stay_diameter in FACNOR_REQUIRES_EYE_TURNBUCKLE:
            conn.execute(
                """
                INSERT INTO Facnor_Requires_Eye_Turnbuckle (unit_name, stay_diameter)
                VALUES (?, ?)
                """,
                (unit_name, stay_diameter)
            )
            count += 1
        conn.commit()
        print(f"Inserted {count} rows into Facnor_Requires_Eye_Turnbuckle.")

def import_all():
    import_facnor_selection_criteria()
    import_facnor_requires_eye_turnbuckle()
    import_furlex_selection_criteria()
    import_furlex_parts_numbers()
    import_furlex_link_plates()
    import_harken_base_unit_part_numbers()
    import_harken_rod_adapters()
    import_harken_toggles()
    import_harken_selection_criteria()  # <-- Added missing call
    import_profurl_selection_criteria()
    import_profurl_requires_swageless_eye()
    import_profurl_part_numbers()
    import_profurl_turnbuckle_cylinders()
    import_profurl_link_plates()
    import_profurl_prefeeders()
    import_profurl_reefing_kits()

if __name__ == "__main__":
    import_all()
