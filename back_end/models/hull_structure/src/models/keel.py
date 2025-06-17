class Keel:
    def __init__(self, yacht_id, keel_type: str, draft: float):
        self.yacht_id = yacht_id
        self.keel_type = keel_type  # Type of keel (e.g., fin, full, bulb)
        self.draft = draft  # Draft of the keel in meters

    def get_keel_info(self):
        return {
            "keel_type": self.keel_type,
            "draft": self.draft,
        }
