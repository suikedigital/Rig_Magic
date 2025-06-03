from models.settings.settings_service import SettingsService
from models.settings.models.settings import Settings

# Create the service
service = SettingsService()

yacht_id = 42
settings_data = {
    "yacht_id": yacht_id,
    "wind_speed_in_knots": 25,
    "length_safety_factor": 1.2,
    "halyard_load_safety_factor": 2.5,
    "dynamic_load_safety_factor": 1.8
}

# Save settings from dict
service.save_settings_from_dict(settings_data)

# Retrieve and check
retrieved = service.get_settings(yacht_id)
assert retrieved is not None, "Settings not found!"
assert retrieved.yacht_id == yacht_id
assert retrieved.wind_speed_in_knots == 25
assert abs(retrieved.length_safety_factor - 1.2) < 1e-6
assert abs(retrieved.halyard_load_safety_factor - 2.5) < 1e-6
assert abs(retrieved.dynamic_load_safety_factor - 1.8) < 1e-6
print("[TEST PASS] Settings saved and retrieved correctly.")

# Overwrite settings
settings_data2 = settings_data.copy()
settings_data2["wind_speed_in_knots"] = 30
service.save_settings_from_dict(settings_data2)
retrieved2 = service.get_settings(yacht_id)
assert retrieved2.wind_speed_in_knots == 30, "Settings not overwritten!"
print("[TEST PASS] Settings overwrite works correctly.")

# Delete settings
service.delete_settings(yacht_id)
assert service.get_settings(yacht_id) is None, "Settings not deleted!"
print("[TEST PASS] Settings deletion works correctly.")

service.close()
