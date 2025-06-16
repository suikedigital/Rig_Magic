"""
Termination module
-----------------
This module defines the Termination class, representing the end termination of a rope in the running rigging system.

The Termination class encapsulates the type of termination (e.g., splice, whipping) and any associated hardware (e.g., shackle, thimble).

Classes:
    Termination: Represents a rope end termination with type and optional hardware.
"""

from typing import Optional


class Termination:
    """
    Represents a rope end termination.

    Attributes:
        term_type (str): The type of termination (e.g., 'Splice', 'Whipping').
        hardware (str, optional): Hardware attached to the termination (e.g., 'Shackle').

    Args:
        term_type (str): The type of termination.
        hardware (str, optional): Hardware attached to the termination.
    """
    def __init__(self, term_type: str, hardware: Optional[str] = None):
        """
        Represents a rope termination (end), e.g., eye splice, knot, with optional hardware.

        Args:
            term_type (str): Type of termination (e.g., 'flemish eye', 'knotted', 'whipping').
            hardware (str, optional): Hardware attached (e.g., 'snap shackle', 'bow shackle').
        """
        self.term_type = term_type
        self.hardware = hardware

    def __str__(self):
        hw = f", Hardware: {self.hardware}" if self.hardware else ""
        return f"Termination: {self.term_type}{hw}"