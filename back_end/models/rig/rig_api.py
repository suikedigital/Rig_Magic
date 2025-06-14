from fastapi import FastAPI, HTTPException
from typing import Optional
from back_end.models.rig.service import RigService

app = FastAPI()
rig_service = RigService()

@app.get("/rig/{yacht_id}")
def get_rig(yacht_id: int):
    rig = rig_service.get_rig(yacht_id)
    if not rig:
        raise HTTPException(status_code=404, detail="Rig not found")
    return rig.__dict__
