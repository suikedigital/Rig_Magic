from models.hull_structure.service import HullStructureService

hullstructureservice = HullStructureService()

yacht_id = 1

hullstructureservice.save_keel(yacht_id, keel_type="Fin", draft=2.5)
hullstructureservice.save_rudder(yacht_id, rudder_type="Skeg")
hullstructureservice.save_hull(
    hull_type="monohull",
    yacht_id = yacht_id,
    loa=10.0,
    lwl=9.0,
    beam=3.5,
    displacement=5000,
    ballast=1500
)