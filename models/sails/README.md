# Sails Module

This module provides a standalone, extensible system for modeling yacht sails, including a factory for creating and managing different sail types.

## Features
- Abstract base class for sails (`BaseSail`)
- Concrete sail types: Mainsail, Jib, Genoa, Staysail, CodeZero, SymSpinnaker, AsymSpinnaker, Trisail
- Factory pattern for easy sail instantiation and management
- Type-safe sail selection using `SailType` enum
- Area and aerodynamic force calculations for each sail
- Fully tested with `unittest`

## Installation
Clone or copy this module into your project. No external dependencies are required.

## Usage

### 1. Prepare Sail Data
You need a `saildata` object with the required attributes for each sail (see `DummySailData` in `tests/test_sail_factory.py` for an example).

### 2. Create a SailFactory
```python
from models.sail_factory import SailFactory, SailType
factory = SailFactory(saildata)
```

### 3. Add Sails to the Factory
```python
factory.add_sail_type_to_possible_on_boat(SailType.MAINSAIL)
factory.add_sail_type_to_possible_on_boat(SailType.JIB, {'luff': 8.0, 'foot': 2.5})
```

### 4. Generate Sails
```python
factory.generate_all_sails_on_boat()
```

### 5. Retrieve and Use Sails
```python
mainsail = factory.get(SailType.MAINSAIL)
print(mainsail.area)
force = mainsail.aerodynamic_force(wind_speed_knots=12)
```

### 6. List Available Sail Types
```python
print(SailFactory.available_types())
```

## Testing
Run the test suite with:
```sh
python -m unittest tests/test_sail_factory.py
```

## Extending
To add a new sail type:
1. Create a new class in `models/sails/` inheriting from `BaseSail`.
2. Implement the `area` property and any custom logic.
3. Add the new class to the `_registry` in `SailFactory` and to the `SailType` enum.

---
For more details, see the docstrings in each module and the test file for usage examples.
