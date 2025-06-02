# models/ropes/models/ropes/halyards

This directory contains all halyard rope type classes for the running rigging management system.

## Rope Types
- `base_halyard.py`: Abstract base class for all halyards, providing shared logic for load, length, and diameter calculation.
- `main_halyard.py`: Main halyard implementation.
- `genoa_halyard.py`: Genoa halyard implementation.
- `jib_halyard.py`: Jib halyard implementation.
- `code_zero_halyard.py`: Code Zero halyard implementation.
- `trisail_halyard.py`: Trisail halyard implementation.
- `spinnaker_halyard.py`: Spinnaker halyard implementation.
- `staysail_halyard.py`: Staysail halyard implementation.
- `topping_lift_halyard.py`: Topping lift halyard implementation.

Each halyard class encapsulates the logic for its specific rope type, including default terminations, color, and calculation methods.
