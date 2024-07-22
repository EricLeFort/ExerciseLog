import unittest

from exercise_log.strength import (
    CardioType,
    CountType,
    Exercise,
    ExerciseType,
    SetRating,
    SetType,
    TensileFocus,
)

EXPECTED_CARDIO_TYPE_COUNT = 4
EXPECTED_COUNT_TYPE_COUNT = 3
EXPECTED_EXERCISE_COUNT = 91
EXPECTED_EXERCISE_TYPE_COUNT = 7
EXPECTED_SET_RATING_COUNT = 11
EXPECTED_SET_TYPE_COUNT = 4
EXPECTED_TENSILE_FOCUS_COUNT = 4


class TestStrength(unittest.TestCase):
    def test_enums_are_complete(self) -> None:
        """Simple check that the expected number of values are present in the enums used by this module."""
        msg = f'Expected "{EXPECTED_CARDIO_TYPE_COUNT}" values in the CardioType but was "{len(CardioType)}".'
        self.assertEqual(EXPECTED_CARDIO_TYPE_COUNT, len(CardioType), msg)
        msg = f'Expected "{EXPECTED_COUNT_TYPE_COUNT}" values in the CountType but was "{len(CountType)}".'
        self.assertEqual(EXPECTED_COUNT_TYPE_COUNT, len(CountType), msg)
        msg = f'Expected "{EXPECTED_EXERCISE_COUNT}" values in the Exercise but was "{len(Exercise)}".'
        self.assertEqual(EXPECTED_EXERCISE_COUNT, len(Exercise), msg)
        msg = f'Expected "{EXPECTED_EXERCISE_TYPE_COUNT}" values in the ExerciseType but was "{len(ExerciseType)}".'
        self.assertEqual(EXPECTED_EXERCISE_TYPE_COUNT, len(ExerciseType), msg)
        msg = f'Expected "{EXPECTED_SET_RATING_COUNT}" values in the SetRating but was "{len(SetRating)}".'
        self.assertEqual(EXPECTED_SET_RATING_COUNT, len(SetRating), msg)
        msg = f'Expected "{EXPECTED_SET_TYPE_COUNT}" values in the SetType but was "{len(SetType)}".'
        self.assertEqual(EXPECTED_SET_TYPE_COUNT, len(SetType), msg)
        msg = f'Expected "{EXPECTED_TENSILE_FOCUS_COUNT}" values in the TensileFocus but was "{len(TensileFocus)}".'
        self.assertEqual(EXPECTED_TENSILE_FOCUS_COUNT, len(TensileFocus), msg)
