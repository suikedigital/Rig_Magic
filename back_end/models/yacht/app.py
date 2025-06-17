"""
Yacht API Orchestrator (entrypoint)
---------------------
This file is the entrypoint for the yacht orchestrator microservice.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
import requests
from fastapi.middleware.cors import CORSMiddleware
import re

# Microservice endpoints (use Docker Compose service names)
SAILDATA_API = "http://saildata:8001"
SAILS_API = "http://sails:8020"
ROPES_API = "http://ropes:8010"
HULL_API = "http://hull_structure:8004"
PROFILE_API = "http://profile:8003"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Models ---
class KeelCreateRequest(BaseModel):
    keel_type: str
    draft: float
    base_id: Optional[int] = None


class RopeTypeRequest(BaseModel):
    yacht_id: int
    rope_type: str
    led_aft: float = 0.0
    config: dict = None


class SailTypeRequest(BaseModel):
    yacht_id: int
    sail_type: str
    config: dict = None


class YachtCreateRequest(BaseModel):
    yacht_id: Optional[int] = None
    base_yacht: Optional[Dict[str, Any]] = None
    profile: Optional[Dict[str, Any]] = None
    hull: Optional[Dict[str, Any]] = None
    keel: Optional[Dict[str, Any]] = None
    rudder: Optional[Dict[str, Any]] = None
    saildata: Optional[Dict[str, Any]] = None
    rig: Optional[Dict[str, Any]] = None
    possible_sails: Optional[List[Union[str, Dict[str, Any]]]] = None
    possible_ropes: Optional[List[Union[str, Dict[str, Any]]]] = None
    sails: Optional[List[Dict[str, Any]]] = None
    ropes: Optional[List[Dict[str, Any]]] = None
    # Add more as needed


# --- Microservice Registry ---
MICROSERVICES = {
    "profile": f"{PROFILE_API}/profile/{{yacht_id}}",
    "hull": f"{HULL_API}/hull/{{yacht_id}}",
    "keel": f"{HULL_API}/hull/keel/{{yacht_id}}",
    "rudder": f"{HULL_API}/hull/rudder/{{yacht_id}}",  # <-- Add rudder microservice
    "sails": f"{SAILS_API}/sails/{{yacht_id}}",
    "saildata": f"{SAILDATA_API}/saildata/{{yacht_id}}",
    "ropes": f"{ROPES_API}/ropes/{{yacht_id}}",
}


@app.get("/yachts/search")
def search_yachts(query: str = Query("")):
    # Call profile microservice to get all profiles
    try:
        resp = requests.get(f"{PROFILE_API}/profile/all")
        resp.raise_for_status()
        profiles = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Profile service unavailable: {e}")

    # Search relevant fields
    query_lower = query.lower()

    def matches(profile):
        for field in ["yacht_class", "model", "builder", "designer", "version"]:
            value = profile.get(field, "")
            if value and query_lower in str(value).lower():
                return True
        return False

    results = [p for p in profiles if matches(p)]
    return {"results": results}
