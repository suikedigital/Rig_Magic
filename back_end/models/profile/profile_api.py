from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from back_end.models.profile.service import YachtProfileService

app = FastAPI()
profile_service = YachtProfileService()

class ProfileRequest(BaseModel):
    yacht_id: int
    base_id: Optional[int] = None
    yacht_class: Optional[str] = None
    model: Optional[str] = None
    version: Optional[str] = None
    builder: Optional[str] = None
    designer: Optional[str] = None
    year_introduced: Optional[int] = None
    production_start: Optional[int] = None
    production_end: Optional[int] = None
    country_of_origin: Optional[str] = None
    notes: Optional[str] = None

@app.post("/profile/")
def add_profile(req: ProfileRequest):
    profile_service.save_profile(req.dict())
    return {"status": "ok"}

@app.get("/profile/{yacht_id}")
def get_profile(yacht_id: int):
    profile = profile_service.get_profile(yacht_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile.__dict__

@app.delete("/profile/{yacht_id}")
def delete_profile(yacht_id: int):
    profile_service.delete_profile(yacht_id)
    return {"status": "deleted"}

@app.get("/profile/")
def list_profiles():
    return profile_service.db.list_all()
