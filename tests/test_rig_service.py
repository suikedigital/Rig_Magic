from models.rig.rig_service import RigService

# Instantiate the service
rig_service = RigService()
yacht_id1 = 1
yacht_id2 = 2
yacht_id3 = 3  # Example yacht ID, replace with actual ID as needed

# Create a Sloop rig with a boom 1.5m above deck
sloop = rig_service.create_rig("Sloop", yacht_id1, boom_above_deck=1.5)
rig_service.save_rig(sloop)
print(f"Created rig: {sloop.rig_type}, boom above deck: {sloop.boom_above_deck}m")

# Create a CatBoat rig with a boom 0.8m above deck
catboat = rig_service.create_rig("CatBoat", yacht_id2, boom_above_deck=0.8)
rig_service.save_rig(catboat)
print(f"Created rig: {catboat.rig_type}, boom above deck: {catboat.boom_above_deck}m")

# Create a Ketch rig with no boom height specified
ketch = rig_service.create_rig("Ketch", yacht_id3)
rig_service.save_rig(ketch)
print(f"Created rig: {ketch.rig_type}, boom above deck: {ketch.boom_above_deck}")
