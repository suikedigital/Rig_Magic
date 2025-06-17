class BaseYacht:
    _next_base_id = 1  # private class variable

    def __init__(self, profile, hull, rig, saildata):
        """
        Initializes a BaseYacht instance with an auto-incremented base_id.
        """
        self.base_id = BaseYacht._next_base_id
        BaseYacht._next_base_id += 1
        self.profile = profile
        self.hull = hull
        self.rig = rig
        self.saildata = saildata

    def save_profile(self):
        """
        Saves the yacht profile in microservice.
        """
        raise NotImplementedError("Service call not implemented.")

    def save_hull(self):
        """
        Saves the yacht hull structure in microservice.
        """
        raise NotImplementedError("Service call not implemented.")

    def save_rig(self):
        """
        Saves the yacht rig configuration in microservice.
        """
        raise NotImplementedError("Service call not implemented.")

    def save_saildata(self):
        """
        Saves the yacht sail data in microservice.
        """
        raise NotImplementedError("Service call not implemented.")
