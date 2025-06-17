# Add 2 blank lines before each top-level function/class as per E302


class MonoHull:
    def __init__(self, length, beam, draft):
        self.length = length
        self.beam = beam
        self.draft = draft

    def volume_displaced(self):
        # Calculate the volume of water displaced by the hull
        return self.length * self.beam * self.draft


def some_top_level_function():
    pass


class Monohull:
    def __init__(self, hull_material):
        self.hull_material = hull_material

    def __str__(self):
        return f"Monohull with {self.hull_material} hull material."
