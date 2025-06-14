import unittest
from back_end.models.profile.models.yacht_profile import YachtProfile
from back_end.models.profile.models.factory import YachtProfileFactory
from back_end.models.profile.service import YachtProfileService
import os

# Example use case: Creating and saving a yacht profile with base_id
# Initialize the service (uses default DB or specify db_path)
profile_service = YachtProfileService()

# Create a new yacht profile (user yacht referencing a base yacht)
profile = YachtProfile(
    yacht_id=101,           # Unique ID for this yacht (user yacht)
    base_id=1,             # Reference to the base yacht's ID
    yacht_class="Swan 48",
    model="Oceanis",
    version="MKII",
    builder="Nautor's Swan",
    designer="Sparkman & Stephens",
    year_introduced=1985,
    production_start=1985,
    production_end=1990,
    country_of_origin="Finland",
    notes="User-customized yacht based on Swan 48 base."
)

# Save the profile
profile_service.save_profile(profile)

# Retrieve and print the profile
retrieved = profile_service.get_profile(101)
print(retrieved.__dict__ if retrieved else "Profile not found.")

# Clean up (optional)
profile_service.delete_profile(101)
profile_service.close()

class TestYachtProfileService(unittest.TestCase):
    TEST_DB = "test_yacht_profiles.db"

    def setUp(self):
        # Remove test db if exists
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)
        self.service = YachtProfileService(db_path=self.TEST_DB)

    def tearDown(self):
        self.service.close()
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    def test_save_and_get_profile_with_base_id(self):
        # Create and save a profile with base_id
        profile = YachtProfile(
            yacht_id=1,
            base_id=100,
            yacht_class="Swan 48",
            model="Oceanis",
            version="MKII",
            builder="Nautor's Swan",
            designer="Sparkman & Stephens",
            year_introduced=1985,
            production_start=1985,
            production_end=1990,
            country_of_origin="Finland",
            notes="Test yacht profile."
        )
        self.service.save_profile(profile)
        # Retrieve
        loaded = self.service.get_profile(1)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.yacht_id, 1)
        self.assertEqual(loaded.base_id, 100)
        self.assertEqual(loaded.yacht_class, "Swan 48")
        self.assertEqual(loaded.model, "Oceanis")
        self.assertEqual(loaded.version, "MKII")
        self.assertEqual(loaded.builder, "Nautor's Swan")
        self.assertEqual(loaded.designer, "Sparkman & Stephens")
        self.assertEqual(loaded.year_introduced, 1985)
        self.assertEqual(loaded.production_start, 1985)
        self.assertEqual(loaded.production_end, 1990)
        self.assertEqual(loaded.country_of_origin, "Finland")
        self.assertEqual(loaded.notes, "Test yacht profile.")

    def test_delete_profile(self):
        profile = YachtProfile(
            yacht_id=2,
            base_id=None,
            yacht_class="TestClass"
        )
        self.service.save_profile(profile)
        self.assertIsNotNone(self.service.get_profile(2))
        self.service.delete_profile(2)
        self.assertIsNone(self.service.get_profile(2))

if __name__ == "__main__":
    unittest.main()
