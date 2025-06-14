from back_end.models.yacht.models.base_yacht.base_yacht import BaseYacht

class BaseYachtFactory:
    @staticmethod
    def from_row(row, columns):
        data = dict(zip(columns, row))
        return BaseYacht(**data)

    @staticmethod
    def from_dict(data):
        return BaseYacht(**data)