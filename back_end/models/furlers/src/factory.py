from src.facnor import FacnorFurler
from src.furlex import Furlex
from src.harken import HarkenFurler
from src.profurl import ProfurlFurler


from src.database import (
    get_facnor_selection_criteria,
    get_facnor_requires_eye_turnbuckle,
    get_furlex_selection_criteria,
    get_harken_selection_criteria,
    get_profurl_selection_criteria,
    requires_profurl_swageless_eye
)


class Factory:
    """
    Factory class to create instances of various classes.
    """
    @staticmethod
    def spec_facnor(loa, stay_diameter, stay_length):
        possible_furlers = []
        for row in get_facnor_selection_criteria():
            unit_name = row['unit_name']
            min_loa = row['min_loa']
            max_loa = row['max_loa']
            min_dia = row['min_dia']
            max_dia = row['max_dia']
            if min_loa <= loa <= max_loa and min_dia <= stay_diameter <= max_dia:
                requires_eye_turnbuckle = (unit_name, stay_diameter) in get_facnor_requires_eye_turnbuckle()
                model = FacnorFurler(
                    unit_name, stay_diameter, stay_length, requires_eye_turnbuckle
                )
                possible_furlers.append(model)
        return possible_furlers 
    
    @staticmethod
    def spec_furlex(stay_diameter, rm, displacement, stay_length, rod=False, fractional_rig=False):
        possible_furlers = []
        for unit_name, wire_diam, rod_diam, max_rm, max_disp in get_furlex_selection_criteria():
            if rod:
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
                if rm > max_rm[1] or displacement > max_disp[1]:
                    continue
            else:
                if rm > max_rm[0] or displacement > max_disp[0]:
                    continue
            model = Furlex(unit_name=unit_name, stay_diameter=stay_diameter, stay_length=stay_length, rod_diameter=rod_diam if rod else None)
            possible_furlers.append(model)
        return possible_furlers
    
    @staticmethod
    def spec_harken(loa, stay_diameter, clevis_pin_diam, rod, stay_length):
        possible_furlers = []
        for row in get_harken_selection_criteria():
            unit_name = row['unit_name']
            min_loa = row['min_loa']
            max_loa = row['max_loa']
            wire_diams = row['stay_diameters']
            rod_diams = row['rod_diameters']
            pin_sizes = row['clevis_pin_diameters']
            if min_loa <= loa <= max_loa and stay_diameter in wire_diams:
                if rod and rod_diams is not None and stay_diameter not in rod_diams:
                    continue
                if pin_sizes and clevis_pin_diam not in pin_sizes:
                    continue
                furler = HarkenFurler(unit_name, stay_diameter, clevis_pin_diam, rod, stay_length)
                possible_furlers.append(furler)
            else:
                continue
        return possible_furlers if possible_furlers else []
    
    @staticmethod
    def spec_profurl(loa, sail_area, stay_diameter, clevis_pin_diameter, rod=False, stay_length=None):
        possible_furlers = []
        for row in get_profurl_selection_criteria():
            unit_name = row['unit_name']
            min_loa = row['min_loa']
            max_loa = row['max_loa']
            max_sa = row['max_sa']
            max_wire_dia = row['max_wire_diameter']
            max_rod_dia = row['max_rod_diameter']
            clevis_pin_range = row['clevis_pin_size_range']
            if min_loa <= loa <= max_loa and max_sa >= sail_area and stay_diameter <= max_wire_dia:
                if rod and max_rod_dia is not None and stay_diameter > max_rod_dia:
                    continue
                if clevis_pin_diameter not in clevis_pin_range:
                    continue
                requires_swageless_eye = requires_profurl_swageless_eye(unit_name, stay_diameter)
                model = ProfurlFurler(
                    unit_name, stay_diameter, clevis_pin_diameter, requires_swage_swageless_eye=requires_swageless_eye, stay_length=stay_length
                )
                possible_furlers.append(model)
        return possible_furlers
    
    @staticmethod
    def spec_furlers(loa, sail_area, stay_diameter, clevis_pin_diameter, rod=False, stay_length=None, rm=None, displacement=None, fractional_rig=False):
        """
        Unified entry point to spec all furler brands. Returns a dict of brand: [furlers].
        """
        return {
            'facnor': Factory.spec_facnor(loa, stay_diameter, stay_length),
            'furlex': Factory.spec_furlex(stay_diameter, rm, displacement, stay_length, rod=rod, fractional_rig=fractional_rig),
            'harken': Factory.spec_harken(loa, stay_diameter, clevis_pin_diameter, rod, stay_length),
            'profurl': Factory.spec_profurl(loa, sail_area, stay_diameter, clevis_pin_diameter, rod=rod, stay_length=stay_length)
        }


if __name__ == "__main__":
    test_cases = [
        {
            'label': 'Case 1: LOA=12000, Stay=8, Pin=12, Rod=False, StayLen=13000',
            'params': dict(loa=12000, sail_area=50, stay_diameter=8, clevis_pin_diameter=12, rod=False, stay_length=13000, rm=20, displacement=8, fractional_rig=False)
        },
        {
            'label': 'Case 2: LOA=12000, Stay=8, Pin=15.9, Rod=False, StayLen=14000',
            'params': dict(loa=12000, sail_area=50, stay_diameter=8, clevis_pin_diameter=15.9, rod=False, stay_length=14000, rm=20, displacement=8, fractional_rig=False)
        },
        {
            'label': 'Case 3: LOA=12000, Stay=8, Pin=19.1, Rod=False, StayLen=15000',
            'params': dict(loa=12000, sail_area=50, stay_diameter=8, clevis_pin_diameter=19.1, rod=False, stay_length=15000, rm=20, displacement=8, fractional_rig=False)
        },
        {
            'label': 'Case 4: LOA=10000, Stay=7, Pin=12.7, Rod=False, StayLen=10500',
            'params': dict(loa=10000, sail_area=40, stay_diameter=7, clevis_pin_diameter=12.7, rod=False, stay_length=10500, rm=18, displacement=7, fractional_rig=False)
        },
        {
            'label': 'Case 5: LOA=14000, Stay=12, Pin=19.1, Rod=False, StayLen=16000',
            'params': dict(loa=14000, sail_area=70, stay_diameter=12, clevis_pin_diameter=19.1, rod=False, stay_length=16000, rm=25, displacement=12, fractional_rig=False)
        },
        {
            'label': 'Case 6: LOA=12000, Stay=8, Pin=15.9, Rod=True, StayLen=13500',
            'params': dict(loa=12000, sail_area=50, stay_diameter=8, clevis_pin_diameter=15.9, rod=True, stay_length=13500, rm=20, displacement=8, fractional_rig=False)
        },
        {
            'label': 'Case 7: LOA=6000, Stay=5, Pin=9.5, Rod=False, StayLen=6500',
            'params': dict(loa=6000, sail_area=20, stay_diameter=5, clevis_pin_diameter=9.5, rod=False, stay_length=6500, rm=10, displacement=3, fractional_rig=False)
        },
        {
            'label': 'Case 8: LOA=18000, Stay=14, Pin=22.2, Rod=False, StayLen=20000',
            'params': dict(loa=18000, sail_area=120, stay_diameter=14, clevis_pin_diameter=22.2, rod=False, stay_length=20000, rm=40, displacement=18, fractional_rig=False)
        },
    ]

    for case in test_cases:
        print(f"\n=== {case['label']} ===")
        results = Factory.spec_furlers(**case['params'])
        for brand, furlers in results.items():
            print(f"\n--- {brand.upper()} ---")
            for furler in furlers:
                print(furler)

