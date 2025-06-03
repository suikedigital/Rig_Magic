# we are going to need every variable of the yacht, so that the baseyacht is as acurate as possible.

class BaseYacht:
    def __init__(
        self,
        # Profile/metadata
        yacht_class=None, model=None, version=None, builder=None, designer=None,
        year_introduced=None, production_start=None, production_end=None, country_of_origin=None, notes=None,
        # Hull
        hull_type=None, loa=None, lwl=None, beam=None, draft=None, displacement=None, ballast=None, construction=None,
        # Keel
        keel_type=None, keel_draft=None,
        # Rudder
        rudder_type=None,
        # Rig
        rig_type=None, boom_above_deck=None,
        # SailData (main, jib, genoa, spinnaker, code zero, staysail, trisail, etc.)
        i=None, j=None, p=None, e=None,
        genoa_i=None, genoa_j=None, main_p=None, main_e=None,
        codezero_i=None, codezero_j=None, jib_i=None, jib_j=None,
        spin_i=None, spin_j=None, staysail_i=None, staysail_j=None, trisail_i=None, trisail_j=None,
        # Settings
        wind_speed_in_knots=None, length_safety_factor=None, halyard_load_safety_factor=None, dynamic_load_safety_factor=None,
        # Sails (common fields)
        mainsail_luff=None, mainsail_leech=None, mainsail_foot=None, mainsail_area=None,
        jib_luff=None, jib_leech=None, jib_foot=None, jib_area=None,
        genoa_luff=None, genoa_leech=None, genoa_foot=None, genoa_area=None, genoa_overlap_percent=None,
        # Add more sail types as needed
        **kwargs
    ):
        # Profile
        self.yacht_class = yacht_class
        self.model = model
        self.version = version
        self.builder = builder
        self.designer = designer
        self.year_introduced = year_introduced
        self.production_start = production_start
        self.production_end = production_end
        self.country_of_origin = country_of_origin
        self.notes = notes
        # Hull
        self.hull_type = hull_type
        self.loa = loa
        self.lwl = lwl
        self.beam = beam
        self.draft = draft
        self.displacement = displacement
        self.ballast = ballast
        self.construction = construction
        # Keel
        self.keel_type = keel_type
        self.keel_draft = keel_draft
        # Rudder
        self.rudder_type = rudder_type
        # Rig
        self.rig_type = rig_type
        self.boom_above_deck = boom_above_deck
        # SailData
        self.i = i
        self.j = j
        self.p = p
        self.e = e
        self.genoa_i = genoa_i
        self.genoa_j = genoa_j
        self.main_p = main_p
        self.main_e = main_e
        self.codezero_i = codezero_i
        self.codezero_j = codezero_j
        self.jib_i = jib_i
        self.jib_j = jib_j
        self.spin_i = spin_i
        self.spin_j = spin_j
        self.staysail_i = staysail_i
        self.staysail_j = staysail_j
        self.trisail_i = trisail_i
        self.trisail_j = trisail_j
        # Settings
        self.wind_speed_in_knots = wind_speed_in_knots
        self.length_safety_factor = length_safety_factor
        self.halyard_load_safety_factor = halyard_load_safety_factor
        self.dynamic_load_safety_factor = dynamic_load_safety_factor
        # Sails (examples, expand as needed)
        self.mainsail_luff = mainsail_luff
        self.mainsail_leech = mainsail_leech
        self.mainsail_foot = mainsail_foot
        self.mainsail_area = mainsail_area
        self.jib_luff = jib_luff
        self.jib_leech = jib_leech
        self.jib_foot = jib_foot
        self.jib_area = jib_area
        self.genoa_luff = genoa_luff
        self.genoa_leech = genoa_leech
        self.genoa_foot = genoa_foot
        self.genoa_area = genoa_area
        self.genoa_overlap_percent = genoa_overlap_percent
        # Any additional/unknown fields
        for k, v in kwargs.items():
            setattr(self, k, v)
