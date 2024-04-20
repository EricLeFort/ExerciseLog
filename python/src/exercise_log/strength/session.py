from enum import Enum
from typing import Optional

from exercise_log.strength import Exercise, SetRating
from exercise_log.strength.anatomy import MuscleGroup

BICEPS = {MuscleGroup.BICEPS}
TRICEPS = {MuscleGroup.TRICEPS}
ARMS = {MuscleGroup.BICEPS, MuscleGroup.TRICEPS}
BACK = {MuscleGroup.LATS, MuscleGroup.TRAPS, MuscleGroup.RHOMBOIDS, MuscleGroup.SERRATUS}
CHEST = {MuscleGroup.PECS}
CORE = {MuscleGroup.ABS, MuscleGroup.SPINAL_ERECTORS}
LEGS = {
    MuscleGroup.CALVES,
    MuscleGroup.GLUTES,
    MuscleGroup.HAMSTRINGS,
    MuscleGroup.QUADS,
    MuscleGroup.HIP_ABDUCTORS,
    MuscleGroup.HIP_ADDUCTORS,
    MuscleGroup.HIP_FLEXORS,
}
SHOULDERS = {MuscleGroup.DELTS, MuscleGroup.ROTATOR_CUFF}
FOREARMS = {MuscleGroup.FOREARMS}


class SessionFocus(Enum):
    PUSH = TRICEPS.union(CHEST).union(SHOULDERS)
    PULL = BICEPS.union(BACK).union(FOREARMS)
    UPPER = ARMS.union(BACK).union(CHEST).union(CORE).union(SHOULDERS)
    LOWER = LEGS
    FULL_BODY = ARMS.union(BACK).union(CHEST).union(CORE).union(SHOULDERS).union(LEGS)


class ExerciseSet:
    """Stores info about a single set in a Session."""

    def __init__(self, target_count: int, target_weight: float) -> None:
        self.target_count = target_count
        self.target_weight = target_weight

        self._fatigue_score = None

    def get_fatigue_score(self) -> float:
        if self._fatigue_score is not None:
            return self._fatigue_score
        # TODO(eric): compute the fatigue score
        raise NotImplementedError


class Result:
    """Stores info about the result of an ExerciseSet."""

    def __init__(self, count: Optional[int], weight: Optional[float], set_rating: SetRating):
        self.count = count
        self.weight = weight
        self.set_rating = set_rating


class SkippedResult(Result):
    """A special case of Result where the rating is SKIPPED and the counts/weight are None."""

    def __init__(self) -> None:
        super().__init__(None, None, SetRating.SKIPPED)


class SessionInfo:
    def __init__(self, focus: list[MuscleGroup], exercise_sets: dict[str, list[ExerciseSet]]) -> None:
        self.focus = focus

        self.fatigue_score = sum(exercise_set.get_fatigue_score() for exercise, exercise_set in exercise_sets.items())
        # TODO(eric): this will store/compute info about a Session (volume per muscle/muscle group, fatigue score)
        raise NotImplementedError


class Session:
    def __init__(self, focus: SessionFocus) -> None:
        self.focus = focus
        self.sets = {}
        self.results = {}
        self._session_info = SessionInfo(self.focus, self.sets)

    def get_fatigue_score(self) -> float:
        return self._session_info.fatigue_score

    def add_set(self, exercise_set: ExerciseSet) -> None:
        self.sets[exercise_set.exercise] = [*self.sets.get(exercise_set.exercise, []), exercise_set]
        self.results[exercise_set.exercise] = []
        self._session_info = SessionInfo(self.focus, self.sets)

    def add_result(self, exercise: Exercise, result: Result) -> None:
        self.results[exercise] = [*self.results.get(exercise, []), result]

    def complete_session(self) -> None:
        for exercise, sets in self.sets.items():
            # This re-uses the SkippedResult instance but that's fine; it technically could be a singleton anyway
            # It also assumes the exercise has been added to the results dict (which is handled by add_exercise())
            self.results[exercise] += [SkippedResult()] * (len(sets) - len(self.results[exercise]))
        # TODO(eric): save the actual fatigue score (e.g. if more/less reps were hit, or if sets were added/skipped)
        # TODO(eric): save these results somewhere, somehow
