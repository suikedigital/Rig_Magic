class Furlex:
    def __init__(self, unit_name, stay_diameter, rod_diameter=None):
        self.unit_name = unit_name
        self.stay_diameter = stay_diameter
        self.rod_diameter = rod_diameter

    def __repr__(self):
        return f"<Furlex {self.unit_name}, Stay Diameter: {self.stay_diameter}>"

class FurlexSelector:
    FURLER_SPECS = [
        ("Furlex 104S", 4, None, (6.5, 8), (1.4, 1.7)),
        ("Furlex 104S", 5, None, (10, 14.5), (2.1, 3)),
        ("Furlex 104S", 6, None, (17, 22), (3.5, 4)),
        ("Furlex 204S", 6, 5.7, (19, 23), (3.9, 4.5)),
        ("Furlex 204S", 7, 6.4, (27, 34), (5.5, 7)),
        ("Furlex 204S", 8, (7.1, 7.5), (37, 45), (7.5, 9)),
        ("Furlex 304S", 8, (7.1, 7.5), (40, 50), (8, 10)),
        ("Furlex 304S", 10, (8.4, 9.5), (70, 80), (14, 15)),
        ("Furlex 404S", 12, (11.1,), (120, 160), (20, 26)),
        ("Furlex 404S", 14, (11.1, 12.7), (180, 190), (28, 30)),
    ]

    def spec_furlers(self, stay_diameter, rm, displacement, rod=False, fractional_rig=False):
        possible_furlers = []
        for unit_name, wire_diam, rod_diam, max_rm, approx_disp in self.FURLER_SPECS:
            if rod:
                # rod_diam can be a tuple or a single value
                if rod_diam is None:
                    continue
                if isinstance(rod_diam, tuple):
                    if stay_diameter not in rod_diam:
                        continue
                else:
                    if stay_diameter != rod_diam:
                        continue
            else:
                if stay_diameter != wire_diam:
                    continue

            if fractional_rig:
                if rm > max_rm[1] or displacement > approx_disp[1]:
                    continue
            else:
                if rm > max_rm[0] or displacement > approx_disp[0]:
                    continue

            model = Furlex(unit_name=unit_name, stay_diameter=stay_diameter, rod_diameter=rod_diam if rod else None)
            possible_furlers.append(model)
        return possible_furlers
    

def get_matching_furlers():
    selector = FurlexSelector()
    # Example parameters that should return multiple matches
    stay_diameter = 8
    rm = 39
    displacement = 7
    rod = False
    fractional_rig = True
    return selector.spec_furlers(
        stay_diameter=stay_diameter,
        rm=rm,
        displacement=displacement,
        rod=rod,
        fractional_rig=fractional_rig
    )

if __name__ == "__main__":
    furlers = get_matching_furlers()
    if furlers:
        print("Matching Furlex furlers:")
        for f in furlers:
            print(f)
    else:
        print("No matching Furlex furlers found.")
