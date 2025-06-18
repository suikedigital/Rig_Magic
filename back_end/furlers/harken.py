class HarkenFurler:
    def __init__(self, unit_name, stay_diameter, clevis_pin_diam, rod):
        self.unit_name = unit_name
        self.stay_diameter = stay_diameter
        self.clevis_pin_diam = clevis_pin_diam
        self.rod = rod

    def __repr__(self):
        return f"<HarkenFurler {self.unit_name}, Stay Diameter: {self.stay_diameter}, Clevis Pin Diameter: {self.clevis_pin_diam}, Rod: {self.rod}>"
    
class HarkenFurlerSelector:
    FURLER_SPECS = [
        # Harken furler specifications
        # Unit name, Min LOA (m), Max LOA (m), Wire Diams (mm), Rod Diams,  Pin sizes (mm)
        ("Harken MKIV Unit 0" , 6500, 9000, (4, 5, 6), (4.37, 5.03), (7.9, 9.5, 11.1)),
        ("Harken MKIV Unit 1" , 8300, 11000, (6, 7, 8), (5.72, 6.35, 7.14), (12.7, 15.9)),
        ("Harken MKIV Unit 2" , 10600, 14200, (8, 10), (7.14, 8.38, 9.53), (15.9, 19.1)),
        ("Harken MKIV Unit 3" , 13700, 18300, (11, 12), (9.53, 11.1), (19.1, 22.2)),
        ("Harken MKIV Unit 4" , 19800, 24400, (12, 14, 16),(11.1, 12.7, 14.3), (22.2, 25.4, 28.6)),
        ("Harken MKIV Ocean Unit 0" , 6500, 9000, (4, 5, 6), (4.37, 5.03), (7.9, 9.5, 11.1)),
        ("Harken MKIV Ocean Unit 1" , 8300, 11000, (6, 7, 8), (5.72, 6.35, 7.14), (12.7, 15.9)),
        ("Harken MKIV Ocean Unit 2" , 10600, 14200, (11, 8, 10), (7.14, 8.38, 9.53), (15.9, 19.1)),
        ("Harken MKIV Ocean Unit 3" , 13700, 24400, (11, 12, 14, 16), (9.53, 11.1, 12.7, 14.3), (19.1, 22.2, 25.4, 28.8)),
        ("Harken MKIV Underdeck Unit 0", 6700, 9100, (5, 6), (4.37, 5.03), (None)),
        ("Harken MKIV Underdeck Unit 1", 8300, 11000, (6, 7, 8), (5.72, 6.35), (12.7)),
        ("Harken MKIV Underdeck Unit 2", 10600, 14200, (8, 10), (7.14, 8.38), (15.9)),
        ("Harken MKIV Underdeck Unit 3", 13700, 18300, (11, 12), (9.53, 11.1), (19.1, 22.2)),
    ]

    def spec_furlers(self, loa, stay_diameter, clevis_pin_diam, rod=False):
        possible_furlers = []
        for unit_name, min_loa, max_loa, wire_diams, rod_diams, pin_sizes in self.FURLER_SPECS:
            if min_loa <= loa <= max_loa and stay_diameter in wire_diams:
                if rod and rod_diams is not None and stay_diameter not in rod_diams:
                    continue
                # Safely handle None or non-iterable pin_sizes
                if not pin_sizes or pin_sizes is None or clevis_pin_diam not in (pin_sizes if isinstance(pin_sizes, tuple) else (pin_sizes,)):
                    continue
                model = HarkenFurler(unit_name, stay_diameter, clevis_pin_diam, rod)
                possible_furlers.append(model)
        return possible_furlers if possible_furlers else []

if __name__ == "__main__":
    selector = HarkenFurlerSelector()
    # Example parameters that should return multiple matches
    loa = 10400  # Length Over All in mm
    stay_diameter = 8  # Diameter of the stay in mm
    clevis_pin_diam = 12.7  # Diameter of the clevis pin in mm
    rod = False  # Whether rod is used or not

    matching_furlers = selector.spec_harkens(loa, stay_diameter, clevis_pin_diam, rod)
    if matching_furlers:
        for furler in matching_furlers:
            print(furler)
    else:
        print("No matching Harken furlers found.")