"""
Yacht API Orchestrator
---------------------
Central API for orchestrating yacht creation, updates, and aggregation across all microservices.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
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
            ropes_url = f"{ROPES_API}/ropes/possible/{yacht_id}"
        else:
            sails_url = f"{SAILS_API}/sails/{yacht_id}"
            ropes_url = f"{ROPES_API}/ropes/{yacht_id}"
        sails_resp = requests.get(sails_url)
        if sails_resp.ok:
            result["sails"] = sails_resp.json()
        elif sails_resp.status_code == 404:
            result["sails"] = []
        else:
            errors["sails"] = f"{sails_resp.status_code}: {sails_resp.text}"
            result["sails"] = []
        # Fetch ropes (possible for base, full for user)
        ropes_resp = requests.get(ropes_url)
        if ropes_resp.ok:
            result["ropes"] = ropes_resp.json()
        elif ropes_resp.status_code == 404:
            result["ropes"] = []
        else:
            errors["ropes"] = f"{ropes_resp.status_code}: {ropes_resp.text}"
            result["ropes"] = []
    except Exception as e:
        errors["sails"] = str(e)
        result["sails"] = []
        errors["ropes"] = str(e)
        result["ropes"] = []
    # Fetch saildata directly for frontend display
    saildata_url = MICROSERVICES["saildata"].format(yacht_id=yacht_id)
    try:
        resp = requests.get(saildata_url)
        if resp.ok:
            result["saildata"] = resp.json()
        elif resp.status_code == 404:
            result["saildata"] = None
        else:
            errors["saildata"] = f"{resp.status_code}: {resp.text}"
            result["saildata"] = None
    except Exception as e:
        errors["saildata"] = str(e)
        result["saildata"] = None

    # Fetch other microservices as before
    for key, url_template in MICROSERVICES.items():
        if key in ("profile", "sails", "ropes", "saildata"):  # already handled or redundant
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
    # Auto-increment yacht_id if not provided
    if req.yacht_id is None:
        # This is a simple example; in production, use a DB sequence or atomic counter
        import sqlite3
        conn = sqlite3.connect("back_end/data/settings.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS yacht_id_counter (id INTEGER PRIMARY KEY AUTOINCREMENT)")
        c.execute("INSERT INTO yacht_id_counter DEFAULT VALUES")
        conn.commit()
        c.execute("SELECT last_insert_rowid()")
        yacht_id = c.fetchone()[0]
        conn.close()
    else:
        yacht_id = req.yacht_id

    # Save profile
    if req.profile:
        profile = dict(req.profile)
        profile["yacht_id"] = yacht_id
        r = requests.post(f"{PROFILE_API}/profile/", json=profile)
        r.raise_for_status()
    # Save hull
    if req.hull:
        hull = dict(req.hull)
        hull["yacht_id"] = yacht_id
        r = requests.post(f"{HULL_API}/hull/hull", json=hull)
        r.raise_for_status()
    # Save keel
    if req.keel:
        keel = dict(req.keel)
        keel["yacht_id"] = yacht_id
        r = requests.post(f"{HULL_API}/hull/keel", json=keel)
        r.raise_for_status()
    # Save rudder
    if req.rudder:
        rudder = dict(req.rudder)
        rudder["yacht_id"] = yacht_id
        r = requests.post(f"{HULL_API}/hull/rudder", json=rudder)
        r.raise_for_status()
    # Save saildata
    if req.saildata:
        saildata = dict(req.saildata)
        saildata["yacht_id"] = yacht_id
        r = requests.post(f"{SAILDATA_API}/saildata/", json=saildata)
        r.raise_for_status()
    # Save rig
    if req.rig:
        rig = dict(req.rig)
        rig["yacht_id"] = yacht_id
        # TODO: Add rig microservice endpoint if available
        # r = requests.post(f"{RIG_API}/rig/", json=rig)
        # r.raise_for_status()
    # Save possible sails
    if req.possible_sails:
        for sail in req.possible_sails:
            sail_type = sail["sail_type"] if isinstance(sail, dict) else sail
            r = requests.post(f"{SAILS_API}/sails/possible/{yacht_id}", json={"sail_type": sail_type})
            r.raise_for_status()
    # Save possible ropes
    if req.possible_ropes:
        for rope in req.possible_ropes:
            rope_type = rope["rope_type"] if isinstance(rope, dict) else rope
            r = requests.post(f"{ROPES_API}/ropes/possible/{yacht_id}", json={"rope_type": rope_type})
            r.raise_for_status()
    # Save sails
    if req.sails:
        for sail in req.sails:
            sail_data = dict(sail)
            sail_data["yacht_id"] = yacht_id
            r = requests.post(f"{SAILS_API}/sails/add_sail_type", json=sail_data)
            r.raise_for_status()
    # Save ropes
    if req.ropes:
        for rope in req.ropes:
            rope_data = dict(rope)
            rope_data["yacht_id"] = yacht_id
            r = requests.post(f"{ROPES_API}/ropes/add_rope_type", json=rope_data)
            r.raise_for_status()
    return {"status": "ok", "yacht_id": yacht_id, "message": f"Yacht {yacht_id} created and orchestrated."}

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

@app.get("/sails/possible/{yacht_id}")
def get_possible_sails_passthrough(yacht_id: int):
    url = f"{SAILS_API}/sails/possible/{yacht_id}"
    resp = requests.get(url)
    if resp.ok:
        return resp.json()
    elif resp.status_code == 404:
        return []
    else:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

@app.get("/ropes/possible/{yacht_id}")
def get_possible_ropes_passthrough(yacht_id: int):
    url = f"{ROPES_API}/ropes/possible/{yacht_id}"
    resp = requests.get(url)
    if resp.ok:
        return resp.json()
    elif resp.status_code == 404:
        return []
    else:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

# --- End of yacht_api.py ---
