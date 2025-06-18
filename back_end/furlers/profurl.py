class ProfurlFurler:
    """
    Class to handle the profurl functionality.
    """
    def __init__(self, unit_name, stay_diameter, clevis_pin_diameter, requires_swage_swageless_eye=False):
        self.unit_name = unit_name
        self.stay_diameter = stay_diameter
        self.clevis_pin_diameter = clevis_pin_diameter
        self.requires_swage_swageless_eye = requires_swage_swageless_eye

    def __repr__(self):
        return (
            f"<ProfurlFurlerModel name={self.unit_name}, "
            f"Stay Diameter={self.stay_diameter}, "
            f"Clevis Pin Diameter={self.clevis_pin_diameter}, "
            f"Requires Swageless Eye={self.requires_swage_swageless_eye}>"
        )

class ProfurlSelector:
    Furler_Specs =[
        # Profurl furler specifications
        # Unit name, Min LOA (mm), Max LOA (mm), Max SA (m2), Max wire Dia (mm), Max Rod Dia (mm), clevis pin size range
        ("R250", 6000, 9000, 30, 6.35, 4.37, (8, 10, 12, 14, 16)),
        ("R350", 8500, 12500, 45, 8, 6.35, (8, 10, 12, 14, 16)),
        ("R420", 11500, 14500, 70, 10, 7.14, (10, 12, 14, 16, 19, 22, 25)),
        ("R430", 12000, 15500, 90, 11.1, 7.92, (10, 12, 14, 16, 19, 22, 25)),
        ("R480", 13500, 19000, 100, 12.7, 9.53, (16, 18, 19, 22, 25, 28)),
        ("C260", 5000, 7000, 15, 5, None, (None)),
        ("C290", 7000, 9500, 30, 6, 4.37, (8, 10, 12, 14, 16)),  # Fixed: removed extra value
        ("C320", 9250, 11000, 40, 7, 5.03, (8, 10, 12, 14, 16)),
        ("C350", 10500, 12500, 55, 8, 6.35, (10, 12, 14, 16, 19, 22, 25)),
        ("C420", 12000, 15000, 80, 10, 7.14, (10, 12, 14, 16, 19, 22, 25)),
        ("C430", 13000, 17000, 100, 12.7, 9.53, (10, 12, 14, 16, 19, 22, 25)),
        ("C480", 13500, 17500, 120, 14.3, 10.72, (16, 18, 19, 22, 25, 28)),
        ("C520", 16500, 18000, 140, 16, 12.70, (16, 18, 19, 22, 25, 28)),
        ("C530", 18500, 27000, 220, 19, 14.27, (16, 18, 19, 22, 25, 28))
    ]

    REQUIRES_SWAGELES_EYE ={
        # Profurl models that require a swage-less eye
        # Unit name, stay diameter
        ("R480", 14),
        ("C290", 7),
        ("C320", 8),
        ("C350", 10),
        ("C350", 12.7),
        ("C520", 19)
    }

    def spec_profurl(self, loa, sail_area, stay_diameter, clevis_pin_diameter, rod=False):
        possible_furlers = []
        for unit_name, min_loa, max_loa, max_sa, max_wire_dia, max_rod_dia, clevis_pin_range in self.Furler_Specs:
            if min_loa <= loa <= max_loa and max_sa >= sail_area and stay_diameter <= max_wire_dia:
                if rod and max_rod_dia is not None and stay_diameter > max_rod_dia:
                    continue
                if clevis_pin_diameter not in clevis_pin_range:
                    continue
                requires_swageless_eye = (unit_name, stay_diameter) in self.REQUIRES_SWAGELES_EYE
                model = ProfurlFurler(
                    unit_name, stay_diameter, clevis_pin_diameter, requires_swage_swageless_eye=requires_swageless_eye
                )
                possible_furlers.append(model)
        return possible_furlers
            

if __name__ == "__main__":
    selector = ProfurlSelector()
    # Example parameters: adjust as needed
    loa = 19000
    sail_area = 40
    stay_diameter = 8
    rod = False
    clevis_pin = 16

    # Get matching furlers
    matching_furlers = selector.spec_profurl(
        loa=loa,
        sail_area=sail_area,
        stay_diameter=stay_diameter,
        rod=rod,
        clevis_pin_diameter=clevis_pin
    )
    if matching_furlers:
        print(f"Matching Profurl furlers for LOA {loa} mm, sail area {sail_area} m², stay diameter {stay_diameter} mm, rod={rod}, clevis pin diameter {clevis_pin}:")
        for furler in matching_furlers:
            print(furler)
    else:
        print("No matching Profurl furlers found.")
