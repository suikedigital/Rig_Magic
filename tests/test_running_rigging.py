"""
Test suite for the Running Rigging Management system.
Covers rope/rigging instantiation, port/starboard logic for sheets and guys, and config overrides.
"""
import pytest
from models.yacht.yacht import Yacht
from models.ropes_rigging.components.termination import Termination
from models.registry.rope_registry import ROPE_REGISTRY

@pytest.fixture
def yacht():
    # Minimal yacht for testing
    return Yacht(i=20.0, j=5, p=11.0, e=3.5, boom_above_deck=1.0, boat_length=8.0)

def ensure_sails(yacht, sail_types):
    for sail_type in sail_types:
        if sail_type not in yacht.sailwardrobe.sail_types:
            yacht.sailwardrobe.add_sail_type(sail_type)
    from models.sails.sail_registry import SAIL_REGISTRY
    yacht.sailwardrobe.generate_sails(SAIL_REGISTRY)

def test_add_halyard_and_sheets_and_guys(yacht):
    # Add required sails for spinnaker halyard
    ensure_sails(yacht, ["SymSpinnaker", "AsymSpinnaker"])
    # Add a halyard and its associated sheets and guys
    yacht.running_rigging.add_rope_and_sheet("SpinnakerHalyard", led_aft=2.0)
    # Should add SpinnakerHalyard, SymSpinSheet_Port, SymSpinSheet_Starboard, AsymSpinSheet_Port, AsymSpinSheet_Starboard, SymSpinGuy_Port, SymSpinGuy_Starboard
    expected = [
        "SpinnakerHalyard",
        "SymSpinSheet_Port", "SymSpinSheet_Starboard",
        "AsymSpinSheet_Port", "AsymSpinSheet_Starboard",
        "SymSpinGuy_Port", "SymSpinGuy_Starboard"
    ]
    for rope in expected:
        assert rope in yacht.running_rigging.rope_types

    yacht.running_rigging.generate_ropes(ROPE_REGISTRY)
    for rope in expected:
        assert rope in yacht.running_rigging.ropes
        # Check side attribute for sheets and guys
        if "_Port" in rope or "_Starboard" in rope:
            assert getattr(yacht.running_rigging.ropes[rope], "side") in ("Port", "Starboard")

def test_config_override(yacht):
    ensure_sails(yacht, ["Genoa"])
    yacht.running_rigging.add_rope_and_sheet("GenoaHalyard", led_aft=1.0)
    yacht.running_rigging.set_rope_config("GenoaSheet_Port", {"colour": "Red"})
    yacht.running_rigging.generate_ropes(ROPE_REGISTRY)
    sheet = yacht.running_rigging.ropes["GenoaSheet_Port"]
    assert sheet.colour == "Red"

def test_unique_instances_for_sides(yacht):
    ensure_sails(yacht, ["CodeZero"])
    yacht.running_rigging.add_rope_and_sheet("CodeZeroHalyard", led_aft=0.0)
    yacht.running_rigging.generate_ropes(ROPE_REGISTRY)
    port = yacht.running_rigging.ropes["CodeZeroSheet_Port"]
    starboard = yacht.running_rigging.ropes["CodeZeroSheet_Starboard"]
    assert port is not starboard
    assert port.side == "Port"
    assert starboard.side == "Starboard"

def test_halyard_only_addition(yacht):
    ensure_sails(yacht, ["Mainsail"])
    yacht.running_rigging.add_rope_type("MainHalyard", led_aft=0.0)
    yacht.running_rigging.generate_ropes(ROPE_REGISTRY)
    assert "MainHalyard" in yacht.running_rigging.ropes
    assert hasattr(yacht.running_rigging.ropes["MainHalyard"], "type")

def test_invalid_rope_type_raises(yacht):
    yacht.running_rigging.add_rope_type("NonexistentRope")
    with pytest.raises(KeyError):
        yacht.running_rigging.generate_ropes(ROPE_REGISTRY)

def test_trisail_halyard_addition(yacht):
    ensure_sails(yacht, ["Trisail"])
    yacht.running_rigging.add_rope_type("TrisailHalyard", led_aft=0.0)
    yacht.running_rigging.generate_ropes(ROPE_REGISTRY)
    assert "TrisailHalyard" in yacht.running_rigging.ropes
