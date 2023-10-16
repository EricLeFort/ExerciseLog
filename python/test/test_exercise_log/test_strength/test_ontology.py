import unittest

from exercise_log.strength import Exercise
from exercise_log.strength.ontology import ExerciseInfo, Field, EXERCISE_INFO

class TestOntology(unittest.TestCase):
    def test_exercise_info_is_complete(self):
        """Simple check that every field is populated in EXERCISE_INFO"""
        for exercise in Exercise:
            for field in Field:
                if field not in EXERCISE_INFO[exercise]:
                    self.fail(f'Expected field "{field}" in the exercise info for "{exercise}" but was missing')

    def test_one_to_one_relationship_from_exercise_to_exercise_info(self):
        """Checks that every Exercise has a corresponding ExerciseInfo"""
        self.assertEqual(
            len(Exercise),
            len(ExerciseInfo),
            "There are {} Exercises but {} ExerciseInfos, these should be equal",
        )
        for exercise in Exercise:
            self.assertIn(exercise, ExerciseInfo, f'Exercise "{exercise}" doesn\'t have a corresponding ExerciseInfo')

    def test_check_that_inherit_from_maintains_overriden_fields_using_barbell_bicep_curl(self):
        """Verifies the INHERITS_FROM logic on BARBELL_BICEP_CURL"""
        barbell_curls = EXERCISE_INFO[Exercise.BARBELL_BICEP_CURL]
        curls = EXERCISE_INFO[Exercise.BICEP_CURL]

        # All fields should be identical except for Field.IS_UNILATERAL and Field.IS_LIMB_INDEPENDENT
        for field, value in curls.items():
            self.assertIn(field, barbell_curls, f'Field "{field}" missing from Barbell Bicep Curl')
            if field in {Field.IS_UNILATERAL, Field.IS_LIMB_INDEPENDENT}:
                self.assertTrue(value, f'"{field}" should be True for Bicep Curl')
                self.assertFalse(barbell_curls[field], f'"{field}" should be False for Barbell Bicep Curl')
            else:
                self.assertEqual(
                    value,
                    barbell_curls[field],
                    f'Field "{field}" differs between Bicep Curl and Barbell Bicep Curl'
                )
