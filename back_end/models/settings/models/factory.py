from .settings import Settings

class SettingsFactory:
    @staticmethod
    def from_dict(data: dict):
        return Settings(
            yacht_id=data["yacht_id"],
            wind_speed_in_knots=data["wind_speed_in_knots"],
            length_safety_factor=data["length_safety_factor"],
            halyard_load_safety_factor=data["halyard_load_safety_factor"],
            dynamic_load_safety_factor=data["dynamic_load_safety_factor"]
        )

    @staticmethod
    def from_row(row):
        # row: (yacht_id, wind_speed_in_knots, length_safety_factor, halyard_load_safety_factor, dynamic_load_safety_factor)
        return Settings(
            yacht_id=row[0],
            wind_speed_in_knots=row[1],
            length_safety_factor=row[2],
            halyard_load_safety_factor=row[3],
            dynamic_load_safety_factor=row[4]
        )
