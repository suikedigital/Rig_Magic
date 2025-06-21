from src.database import find_furlex_part, find_furlex_link_plate

class Furlex:
    def __init__(self, unit_name, stay_diameter, rod_diameter=None, stay_length=None):
        self.unit_name = unit_name
        self.stay_diameter = stay_diameter
        self.rod_diameter = rod_diameter
        self.stay_length = stay_length
        self.part_numbers = []
        self.link_plate = self.get_link_plate()

        # Use the database to select the part numbers
        if stay_length is not None:
            part_info = find_furlex_part(unit_name, stay_diameter, stay_length)
        else:
            # If no stay_length given, use the shortest available
            part_info = find_furlex_part(unit_name, stay_diameter, 0)
        if part_info:
            self.stay_length = part_info['stay_length']
            self.part_numbers = [
                part_info['sta_lok_part_number'],
                part_info['rigging_screw_part_number'],
                part_info['stud_terminal_part_number']
            ]

    def __repr__(self):
        return (f"<Furlex {self.unit_name}, Stay Diameter: {self.stay_diameter}, "
                f"Stay Length: {self.stay_length}, Part Numbers: [StaLok Eye: {self.part_numbers[0]}, Riggingscrew: {self.part_numbers[1]}, Stud Terminal: {self.part_numbers[2]}],"
                f"Link Plate (if required): {self.link_plate}>")
        
    def select_terminal(self, terminal_type):
        """
        Selects the appropriate terminal part number based on the terminal type.
        Terminal types can be 'Stalok', 'Riggingscrew', or 'Stud Terminal'.
        """
        if terminal_type not in ['Stalok', 'Riggingscrew', 'Stud Terminal']:
            raise ValueError("Invalid terminal type. Choose from 'Stalok', 'Riggingscrew', or 'Stud Terminal'.")
        for part_number in self.part_numbers:
            if terminal_type == 'Stalok':
                return self.part_numbers[0]
            elif terminal_type == 'Riggingscrew':
                return self.part_numbers[1]
            elif terminal_type == 'Stud Terminal':
                return self.part_numbers[2] 
        return None
    
    def get_link_plate(self):
        """
        Returns the link plate part number for the current furler model.
        """
        return find_furlex_link_plate(self.stay_diameter)
