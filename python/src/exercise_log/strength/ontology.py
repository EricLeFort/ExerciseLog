from exercise_log.strength import CountType, ExerciseType, TensileFocus
from exercise_log.strength.anatomy import MuscleGroup, Muscle
from exercise_log.strength.constants import (
    ANTAGONIST_MUSCLES,
    COUNT_TYPE,
    EXERCISE_TYPE,
    MUSCLE_GROUPS_WORKED,
    MUSCLES_WORKED,
    OPTIMAL_REP_RANGE,
    REQUIRES_MACHINE,
    TENSILE_FOCUS,
)
from exercise_log.strength import Exercise
from exercise_log.utils import StrEnum


# Rep ranges for various common groups of exercise type
NERVOUS_SYSTEM_WEIGHTING = (1, 1)
EXPLOSIVE_COMPOUND_REP_RANGE = (1, 5)
COMPLEX_COMPOUND_REP_RANGE = (1, 10)
SIMPLE_COMPOUND_REP_RANGE = (5, 12)
STEP_BASED_COMPOUND_REP_RANGE = (40, 80)
UPPER_ISOLATED_REP_RANGE = (5, 15)
LOWER_ISOLATED_REP_RANGE = (8, 20)
ISOMETRIC_REP_RANGE = (30, 120)
CALI_PLYO_REP_RANGE = (5, 20)
ROTATOR_CUFF_REP_RANGE = (10, 25)


# Ideal strength ratios:
# Tricep should be slightly stronger than bicep
# Hip abductors and adductors should be fairly close in strength


class ExerciseInfo:
    """
    Stores metadata about an Exercise such as which muscles and muscle groups it works, which antagonist muscle is
    worked, and which ExerciseType it is.
    """
    def __init__(self, exercise: Exercise):
        """
        Initializes an ExerciseInfo by looking up the relevant data for the given Exercise.
        """
        info = EXERCISE_INFO[exercise]

        self.count_type = CountType[info[COUNT_TYPE]]
        self.exercise_type = ExerciseType[info[EXERCISE_TYPE]]
        self.requires_machine = info[REQUIRES_MACHINE]
        self.tensile_focus = TensileFocus[info[TENSILE_FOCUS]]
        self.optimal_rep_range = info[OPTIMAL_REP_RANGE]

        self.muscles_worked = info[MUSCLES_WORKED]
        self.muscle_groups_worked = info[MUSCLE_GROUPS_WORKED]
        self.antagonist_muscles = info[ANTAGONIST_MUSCLES]

        self._fatigue_factor = None

    def get_fatigue_factor(self):
        if self._fatigue_factor is not None:
            return self._fatigue_factor
        # TODO write logic to estimate "FATIGUE_FACTOR - The amount of systemic fatigue accumulated by the exercise. Useful for session planning."
        #      This is basically just a summation for every muscle worked dependant on 1. muscle size/energy requirement, 2. % activation of that muscle.
        pass


# TODO: come back later and fill in:
#.        * set of strings of antagonist muscles for each exercise
#         * percentages for muscles/groups worked (should be as a percentage of that muscle's effort)
# TODO: add info about the capacity of a muscle/muscle group (e.g. biceps/triceps can handle more volume than quads)

"""
This is a large data field containing metadata about the various exercises logged in this repo.

Fields:
COUNT_TYPE - The way to count this exercise. An isometric movement is measured in seconds, a compound lift in reps.
EXERCISE_TYPE - The type of exercise. E.g. compound weight lifting, calisthenics, etc.
REQUIRES_MACHINE - Whether a machine in required. Useful for knowing if an exercise can be compared across gyms.
TENSILE_FOCUS - The type of muscle contraction happening during the primary portion of the lift.
OPTIMAL_REP_RANGE - A bound of the ideal count for this exercise. They are just guiding values, not strict rules.
MUSCLE_GROUPS_WORKED - A dict from the major muscle groups worked to a % activation of that muscle group.
  e.g. biceps are involved in pec flies but their activation percentage is much lower than that of the pecs
MUSCLES_WORKED - A dict from the muscles worked to a % activation of that muscle.
ANTAGONIST_MUSCLES - A set the antagonist muscles for the movement. Useful for root causing instability issues.
"""
EXERCISE_INFO = {
    Exercise.FIFTH_POINT_OF_FLIGHT: {
        COUNT_TYPE: CountType.SECONDS,
        EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.ARNOLD_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BARBELL_BICEP_CURL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BARBELL_CALF_RAISE: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BARBELL_OVERHEAD_TRICEP_EXTENSION: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BENCH_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BENT_OVER_LATERAL_LIFT: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BENT_OVER_SINGLE_ARM_BARBELL_ROW: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BICEP_CURL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BURPEES: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.PLYOMETRIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.EXPLOSIVE,
        OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CABLE_LATERAL_LIFT: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CABLE_PEC_FLIES: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CALF_RAISE: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CLEAN_AND_JERK: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.EXPLOSIVE,
        OPTIMAL_REP_RANGE: EXPLOSIVE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CLOSE_GRIP_LAT_PULLDOWN: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CONCENTRAION_CURL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DEADLIFT: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DEC_BENCH_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DEFICIT_PUSH_UPS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DELT_FLIES: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DUMBBELL_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.FINGER_CURL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.FRONT_LIFT: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.FULL_CANS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: ROTATOR_CUFF_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.GOOD_MORNING: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.HAMMER_CURL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.HEX_BAR_DEADLIFT: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.INC_BENCH_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.INC_DUMBBELL_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.JUMPING_JACKS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.PLYOMETRIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.EXPLOSIVE,
        OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.KETTLEBELL_FLIPS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LAT_PULLDOWN: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LAT_PULLDOWN_HANG: {
        COUNT_TYPE: CountType.SECONDS,
        EXERCISE_TYPE: ExerciseType.WEIGHTED_COMPOUND_ISOMETRIC,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LAT_PUSHDOWN: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },Exercise.LATERAL_LIFT: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LAWNMOWERS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_CURL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_EXTENSION: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_PRESS_CALF_RAISE: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_RAISE: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LONG_HANG_DEADLIFT: {
        COUNT_TYPE: CountType.SECONDS,
        EXERCISE_TYPE: ExerciseType.WEIGHTED_COMPOUND_ISOMETRIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LUNGES: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_BENCH_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_HIP_ABDUCTORS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_HIP_ADDUCTORS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_INCLINE_BENCH_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_PEC_FLIES: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MILITARY_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.NEUTRAL_GRIP_PULL_UP: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.OVERHEAD_TRICEP_EXTENSION: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PLANK: {
        COUNT_TYPE: CountType.SECONDS,
        EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PREACHER_CURL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PUSH_UPS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PUSH_UPS_PERFECT_DEVICE: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PULLOVERS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.RES_LAT_PULLDOWN: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.RES_SEATED_ROW: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.RES_TRICEP_PUSHDOWN: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SEATED_ROW: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SEATED_ROW_WIDE_NATURAL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SIDE_LYING_EXTERNAL_ROTATION: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: ROTATOR_CUFF_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SIDE_PLANK: {
        COUNT_TYPE: CountType.SECONDS,
        EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SINGLE_ARM_FARMERS_CARRY: {
        COUNT_TYPE: CountType.STEPS,
        EXERCISE_TYPE: ExerciseType.WEIGHTED_COMPOUND_ISOMETRIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        OPTIMAL_REP_RANGE: STEP_BASED_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SINGLE_LEG_LEG_CURL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SINGLE_LEG_LEG_EXTENSION: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SHRUGS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SKULLCRUSHERS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SQUATS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.QUADS: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SQUAT_WALKOUT: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.WEIGHTED_COMPOUND_ISOMETRIC,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        OPTIMAL_REP_RANGE: NERVOUS_SYSTEM_WEIGHTING,
        MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.QUADS: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.STRICT_PRESS: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.TRICEP_PUSHDOWN: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.UPWARD_CABLE_PEC_FLIES: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: True,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.WIDE_GRIP_PULL_UP: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.WRIST_CURL: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.WRIST_EXTENSION: {
        COUNT_TYPE: CountType.REPS,
        EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        REQUIRES_MACHINE: False,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
}
