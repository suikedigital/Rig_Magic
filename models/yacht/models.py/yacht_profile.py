# yachts/profile.py

class YachtProfile:
    def __init__(
        self,
        yacht_class: str = None,
        model: str = None,
        designer: str = None,
        manufacturer: str = None,
        year_built: int = None,
        build_material: str = None,
        notes: str = None
    ):
        self.yacht_class = yacht_class        # e.g., "Swan 48"
        self.model = model                    # e.g., "MKII"
        self.designer = designer              # e.g., "Sparkman & Stephens"
        self.manufacturer = manufacturer      # e.g., "Nautor's Swan"
        self.year_built = year_built
        self.build_material = build_material  # e.g., "GRP", "Aluminum", "Wood"
        self.notes = notes or ""
