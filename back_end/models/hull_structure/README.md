# Hull Structure Microservice

This service manages hull, keel, and rudder data for yachts.

## Endpoints
- `POST /hull/keel` — Add a keel
- `GET /hull/keel/{yacht_id}` — Get a keel
- `POST /hull/rudder` — Add a rudder
- `GET /hull/rudder/{yacht_id}` — Get a rudder
- `POST /hull/hull` — Add a hull
- `GET /hull/{yacht_id}` — Get a hull
- `DELETE /hull/{yacht_id}` — Delete all hull data for a yacht
- `DELETE /hull/keel/{yacht_id}` — Delete a keel
- `DELETE /hull/rudder/{yacht_id}` — Delete a rudder

## Environment Variables
- `HULL_STRUCTURE_DB_PATH` — Path to the hull structure database (default: `hull_structure.db`)

## Running Locally
```
pip install -r requirements.txt
uvicorn app:app --reload
```

## Testing
```
pytest tests/
```
