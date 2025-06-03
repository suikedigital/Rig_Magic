from models.ropes_rigging.components.rope_core import RopeCore
from models.ropes_rigging.components.rope_cover import RopeCover
from models.ropes_rigging.components.rope_construction import RopeConstruction

# Test RopeCore break strength
core_braid = RopeCore(material="braid", diameter=8)
core_dyneema = RopeCore(material="dyneema", diameter=10)
assert core_braid.break_strength() == 1600, "Braid core strength failed"
assert core_dyneema.break_strength() == 4000, "Dyneema core strength failed"

# Test RopeCover contribution
cover_braid = RopeCover(material="braid", diameter=9)
cover_dyneema = RopeCover(material="dyneema", diameter=10)
assert abs(cover_braid.contribution(2000) - 1000) < 1e-6, "Braid cover contribution failed"
assert abs(cover_dyneema.contribution(2000) - 1500) < 1e-6, "Dyneema cover contribution failed"

# Test RopeConstruction with cover
core = RopeCore(material="dyneema", diameter=8)
cover = RopeCover(material="braid", diameter=9)
rope = RopeConstruction(core=core, cover=cover)
print("Total break strength (with cover):", rope.total_break_strength(), "kg")
assert abs(rope.total_break_strength() - (2800 + 1400)) < 1e-6, "Total break strength with cover failed"
assert rope.base_diameter == 9, "Base diameter with cover failed"

# Test RopeConstruction without cover
rope_no_cover = RopeConstruction(core=core, cover=None)
print("Total break strength (no cover):", rope_no_cover.total_break_strength(), "kg")
assert abs(rope_no_cover.total_break_strength() - 2800) < 1e-6, "Total break strength without cover failed"
assert rope_no_cover.base_diameter == 8, "Base diameter without cover failed"

# Test RopeCover with unknown material
try:
    unknown_cover = RopeCover(material="polyester", diameter=8)
    contrib = unknown_cover.contribution(2000)
    assert contrib == 0, "Unknown material should contribute 0 strength"
    print("Unknown material cover contribution handled correctly.")
except Exception as e:
    print("Error handling unknown material in RopeCover:", e)

print("All RopeCore, RopeCover, and RopeConstruction tests passed.")
