from src.database import (
    find_profurl_part,
    get_profurl_link_plate,
    get_profurl_turnbuckle_cylinder,
    get_profurl_reefing_kit,
    get_profurl_prefeeder
)


class ProfurlFurler:
    """
    Class to handle the profurl functionality.
    """
    def __init__(self, unit_name, stay_diameter, clevis_pin_diameter, requires_swage_swageless_eye=False, stay_length=None):
        self.unit_name = unit_name
        self.stay_diameter = stay_diameter
        self.clevis_pin_diameter = clevis_pin_diameter
        self.requires_swage_swageless_eye = requires_swage_swageless_eye
        self.stay_length = stay_length
        self.base_part_number = self.get_part_number()
        self.optional_link_plate = self.get_link_plate()
        self.optional_turnbuckle_cylinder = self.get_turnbuckle_cylinder()
        self.optional_reefing_kit = self.get_reefing_kit()
        self.optional_prefeeder = self.get_prefeeder()

    def __repr__(self):
        return (
            f"<ProfurlFurlerModel name={self.unit_name}, "
            f"Stay Diameter={self.stay_diameter}, "
            f"Clevis Pin Diameter={self.clevis_pin_diameter}, "
            f"Requires Swageless Eye={self.requires_swage_swageless_eye}, "
            f"Base Part Number={self.base_part_number}, "
            f"Link Plate={self.optional_link_plate}, "
            f"Turnbuckle Cylinder={self.optional_turnbuckle_cylinder}, "
            f"Reefing Kit={self.optional_reefing_kit}, "
            f"Prefeeder={self.optional_prefeeder}>"
        )

    def get_part_number(self):
        if self.unit_name and self.stay_length:
            part_info = find_profurl_part(self.unit_name, self.stay_length)
            if part_info:
                self.stay_length = part_info['stay_length']
                return part_info['part_number']
        return None

    def get_link_plate(self):
        return get_profurl_link_plate(self.unit_name)

    def get_turnbuckle_cylinder(self):
        return get_profurl_turnbuckle_cylinder(self.unit_name)

    def get_reefing_kit(self):
        return get_profurl_reefing_kit(self.unit_name)

    def get_prefeeder(self):
        return get_profurl_prefeeder(self.unit_name)
