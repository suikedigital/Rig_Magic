from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from back_end.models.hull_structure.service import HullStructureService

app = FastAPI()
hull_service = HullStructureService()

class KeelRequest(BaseModel):
    yacht_id: int
    keel_type: str
    draft: float
    base_id: Optional[int] = None

class RudderRequest(BaseModel):
    yacht_id: int
    rudder_type: str
    base_id: Optional[int] = None

class HullRequest(BaseModel):
    yacht_id: int
    hull_type: str
    loa: Optional[float] = None
    lwl: Optional[float] = None
    beam: Optional[float] = None
    displacement: Optional[float] = None
    ballast: Optional[float] = None
    base_id: Optional[int] = None

@app.post("/hull/keel")
def add_keel(req: KeelRequest):
    hull_service.save_keel(req.yacht_id, req.keel_type, req.draft)
    return {"status": "ok"}

@app.get("/hull/keel/{yacht_id}")
def get_keel(yacht_id: int):
    keel = hull_service.get_keel(yacht_id)
    if not keel:
        raise HTTPException(status_code=404, detail="Keel not found")
    return keel.__dict__

@app.post("/hull/rudder")
def add_rudder(req: RudderRequest):
    hull_service.save_rudder(req.yacht_id, req.rudder_type)
    return {"status": "ok"}

@app.get("/hull/rudder/{yacht_id}")
def get_rudder(yacht_id: int):
    rudder = hull_service.get_rudder(yacht_id)
    if not rudder:
        raise HTTPException(status_code=404, detail="Rudder not found")
    return rudder.__dict__

@app.post("/hull/hull")
def add_hull(req: HullRequest):
    hull_service.save_hull(req)
    return {"status": "ok"}

@app.get("/hull/{yacht_id}")
def get_hull(yacht_id: int):
    hull = hull_service.get_hull(yacht_id)
    if not hull:
        raise HTTPException(status_code=404, detail="Hull not found")
    return hull.__dict__

@app.delete("/hull/{yacht_id}")
def delete_all(yacht_id: int):
    hull_service.delete_all_by_yacht(yacht_id)
    return {"status": "deleted"}
