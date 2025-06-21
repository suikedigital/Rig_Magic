print("temp_data.py loaded successfully")

FURLEX_PART_NUMBERS = {
    "Furlex 104s": {
        #Wire diameter in mm
        4: {
        # Stay length in mm
                    #Stalok , Riggingscrew, Stud Terminal
            8100: ["030-020-51", "030-020-61", "030-020-91"],
            10500: ["030-020-52", "030-020-62", "030-020-92"],
        },
        5: {
            8100: ["030-020-53", "030-020-63", "030-020-93"],
            10500: ["030-020-54", "030-020-64", "030-020-94"],
            12900: ["030-020-55", "030-020-65", "030-020-95"],
        },
        6: {
            10500: ["030-020-56", "030-020-66", "030-020-96"],
            12900: ["030-020-57", "030-020-67", "030-020-97"],
        },
    },
    "Furlex 204s": {
        6: {
            10550: ["035-025-51", "035-025-61", "035-025-91"],
            12950: ["035-025-52", "035-025-62", "035-025-92"],
            15350: ["035-025-53", "035-025-63", "035-025-93"],
        },
        7: {
            12950: ["035-025-54", "035-025-64", "035-025-94"],
            15350: ["035-025-55", "035-025-65", "035-025-95"],
            17750: ["035-025-56", "035-025-66", "035-025-96"],
        },
        8: {
            15350: ["035-025-57", "035-025-67", "035-025-97"],
            17750: ["035-025-58", "035-025-68", "035-025-98"],
        },
    },
    "Furlex 304s": {
        8: {
            15450: ["042-031-51", "042-031-61", "042-031-91"],
            17850: ["042-031-52", "042-031-62", "042-031-92"],
        },
        10: {
            15480: ["042-031-53", "042-031-63", "042-031-93"],
            17880: ["042-031-54", "042-031-64", "042-031-94"],
            20280: ["042-031-55", "042-031-65", "042-031-95"],
        },
    },
    "Furlex 404s": {
        12: {
            17700: ["052-038-51", "052-038-61", "052-038-91"],
            20100: ["052-038-52", "052-038-62", "052-038-92"],
            22500: ["052-038-53", "052-038-63", "052-038-93"],
        },
        14: {
            20100: ["052-038-54", "052-038-64", "052-038-94"],
        },
    },
}              #4          #5mm.      #6/7mm.      #8/10mm.    #12mm       #14mm
FURLEX_LINK_PLATES = [
    [4, "517-944-01"],
    [5, "517-945-01"],
    [6, "517-063-01"],
    [7, "517-063-01"],
    [8, "517-062-01"],
    [10, "517-062-01"],
    [12, "517-075-01"],
    [14, "517-076-01"]
]
# HARKEN_FURLER_PART_NUMBERS START
# each furler type has its own dictornaty, you will need to extract the toggles, rod adapters, and connectors from each dictionary
MKIV_PART_NUMBERS = {
    "Harken MKIV Unit 0": {
        "Base": "7410.10",
        "Foil": ("7410.30", 11700),
        "Toggles": {
            7.9: [
                {"part_number": "7410.20 5/16", "type": "Eye/Jaw"},
            ],
            9.5: [
                {"part_number": "7410.20 3/8", "type": "Eye/Jaw"},
            ],
            11.1: [
                {"part_number": "7410.20 7/16", "type": "Eye/Jaw"},
            ],
        },
        "Connector": "7410.31",
        "Rod_adapter": (
            ("7420 -4", 4.37, "UNF-7/16"),
            ("7421 -6", 5.03, "UNF-7/16"),
        ),
    },
    "Harken MKIV Unit 1": {
        "Base": "7411.10",
        "Foil": ("7411.30", 13990),
        "Toggles": {
            12.7: [
                {"part_number": "7411.20 1/2", "type": "Eye/Jaw"},
                {"part_number": "7311.20 1/2", "type": "Jaw/Jaw"},
                {"part_number": "7311.21 1/2", "type": "Long_Link_Tog"},
            ],
            15.9: [
                {"part_number": "7311.20 5/8", "type": "Stud/Jaw", "thread": "UNF-5/8"},
                {"part_number": "7311.21 5/8", "type": "Long_Link_Tog"},
            ],
        },
        "Connector": "7411.31",
        "Rod_adapter": (
            ("7422 -8", 5.72, "UNF-1/2"),
            ("7423 -10", 6.35, "UNF-1/2"),
            ("7424 -12", 7.14, "UNF-5/8"),
        ),
    },
    "Harken MKIV Unit 2": {
        "Base": "7412.10",
        "Foil": ("7412.30", 18380),
        "Toggles": {
            15.9: [
                {"part_number": "7412.20 5/8", "type": "Eye/Jaw"},
                {"part_number": "7312.20 5/8", "type": "Jaw/Jaw"},
                {"part_number": "7312.21 5/8", "type": "Long_Link_Tog"},
            ],
            19.1: [
                {"part_number": "7312.20 3/4", "type": "Stud/Jaw", "thread": "UNF-3/4"},
                {"part_number": "7312.21 3/4", "type": "Long_Link_Tog"},
            ],
        },
        "Connector": "7412.31",
        "Rod_adapter": (
            ("7424 -12", 7.14, "UNF-5/8"),
            ("7425 -17", 8.38, "UNF-5/8"),
            ("7427 -22", 9.53, "UNF-3/4"),
        ),
    },
    "Harken MKIV Unit 3": {
        "Base": ("7413.10", "No Furling Line"),
        "Foil": ("7413.30", 22760),
        "Toggles": {
            19.1: [
                {"part_number": "7413.20 3/4", "type": "Jaw/Jaw"},
                {"part_number": "7313.21 3/4", "type": "Long_Link_Tog"},
            ],
            22.2: [
                {"part_number": "7413.20 7/8", "type": "Jaw/Jaw"},
                {"part_number": "7313.21 7/8", "type": "Long_Link_Tog"},
            ],
        },
        "Connector": "7413.31",
        "Rod_adapter": (
            ("7426 -22", 9.53, "UNF-3/4"),
            ("7427 -30", 11.1, "UNF-7/8"),
        ),
    },
    "Harken MKIV Unit 4": {
        "Base": ("7414.10", "No Furling Line"),
        "Foil": ("7414.30", 22880),
        "Toggles": {
            22.2: [
                {"part_number": "7414.20 7/8", "type": "Jaw/Jaw"},
            ],
            25.4: [
                {"part_number": "7414.20 1", "type": "Jaw/Jaw"},
            ],
            28.57: [
                {"part_number": "7414.20 1 1/8", "type": "Jaw/Jaw"},
            ],
        },
        "Connector": "7414.31",
        "Rod_adapter": (
            ("7427 -30", 11.1, "UNF-7/8"),
            ("7428 -40", 12.7, "UNF-1"),
            ("7429 -48", 28.6, "UNF-1 1/8"),
        ),
    },
}

MKIV_OCEAN_PART_NUMBERS = {
    "Harken MKIV Ocean Unit 0": {
        "Base": "7510.10",
        "Foil": ("7510.30", 11700),
        "Toggles": {
            7.9: [
                {"part_number": "7410.20 5/16", "type": "Eye/Jaw"},
            ],
            9.5: [
                {"part_number": "7410.20 3/8", "type": "Eye/Jaw"},
            ],
            11.1: [
                {"part_number": "7410.20 7/16", "type": "Eye/Jaw"},
            ],
        },
        "Connector": "7510.31",
        "Rod_adapter": (
            ("7420 -4", 4.37, "UNF-7/16"),
            ("7421 -6", 5.03, "UNF-7/16"),
        ),
    },
    "Harken MKIV Ocean Unit 1": {
        "Base": "7511.10",
        "Foil": ("7511.30", 13990),
        "Toggles": {
            12.7: [
                {"part_number": "7411.20 1/2", "type": "Eye/Jaw"},
                {"part_number": "7311.20 1/2", "type": "Jaw/Jaw"},
                {"part_number": "7311.21 1/2", "type": "Long_Link_Tog"},
            ],
            15.9: [
                {"part_number": "7311.20 5/8", "type": "Stud/Jaw", "thread": "UNF-5/8"},
                {"part_number": "7311.21 5/8", "type": "Long_Link_Tog"},
            ],
        },
        "Connector": "7511.31",
        "Rod_adapter": (
            ("7422 -8", 5.72, "UNF-1/2"),
            ("7423 -10", 6.35, "UNF-1/2"),
            ("7424 -12", 7.14, "UNF-5/8"),
        ),
    },
    "Harken MKIV Ocean Unit 2": {
        "Base": "7512.10",
        "Foil": ("7512.30", 18380),
        "Toggles": {
            15.9: [
                {"part_number": "7412.20 5/8", "type": "Eye/Jaw"},
                {"part_number": "7312.20 5/8", "type": "Jaw/Jaw"},
                {"part_number": "7312.21 5/8", "type": "Long_Link_Tog"},
            ],
            19.1: [
                {"part_number": "7312.20 3/4", "type": "Stud/Jaw", "thread": "UNF-3/4"},
                {"part_number": "7312.21 3/4", "type": "Long_Link_Tog"},
            ],
        },
        "Connector": "7512.31",
        "Rod_adapter": (
            ("7424 -12", 7.14, "UNF-5/8"),
            ("7425 -17", 8.38, "UNF-5/8"),
            ("7427 -22", 9.53, "UNF-3/4"),
        ),
    },
    "Harken MKIV Ocean Unit 3": {
        "Base": ("7513.10", "No Furling Line"),
        "Foil": ("7513.30", 22760),
        "Toggles": {
            19.1: [
                {"part_number": "7413.20 3/4", "type": "Jaw/Jaw"},
                {"part_number": "7313.21 3/4", "type": "Long_Link_Tog"},
            ],
            22.2: [
                {"part_number": "7413.20 7/8", "type": "Jaw/Jaw"},
                {"part_number": "7313.21 7/8", "type": "Long_Link_Tog"},
            ],
            25.4: [
                {"part_number": "7413.20 1", "type": "Jaw/Jaw"},
                {"part_number": "7513.21 1", "type": "Long_Link_Tog"},
            ],
            28.6: [
                {"part_number": "7413.20 1 1/8", "type": "Jaw/Jaw"},
                {"part_number": "7513.21 1 1/8", "type": "Long_Link_Tog"},
            ],
        },
        "Connector": "7513.31",
        "Rod_adapter": (
            ("7426 -22", 9.53, "UNF-3/4"),
            ("7427 -30", 11.1, "UNF-7/8"),
            ("7428 -40", 12.7, "UNF-1"),
            ("7429 -48", 28.6, "UNF-1 1/8"),
        ),
    },
}

MKIV_UNDERDECK_PART_NUMBERS = {
    "Harken MKIV Underdeck Unit 0": {
        "Base": "7410.11",
        "Foil": ("7410.30", 11700),
        "Connector": "7410.31",
    },
    "Harken MKIV Underdeck Unit 1": {
        "Base": ("7411.11 1/2", 12.7),
        "Foil": ("7411.30", 13990),
        "Connector": "7411.31",
    },
    "Harken MKIV Underdeck Unit 2": {
        "Base": ("7412.11 5/8", 15.9),
        "Foil": ("7412.30", 18380),
        "Connector": "7412.31",
    },
    "Harken MKIV Underdeck Unit 3": {
        "Base": (("7413.11 3/4", 19.1), ("7413.11 7/8", 22.2)),
        "Foil": ("7410.30", 22880),
        "Connector": "7410.31",
    },
}

# HARKEN_FURLER_PART_NUMBERS END

FACNOR_SELECTION_CRITERIA = [
    # Facnor furler specifications
    # Unit name, Min LOA (m), Max LOA (m), Min Wire Dia (mm), Max Wire Dia (mm)
    ("Facnor LS-60", 5500, 7000, 0, 5),
    ("Facnor LS-70", 6500, 8000, 0, 5),
    ("Facnor LS-100", 7500, 9000, 0, 6),
    ("Facnor LS-130", 8000, 11000, 0, 7),
    ("Facnor LS-165", 9000, 12000, 0, 10),
    ("Facnor LS-180", 10000, 13000, 0, 10),
    ("Facnor LS-200", 11500, 14000, 0, 12),
    ("Facnor LS-290", 13000, 18000, 0, 14),
    ("Facnor LS-330", 15000, 28000, 0, 22),
    ("Facnor RX-70", 6500, 8000, 0, 5),
    ("Facnor RX-100", 7500, 8500, 5, 6),
    ("Facnor RX-130", 8000, 9500, 6, 7),
    ("Facnor RX-165", 9000, 11500, 0, 8),
    ("Facnor RX-220", 10000, 12500, 8, 10),
    ("Facnor RX-260", 11500, 15000, 0, 10),
    ("Facnor RX-300", 13000, 18000, 0, 12.7)
]

FACNOR_REQUIRES_EYE_TURNBUCKLE = {
    # Facnor models that require an eye turnbuckle
    # name, dia
    ("Facnor LS-130", 7),
    ("Facnor LS-165", 10),
    ("Facnor LS-180", 10),
    ("Facnor LS-200", 12),
    ("Facnor LS-290", 14),
    ("Facnor LS-330", 22),
}
FURLEX_SELECTION_CRITERIA = [
    ("Furlex 104s", 4, None, (6.5, 8), (1.4, 1.7)),
    ("Furlex 104s", 5, None, (10, 14.5), (2.1, 3)),
    ("Furlex 104s", 6, None, (17, 22), (3.5, 4)),
    ("Furlex 204s", 6, 5.7, (19, 23), (3.9, 4.5)),
    ("Furlex 204s", 7, 6.4, (27, 34), (5.5, 7)),
    ("Furlex 204s", 8, (7.1, 7.5), (37, 45), (7.5, 9)),
    ("Furlex 304s", 8, (7.1, 7.5), (40, 50), (8, 10)),
    ("Furlex 304s", 10, (8.4, 9.5), (70, 80), (14, 15)),
    ("Furlex 404s", 12, (11.1,), (120, 160), (20, 26)),
    ("Furlex 404s", 14, (11.1, 12.7), (180, 190), (28, 30)),
]
HARKEN_SELECTION_CRITERIA = [
    # (unit_name, min_loa, max_loa, wire_diams, rod_diams, pin_sizes, underdeck)
    ("Harken MKIV Unit 0", 6500, 9000, (4, 5, 6), (4.37, 5.03), (7.9, 9.5, 11.1)),
    ("Harken MKIV Unit 1", 8300, 11000, (6, 7, 8), (5.72, 6.35, 7.14), (12.7, 15.9)),
    ("Harken MKIV Unit 2", 10600, 14200, (8, 10), (7.14, 8.38, 9.53), (15.9, 19.1)),
    ("Harken MKIV Unit 3", 13700, 18300, (11, 12), (9.53, 11.1), (19.1, 22.2)),
    ("Harken MKIV Unit 4", 19800, 24400, (12, 14, 16), (11.1, 12.7, 14.3), (22.2, 25.4, 28.57)),
    ("Harken MKIV Ocean Unit 0", 6500, 9000, (4, 5, 6), (4.37, 5.03), (7.9, 9.5, 11.1)),
    ("Harken MKIV Ocean Unit 1", 8300, 11000, (6, 7, 8), (5.72, 6.35, 7.14), (12.7, 15.9)),
    ("Harken MKIV Ocean Unit 2", 10600, 14200, (8, 10), (7.14, 8.38, 9.53), (15.9, 19.1)),
    ("Harken MKIV Ocean Unit 3", 13700, 18300, (11, 12), (9.53, 11.1), (19.1, 22.2, 25.4, 28.6)),
    ("Harken MKIV Underdeck Unit 0", 6700, 9100, (5, 6), (4.37, 5.03), (None)),
    ("Harken MKIV Underdeck Unit 1", 8300, 11000, (6, 7, 8), (5.72, 6.35), (12.7,)),
    ("Harken MKIV Underdeck Unit 2", 10600, 14200, (8, 10), (7.14, 8.38), (15.9,)),
    ("Harken MKIV Underdeck Unit 3", 13700, 18300, (11, 12), (9.53, 11.1), (19.1, 22.2)),
]

PROFURL_SELECTION_CRITERIA =[
    # Profurl furler specifications
    # Unit name, Min LOA (mm), Max LOA (mm), Max SA (m2), Max wire Dia (mm), Max Rod Dia (mm), clevis pin size range
    ("R250", 6000, 9000, 30, 6.35, 4.37, (8, 10, 12, 14, 16)),
    ("R350", 8500, 12500, 45, 8, 6.35, (8, 10, 12, 14, 16)),
    ("R420", 11500, 14500, 70, 10, 7.14, (10, 12, 14, 16, 19, 22, 25)),
    ("R430", 12000, 15500, 90, 11.1, 7.92, (10, 12, 14, 16, 19, 22, 25)),
    ("R480", 13500, 19000, 100, 12.7, 9.53, (16, 18, 19, 22, 25, 28)),
    ("C260", 5000, 7000, 15, 5, None, (None)),
    ("C290", 7000, 9500, 30, 6, 4.37, (8, 10, 12, 14, 16)),
    ("C320", 9250, 11000, 40, 7, 5.03, (8, 10, 12, 14, 16)),
    ("C350", 10500, 12500, 55, 8, 6.35, (10, 12, 14, 16, 19, 22, 25)),
    ("C420", 12000, 15000, 80, 10, 7.14, (10, 12, 14, 16, 19, 22, 25)),
    ("C430", 13000, 17000, 100, 12.7, 9.53, (10, 12, 14, 16, 19, 22, 25)),
    ("C480", 13500, 17500, 120, 14.3, 10.72, (16, 18, 19, 22, 25, 28)),
    ("C520", 16500, 18000, 140, 16, 12.70, (16, 18, 19, 22, 25, 28)),
    ("C530", 18500, 27000, 220, 19, 14.27, (16, 18, 19, 22, 25, 28))
]

PROFURL_REQUIRES_SWAGELES_EYE ={
    # Profurl models that require a swage-less eye
    # Unit name, stay diameter
    ("R480", 14),
    ("C290", 7),
    ("C320", 8),
    ("C350", 10),
    ("C350", 12.7),
    ("C520", 19)
}

# Auto-generated Profurl part numbers dictionary
# Structure: {unit: {stay_length_mm: part_number}}
PROFURL_PART_NUMBERS = {
    'R250': {
        8000: 'R25008',
        10000: 'R25010',
        12000: 'R25012',
    },
    'R480': {
        18000: 'R48018',
        20000: 'R48020',
        22000: 'R48022',
    },
    'C290': {
        8000: 'C29008',
        10000: 'C29010',
        12000: 'C29012',
        14000: 'C29014',
    },
    'C320': {
        8000: 'C32008',
        10000: 'C32010',
        12000: 'C32012',
        14000: 'C32014',
        16000: 'C32016',
    },
    'C350': {
        12000: 'C35012',
        14000: 'C35014',
        16000: 'C35016',
        18000: 'C35018',
    },
    'C420': {
        16000: 'C42016',
        18000: 'C42018',
        20000: 'C42020',
    },
    'C430': {
        18000: 'C43018',
        20000: 'C43020',
        22000: 'C43022',
    },
    'C480': {
        18000: 'C48018',
        20000: 'C48020',
        22000: 'C48022',
    },
    'C520': {
        20000: 'C52020',
        22000: 'C52022',
        24000: 'C52024',
    },
    'C530': {
        22000: 'C53022',
        24000: 'C53024',
        26000: 'C53026',
    },
}

# Turnbuckle _cylinder part numbers
PROFURL_TURNBUCKLE_CYLINDERS = {
    'R250': 'PF-P251040',
    'R350': 'PF-P256040',
    'R420': 'PF-P255040',
    'R430': 'PF-P254040',
    'R480': 'PF-P265040',
    'C260': 'PF-P261040',
    'C290': 'PF-P262040',
    'C320': 'PF-P252040',
    'C350': 'PF-P253040',
    'C420': 'PF-P254040',
    'C430': 'PF-P254040',
    'C480': 'PF-P265040',
    'C520': 'PF-P268040',
    'C530': 'PF-P268040'
}

# Link plates for Profurl furlers
PROFURL_LINK_PLATES = {
    "PF-P250313": ["C290", "C320", "R250", "R350"],
    "PF-P253312": ["C350", "C360", "C370", "C390", "C420", "C430", "R420", "R430"],
    "PF-P265212": ["C480", "C490", "C520", "C530", "R480"],
    "PF-P265222": ["C480", "C490", "C520", "C530", "R480"],
}

PROFURL_PREFEEDER_PART_NUMBERS = {
    7485: ["C290","C320","C350","C420","C430","C480","C520","C530"]
}

PROFURL_REEFING_KIT_PART_NUMBERS = {
    "PF-P250901": {
        "models": ["C260", "C320", "R250", "R350"],
        "description": "20m reefing line Ø 6mm"
    },
    "PF-P250902": {
        "models": ["C290", "C300", "C310", "C320", "C330", "C340", "C350", "C360", "C370", "C380", "C390", "C400", "C410", "C420", "C430", "R350", "R360", "R370", "R380", "R390", "R400", "R410", "R420", "R430"],
        "description": "25m reefing line Ø 8mm"
    },
    "PF-P250903": {
        "models": ["C350", "C360", "C370", "C380", "C390", "C400", "C410", "C420", "C430", "C440", "C450", "C460", "C470", "C480", "R350", "R360", "R370", "R380", "R390", "R400", "R410", "R420", "R430", "R440", "R450", "R460", "R470", "R480"],
        "description": "25m reefing line Ø 10mm"
    },
    "PF-P250904": {
        "models": ["C430", "C440", "C450", "C460", "C470", "C480", "C490", "C500", "C510", "C520", "C530", "R420", "R430"],
        "description": "30m reefing line Ø 10mm"
    }
}