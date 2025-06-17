"""
SailData class for the Running Rigging Management system.

Stores all relevant sail and rigging dimensions for a yacht, including main, jib, genoa,
spinnaker, code zero, staysail, and trisail measurements. Allows for easy extension and
overriding of values via keyword arguments.
"""

from back_end.logger import get_logger

logger = get_logger(__name__)


class SailData:
    def __init__(self, yacht_id, i, j, p, e, base_id=None, **kwargs):
        """
        Represents the sail data for a yacht.

        Parameters:
            i (float): Height of the forestay (I).
            j (float): Base of the foretriangle (J).
            p (float): Height of the mainsail luff (P).
            e (float): Foot of the mainsail (E).
            yacht_id (str): Unique identifier for the yacht.
            base_id (str): Identifier for the base yacht, if different from the user yacht.
            kwargs: Any sail data value which can and should be overridden.
        """
        # Main attributes
        self.yacht_id = yacht_id
        self.base_id = base_id
        self.i = i
        self.j = j
        self.p = p
        self.e = e
        self.genoa_i = kwargs.get("genoa_i", i)
        self.genoa_j = kwargs.get("genoa_j", j)
        self.main_p = kwargs.get("main_p", p)
        self.main_e = kwargs.get("main_e", e)
        self.codezero_i = kwargs.get("codezero_i", i)
        self.codezero_j = kwargs.get("codezero_j", j)
        self.jib_i = kwargs.get("jib_i", i)
        self.jib_j = kwargs.get("jib_j", j)
        self.spin_i = kwargs.get("spin_i", i)
        self.spin_j = kwargs.get("spin_j", j)
        self.staysail_i = kwargs.get("staysail_i", i)
        self.staysail_j = kwargs.get("staysail_j", j)
        self.trisail_i = kwargs.get("trisail_i", i)
        self.trisail_j = kwargs.get("trisail_j", j)

        # Any other extras as attributes (lowercased for consistency)
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)

    def to_dict(self):
        d = self.__dict__.copy()
        return d

    def strip_base_keys(self):
        # Remove base keys from the dictionary
        base_keys = {"yacht_id", "i", "j", "p", "e"}
        return {k: v for k, v in self.to_dict().items() if k not in base_keys}

    @classmethod
    def from_dict(cls, data: dict):
        # Extract required args, pass the rest as kwargs
        yacht_id = data.get("yacht_id")
        i = data.get("i")
        j = data.get("j")
        p = data.get("p")
        e = data.get("e")
        base_keys = {"yacht_id", "i", "j", "p", "e", }
        kwargs = {k: v for k, v in data.items() if k not in base_keys}
        return cls(yacht_id, i, j, p, e, **kwargs)

    def __str__(self):
        return f"SailData(yacht_id={self.yacht_id}, i={self.i}, j={self.j}, p={self.p}, e={self.e} kwargs={self.strip_base_keys()})"


if __name__ == "__main__":
    # Example usage
    sail_data = SailData(
        yacht_id=1,
        i=10,
        j=5,
        p=15,
        e=7,
        codezero_i=12,
        jib_i=8,
        jib_j=4
    )
    print(sail_data.to_dict())