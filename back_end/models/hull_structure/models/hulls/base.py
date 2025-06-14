# hulls/base.py
from abc import ABC, abstractmethod
from enum import Enum


class BaseHull(ABC):
    """
    Abstract base class for yacht hulls.
    """

    def __init__(self, yacht_id, loa: int, lwl: int, beam: int, displacement: int, ballast: int, construction: str):
        self.yacht_id = yacht_id  # Unique identifier for the yacht
        self.loa = loa  # LOA (Length Overall) mm
        self.lwl = lwl # LWL (Length Waterline) mm
        self.beam = beam      # Beam (width) mm
        self.displacement = displacement # Displacement (weight) kg
        self.ballast = ballast # Ballast weight (kg)
        self.construction = construction

    @abstractmethod
    def hull_type(self):
        pass

    def dimensions(self) -> dict:
        return {
            "loa": self.loa,
            "lwl": self.lwl,
            "beam": self.beam,
            "draft": self.draft,
            "displacement": self.displacement,
            "ballast": self.ballast,
            "construction": self.construction
        }

    def displacement_factor(self) -> float:
        """
        Returns a generic factor for load calculations.
        You can override this for more accurate modeling.
        """
        return self.length * self.beam * self.draft
