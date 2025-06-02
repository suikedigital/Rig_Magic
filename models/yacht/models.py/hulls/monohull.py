# hulls/monohull.py
from hulls.base import BaseHull, HullType

class Monohull(BaseHull):
    def hull_type(self) -> HullType:
        return HullType.MONOHULL
