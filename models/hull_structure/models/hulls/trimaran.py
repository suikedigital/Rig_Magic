# hulls/trimaran.py
from models.hull_structure.models.hulls.base import BaseHull

class Trimaran(BaseHull):
    def __init__(self, yacht_id, loa: int, lwl: int, beam: int, displacement: int, ballast: int, construction: str):
        """
        Initialize a monohull yacht with its dimensions and characteristics.

        Args:
            loa (int): Length Overall in mm.
            lwl (int): Length Waterline in mm.
            beam (int): Beam (width) in mm.
            draft (int): Draft (vertical depth) in mm.
            displacement (int): Displacement (weight) in kg.
            ballast (int): Ballast weight in kg.
        """
        super().__init__(yacht_id, loa, lwl, beam, draft, displacement, ballast)

