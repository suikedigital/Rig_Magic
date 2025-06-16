# Minimal FastAPI app for Docker build
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from .service import RopeService
from back_end.logger import get_logger

app = FastAPI()
rope_service = RopeService()
logger = get_logger(__name__)


class RopeRequest(BaseModel):
    yacht_id: int
    rope_type: str
    led_aft: Optional[float] = 0.0
    config: Optional[Dict[str, Any]] = None


class GenerateRopesRequest(BaseModel):
    yacht_id: int
    wind_speed_in_knots: Optional[float] = 30
    halyard_load_safety_factor: Optional[float] = 4
    dynamic_load_safety_factor: Optional[float] = 2
    length_safety_factor: Optional[float] = 2


class PossibleRopeRequest(BaseModel):
    rope_type: str


# --- POSSIBLE ROPES ROUTES (must be before generic /ropes/{yacht_id}) ---
@app.get("/ropes/possible/{yacht_id}")
def get_possible_ropes(yacht_id: int):
    ropes = rope_service.db.get_possible_ropes(yacht_id)
    logger.debug(f"[DEBUG] GET /ropes/possible/{yacht_id} returns: {ropes}")
    if ropes is None:
        return []
    return [{"rope_type": rope_type} for rope_type, _ in ropes]


@app.post("/ropes/possible/{yacht_id}")
def add_possible_rope(yacht_id: int, req: PossibleRopeRequest):
    rope_service.db.save_possible_rope(yacht_id, req.rope_type)
    return {"status": "ok"}


@app.delete("/ropes/possible/{yacht_id}/{rope_type}")
def remove_possible_rope(yacht_id: int, rope_type: str):
    import sqlite3

    with sqlite3.connect(rope_service.db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM ropes_possible WHERE yacht_id = ? AND rope_type = ?",
            (yacht_id, rope_type),
        )
        conn.commit()
    return {"status": "ok"}


@app.delete("/ropes/possible/{yacht_id}")
def delete_possible_ropes(yacht_id: int):
    logger.debug(f"[DEBUG] Deleting all possible ropes for yacht_id={yacht_id}")
    rope_service.db.delete_possible_ropes(yacht_id)
    return {"status": "deleted"}


@app.post("/ropes/add_rope_type")
def add_rope_type(req: RopeRequest):
    result = rope_service.add_rope_type(
        req.yacht_id, req.rope_type, req.led_aft, **(req.config or {})
    )
    return {"status": "ok", "message": result}


@app.post("/ropes/generate")
def generate_ropes(req: GenerateRopesRequest):
    try:
        rope_service.generate_ropes(
            req.yacht_id,
            wind_speed_in_knots=req.wind_speed_in_knots,
            halyard_load_safety_factor=req.halyard_load_safety_factor,
            dynamic_load_safety_factor=req.dynamic_load_safety_factor,
            length_safety_factor=req.length_safety_factor,
        )
        return {"status": "ok"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@app.get("/ropes/{yacht_id}/{rope_type}")
def get_rope(yacht_id: int, rope_type: str):
    rope = rope_service.get_rope(yacht_id, rope_type)
    if not rope:
        raise HTTPException(status_code=404, detail="Rope not found")
    if hasattr(rope, "to_dict"):
        return rope.to_dict()
    return rope


@app.get("/ropes/{yacht_id}")
def get_ropes(yacht_id: int):
    ropes = rope_service.db.get_ropes_by_yacht(yacht_id)
    keys = [
        "id",
        "yacht_id",
        "base_id",
        "rope_type",
        "construction",
        "colour",
        "length",
        "diameter",
        "upper_term_type",
        "upper_hardware",
        "lower_term_type",
        "lower_hardware",
        "led_aft",
        "required_wl_kg",
        "config",
    ]
    return [dict(zip(keys, row)) for row in ropes]


@app.delete("/ropes/{yacht_id}/{rope_type}")
def delete_rope(yacht_id: int, rope_type: str):
    # Not implemented in RopeDatabase, placeholder for future
    raise HTTPException(status_code=501, detail="Delete not implemented yet")


@app.delete("/ropes/{yacht_id}")
def delete_ropes(yacht_id: int):
    rope_service.delete_ropes_by_yacht(yacht_id)
    return {"status": "ok"}


@app.post("/ropes/set_rope_config")
def set_rope_config(req: RopeRequest):
    result = rope_service.set_rope_config(req.yacht_id, req.rope_type, req.config or {})
    return {"status": "ok", "message": result}


@app.get("/")
def read_root():
    return {"message": "Hello from ropes!"}
