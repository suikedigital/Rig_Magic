from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.factory import Factory
from typing import List, Dict, Any

app = FastAPI()

class FurlerSpecRequest(BaseModel):
    loa: int
    sail_area: float
    stay_diameter: float
    clevis_pin_diameter: float
    rod: bool = False
    stay_length: int
    rm: float = 0
    displacement: float = 0
    fractional_rig: bool = False

@app.post("/spec_furlers")
def spec_furlers_api(spec: FurlerSpecRequest) -> Dict[str, List[Any]]:
    results = Factory.spec_furlers(
        loa=spec.loa,
        sail_area=spec.sail_area,
        stay_diameter=spec.stay_diameter,
        clevis_pin_diameter=spec.clevis_pin_diameter,
        rod=spec.rod,
        stay_length=spec.stay_length,
        rm=spec.rm,
        displacement=spec.displacement,
        fractional_rig=spec.fractional_rig
    )
    # Convert results to JSON-serializable format
    def serialize(obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)
    return {brand: [serialize(f) for f in furlers] for brand, furlers in results.items()}
