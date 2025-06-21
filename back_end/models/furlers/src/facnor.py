class FacnorFurler:
    def __init__(self, unit_name, stay_diam, stay_length, requires_eye_turnbuckle):
        self.unit_name = unit_name
        self.stay_diam = stay_diam
        self.stay_length = stay_length
        self.requires_eye_turnbuckle = requires_eye_turnbuckle

    def __repr__(self):
        return (
            f"<FacnorFurlerModel name={self.unit_name}, RequiresEyeTurnbuckle={self.requires_eye_turnbuckle}>"
        )
