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