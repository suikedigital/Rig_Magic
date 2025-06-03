from models.yacht.models.yacht_profile import YachtProfile


from models.hull_structure.hull_structure_service import HullStructureService
from models.saildata.saildata_service import SailDataService
from models.sails.sail_service import SailService
from models.settings.settings_service import SettingsService
from models.ropes_rigging.rope_service import RopeService
from models.rig.rig_service import RigService


hullservice = HullStructureService()

yacht_id = 2

hullservice.save_hull(hull_type="Monohull", yacht_id=yacht_id, loa=11410, lwl=9680, beam=3680, displacement=6430, ballast=2020, construction="GRP")
hullservice.save_keel(yacht_id=yacht_id, keel_type="Fin", draft=1930)
hullservice.save_rudder(yacht_id=yacht_id, rudder_type="Spade")

saildataservice = SailDataService()

saildataservice.save_saildata_from_dict(yacht_id, {"i": 13650, "j": 3820, "p": 11900, "e": 4240})

saildata = saildataservice.get_saildata(yacht_id)

sailservice = SailService(saildata, yacht_id=yacht_id)

sailservice.add_sail_type("Mainsail")
sailservice.add_sail_type("Genoa")

sailservice.generate_sails = sailservice.generate_sails()

settingservice = SettingsService()
settings = settingservice.get_settings(yacht_id=yacht_id)
settings_dict = settings.to_dict()


ropeservice = RopeService(saildata, 
                          sail_service=sailservice, 
                          wind_speed_in_knots=settings_dict["wind_speed_in_knots"], 
                          halyard_load_safety_factor=settings_dict["halyard_load_safety_factor"], 
                          dynamic_load_safety_factor=settings_dict["dynamic_load_safety_factor"], 
                          length_safety_factor=settings_dict["length_safety_factor"])

RigService = RigService()
rig = RigService("Sloop", yacht_id=yacht_id, boom_above_deck=1.0)
rig_dict = rig.to_dict()

yacht_profile = YachtProfile(
    yacht_id=2,
    yacht_class="Jeanneau",
    model="Sun Odyssey",
    version="37",
    designer="Jacqes Fauroux",
    builder="Jeanneau Yachts",
    year_introduced=None,
    production_start=1998,
    production_end=None,
    country_of_origin="France",
    notes="A classic cruising yacht known for its performance and comfort."
)

