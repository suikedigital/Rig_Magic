from .yacht_profile import YachtProfile


class YachtProfileFactory:

    @staticmethod
    def from_row(row, columns):
        data = dict(zip(columns, row))
        # Ensure 'name' and 'spec' are present (nullable)
        if 'name' not in data:
            data['name'] = None
        if 'spec' not in data:
            data['spec'] = None
        return YachtProfile(**data)

    @staticmethod
    def from_dict(data):
        # Ensure 'name' and 'spec' are present (nullable)
        if 'name' not in data:
            data['name'] = None
        if 'spec' not in data:
            data['spec'] = None
        return YachtProfile(**data)
