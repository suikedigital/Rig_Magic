from .models.yacht.models.yacht_factory import YachtFactory

class YachtService:
    def create_yacht(self, yacht_data: dict):
        """
        Create a new yacht instance based on the provided data.
        
        Args:
            yacht_data (dict): Dictionary containing yacht attributes.
        
        Returns:
            Yacht: An instance of the Yacht class.
        """
        yacht_factory = YachtFactory()

        yacht = yacht_factory.create_from_dict(yacht_data)
        return yacht