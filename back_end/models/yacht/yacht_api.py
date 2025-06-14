"""
Yacht API Orchestrator
---------------------
Central API for orchestrating yacht creation, updates, and aggregation across all microservices.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import requests
from fastapi.middleware.cors import CORSMiddleware

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
class YachtCreateRequest(BaseModel):
    yacht_id: int
    base_yacht: Optional[Dict[str, Any]] = None
    saildata: Optional[Dict[str, Any]] = None
    hull: Optional[Dict[str, Any]] = None
    profile: Optional[Dict[str, Any]] = None

class RopeTypeRequest(BaseModel):
    yacht_id: int
    rope_type: str
    led_aft: float = 0.0
    config: dict = None

class SailTypeRequest(BaseModel):
    yacht_id: int
    sail_type: str
    config: dict = None

class KeelCreateRequest(BaseModel):
    keel_type: str
    draft: float
    base_id: Optional[int] = None

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

# --- Aggregation Helper ---
def aggregate_yacht_data(yacht_id: int):
    result = {"yacht_id": yacht_id}
    errors = {}
    # Fetch profile first to check if base yacht
    profile_url = MICROSERVICES["profile"].format(yacht_id=yacht_id)
    try:
        profile_resp = requests.get(profile_url)
        if profile_resp.ok:
            result["profile"] = profile_resp.json()
            base_id = result["profile"].get("base_id", 0)
        else:
            result["profile"] = None
            base_id = 0
    except Exception as e:
        errors["profile"] = str(e)
        result["profile"] = None
        base_id = 0
    # Fetch sails: possible for base, full for user
    try:
        if str(base_id) in ("0", "None", "", "null"):  # base yacht
            sails_url = f"{SAILS_API}/sails/possible/{yacht_id}"
        else:
            sails_url = f"{SAILS_API}/sails/{yacht_id}"
        sails_resp = requests.get(sails_url)
        if sails_resp.ok:
            result["sails"] = sails_resp.json()
        elif sails_resp.status_code == 404:
            result["sails"] = []
        else:
            errors["sails"] = f"{sails_resp.status_code}: {sails_resp.text}"
            result["sails"] = []
    except Exception as e:
        errors["sails"] = str(e)
        result["sails"] = []
    # Fetch other microservices as before
    for key, url_template in MICROSERVICES.items():
        if key in ("profile", "sails"):  # already handled
            continue
        url = url_template.format(yacht_id=yacht_id)
        try:
            resp = requests.get(url)
            if resp.ok:
                result[key] = resp.json()
            elif resp.status_code == 404:
                result[key] = None
            else:
                errors[key] = f"{resp.status_code}: {resp.text}"
                result[key] = None
        except Exception as e:
            errors[key] = str(e)
            result[key] = None
    if errors:
        result["fetch_errors"] = errors
    return result

# --- Search Endpoints ---
@app.get("/yachts/search")
def search_yachts(query: str = ""):
    """
    Freeform search for base yachts (base_id == 0 or None) in the profile database.
    Splits the query into terms and matches any term in yacht_class, model, version, builder, designer, name, or variant.
    Returns a list of matching yachts (never an object).
    """
    try:
        resp = requests.get(f"{PROFILE_API}/profile/")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        profiles = resp.json()
        filtered = []
        # Split query into lowercase terms
        terms = [t.lower() for t in query.strip().split() if t.strip()]
        for p in profiles:
            base_id = p.get("base_id")
            if str(base_id).lower() not in ("none", "0", "", "null"):
                continue  # Only base yachts
            # Gather all searchable fields
            fields = [
                str(p.get("yacht_class", "")).lower(),
                str(p.get("model", "")).lower(),
                str(p.get("version", "")).lower(),
                str(p.get("builder", "")).lower(),
                str(p.get("designer", "")).lower(),
                str(p.get("name", "")).lower(),
                str(p.get("variant", "")).lower(),
            ]
            # Each term must match at least one field (partial match)
            matches_query = all(any(term in field for field in fields) for term in terms) if terms else True
            if matches_query:
                filtered.append(p)
        # Always return a list, even if empty
        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile microservice error: {e}")

# --- CRUD Endpoints ---
@app.post("/yachts/create")
def create_yacht(req: YachtCreateRequest):
    if req.hull:
        try:
            r = requests.post(f"{HULL_API}/hull/create", json=req.hull)
            r.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hull creation failed: {e}")
    if req.saildata:
        try:
            r = requests.post(f"{SAILDATA_API}/saildata/create", json=req.saildata)
            r.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Saildata creation failed: {e}")
    try:
        r = requests.post(f"{SAILS_API}/sails/generate", json={"yacht_id": req.yacht_id})
        r.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sails generation failed: {e}")
    try:
        r = requests.post(f"{ROPES_API}/ropes/generate", json={"yacht_id": req.yacht_id})
        r.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ropes generation failed: {e}")
    if req.profile:
        try:
            r = requests.post(f"{PROFILE_API}/profile/create", json=req.profile)
            r.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Profile creation failed: {e}")
    return {"status": "ok", "message": f"Yacht {req.yacht_id} created and orchestrated."}

@app.get("/yachts/{yacht_id}")
def get_yacht(yacht_id: int):
    return aggregate_yacht_data(yacht_id)

@app.delete("/yachts/{yacht_id}")
def delete_yacht(yacht_id: int):
    errors = {}
    for key, url_template in MICROSERVICES.items():
        url = url_template.format(yacht_id=yacht_id)
        try:
            resp = requests.delete(url)
            if resp.status_code != 200:
                errors[key] = resp.text
        except Exception as e:
            errors[key] = str(e)
    if errors:
        raise HTTPException(status_code=500, detail={"delete_errors": errors})
    return {"status": "ok", "message": f"Yacht {yacht_id} and all subcomponents deleted."}

# --- Pass-through Endpoints for Subcomponents (optional, add as needed) ---
@app.post("/yachts/{yacht_id}/hull/create")
def create_hull(yacht_id: int, hull_data: dict):
    try:
        resp = requests.post(f"{HULL_API}/hull/create", json=hull_data)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/keel/create")
def create_keel(yacht_id: int, keel_data: KeelCreateRequest):
    try:
        payload = keel_data.dict()
        payload["yacht_id"] = yacht_id
        resp = requests.post(f"{HULL_API}/hull/keel", json=payload)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/sails/add")
def add_sail(yacht_id: int, sail: SailTypeRequest):
    try:
        resp = requests.post(f"{SAILS_API}/sails/add_sail_type", json=sail.dict())
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/ropes/add")
def add_rope(yacht_id: int, rope: RopeTypeRequest):
    try:
        resp = requests.post(f"{ROPES_API}/ropes/add_rope_type", json=rope.dict())
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/saildata/create")
def create_saildata(yacht_id: int, saildata: dict):
    try:
        resp = requests.post(f"{SAILDATA_API}/saildata/create", json=saildata)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/profile/create")
def create_profile(yacht_id: int, profile_data: dict):
    try:
        resp = requests.post(f"{PROFILE_API}/profile/create", json=profile_data)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

# --- End of yacht_api.py ---
