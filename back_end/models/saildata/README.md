# Saildata Microservice

This service manages saildata for yachts.

## Endpoints
- `POST /saildata/` — Add saildata
- `GET /saildata/{yacht_id}` — Get saildata
- `GET /saildata/debug/list_ids` — List all yacht IDs
- `DELETE /saildata/{yacht_id}` — Delete saildata for a yacht

## Environment Variables
- `SAILDATA_DB_PATH` — Path to the saildata database (default: `sail_data.db`)

## Running Locally
```
pip install -r requirements.txt
uvicorn app:app --reload
```

## Testing
```
pytest tests/
```
