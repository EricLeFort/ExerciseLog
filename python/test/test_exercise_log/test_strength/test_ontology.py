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
        self.assertEqual(
            len(Exercise),
            len(ExerciseInfo),
            "There are {} Exercises but {} ExerciseInfos, these should be equal",
        )
        for exercise in Exercise:
            self.assertIn(exercise, ExerciseInfo, f'Exercise "{exercise}" doesn\'t have a corresponding ExerciseInfo')
