# ropes

This module manages all rope-related logic for the running rigging management system. It includes:
- Rope creation and configuration
- Rope type registries
- Rope service logic for generating and managing ropes
- Database integration for rope storage

## Structure
- `rope_service.py`: Main service for rope generation and management
- `models/`: Rope models, factories, and database logic
- `models/ropes/`: Rope type definitions (halyards, sheets, etc.)
- `models/components/`: Rope construction and termination types

## Usage
Import and use `RopeService` to generate and manage ropes for a yacht. All rope types and calculations are handled automatically.
