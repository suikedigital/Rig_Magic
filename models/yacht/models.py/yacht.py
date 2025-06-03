"""
Yacht module
------------
This module defines the Yacht class, representing a yacht and its key properties for running rigging and sail calculations.

The Yacht class encapsulates yacht dimensions, rig type, hull, profile, and provides access to running rigging and sail wardrobe systems.

Classes:
    Yacht: Represents a yacht with rigging, hull, profile, and sail wardrobe.
"""

from .saildata import SailData
from .. import running_rigging
from models.sails.sail_service import SailService
from .. import mainsheetsystem
from .hulls.base import BaseHull
from .yacht_profile import YachtProfile


class Yacht:
    """
    Represents a yacht and its key properties for running rigging and sail calculations.

    Attributes:
        hull (BaseHull): The hull object (monohull, catamaran, etc).
        rig_type (str): Type of rig (e.g., sloop, cutter).
        profile (YachtProfile): Yacht profile (designer, model, etc).
        saildata (SailData): Sail and rigging dimensions.
        running_rigging (RunningRigging): Running rigging system.
        sail_wardrobe (SailWardrobe): Sail wardrobe system.
        mainsheet_system (MainsheetSystem): Mainsheet system.
        wind_speed_knots (float): Default wind speed for calculations.
    """

    def __init__(self, yacht_id, hull: BaseHull, rig_type: str, profile: YachtProfile, saildata: SailData):
        self.yacht_id = yacht_id
        self.profile = profile

        self.hull = hull

        self.rig_type = rig_type
        self.saildata = saildata

        self.running_rigging = running_rigging.RunningRigging(self)
        self.sail_service = SailService(saildata.to_dict())
        self.mainsheet_system = mainsheetsystem.MainsheetSystem(purchase_ratio=6, routing="traditional")
        self.wind_speed_knots = 35.0

    def describe(self):
        return {
            "hull": type(self.hull).__name__,
            "rig_type": self.rig_type,
            "profile": self.profile.__dict__,
            "saildata": self.saildata.__dict__,
        }
