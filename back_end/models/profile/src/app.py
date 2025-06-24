# Minimal FastAPI app for Docker build
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from .service import YachtProfileService
from fastapi import Request

app = FastAPI()
profile_service = YachtProfileService()


class ProfileRequest(BaseModel):
    yacht_id: int
    base_id: Optional[int] = None
    name: Optional[str] = None  # NEW: user-given name
    yacht_class: Optional[str] = None
    model: Optional[str] = None
    spec: Optional[str] = None  # NEW: performance spec
    version: Optional[str] = None
    builder: Optional[str] = None
    designer: Optional[str] = None
    year_introduced: Optional[int] = None
    production_start: Optional[int] = None
    production_end: Optional[int] = None
    country_of_origin: Optional[str] = None
    notes: Optional[str] = None


class ProfileResponse(BaseModel):
    id: Optional[int] = None
    yacht_id: Optional[int] = None
    base_id: Optional[int] = None
    name: Optional[str] = None  # NEW: user-given name
    yacht_class: Optional[str] = None
    model: Optional[str] = None
    spec: Optional[str] = None  # NEW: performance spec
    version: Optional[str] = None
    builder: Optional[str] = None
    designer: Optional[str] = None
    year_introduced: Optional[int] = None
    production_start: Optional[int] = None
    production_end: Optional[int] = None
    country_of_origin: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        extra = "allow"


@app.post("/profile/")
def add_profile(req: ProfileRequest):
    profile_service.save_profile(req.dict())
    # Fetch and return the full profile, including yacht_id
    profile = profile_service.get_profile(req.yacht_id)
    if not profile:
        raise HTTPException(status_code=500, detail="Profile creation failed")
    return profile.__dict__


@app.get("/profile/all")
def list_all_profiles(request: Request):
    profiles = profile_service.db.list_all()
    return profiles


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


@app.get("/profile/", response_model=list[ProfileResponse])
def list_profiles():
    profiles = profile_service.db.list_all()
    return [ProfileResponse(**p) for p in profiles]
