# Minimal FastAPI app for Docker build
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from .service import SailService

app = FastAPI()
sail_service = SailService()


class SailTypeRequest(BaseModel):
    yacht_id: int
    sail_type: str
    config: Optional[Dict[str, Any]] = None


class SailConfigRequest(BaseModel):
    yacht_id: int
    sail_type: str
    config: Dict[str, Any]


class GenerateSailsRequest(BaseModel):
    yacht_id: int


class PossibleSailRequest(BaseModel):
    sail_type: str
    config: Optional[Dict[str, Any]] = None


# --- POSSIBLE SAILS ROUTES (must be before generic /sails/{yacht_id}) ---
@app.get("/sails/possible/{yacht_id}")
def get_possible_sails(yacht_id: int):
    sails = sail_service.get_possible_sails(yacht_id)
    print(f"[DEBUG] GET /sails/possible/{yacht_id} returns: {sails}")
    if sails is None:
        return []
    return sails


@app.post("/sails/possible/{yacht_id}")
def add_possible_sail(yacht_id: int, req: PossibleSailRequest):
    sail_service.add_possible_sail(yacht_id, req.sail_type, req.config)
    return {"status": "ok"}


@app.delete("/sails/possible/{yacht_id}")
def remove_possible_sail(yacht_id: int, sail_type: str):
    return sail_service.remove_possible_sail(yacht_id, sail_type)


@app.post("/sails/add_sail_type")
def add_sail_type(req: SailTypeRequest):
    sail_service.add_sail_type(req.yacht_id, req.sail_type, req.config)
    return {"status": "ok"}


@app.post("/sails/set_sail_config")
def set_sail_config(req: SailConfigRequest):
    sail_service.set_sail_config(req.yacht_id, req.sail_type, req.config)
    return {"status": "ok"}


@app.post("/sails/generate")
def generate_sails(req: GenerateSailsRequest):
    sail_service.generate_sails(req.yacht_id)
    return {"status": "ok"}


@app.get("/sails/{yacht_id}/{sail_type}")
def get_sail(yacht_id: int, sail_type: str):
    sail = sail_service.get_sail(yacht_id, sail_type)
    if not sail:
        raise HTTPException(status_code=404, detail="Sail not found")
    return sail


@app.get("/sails/{yacht_id}")
def get_sails(yacht_id: int):
    return sail_service.get_sails_from_db(yacht_id)


@app.get("/sails/{yacht_id}/{sail_type}/aero_force")
def get_aero_force(yacht_id: int, sail_type: str, wind_speed: float):
    force = sail_service.get_aero_force(yacht_id, sail_type, wind_speed)
    if force is None:
        raise HTTPException(status_code=404, detail="Sail or force not found")
    return {"aero_force": force}


@app.delete("/sails/{yacht_id}")
def delete_sails(yacht_id: int):
    sail_service.delete_sails_by_yacht(yacht_id)
    return {"status": "ok"}


@app.delete("/sails/possible/{yacht_id}")
def delete_possible_sails(yacht_id: int):
    print(f"[DEBUG] Deleting all possible sails for yacht_id={yacht_id}")
    sail_service.db.delete_possible_sails(yacht_id)
    return {"status": "deleted"}
