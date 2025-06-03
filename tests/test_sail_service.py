from models.sails.sail_service import SailService

# Test for single yacht
yacht_id = 1

saildata = SailData(
    yacht_id,
    i=10.0,
    j=5.0,
    p=8.0,
    e=4.0,
)

sail_service = SailService(saildata.to_dict(), yacht_id=yacht_id)

sail_service.add_sail_type("Mainsail")
sail_service.add_sail_type("Genoa")

sail_service.set_sail_config("Genoa", {"luff": 15.0, "foot": 7.5, "overlap_percent": 150})

sail_service.generate_sails()
sail_service.get_sail("Mainsail")
sail_service.get_sail("Genoa")

sail_service.get_aero_force("Mainsail", 10.0)

# Test for multiple yachts with different configs

yacht_configs = [
    {
        "yacht_id": 2,
        "saildata": SailData(2, i=12.0, j=6.0, p=9.0, e=4.5),
        "sails": [
            ("Mainsail", {}),
            ("Jib", {"luff": 13.0, "foot": 6.5}),
        ],
        "aero_forces": [
            ("Mainsail", 12.0),
            ("Jib", 12.0),
        ],
    },
    {
        "yacht_id": 3,
        "saildata": SailData(3, i=14.0, j=7.0, p=10.0, e=5.0),
        "sails": [
            ("Mainsail", {}),
            ("Staysail", {"luff": 10.0, "foot": 4.0}),
            ("Genoa", {"luff": 16.0, "foot": 8.0, "overlap_percent": 140}),
        ],
        "aero_forces": [
            ("Mainsail", 15.0),
            ("Staysail", 15.0),
            ("Genoa", 15.0),
        ],
    },
]

for config in yacht_configs:
    print(f"\n--- Testing yacht_id {config['yacht_id']} ---")
    service = SailService(config["saildata"].to_dict(), yacht_id=config["yacht_id"])
    for sail_type, sail_cfg in config["sails"]:
        service.add_sail_type(sail_type)
        if sail_cfg:
            service.set_sail_config(sail_type, sail_cfg)
    service.generate_sails()
    for sail_type, _ in config["sails"]:
        sail = service.get_sail(sail_type)
        print(f"Sail for yacht {config['yacht_id']}, type {sail_type}: {sail}")
    for sail_type, wind in config["aero_forces"]:
        force = service.get_aero_force(sail_type, wind)
        print(f"Aero force for yacht {config['yacht_id']}, {sail_type} at {wind}kt: {force}")