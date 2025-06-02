# hulls/catamaran.py
from hulls.base import BaseHull, HullType

class Catamaran(BaseHull):
    def __init__(self, length: float, beam: float, draft: float, bridgedeck_clearance: float = 0.5):
        super().__init__(length, beam, draft)
        self.bridgedeck_clearance = bridgedeck_clearance

    def hull_type(self) -> HullType:
        return HullType.CATAMARAN

    def displacement_factor(self) -> float:
        # Catamarans distribute weight over 2 hulls
        return 0.85 * super().displacement_factor()
