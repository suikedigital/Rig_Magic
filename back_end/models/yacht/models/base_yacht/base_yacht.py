
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
        return Services().profile_service.save_profile(self.base_id, self.profile)
    
    def save_hull(self):
        """
        Saves the yacht hull structure in microservice.
        """
        return Services().hull_service.save_hull(self.base_id, self.hull)
    
    def save_rig(self):
        """
        Saves the yacht rig configuration in microservice.
        """
        return Services().rig_service.save_rig(self.base_id, self.rig)
    
    def save_saildata(self):
        """
        Saves the yacht sail data in microservice.
        """
        return Services().saildata.save_saildata(self.base_id, self.saildata)
