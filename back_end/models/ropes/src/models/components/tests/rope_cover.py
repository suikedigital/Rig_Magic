class RopeCover:
    def __init__(self, material, diameter):
        self.material = material
        self.diameter = diameter
    def contribution(self, base):
        if self.material == "braid":
            return 1000
        if self.material == "dyneema":
            return 1500
        return 0.5 * base
