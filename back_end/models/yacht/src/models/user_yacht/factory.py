from ...service import BaseYachtService
# from ..user_yacht_service import UserYachtService  # Not found, please implement or correct path
from .user_yacht import UserYacht

class UserYachtFactory:
    @staticmethod
    def create_user_yacht_from_base(base_yacht_id, owner_id, name, services):
        base_yacht = BaseYachtService().get_base_yacht_by_id(base_yacht_id)
        if not base_yacht:
            raise ValueError(f"Base yacht with id {base_yacht_id} not found.")
        # Create UserYacht object
        user_yacht = UserYacht(
            yacht_id=None,  # Will be set by DB
            base_yacht_id=base_yacht_id,
            owner_id=owner_id,
            name=name,
            services=services,
        )
        # Save to DB and get new yacht_id
        # yacht_id = UserYachtService().save_user_yacht(user_yacht)  # Uncomment and fix if UserYachtService is implemented
        yacht_id = None  # Placeholder
        # Initialize microservices with defaults
        services.profile_service.initialize_from_base(yacht_id, base_yacht)
        services.hull_service.initialize_from_base(yacht_id, base_yacht)
        services.saildata.initialize_from_base(yacht_id, base_yacht)
        services.sail_service.initialize_from_base(yacht_id, base_yacht)
        services.rig_service.initialize_from_base(yacht_id, base_yacht)
        
        # ...add more as needed
        return yacht_id

    @staticmethod
    def get_user_yacht(yacht_id, user_id=None):
        """
        Retrieves a user yacht by yacht_id (and optionally user_id).
        """
        # user_yacht_service = UserYachtService()  # Uncomment and fix if UserYachtService is implemented
        # return user_yacht_service.get_user_yacht_by_id(yacht_id, user_id)
        return None  # Placeholder

    @staticmethod
    def list_user_yachts(owner_id=None):
        """
        Lists all user yachts for a given owner/user.
        """
        # user_yacht_service = UserYachtService()  # Uncomment and fix if UserYachtService is implemented
        # return user_yacht_service.list_user_yachts(owner_id)
        return []  # Placeholder

    @staticmethod
    def get_yacht_profile(yacht_id: int, user_id: int = None):
        """
        Retrieves the yacht profile for a given yacht ID and user ID.
        If user_id is provided, it returns the user's specific profile.
        If not, it returns the base yacht profile.
        """
        if user_id:
            return UserYachtFactory.get_user_yacht(yacht_id, user_id)
        else:
            base_service = BaseYachtService()
            return base_service.get_base_yacht_by_id(yacht_id)