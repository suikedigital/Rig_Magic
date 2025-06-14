# sails_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from back_end.models.sails.sail_service import SailService

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
