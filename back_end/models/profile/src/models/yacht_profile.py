# yachts/profile.py


class YachtProfile:
    def __init__(
        self,
        yacht_id: int,
        base_id: int = None,
        name: str = None,  # NEW: user-given name
        yacht_class: str = None,
        model: str = None,
        spec: str = None,  # NEW: performance spec
        version: str = None,
        builder: str = None,
        designer: str = None,
        year_introduced: int = None,
        production_start: int = None,
        production_end: int = None,
        country_of_origin: str = None,
        notes: str = None,
        id: int = None,  # Accept id for DB compatibility
    ):
        self.id = id
        self.yacht_id = yacht_id
        self.base_id = base_id
        self.name = name
        self.yacht_class = yacht_class  # e.g., "Swan 48"
        self.model = model  # e.g., "Oceanis"
        self.spec = spec  # e.g., "IRC 1.050"
        self.version = version  # e.g., "MKII"
        self.designer = designer  # e.g., "Sparkman & Stephens"
        self.builder = builder  # e.g., "Nautor's Swan"
        self.year_introduced = year_introduced  # e.g., 1985
        self.production_start = production_start  # e.g., 1985
        self.production_end = production_end  # e.g., 1990
        self.country_of_origin = country_of_origin
        self.notes = notes or ""
