# Dummy RopeCover for import resolution
class RopeCover:
    def __init__(self, material, diameter):
        self.material = material
        self.diameter = diameter
    def contribution(self, base):
        return 0.5 * base
