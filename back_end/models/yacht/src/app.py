"""
Yacht API Orchestrator (entrypoint)
---------------------
This file is the entrypoint for the yacht orchestrator microservice.
"""

from fastapi import FastAPI, HTTPException, Query, Body, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union
import requests
from fastapi.middleware.cors import CORSMiddleware
from src.logger import get_logger
import sys
import traceback

logger = get_logger(__name__)

# Microservice endpoints (use Docker Compose service names)
SAILDATA_API = "http://saildata:8001"
SAILS_API = "http://sails:8020"
ROPES_API = "http://ropes:8010"
HULL_API = "http://hull_structure:8004"
PROFILE_API = "http://profile:8003"
USER_PROFILE_API = "http://user_profile:8005"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    "rudder": f"{HULL_API}/hull/rudder/{{yacht_id}}",
    "sails": f"{SAILS_API}/sails/{{yacht_id}}",
    "saildata": f"{SAILDATA_API}/saildata/{{yacht_id}}",
    "ropes": f"{ROPES_API}/ropes/{{yacht_id}}",
    "possible_sails": f"{SAILS_API}/sails/possible/{{yacht_id}}",
    "possible_ropes": f"{ROPES_API}/ropes/possible/{{yacht_id}}",
}


@app.get("/yachts/search")
def search_yachts(query: str = Query("", description="Free-form search query")):
    # Call the profile microservice to get all profiles
    try:
        resp = requests.get("http://profile:8003/profile/all", timeout=5)
        resp.raise_for_status()
        profiles = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Profile service unavailable: {e}")
    # Fields to search
    search_fields = ["yacht_class", "model", "builder", "designer", "version"]
    query_lower = query.lower()
    results = []
    for profile in profiles:
        for field in search_fields:
            value = str(profile.get(field, "")).lower()
            if query_lower in value:
                results.append(profile)
                break
    # Sort by yacht_id descending and limit to 10
    results = sorted(results, key=lambda x: int(x.get("yacht_id", 0)), reverse=True)[:10]
    return results


@app.get("/yacht/{yacht_id}")
def get_yacht(yacht_id: int):
    logger.debug(f"=== YACHT DEBUG START === yacht_id: {yacht_id}")
    """
    Orchestrate calls to all microservices to build a full yacht profile.
    Be tolerant of missing data: return partial results if any component exists.
    """
    result = {"yacht_id": yacht_id}
    found_any = False
    errors = {}
    # Query each microservice for this yacht_id
    for key, url_template in MICROSERVICES.items():
        url = url_template.format(yacht_id=yacht_id)
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 404:
                logger.warning(f"[DEBUG] {key}: 404 Not Found")
                result[key] = None
                continue
            resp.raise_for_status()
            data = resp.json()
            logger.debug(f"[DEBUG] {key}:", data)
            # Tolerant: found_any if any non-empty dict or non-empty list
            if (isinstance(data, dict) and data) or (
                isinstance(data, list) and len(data) > 0
            ):
                found_any = True
                logger.debug(f"[DEBUG] found_any set True by {key}")
            result[key] = data
        except Exception as e:
            errors[key] = str(e)
            result[key] = None
            logger.debug(f"[DEBUG] {key}: Exception {e}")
    # For backward compatibility, also add possible_sails/ropes to top-level if present
    if result.get("possible_sails") is not None:
        result["possible_sails"] = result["possible_sails"]
    if result.get("possible_ropes") is not None:
        result["possible_ropes"] = result["possible_ropes"]
    logger.debug(f"[DEBUG] Final found_any: {found_any}")
    logger.debug(f"[DEBUG] Final result: {result}")
    if not found_any:
        raise HTTPException(
            status_code=404, detail="Yacht not found in any microservice"
        )
    if errors:
        result["errors"] = errors
    return result


@app.post("/yacht/")
def create_yacht(req: YachtCreateRequest):
    """
    Orchestrate creation of a yacht by sending data to all relevant microservices.
    """
    yacht_id = req.yacht_id
    responses = {}
    errors = {}
    # Profile
    if req.profile:
        try:
            resp = requests.post(f"{PROFILE_API}/profile/", json=req.profile, timeout=5)
            resp.raise_for_status()
            responses["profile"] = resp.json()
        except Exception as e:
            errors["profile"] = str(e)
    # Hull
    if req.hull:
        try:
            resp = requests.post(f"{HULL_API}/hull/hull", json=req.hull, timeout=5)
            resp.raise_for_status()
            responses["hull"] = resp.json()
        except Exception as e:
            errors["hull"] = str(e)
    # Keel
    if req.keel:
        try:
            resp = requests.post(f"{HULL_API}/hull/keel", json=req.keel, timeout=5)
            resp.raise_for_status()
            responses["keel"] = resp.json()
        except Exception as e:
            errors["keel"] = str(e)
    # Rudder
    if req.rudder:
        try:
            resp = requests.post(f"{HULL_API}/hull/rudder", json=req.rudder, timeout=5)
            resp.raise_for_status()
            responses["rudder"] = resp.json()
        except Exception as e:
            errors["rudder"] = str(e)
    # Saildata
    if req.saildata:
        try:
            resp = requests.post(
                f"{SAILDATA_API}/saildata/", json=req.saildata, timeout=5
            )
            resp.raise_for_status()
            responses["saildata"] = resp.json()
        except Exception as e:
            errors["saildata"] = str(e)
    # Sails
    if req.sails:
        for sail in req.sails:
            try:
                resp = requests.post(
                    f"{SAILS_API}/sails/add_sail_type", json=sail, timeout=5
                )
                resp.raise_for_status()
                responses.setdefault("sails", []).append(resp.json())
            except Exception as e:
                errors.setdefault("sails", []).append(str(e))
    # Ropes
    if req.ropes:
        for rope in req.ropes:
            try:
                resp = requests.post(
                    f"{ROPES_API}/ropes/add_rope_type", json=rope, timeout=5
                )
                resp.raise_for_status()
                responses.setdefault("ropes", []).append(resp.json())
            except Exception as e:
                errors.setdefault("ropes", []).append(str(e))
    # Possible Sails
    if req.possible_sails:
        logger.info(f"[Orchestrator] possible_sails: {req.possible_sails}")
        try:
            for sail_type in req.possible_sails:
                sail_payload = {
                    "yacht_id": yacht_id,
                    "sail_type": (
                        sail_type
                        if isinstance(sail_type, str)
                        else sail_type.get("sail_type")
                    ),
                    "config": (
                        sail_type.get("config") if isinstance(sail_type, dict) else None
                    ),
                }
                logger.info(
                    f"[Orchestrator] POST /sails/possible/{yacht_id} payload: {sail_payload}"
                )
                resp = requests.post(
                    f"{SAILS_API}/sails/possible/{yacht_id}",
                    json=sail_payload,
                    timeout=5,
                )
                resp.raise_for_status()
            responses["possible_sails"] = "ok"
        except Exception as e:
            errors["possible_sails"] = str(e)
    # Possible Ropes
    if req.possible_ropes:
        logger.info(f"[Orchestrator] possible_ropes: {req.possible_ropes}")
        try:
            for rope_type in req.possible_ropes:
                rope_payload = {
                    "yacht_id": yacht_id,
                    "rope_type": (
                        rope_type
                        if isinstance(rope_type, str)
                        else rope_type.get("rope_type")
                    ),
                    "config": (
                        rope_type.get("config") if isinstance(rope_type, dict) else None
                    ),
                }
                logger.info(
                    f"[Orchestrator] POST /ropes/possible/{yacht_id} payload: {rope_payload}"
                )
                resp = requests.post(
                    f"{ROPES_API}/ropes/possible/{yacht_id}",
                    json=rope_payload,
                    timeout=5,
                )
                resp.raise_for_status()
            responses["possible_ropes"] = "ok"
        except Exception as e:
            errors["possible_ropes"] = str(e)
    # Add more as needed for rig, etc.
    result = {"responses": responses}
    if errors:
        result["errors"] = errors
    return result


@app.delete("/yacht/{yacht_id}")
def delete_yacht(yacht_id: int):
    errors = {}
    responses = {}
    # Profile
    try:
        resp = requests.delete(f"{PROFILE_API}/profile/{yacht_id}", timeout=5)
        if resp.status_code not in (200, 204, 404):
            errors["profile"] = resp.text
        else:
            responses["profile"] = resp.status_code
    except Exception as e:
        errors["profile"] = str(e)
    # Hull
    try:
        resp = requests.delete(f"{HULL_API}/hull/{yacht_id}", timeout=5)
        if resp.status_code not in (200, 204, 404):
            errors["hull"] = resp.text
        else:
            responses["hull"] = resp.status_code
    except Exception as e:
        errors["hull"] = str(e)
    # Keel
    try:
        resp = requests.delete(f"{HULL_API}/hull/keel/{yacht_id}", timeout=5)
        if resp.status_code not in (200, 204, 404):
            errors["keel"] = resp.text
        else:
            responses["keel"] = resp.status_code
    except Exception as e:
        errors["keel"] = str(e)
    # Rudder
    try:
        resp = requests.delete(f"{HULL_API}/hull/rudder/{yacht_id}", timeout=5)
        if resp.status_code not in (200, 204, 404):
            errors["rudder"] = resp.text
        else:
            responses["rudder"] = resp.status_code
    except Exception as e:
        errors["rudder"] = str(e)
    # Saildata
    try:
        resp = requests.delete(f"{SAILDATA_API}/saildata/{yacht_id}", timeout=5)
        if resp.status_code not in (200, 204, 404):
            errors["saildata"] = resp.text
        else:
            responses["saildata"] = resp.status_code
    except Exception as e:
        errors["saildata"] = str(e)
    # Sails
    try:
        resp = requests.delete(f"{SAILS_API}/sails/{yacht_id}", timeout=5)
        if resp.status_code not in (200, 204, 404):
            errors["sails"] = resp.text
        else:
            responses["sails"] = resp.status_code
    except Exception as e:
        errors["sails"] = str(e)
    # Ropes
    try:
        resp = requests.delete(f"{ROPES_API}/ropes/{yacht_id}", timeout=5)
        if resp.status_code not in (200, 204, 404):
            errors["ropes"] = resp.text
        else:
            responses["ropes"] = resp.status_code
    except Exception as e:
        errors["ropes"] = str(e)
    # Possible Sails
    try:
        resp = requests.delete(f"{SAILS_API}/sails/possible/{yacht_id}", timeout=5)
        if resp.status_code not in (200, 204, 404):
            errors["possible_sails"] = resp.text
        else:
            responses["possible_sails"] = resp.status_code
    except Exception as e:
        errors["possible_sails"] = str(e)
    # Possible Ropes
    try:
        resp = requests.delete(f"{ROPES_API}/ropes/possible/{yacht_id}", timeout=5)
        if resp.status_code not in (200, 204, 404):
            errors["possible_ropes"] = resp.text
        else:
            responses["possible_ropes"] = resp.status_code
    except Exception as e:
        errors["possible_ropes"] = str(e)
    result = {"responses": responses}
    if errors:
        result["errors"] = errors
    if errors:
        return JSONResponse(status_code=207, content=result)
    return {"status": "ok", **result}


def add_yacht_to_user(user_id: str, yacht_id: int):
    """
    Add a yacht to the user's yacht_ids list using the dedicated endpoint.
    """
    resp = requests.post(
        f"{USER_PROFILE_API}/users/{user_id}/add_yacht",
        json={"yacht_id": str(yacht_id)},
        timeout=5,
    )
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=f"Failed to add yacht to user: {resp.text}")
    return resp.json()


def clone_yacht(yacht_id: int, user_id: int, name: str = None, spec: str = None, notes: str = None):
    """
    Clone a yacht by copying its profile, hull, keel, rudder, saildata, sails, and ropes.
    Assign the new yacht to the user by updating their yacht_ids list.
    Optionally override name, spec, notes.
    """
    print(f"[clone_yacht] called with yacht_id={yacht_id}, user_id={user_id}, name={name}, spec={spec}, notes={notes}", flush=True)
    logger.info(f"[clone_yacht] called with yacht_id={yacht_id}, user_id={user_id}, name={name}, spec={spec}, notes={notes}")
    try:
        yacht = get_yacht(yacht_id)
        print(f"[clone_yacht] get_yacht returned: {yacht}", flush=True)
        yacht_data = yacht.dict() if hasattr(yacht, 'dict') else dict(yacht)
        base_id = yacht_data.pop("yacht_id", None)
        yacht_data["base_id"] = base_id
        # Override profile fields if provided
        if "profile" in yacht_data and isinstance(yacht_data["profile"], dict):
            if name:
                yacht_data["profile"]["model"] = name
            if spec:
                yacht_data["profile"]["spec"] = spec
            if notes:
                yacht_data["profile"]["notes"] = notes
        # Remove possible_sails and possible_ropes from yacht_data before creation
        possible_sails = yacht_data.pop("possible_sails", None)
        possible_ropes = yacht_data.pop("possible_ropes", None)
        print(f"[clone_yacht] yacht_data for create_yacht: {yacht_data}", flush=True)
        create_result = create_yacht(YachtCreateRequest(**yacht_data))
        print(f"[clone_yacht] create_yacht result: {create_result}", flush=True)
        # Try to extract new yacht_id from the profile response
        new_yacht_id = None
        if isinstance(create_result, dict):
            profile_resp = create_result.get("responses", {}).get("profile")
            if profile_resp and isinstance(profile_resp, dict):
                new_yacht_id = profile_resp.get("yacht_id") or profile_resp.get("id")
        if not new_yacht_id:
            print("[clone_yacht] Could not determine new yacht_id", flush=True)
            logger.error("[clone_yacht] Could not determine new yacht_id")
            raise HTTPException(status_code=500, detail="Could not determine new yacht_id")
        # --- Now POST possible_sails and possible_ropes with new_yacht_id ---
        if possible_sails:
            for sail_type in possible_sails:
                sail_payload = {
                    "yacht_id": new_yacht_id,
                    "sail_type": sail_type if isinstance(sail_type, str) else sail_type.get("sail_type") or sail_type.get("type"),
                    "config": sail_type.get("config") if isinstance(sail_type, dict) else None,
                }
                logger.info(f"[Orchestrator] POST /sails/possible/{new_yacht_id} payload: {sail_payload}")
                requests.post(f"{SAILS_API}/sails/possible/{new_yacht_id}", json=sail_payload, timeout=5)
        if possible_ropes:
            for rope_type in possible_ropes:
                rope_payload = {
                    "yacht_id": new_yacht_id,
                    "rope_type": rope_type if isinstance(rope_type, str) else rope_type.get("rope_type"),
                    "config": rope_type.get("config") if isinstance(rope_type, dict) else None,
                }
                logger.info(f"[Orchestrator] POST /ropes/possible/{new_yacht_id} payload: {rope_payload}")
                requests.post(f"{ROPES_API}/ropes/possible/{new_yacht_id}", json=rope_payload, timeout=5)
        add_yacht_to_user(user_id, new_yacht_id)
        print(f"[clone_yacht] Successfully cloned yacht. new_yacht_id={new_yacht_id}", flush=True)
        logger.info(f"[clone_yacht] Successfully cloned yacht. new_yacht_id={new_yacht_id}")
        return {"new_yacht_id": new_yacht_id}
    except HTTPException as e:
        print(f"[clone_yacht] HTTPException: {e}", flush=True)
        logger.error(f"[clone_yacht] HTTPException: {e}")
        raise HTTPException(status_code=e.status_code, detail=f"Yacht not found: {e.detail}")
    except Exception as e:
        print(f"[clone_yacht] Exception: {e}", flush=True)
        logger.error(f"[clone_yacht] Exception: {e}")
        raise


@app.post("/yacht/clone")
def clone_yacht_endpoint(data: dict = Body(...)):
    print("[clone_yacht_endpoint] called with data:", data, flush=True)
    logger.info(f"[clone_yacht_endpoint] called with data: {data}")
    original_yacht_id = data.get("originalBoatId")
    user_id = data.get("userId")
    name = data.get("name")
    spec = data.get("spec")
    notes = data.get("notes")
    if not original_yacht_id or not user_id:
        print("[clone_yacht_endpoint] Missing originalBoatId or userId", flush=True)
        logger.error("[clone_yacht_endpoint] Missing originalBoatId or userId")
        raise HTTPException(status_code=400, detail="Missing originalBoatId or userId")
    try:
        result = clone_yacht(original_yacht_id, user_id, name=name, spec=spec, notes=notes)
        print(f"[clone_yacht_endpoint] clone_yacht result: {result}", flush=True)
        logger.info(f"[clone_yacht_endpoint] clone_yacht result: {result}")
        return result
    except Exception as e:
        print(f"[clone_yacht_endpoint] Exception: {e}", flush=True)
        logger.error(f"[clone_yacht_endpoint] Exception: {e}")
        raise


# Global exception handler for FastAPI
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("UNCAUGHT EXCEPTION:", exc, flush=True)
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


def handle_exception(exc_type, exc_value, exc_traceback):
    print("UNCAUGHT EXCEPTION (sys):", exc_value, flush=True)
    traceback.print_exception(exc_type, exc_value, exc_traceback)


sys.excepthook = handle_exception

