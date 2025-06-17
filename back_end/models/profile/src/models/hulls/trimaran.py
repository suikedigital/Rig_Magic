# Add 2 blank lines before each top-level function/class as per E302


class Trimaran:
    pass

    def __init__(self, hull_length, beam_width, draft_depth, hull_material, ama_length):
        self.hull_length = hull_length
        self.beam_width = beam_width
        self.draft_depth = draft_depth
        self.hull_material = hull_material
        self.ama_length = ama_length

    def calculate_sail_area(self):
        # Formula for sail area calculation
        return 0.5 * self.hull_length * self.beam_width

    def display_specs(self):
        print("Trimaran Specifications:")
        print(f"Hull Length: {self.hull_length} meters")
        print(f"Beam Width: {self.beam_width} meters")
        print(f"Draft Depth: {self.draft_depth} meters")

    def __str__(self):
        return f"Trimaran with {self.hull_material} hull material."

    def __post_init__(self):
        print(f"Trimaran hull created with beams: {self.beams}")

    def get_ama_length(self):
        return self.ama_length


# Add 2 blank lines before each top-level function/class as per E302


def main():
    trimaran = Trimaran(12, 8, 1.5, "Fiberglass", 14)
    trimaran.display_specs()
    sail_area = trimaran.calculate_sail_area()
    print(f"Sail Area: {sail_area} square meters")


if __name__ == "__main__":
    main()
