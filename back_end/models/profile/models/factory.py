from back_end.models.profile.models.yacht_profile import YachtProfile

class YachtProfileFactory:
    @staticmethod
    def from_row(row, columns):
        data = dict(zip(columns, row))
        return YachtProfile(**data)

    @staticmethod
    def from_dict(data):
        return YachtProfile(**data)