class RopeCore:
    def __init__(self, material, diameter):
        self.material = material
        self.diameter = diameter
    def break_strength(self):
        if self.material == "braid":
            return 1600
        if self.material == "dyneema":
            return 4000
        return 1000
