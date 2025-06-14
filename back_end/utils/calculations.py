"""
Utility functions for rope and rigging calculations.
"""


import math


def sheet_load_kg(
    force_newtons: float,
    sheet_angle_deg: float,
    safety_factor: float = 1.5,
    dynamic_factor: float = 1.5
) -> float:
    """
    Calculate the sheet line load in kilograms.

    Parameters:
    - force_newtons: Total aerodynamic force on the sail (N)
    - sheet_angle_deg: Angle of sheet to the clew pull direction (degrees)
    - safety_factor: Engineering margin (default 1.5)
    - dynamic_factor: Motion/gust compensation factor (default 1.5)

    Returns:
    - Line load in kilograms (kg)

    Notes:
    Sheet load is the horizontal component of sail force, resolved along the sheet.
    """
    angle_rad = math.radians(sheet_angle_deg)
    load_n = force_newtons * math.cos(angle_rad) * safety_factor * dynamic_factor
    return load_n / 9.80665  # Convert N to kg


def example_usage():
    """
    Example calculation of halyard and sheet loads for a sail.

    Adjust the values to match your sail and conditions.
    """
    sail_area = 40.0            # m², projected area
    wind_speed = 20.0           # knots, apparent
    halyard_angle = 35          # degrees
    sheet_angle = 25            # degrees

    # Calculate aerodynamic force
    force_n = aerodynamic_force(sail_area, wind_speed)

    # Calculate loads
    halyard_kg = halyard_load_kg(force_n, halyard_angle)
    sheet_kg = sheet_load_kg(force_n, sheet_angle)

    print(f"Aerodynamic Force: {force_n:.2f} N")
    print(f"Halyard Load: {halyard_kg:.2f} kg")
    print(f"Sheet Load: {sheet_kg:.2f} kg")
