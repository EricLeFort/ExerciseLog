import unittest

from exercise_log.strength import Exercise
from exercise_log.strength.ontology import EXERCISE_INFO, ExerciseInfo, Field


class TestOntology(unittest.TestCase):
    def test_exercise_info_is_complete(self):
        """Simple check that every field is accessible and not None"""
        for exercise in Exercise:
            try:
                info = ExerciseInfo(exercise)
            except ValueError as ve:
                self.fail(ve)
            for field in Field:
                msg = f'Expected field "{field}" in the exercise info for "{exercise}" but was None'
                self.assertIsNotNone(ExerciseInfo._get_field(exercise, field), msg)

    def test_one_to_one_relationship_from_exercise_to_exercise_info(self):
        """Checks that every Exercise has a corresponding ExerciseInfo"""
        self.assertEqual(
            len(Exercise),
            len(ExerciseInfo),
            f"There are {len(Exercise)} Exercises but {len(ExerciseInfo)} ExerciseInfos, these should be equal",
        )
        for exercise in Exercise:
            self.assertIn(exercise, ExerciseInfo, f'Exercise "{exercise}" doesn\'t have a corresponding ExerciseInfo')

    def test_check_that_inherit_from_maintains_overriden_fields_using_barbell_bicep_curl(self):
        """Verifies the INHERITS_FROM logic on BARBELL_BICEP_CURL"""
        try:
            barbell_curls = ExerciseInfo(Exercise.BARBELL_BICEP_CURL)
        except ValueError as ve:
            self.fail(ve)
        curls = EXERCISE_INFO[Exercise.BICEP_CURL]

        # All fields should be identical except for Field.IS_UNILATERAL and Field.IS_LIMB_INDEPENDENT
        for field, value in curls.items():
            result = barbell_curls._get_field(Exercise.BARBELL_BICEP_CURL, field)
            if field in {Field.IS_UNILATERAL, Field.IS_LIMB_INDEPENDENT}:
                self.assertTrue(value, f'"{field}" should be True for Bicep Curl')
                self.assertFalse(result, f'"{field}" should be False for Barbell Bicep Curl')
            else:
                self.assertEqual(value, result, f'Field "{field}" differs between Bicep Curl and Barbell Bicep Curl')
