from harken import HarkenFurlerSelector
from furlex import FurlexSelector
from profurl import ProfurlSelector
from facnor import FacnorSelector

class FurlerService:
    def __init__(self):
        self.harken_selector = HarkenFurlerSelector()
        self.furlex_selector = FurlexSelector()
        self.profurl_selector = ProfurlSelector()
        self.facnor_selector = FacnorSelector()

    def spec_furlers(self, loa, stay_diameter, sail_area=None, clevis_pin_diameter=None, rod=False, fractional_rig=False, rm=None, displacement=None):
        """
        Get a list of possible furlers based on the specifications provided.
        
        :param loa: Length Over All in mm
        :param stay_diameter: Diameter of the forstay wire in mm
        :param sail_area: Sail area in m² (optional, used for Profurl)
        :param clevis_pin_diameter: Clevis pin diameter in mm (optional, used for Harken and Profurl)
        :param rod: Boolean indicating if rod is used (optional)
        :param fractional_rig: Boolean indicating if fractional rig is used (optional)
        :param rm: Righting moment (KnM) (optional, used for Furlex)
        :param displacement: Displacement (tons) (optional, used for Furlex)
        :return: List of possible furler models
        """
        furlers = []
        furlers.extend(self.harken_selector.spec_furlers(loa, stay_diameter, clevis_pin_diameter, rod))
        # Only call Furlex if rm and displacement are provided
        furlers.extend(self.furlex_selector.spec_furlers(stay_diameter, rm, displacement, rod, fractional_rig))
        furlers.extend(self.profurl_selector.spec_furlers(loa, sail_area, stay_diameter, clevis_pin_diameter, rod))
        furlers.extend(self.facnor_selector.spec_furlers(loa, stay_diameter))
        return furlers
    
    def test_furler_service_variants(self):
        service = FurlerService()
        # List of parameter sets to test
        test_cases = [
            # (loa, stay_diameter, sail_area, clevis_pin_diameter, rod, fractional_rig, rm, displacement)
            (11000, 8, 40, 12.7, False, True, 39, 7),
            (9000, 6, 28, 9.5, False, False, 22, 4),
            (13000, 10, 55, 14, True, False, 70, 14),
            (15000, 12, 70, 16, False, True, 120, 20),
            (7000, 5, 20, 8, False, False, 10, 2),
            (12000, 7, 35, 10, False, True, 34, 6),
            (10000, 8, 45, 12, True, False, 45, 8),
            (14000, 10, 60, 14, False, False, 80, 15),
            (8000, 6, 25, 9.5, False, True, 19, 3.5),
            (16000, 14, 80, 18, True, False, 180, 28),
        ]
        for i, (loa, stay_diameter, sail_area, clevis_pin_diameter, rod, fractional_rig, rm, displacement) in enumerate(test_cases, 1):
            print(f"\nTest case {i}: LOA={loa}, Stay Diameter={stay_diameter}, Sail Area={sail_area}, Clevis Pin={clevis_pin_diameter}, Rod={rod}, Fractional Rig={fractional_rig}, RM={rm}, Displacement={displacement}")
            matching_furlers = service.spec_furlers(loa, stay_diameter, sail_area, clevis_pin_diameter, rod, fractional_rig, rm, displacement)
            if matching_furlers:
                for furler in matching_furlers:
                    print(furler)
            else:
                print("No matching furlers found.")

if __name__ == "__main__":
    service = FurlerService()
    # Example parameters
    service.test_furler_service_variants()

