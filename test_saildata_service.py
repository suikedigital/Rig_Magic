from models.saildata.saildata_service import SailDataService

yacht_1 = 1 

saildata_dict = {
    "i": 12.0,
    "j": 4.0,
    "p": 11.0,
    "e": 4.5,

    "codezero_i": 12.0,
    "codezero_j": 6.0,
    "jib_i": 8.0,
    "jib_j": 4.0
}

yacht_2 = 2
saildata_dict_2 = {
    "i": 10.0,
    "j": 5.0,
    "p": 8.0,
    "e": 4.0,
    "codezero_i": 12.0,
    "codezero_j": 6.0,
    "spin_i": 10.0,
    "spin_j": 5.0,
    "jib_i": 8.0,
    "jib_j": 4.0
}

saildata_service = SailDataService()

saildata_service.save_saildata_from_dict(yacht_1, saildata_dict)
saildata_service.save_saildata_from_dict(yacht_2, saildata_dict_2)

loaded_saildata = saildata_service.get_saildata(yacht_2)




print(f"{loaded_saildata}")


