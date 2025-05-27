"""
Utility functions for rope and rigging calculations.
"""

import math 

def round_up_half_meter(value: float) -> float:
    """
    Round up a value to the nearest half meter.

    Args:
        value (float): The value to round up.

    Returns:
        float: The value rounded up to the nearest 0.5 meter.
    """
    return math.ceil(value * 2) / 2