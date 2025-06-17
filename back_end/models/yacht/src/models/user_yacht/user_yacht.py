class UserYacht:
    def __init__(self, base_yacht_id, yacht_id, owner_id, name, services, yacht_type):
        """
        Initializes a UserYacht instance with the given yacht_id, owner_id, and name.
        """
        self.base_yacht_id = base_yacht_id
        self.yacht_id = yacht_id
        self.owner_id = owner_id
        self.name = name
        self.services = services
        self.yacht_type = yacht_type

    def load_profile(self):
        """
        Retrieves the yacht profile using the services provided.
        """
        return self.services.get_yacht_profile(self.yacht_id)

    def load_hull(self):
        """
        Retrieves the yacht hull using the services provided.
        """
        return self.services.get_yacht_hull(self.yacht_id)

    def load_rig(self):
        """
        Retrieves the yacht rig using the services provided.
        """
        return self.services.get_yacht_rig(self.yacht_id)

    def load_sails(self):
        """
        Retrieves the yacht sails using the services provided.
        """
        return self.services.get_yacht_sails(self.yacht_id)

    def get_running_rigging(self):
        """
        Retrieves the yacht running rigging using the services provided.
        """
        return self.services.get_yacht_running_rigging(self.yacht_id)

    def get_saildata(self):
        """
        Retrieves the yacht sail data using the services provided.
        """
        return self.services.get_yacht_sail_data(self.yacht_id)

    def get_standing_rigging(self):
        """
        Retrieves the yacht standing rigging using the services provided.
        """
        return self.services.get_yacht_standing_rigging(self.yacht_id)