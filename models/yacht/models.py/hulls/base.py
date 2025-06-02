# hulls/base.py
from abc import ABC, abstractmethod
from enum import Enum


class HullType(Enum):
    MONOHULL = "monohull"
    CATAMARAN = "catamaran"
    TRIMARAN = "trimaran"
    PROA = "proa"
    OTHER = "other"


class BaseHull(ABC):
    """
    Abstract base class for yacht hulls.
    """

    def __init__(self, length: float, beam: float, draft: float):
        self.length = length  # LOA (Length Overall)
        self.beam = beam      # Beam (width)
        self.draft = draft    # Draft (vertical depth)

    @abstractmethod
    def hull_type(self) -> HullType:
        pass

    def dimensions(self) -> dict:
        return {
            "length": self.length,
            "beam": self.beam,
            "draft": self.draft
        }

    def displacement_factor(self) -> float:
        """
        Returns a generic factor for load calculations.
        You can override this for more accurate modeling.
        """
        return self.length * self.beam * self.draft
