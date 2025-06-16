# Profile Microservice

This service manages yacht profiles.

## Endpoints
- `POST /profile/` — Add a profile
- `GET /profile/{yacht_id}` — Get a profile by yacht ID
- `DELETE /profile/{yacht_id}` — Delete a profile
- `GET /profile/` — List all profiles

## Environment Variables
- `PROFILE_DB_PATH` — Path to the profile database (default: `Profile.db`)

## Running Locally
```
pip install -r requirements.txt
uvicorn app:app --reload
```

## Testing
```
pytest tests/
```
