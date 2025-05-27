# Running Rigging Management System

A flexible, extensible Python system for managing the running rigging (halyards, sheets, guys, and control lines) of yachts. Designed for yacht owners, riggers, and sailmakers to model, configure, and document all running rigging elements with sensible defaults, configuration overrides, and robust documentation.

## Features

- **Modular Rope Architecture:**
  - Base classes for Rope, Halyard, Sheet, and Guy.
  - Extensible registry for dynamic rope creation.
  - Sensible defaults for construction, colour, and terminations.
- **Automatic Pairing:**
  - Sheets and guys are always created in port/starboard pairs.
  - Halyard-to-sheet/guy mapping for easy rigging setup.
- **Configuration & Overrides:**
  - Per-rope configuration (colour, construction, terminations, etc.)
  - Supports custom and default values.
- **Calculation Logic:**
  - Length and diameter calculations for each rope type.
  - Safety margins and yacht-specific parameters.
- **Documentation & Testing:**
  - Comprehensive docstrings for all modules and classes.
  - Pytest-based test suite for core rigging logic.

## Project Structure

```
app.py
models/
    ropes/
        halyards/
        sheets_and_guys/
            sheets/
            guys/
        rope_registry.py
        rope.py
        termination.py
    yacht/
        yacht.py
        running_rigging.py
        saildata.py
        mainsheetsystem.py
utils/
    calculations.py
data/
    rope_specs.json
    termiantions.json
factories/
    rope_factory.py
tests/
    test_running_rigging.py
requirements.txt
README.md
```

## Quick Start

1. **Install dependencies:**
   ```zsh
   pip install -r requirements.txt
   # or, if using pytest for tests:
   pip install pytest
   ```

2. **Run the example app:**
   ```zsh
   python app.py
   ```

3. **Run tests:**
   ```zsh
   pytest
   ```

## Usage Example

```python
from models.yacht.yacht import Yacht
from models.ropes.rope_registry import ROPE_REGISTRY

yacht = Yacht(i=20.0, j=5, p=11.0, e=3.5, boom_above_deck=1.0, boat_length=8.0)
yacht.running_rigging.add_rope_and_sheet("GenoaHalyard", led_aft=1.0)
yacht.running_rigging.set_rope_config("GenoaSheet_Port", {"colour": "Red"})
yacht.running_rigging.generate_ropes(ROPE_REGISTRY)
for name, rope in yacht.running_rigging.ropes.items():
    print(f"{name}: {rope}")
```

## Extending the System
- Add new rope types by subclassing `Rope`, `Sheet`, `Guy`, or `Halyard` and registering them in `rope_registry.py`.
- Update `HALYARD_TO_SHEET` mapping for new halyard/sheet/guy relationships.
- Override calculation logic as needed for custom rigging setups.

## License
MIT License

## Authors
- Suike (project owner)
- Contributors welcome!
