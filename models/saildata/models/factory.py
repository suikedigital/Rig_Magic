from models.saildata.models.saildata import SailData

class SailDataFactory:
    """
    Factory for creating SailData objects for a given yacht_id and parameters.
    """
    @staticmethod
    def create(yacht_id, i, j, p, e, **kwargs):
        return SailData(yacht_id, i, j, p, e, **kwargs)

    @staticmethod
    def from_dict(yacht_id, data: dict):
        return SailData(
            yacht_id=yacht_id,
            i=data.get("i"),
            j=data.get("j"),
            p=data.get("p"),
            e=data.get("e"),
            **{k: v for k, v in data.items() if k not in ["yacht_id", "i", "j", "p", "e"]}
        )
