import sqlite3

class BaseYachtDatabase:
    def __init__(self, db_path="data/base_yachts.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS base_yachts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            yacht_class TEXT,
            model TEXT,
            version TEXT,
            builder TEXT,
            designer TEXT,
            year_introduced INTEGER,
            production_start INTEGER,
            production_end INTEGER,
            country_of_origin TEXT,
            notes TEXT,
            hull_type TEXT,
            loa INTEGER,
            lwl INTEGER,
            beam INTEGER,
            draft INTEGER,
            displacement INTEGER,
            ballast INTEGER,
            construction TEXT,
            keel_type TEXT,
            keel_draft REAL,
            rudder_type TEXT,
            rig_type TEXT,
            boom_above_deck REAL,
            i REAL,
            j REAL,
            p REAL,
            e REAL,
            genoa_i REAL,
            genoa_j REAL,
            main_p REAL,
            main_e REAL,
            codezero_i REAL,
            codezero_j REAL,
            jib_i REAL,
            jib_j REAL,
            spin_i REAL,
            spin_j REAL,
            staysail_i REAL,
            staysail_j REAL,
            trisail_i REAL,
            trisail_j REAL,
            wind_speed_in_knots REAL,
            length_safety_factor REAL,
            halyard_load_safety_factor REAL,
            dynamic_load_safety_factor REAL,
            mainsail TEXT,
            jib TEXT,
            genoa TEXT,
            symmetric_spinnaker TEXT,
            asymmetric_spinnaker TEXT,
            codezero TEXT,
            staysail TEXT,
            trisail TEXT,
            stormjib TEXT
        )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()
