import unittest

from exercise_log.strength.anatomy import Muscle, MuscleGroup

EXPECTED_MUSCLE_COUNT = 86
EXPECTED_MUSCLE_GROUP_COUNT = 20


class TestOntology(unittest.TestCase):
    def test_enums_are_complete(self) -> None:
        """Simple check that the expected number of values are present in the enums used by this module."""
        msg = f'Expected "{EXPECTED_MUSCLE_GROUP_COUNT}" values in the MuscleGroup enum but was "{len(MuscleGroup)}".'
        self.assertEqual(EXPECTED_MUSCLE_GROUP_COUNT, len(MuscleGroup), msg)
        msg = f'Expected "{EXPECTED_MUSCLE_COUNT}" values in the Muscle enum but was "{len(Muscle)}".'
        self.assertEqual(EXPECTED_MUSCLE_COUNT, len(Muscle), msg)
