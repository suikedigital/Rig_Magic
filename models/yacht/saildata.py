"""
SailData class for the Running Rigging Management system.

Stores all relevant sail and rigging dimensions for a yacht, including main, jib, genoa,
spinnaker, code zero, staysail, and trisail measurements. Allows for easy extension and
overriding of values via keyword arguments.
"""

class SailData:
    def __init__(self, i, j, p, e, **kwargs):
        """
        Represents the sail data for a yacht.

        Parameters:
            i (float): Height of the forestay (I).
            j (float): Base of the foretriangle (J).
            p (float): Height of the mainsail luff (P).
            e (float): Foot of the mainsail (E).
            kwargs: Any sail data value which can and should be overridden.
        """
        # Main attributes
        self.genoa_i = i
        self.genoa_j = j
        self.main_p = p
        self.main_e = e
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