"""
Yacht API Orchestrator
---------------------
Central API for orchestrating yacht creation, updates, and aggregation across all microservices.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import requests
import collections
from fastapi.middleware.cors import CORSMiddleware

# Microservice endpoints (use Docker Compose service names)
SAILDATA_API = "http://saildata:8001"
SAILS_API = "http://sails:8020"
ROPES_API = "http://ropes:8010"
HULL_API = "http://hull_structure:8004"
PROFILE_API = "http://profile:8003"

app = FastAPI()

# Add CORS middleware for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

class YachtCreateRequest(BaseModel):
    yacht_id: int
    base_yacht: Optional[Dict[str, Any]] = None  # Optionally pass base yacht config
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

@app.post("/yachts/create")
def create_yacht(req: YachtCreateRequest):
    # 1. Create hull (optional)
    if req.hull:
        try:
            r = requests.post(f"{HULL_API}/hull/create", json=req.hull)
            r.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Hull creation failed: {e}")
    # 2. Create saildata
    if req.saildata:
        try:
            r = requests.post(f"{SAILDATA_API}/saildata/create", json=req.saildata)
            r.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Saildata creation failed: {e}")
    # 3. Create sails
    try:
        r = requests.post(f"{SAILS_API}/sails/generate", json={"yacht_id": req.yacht_id})
        r.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sails generation failed: {e}")
    # 4. Create ropes
    try:
        r = requests.post(f"{ROPES_API}/ropes/generate", json={"yacht_id": req.yacht_id})
        r.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ropes generation failed: {e}")
    # 5. Optionally create profile
    if req.profile:
        try:
            r = requests.post(f"{PROFILE_API}/profile/create", json=req.profile)
            r.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Profile creation failed: {e}")
    return {"status": "ok", "message": f"Yacht {req.yacht_id} created and orchestrated."}

@app.get("/yachts/search/builders")
def get_builders():
    # Query the profile microservice for all profiles and extract unique builders
    try:
        resp = requests.get(f"{PROFILE_API}/profile/")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        profiles = resp.json()
        builders = sorted(set(p.get("builder") for p in profiles if p.get("builder")))
        return builders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile microservice error: {e}")

@app.get("/yachts/search/classes")
def get_classes(builder: str = None, make: str = None, model: str = None):
    try:
        resp = requests.get(f"{PROFILE_API}/profile/")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        profiles = resp.json()
        filtered = profiles
        if builder:
            filtered = [p for p in filtered if p.get("builder") == builder]
        if make:
            filtered = [p for p in filtered if p.get("model") == make]
        if model:
            filtered = [p for p in filtered if p.get("version") == model]
        classes = sorted(set(p.get("yacht_class") for p in filtered if p.get("yacht_class")))
        return classes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile microservice error: {e}")

@app.get("/yachts/search/makes")
def get_makes(builder: str = None, class_: str = None, model: str = None):
    try:
        resp = requests.get(f"{PROFILE_API}/profile/")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        profiles = resp.json()
        filtered = profiles
        if builder:
            filtered = [p for p in filtered if p.get("builder") == builder]
        if class_:
            filtered = [p for p in filtered if p.get("yacht_class") == class_]
        if model:
            filtered = [p for p in filtered if p.get("version") == model]
        makes = sorted(set(p.get("model") for p in filtered if p.get("model")))
        return makes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile microservice error: {e}")

@app.get("/yachts/search/models")
def get_models(builder: str = None, class_: str = None, make: str = None):
    try:
        resp = requests.get(f"{PROFILE_API}/profile/")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        profiles = resp.json()
        filtered = profiles
        if builder:
            filtered = [p for p in filtered if p.get("builder") == builder]
        if class_:
            filtered = [p for p in filtered if p.get("yacht_class") == class_]
        if make:
            filtered = [p for p in filtered if p.get("model") == make]
        models = sorted(set(p.get("version") for p in filtered if p.get("version")))
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile microservice error: {e}")

@app.get("/yachts/search/variants")
def get_variants(builder: str = None, class_: str = None, make: str = None, model: str = None):
    try:
        resp = requests.get(f"{PROFILE_API}/profile/")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        profiles = resp.json()
        filtered = [p for p in profiles if p.get("base_yacht")]  # Only show yachts with base_yacht attribute
        if builder:
            filtered = [p for p in filtered if p.get("builder") == builder]
        if class_:
            filtered = [p for p in filtered if p.get("yacht_class") == class_]
        if make:
            filtered = [p for p in filtered if p.get("model") == make]
        if model:
            filtered = [p for p in filtered if p.get("version") == model]
        variants = sorted(set(p.get("variant") for p in filtered if p.get("variant")))
        return variants
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile microservice error: {e}")

@app.get("/yachts/search/boat")
def get_boat_info(builder: str = None, class_: str = None, make: str = None, model: str = None, variant: str = None):
    try:
        resp = requests.get(f"{PROFILE_API}/profile/")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        profiles = resp.json()
        # Only show base yachts (those with base_id is None)
        filtered = [p for p in profiles if not p.get("base_id")]  # base_id None or 0 means base yacht
        if builder:
            filtered = [p for p in filtered if p.get("builder") == builder]
        if class_:
            filtered = [p for p in filtered if p.get("yacht_class") == class_]
        if make:
            filtered = [p for p in filtered if p.get("model") == make]
        if model:
            filtered = [p for p in filtered if p.get("version") == model]
        if variant:
            filtered = [p for p in filtered if p.get("variant") == variant]
        if filtered:
            return filtered[0]  # Return the first matching boat
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile microservice error: {e}")

@app.get("/yachts/search")
def search_yachts(query: str = "", boat_type: str = None):
    try:
        resp = requests.get(f"{PROFILE_API}/profile/")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        profiles = resp.json()
        filtered = []
        # Treat 'undefined', 'all', '', None as no filter for boat_type
        normalized_boat_type = (boat_type or "").strip().lower() if boat_type else None
        if normalized_boat_type in (None, '', 'undefined', 'all', 'null'):
            normalized_boat_type = None
        # Split query into terms, ignore empty terms
        terms = [t.lower() for t in query.strip().split() if t.strip()]
        for p in profiles:
            base_id = p.get("base_id")
            if str(base_id).lower() not in ("none", "0", "", "null"):
                continue
            # Gather all searchable fields
            fields = [
                str(p.get("yacht_class", "")).lower(),
                str(p.get("model", "")).lower(),
                str(p.get("version", "")).lower(),
                str(p.get("builder", "")).lower(),
                str(p.get("designer", "")).lower(),
                str(p.get("name", "")).lower(),
            ]
            # Each term must match at least one field (partial match)
            matches_query = all(any(term in field for field in fields) for term in terms) if terms else True
            matches_type = not normalized_boat_type or normalized_boat_type == str(p.get("type", "")).lower()
            if matches_query and matches_type:
                filtered.append(p)
        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile microservice error: {e}")

@app.get("/yachts/{yacht_id}")
def get_yacht(yacht_id: int):
    # Aggregate all microservice data for this yacht
    result = {"yacht_id": yacht_id}
    try:
        r = requests.get(f"{SAILDATA_API}/saildata/{yacht_id}")
        if r.ok:
            result["saildata"] = r.json()
    except Exception:
        result["saildata"] = None
    try:
        r = requests.get(f"{SAILS_API}/sails/{yacht_id}")
        if r.ok:
            result["sails"] = r.json()
    except Exception:
        result["sails"] = None
    try:
        r = requests.get(f"{ROPES_API}/ropes/{yacht_id}")
        if r.ok:
            result["ropes"] = r.json()
    except Exception:
        result["ropes"] = None
    try:
        r = requests.get(f"{HULL_API}/hull/{yacht_id}")
        if r.ok:
            result["hull"] = r.json()
    except Exception:
        result["hull"] = None
    try:
        r = requests.get(f"{PROFILE_API}/profile/{yacht_id}")
        if r.ok:
            result["profile"] = r.json()
    except Exception:
        result["profile"] = None
    return result

@app.post("/yachts/{yacht_id}/ropes/add")
def add_rope(yacht_id: int, rope: RopeTypeRequest):
    try:
        resp = requests.post(
            f"{ROPES_API}/ropes/add_rope_type",
            json=rope.dict()
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.get("/yachts/{yacht_id}/ropes")
def get_ropes(yacht_id: int):
    try:
        resp = requests.get(f"{ROPES_API}/ropes/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/ropes/generate")
def generate_ropes(yacht_id: int):
    try:
        resp = requests.post(f"{ROPES_API}/ropes/generate", json={"yacht_id": yacht_id})
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/sails/add")
def add_sail(yacht_id: int, sail: SailTypeRequest):
    try:
        resp = requests.post(
            f"{SAILS_API}/sails/add_sail_type",
            json=sail.dict()
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.get("/yachts/{yacht_id}/sails")
def get_sails(yacht_id: int):
    try:
        resp = requests.get(f"{SAILS_API}/sails/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/sails/generate")
def generate_sails(yacht_id: int):
    try:
        resp = requests.post(f"{SAILS_API}/sails/generate", json={"yacht_id": yacht_id})
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.delete("/yachts/{yacht_id}/sails/{sail_type}")
def delete_sail(yacht_id: int, sail_type: str):
    try:
        resp = requests.delete(f"{SAILS_API}/sails/{yacht_id}/{sail_type}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.delete("/yachts/{yacht_id}/sails")
def delete_sails(yacht_id: int):
    try:
        resp = requests.delete(f"{SAILS_API}/sails/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.delete("/yachts/{yacht_id}/ropes/{rope_type}")
def delete_rope(yacht_id: int, rope_type: str):
    try:
        resp = requests.delete(f"{ROPES_API}/ropes/{yacht_id}/{rope_type}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.delete("/yachts/{yacht_id}/ropes")
def delete_ropes(yacht_id: int):
    try:
        resp = requests.delete(f"{ROPES_API}/ropes/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/hull/create")
def create_hull(yacht_id: int, hull_data: dict):
    try:
        resp = requests.post(f"{HULL_API}/hull/create", json=hull_data)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.get("/yachts/{yacht_id}/hull")
def get_hull(yacht_id: int):
    try:
        resp = requests.get(f"{HULL_API}/hull/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.delete("/yachts/{yacht_id}/hull")
def delete_hull(yacht_id: int):
    try:
        resp = requests.delete(f"{HULL_API}/hull/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/yachts/{yacht_id}/keel/create")
def create_keel(yacht_id: int, keel_data: dict):
    try:
        resp = requests.post(f"{HULL_API}/keel/create", json=keel_data)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.get("/yachts/{yacht_id}/keel")
def get_keel(yacht_id: int):
    try:
        resp = requests.get(f"{HULL_API}/keel/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.delete("/yachts/{yacht_id}/keel")
def delete_keel(yacht_id: int):
    try:
        resp = requests.delete(f"{HULL_API}/keel/{yacht_id}")
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

@app.get("/yachts/{yacht_id}/profile")
def get_profile(yacht_id: int):
    try:
        resp = requests.get(f"{PROFILE_API}/profile/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.delete("/yachts/{yacht_id}/profile")
def delete_profile(yacht_id: int):
    try:
        resp = requests.delete(f"{PROFILE_API}/profile/{yacht_id}")
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

@app.get("/yachts/{yacht_id}/saildata")
def get_saildata(yacht_id: int):
    try:
        resp = requests.get(f"{SAILDATA_API}/saildata/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.delete("/yachts/{yacht_id}/saildata")
def delete_saildata(yacht_id: int):
    try:
        resp = requests.delete(f"{SAILDATA_API}/saildata/{yacht_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.delete("/yachts/{yacht_id}")
def delete_yacht(yacht_id: int):
    errors = {}
    # Try to delete all subcomponents, collect errors but keep going
    for label, url, delete_path in [
        ("ropes", ROPES_API, f"/ropes/{yacht_id}"),
        ("sails", SAILS_API, f"/sails/{yacht_id}"),
        ("hull", HULL_API, f"/hull/{yacht_id}"),
        ("keel", HULL_API, f"/keel/{yacht_id}"),
        ("profile", PROFILE_API, f"/profile/{yacht_id}"),
        ("saildata", SAILDATA_API, f"/saildata/{yacht_id}")
    ]:
        try:
            resp = requests.delete(url + delete_path)
            if resp.status_code != 200:
                errors[label] = resp.text
        except Exception as e:
            errors[label] = str(e)
    if errors:
        raise HTTPException(status_code=500, detail={"delete_errors": errors})
    return {"status": "ok", "message": f"Yacht {yacht_id} and all subcomponents deleted."}
