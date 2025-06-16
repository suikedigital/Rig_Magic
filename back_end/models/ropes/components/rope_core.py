# Dummy RopeCore for import resolution
class RopeCore:
    def __init__(self, material, diameter):
        self.material = material
        self.diameter = diameter
    def break_strength(self):
        return 1000
