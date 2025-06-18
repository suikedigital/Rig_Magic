class FacnorFurler:
    def __init__(self, unit_name, hal_swivel, foil_section, min_loa, max_loa, min_dia, max_dia, requires_eye_turnbuckle):
        self.unit_name = unit_name
        self.hal_swivel = hal_swivel
        self.foil_section = foil_section
        self.min_loa = min_loa
        self.max_loa = max_loa
        self.min_dia = min_dia
        self.max_dia = max_dia
        self.requires_eye_turnbuckle = requires_eye_turnbuckle

    def __repr__(self):
        return (
            f"<FacnorFurlerModel name={self.unit_name}, Halyard swivel= {self.hal_swivel}"
            f"Foil section={self.foil_section}, RequiresEyeTurnbuckle={self.requires_eye_turnbuckle}>"
        )

class FacnorFurlerSelector:
    FURLER_SPECS = [
        # Facnor furler specifications
        # Unit name, Halyard Swivel, foil section, Min LOA (m), Max LOA (m), Min Wire Dia (mm), Max Wire Dia (mm)
        ("Facnor LS-60", "C25", "SX25", 5500, 7000, 0, 5),
        ("Facnor LS-70", "C25", "SX25",6500, 8000, 0, 5),
        ("Facnor LS-100", "C33", "SX33", 7500, 9000, 0, 6),
        ("Facnor LS-130", "C33", "SX33", 8000, 11000, 0, 7),
        ("Facnor LS-165", "C39", "SX39", 9000, 12000, 0, 10),
        ("Facnor LS-180", "C39", "SX39", 10000, 13000, 0, 10),
        ("Facnor LS-200", "C47", "SX47", 11500, 14000, 0, 12),
        ("Facnor LS-290", "C47", "SX47", 13000, 18000, 0, 14),
        ("Facnor LS-330", "C600", "SX53", 15000, 28000, 0, 22),
        ("Facnor RX-70", "C14", "R14", 6500, 8000, 0, 5),
        ("Facnor RX-100", "C14", "R14", 7500, 8500, 5, 6),
        ("Facnor RX-130", "C14", "R14", 8000, 9500, 6, 7),
        ("Facnor RX-165", "C24", "R24", 9000, 11500, 0, 8),
        ("Facnor RX-220", "C26", "R26", 10000, 12500, 8, 10),
        ("Facnor RX-260", "C26", "R26", 11500, 15000, 0, 10),
        ("Facnor RX-300", "C34", "R34", 13000, 18000, 0, 12.7)
    ]

    REQUIRES_EYE_TURNBUCKLE = {
        # Facnor models that require an eye turnbuckle
        # name, dia
        ("Facnor LS-130", 7),
        ("Facnor LS-165", 10),
        ("Facnor LS-180", 10),
        ("Facnor LS-200", 12),
        ("Facnor LS-290", 14),
        ("Facnor LS-330", 22),
    }

    def spec_facnors(self, loa, forstay_wire_diameter):
        possible_furlers = []
        for unit_name, hal_swivel, foil_section, min_loa, max_loa, min_dia, max_dia in selector.FURLER_SPECS:
            if min_loa <= loa <= max_loa and min_dia <= forstay_wire_diameter <= max_dia:
                requires_eye_turnbuckle = (unit_name, forstay_wire_diameter) in selector.REQUIRES_EYE_TURNBUCKLE
                model = FacnorFurler(
                    unit_name, hal_swivel, foil_section, min_loa, max_loa, min_dia, max_dia, requires_eye_turnbuckle
                )
                possible_furlers.append(model)
        return possible_furlers 


if __name__ == "__main__":
    selector = FacnorFurlerSelector()
    loa = 11000  # Example LOA in mm
    forstay_wire_diameter = 7  # Example diameter in mm
    matching_furlers = selector.spec_facnors(loa, forstay_wire_diameter)
    
    if matching_furlers:
        print(f"Possible Facnor furlers for LOA={loa} and forstay diameter={forstay_wire_diameter}:")
        for furler in matching_furlers:
            print(furler)
            if furler.requires_eye_turnbuckle:
                print("  -> Requires removable eye and turnbuckle.")
    else:
        print("No suitable Facnor model found.")