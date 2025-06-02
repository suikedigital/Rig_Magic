# hulls/trimaran.py
from hulls.base import BaseHull, HullType

class Trimaran(BaseHull):
    def hull_type(self) -> HullType:
        return HullType.TRIMARAN

    def displacement_factor(self) -> float:
        # Typically lighter than equivalent monohulls
        return 0.75 * super().displacement_factor()
