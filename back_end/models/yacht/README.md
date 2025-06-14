# Yacht Orchestrator Microservice

This microservice provides a central API for orchestrating yacht creation, updates, and aggregation across all running rigging microservices (hull, saildata, sails, ropes, profile, etc).

## Endpoints

- `POST /yachts/create` — Create a new yacht and orchestrate all related microservices.
- `GET /yachts/{yacht_id}` — Aggregate and return all yacht-related data from all microservices.

## How it works
- Calls each microservice in order (hull, saildata, sails, ropes, profile).
- Aggregates data for a single yacht from all microservices.
- Handles errors and reports failures in orchestration.

## Usage
Run with FastAPI/Uvicorn:

```zsh
uvicorn back_end.models.yacht.yacht_api:app --reload --port 8050
```

Then use the endpoints to create and manage yachts centrally.