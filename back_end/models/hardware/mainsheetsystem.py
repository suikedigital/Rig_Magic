class MainsheetSystem:
    def __init__(self, purchase_ratio: int, routing: str = "traditional"):
        self.purchase = purchase_ratio  # e.g., 6
        self.routing = routing.lower()  # "german", "traditional"
