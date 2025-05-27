"""
Defines the Termination class for rope ends in the Running Rigging Management system.

A Termination represents how a rope is finished at one end, such as an eye splice, knot, or whipping,
optionally with attached hardware (e.g., shackle).
"""

from typing import Optional

class Termination:
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