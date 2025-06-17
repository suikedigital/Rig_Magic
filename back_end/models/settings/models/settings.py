class Settings:
    def __init__(
        self,
        yacht_id: int,
        wind_speed_in_knots: int,
        length_safety_factor: float,
        halyard_load_safety_factor: float,
        dynamic_load_safety_factor: float,
    ):
        self.yacht_id = yacht_id
        self.wind_speed_in_knots = wind_speed_in_knots
        self.length_safety_factor = length_safety_factor
        self.halyard_load_safety_factor = halyard_load_safety_factor
        self.dynamic_load_safety_factor = dynamic_load_safety_factor

    def to_dict(self) -> dict:
        return {
            "yacht_id": self.yacht_id,
            "wind_speed_in_knots": self.wind_speed_in_knots,
            "length_safety_factor": self.length_safety_factor,
            "halyard_load_safety_factor": self.halyard_load_safety_factor,
            "dynamic_load_safety_factor": self.dynamic_load_safety_factor,
        }

    def get(self, key: str):
        return getattr(self, key, None)
