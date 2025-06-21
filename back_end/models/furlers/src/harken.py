from src.database import (
    find_furlex_part, find_furlex_link_plate,
    get_harken_toggles, get_harken_rod_adapters, get_connection
)

class HarkenFurler:
    def __init__(self, unit_name, stay_diameter, clevis_pin_diam, rod, stay_length):
        self.unit_name = unit_name
        self.stay_diameter = stay_diameter
        self.clevis_pin_diam = clevis_pin_diam
        self.rod = rod
        self.stay_length = stay_length
        self.base_part_number = None
        self.toggles = []
        self.additional_foil = None
        self.additional_connector = None
        self.rod_adapters = []

        # Get base part number and foil/connector from DB
        # Find the base unit part with the smallest stay_length >= requested
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT base_unit_part_number, stay_length, additional_foil_part_number, additional_connector_part_number
                   FROM Harken_Base_Unit_Part_Numbers
                   WHERE unit_name = ? AND stay_length >= ?
                   ORDER BY stay_length ASC LIMIT 1''',
                (unit_name, stay_length)
            )
            row = cursor.fetchone()
            if row:
                self.base_part_number = row[0]
                self.stay_length = row[1]
                self.additional_foil = row[2]
                self.additional_connector = row[3]

        # Get toggles from DB
        self.toggles = get_harken_toggles(unit_name)
        # Filter toggles by clevis_pin_diam if provided
        if clevis_pin_diam is not None:
            self.toggles = [t for t in self.toggles if float(t['clevis_pin_diameter']) == float(clevis_pin_diam)]

        # Get rod adapters from DB only if rod is True
        if self.rod:
            # Only include rod adapters matching this unit and rod diameter
            all_adapters = get_harken_rod_adapters()
            self.rod_adapters = [a for a in all_adapters if float(a['rod_diameter']) == float(self.stay_diameter)]
        else:
            self.rod_adapters = []

    def __repr__(self):
        return (f"<HarkenFurler {self.unit_name}, Base: {self.base_part_number}, "
                f"Toggles: {self.toggles}, Additional Foil: {self.additional_foil}, "
                f"Additional Connector: {self.additional_connector}, Rod Adapters: {self.rod_adapters}>")

class HarkenFurlerSelector:

    def spec_and_extract_partnumbers(self, loa, stay_diameter, clevis_pin_diam, rod, stay_length):
        """
        Specs all matching Harken furlers and extracts all relevant part numbers for each.
        Returns a list of dicts, each containing the furler object and a set of part numbers used.
        """
        furlers = self.spec_harkens(loa, stay_diameter, clevis_pin_diam, rod, stay_length)
        results = []
        for furler in furlers:
            part_numbers = set()
            # Add base part number
            if furler.base_part_number:
                if isinstance(furler.base_part_number, tuple):
                    part_numbers.add(furler.base_part_number[0])
                else:
                    part_numbers.add(furler.base_part_number)
            # Add foil and connector if present
            if getattr(furler, 'additional_foil', None):
                part_numbers.add(furler.additional_foil)
            if getattr(furler, 'additional_connector', None):
                part_numbers.add(furler.additional_connector)
            # Add toggles part numbers
            for toggle in getattr(furler, 'toggles', []):
                part_numbers.add(toggle["part_number"])
            # Add rod adapters if present
            for rod_adapter in furler.part_numbers.get("Rod_adapter", []):
                if isinstance(rod_adapter, tuple) and len(rod_adapter) > 0:
                    part_numbers.add(rod_adapter[0])
            results.append({
                "furler": furler,
                "part_numbers": part_numbers
            })
        return results

if __name__ == "__main__":
    selector = HarkenFurlerSelector()
    # Example parameters
    loa = 11000
    stay_diameter = 8
    clevis_pin_diam = 15.9
    rod = False
    stay_length = 12000
    results = selector.spec_and_extract_partnumbers(loa, stay_diameter, clevis_pin_diam, rod, stay_length)
    for result in results:
        print(f"Furler: {result['furler']}")
        print(f"Part Numbers: {sorted(result['part_numbers'])}\n")