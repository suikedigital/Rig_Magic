from models.ropes_rigging.rope_service import RopeService
from models.saildata.saildata_service import SailDataService
from models.sails.sail_service import SailService

# Setup sail data and services
yacht_id = 1
saildata_service = SailDataService()
saildata_service.save_saildata_from_dict(yacht_id=yacht_id, data={
    "i": 12.0,
    "j": 4.0,
    "p": 11.0,
    "e": 4.5,
})
saildata = saildata_service.get_saildata(yacht_id).to_dict()
sail_service = SailService(saildata, yacht_id=yacht_id)

# Add more sails
sail_service.add_sail_type("Mainsail")
sail_service.add_sail_type("Genoa")
sail_service.add_sail_type("Jib")
sail_service.add_sail_type("CodeZero")
sail_service.add_sail_type("Trisail")
sail_service.generate_sails()

# Create RopeService with dependencies
ropeservice = RopeService(
    saildata=saildata,
    sail_service=sail_service,
    wind_speed_in_knots=30,
    halyard_load_safety_factor=3.0,
    dynamic_load_safety_factor=2,
    length_safety_factor=1.00
)

# Add more rope types and configs
ropeservice.add_rope_type("MainHalyard", led_aft=2.0)
ropeservice.add_rope_type("GenoaHalyard", led_aft=0.5)
ropeservice.add_rope_type("JibHalyard", led_aft=1.0)
ropeservice.add_rope_type("CodeZeroHalyard", led_aft=1.8)
ropeservice.add_rope_type("TrisailHalyard", led_aft=1.2)

# Generate all ropes
ropeservice.generate_ropes()

# Retrieve and display ropes
for rope_name in ["MainHalyard", "GenoaHalyard", "JibHalyard", "CodeZeroHalyard", "TrisailHalyard"]:
    rope = ropeservice.get_rope(rope_name)
    print(f"{rope_name}:")
    print(rope)
    # Test: construction.diameter should match rope.diameter
    assert hasattr(rope, 'construction'), f"{rope_name} missing construction attribute"
    assert rope.construction.diameter == rope.diameter, f"{rope_name} construction.diameter ({rope.construction.diameter}) does not match rope.diameter ({rope.diameter})"
    print(f"[TEST PASS] {rope_name} construction.diameter matches rope.diameter: {rope.diameter} mm\n")

# Demonstrate calc_load (requires HALYARD_TO_SAIL mapping and wind speed)
HALYARD_TO_SAIL = {
    "MainHalyard": ["Mainsail"],
    "GenoaHalyard": ["Genoa"],
    "JibHalyard": ["Jib"],
    "CodeZeroHalyard": ["CodeZero"],
    "TrisailHalyard": ["Trisail"]
}
wind_speed_knots = 15
for rope_name in HALYARD_TO_SAIL:
    rope = ropeservice.get_rope(rope_name)
    try:
        load = rope.calc_load(HALYARD_TO_SAIL, wind_speed_knots)
        print(f"{rope_name} Load (kg) at {wind_speed_knots} knots: {load}")
    except Exception as e:
        print(f"Error calculating load for {rope_name}: {e}")