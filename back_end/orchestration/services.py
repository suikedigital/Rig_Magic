# The `yacht_aggregate_service.py` (sometimes called `YachtAggregateService`) is the orchestration layer responsible for aggregating and coordinating data from all the yacht-related microservices. Its main purpose is to provide high-level operations that require data from multiple domains (hull, rig, sails, ropes, settings, etc.) and present a unified interface for working with a complete yacht.

# ---

## Typical Responsibilities of `yacht_aggregate_service.py`

# 1. **Aggregate Full Yacht Profile**
#    - Collects and assembles all data for a given `yacht_id` from each microservice (hull, rig, sails, ropes, settings, etc.).
#    - Returns a comprehensive yacht profile as a single dictionary or object.

# 2. **Create User Yacht from Base Template**
#    - Handles the instantiation of a new user yacht from a base yacht template.
#    - Initializes all required microservices with the correct data.

# 3. **Update/Clone/Delete Yacht**
#    - Coordinates updates, cloning, or deletion of a yacht across all microservices.

# 4. **Validation and Consistency**
#    - Ensures that all required components exist and are consistent for a given yacht.

# 5. **High-Level Business Logic**
#    - Any workflow that spans multiple microservices but is not specific to a single domain.

# ---

## Example: What Would Be in `yacht_aggregate_service.py`

from ..models.hull_structure.service import HullStructureService
from ..models.rig.service import RigService
from ..models.sails.sail_service import SailService
from ..models.saildata.saildata_service import SailDataService
from ..models.ropes.rope_service import RopeService
from ..models.settings.settings_service import SettingsService
from ..models.yacht.user_yacht_service import UserYachtService
from ..models.yacht.base_yacht_service import BaseYachtService
from ..models.profile.service import YachtProfileService


class Services:
    def __init__(self):
        self.profile_service = YachtProfileService()
        self.hull_service = HullStructureService()
        self.rig_service = RigService()
        self.saildata = SailDataService()
        self.sail_service = SailService()
        self.rope_service = RopeService()
        self.settings_service = SettingsService()
        self.user_yacht_service = UserYachtService()
        self.base_yacht_service = BaseYachtService()

