"""
Contains logic related to three major domains:
    1. Loading ontological data relating to strength (e.g. anatomical data, information about exercises, etc.)
    2. Providing a framework to structure strength-training workouts.
    3. Providing a framework to analyze strength progression over time.
"""

from exercise_log.constants import ROOT_ONTOLOGY_DIR
from exercise_log.utils import StrEnum

# Dynamically create these enums using a shared definition
enum_base_dir = f"{ROOT_ONTOLOGY_DIR}/enum/strength"
Exercise = StrEnum.create_from_json(f"{enum_base_dir}/exercise.json", __name__)
ExerciseType = StrEnum.create_from_json(f"{enum_base_dir}/exercise_type.json", __name__)
CardioType = StrEnum.create_from_json(f"{enum_base_dir}/cardio_type.json", __name__)
CountType = StrEnum.create_from_json(f"{enum_base_dir}/count_type.json", __name__)
TensileFocus = StrEnum.create_from_json(f"{enum_base_dir}/tensile_focus.json", __name__)
SetRating = StrEnum.create_from_json(f"{enum_base_dir}/set_rating.json", __name__)
SetType = StrEnum.create_from_json(f"{enum_base_dir}/set_type.json", __name__)

# TODO(eric): ideally a simple lookup like this can be handled as part of the StrEnum generation
SetType.get_rep_range = lambda self: SET_TYPE_TO_REP_RANGE[self]

# TODO(eric): ONE_RM should be 1 and there should instead be logic to rectify results at the scope of an entire workout
SET_TYPE_TO_REP_RANGE = {
    SetType.ONE_RM: (1, 2),  # Include the 2-rep for when you hit 2 at a lower weight and then fail at the next weight
    SetType.STRENGTH: (3, 7),
    SetType.HYPERTROPHY: (8, 14),
    SetType.ENDURANCE: (15, float("inf")),
}
