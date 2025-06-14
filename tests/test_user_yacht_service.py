from orchestration.services import Services
from models.yacht.models.user_yacht.factory import UserYachtFactory

services = Services()
base_yacht_id = 1
owner_id = 1
name = "The Jolly Roger"

# Create user yacht from base yacht
user_yacht_id = UserYachtFactory.create_user_yacht_from_base(
    base_yacht_id=base_yacht_id,
    owner_id=owner_id,
    name=name,
    services=services
)

# Retrieve the user yacht
user_yacht = services.user_yacht_service.get_user_yacht_by_id(user_yacht_id)

print(f"Created user yacht with ID: {user_yacht.yacht_id}, name: {user_yacht.name}, owner: {user_yacht.owner_id}")