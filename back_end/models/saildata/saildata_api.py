from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from back_end.models.saildata.saildata_service import SailDataService

app = FastAPI()
saildata_service = SailDataService()

class SailDataRequest(BaseModel):
    yacht_id: int
    i: float
    j: float
    p: float
    e: float
    base_id: Optional[int] = None
    extras: Optional[Dict[str, Any]] = None

@app.post("/saildata/")
def add_saildata(req: SailDataRequest):
    data = req.dict()
    extras = data.pop("extras", {}) or {}
    data.update(extras)
    saildata_service.save_saildata_from_dict(data["yacht_id"], data)
    return {"status": "ok"}

@app.get("/saildata/{yacht_id}")
def get_saildata(yacht_id: int):
    saildata = saildata_service.get_saildata(yacht_id)
    if not saildata:
        raise HTTPException(status_code=404, detail="SailData not found")
    if hasattr(saildata, "to_dict"):
        return saildata.to_dict()
    return saildata

@app.get("/saildata/debug/list_ids")
def list_ids():
    return saildata_service.db.list_yacht_ids()

@app.delete("/saildata/{yacht_id}")
def delete_saildata(yacht_id: int):
    saildata_service.delete_saildata_by_yacht(yacht_id)
    return {"status": "ok"}

