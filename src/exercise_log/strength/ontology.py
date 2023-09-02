from exercise_log.strength.anatomy import MuscleGroup, Muscle
from exercise_log.strength.constants import (
    ANTAGONIST_MUSCLES,
    COMPOUND_WEIGHT,
    COUNT_TYPE,
    EXERCISE_TYPE,
    MUSCLE_GROUPS_WORKED,
    MUSCLES_WORKED,
    OPTIMAL_REP_RANGE,
    REPS,
    SECONDS,
    STEPS,
    TENSILE_FOCUS,
)
from exercise_log.strength import Exercise
from exercise_log.utils import StrEnum


COMPOUND_REP_RANGE = (3, 12)
ISOMETRIC_CALISTHENIC_REP_RANGE = (30, 120)


class TensileFocus(StrEnum):
    CONCENTRIC = "Concentric"
    ECCENTRIC = "Eccentric"
    ISOMETRIC = "Isometric"


# TODO: come back later and fill in:
#.        * set of strings of antagonist muscles for each exercise
#         * percentages for muscles/groups worked (should be as a percentage of that muscle's effort)
#         * ideal rep ranges
# This is a large data field containing metadata about the various exercises logged in this repo
EXERCISE_INFO = {
    Exercise.FIFTH_POINT_OF_FLIGHT: {
        COUNT_TYPE: SECONDS,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        OPTIMAL_REP_RANGE: ISOMETRIC_CALISTHENIC_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.ARNOLD_PRESS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BARBELL_BICEP_CURL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BARBELL_CALF_RAISE: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BARBELL_OVERHEAD_TRICEP_EXTENSION: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BENCH_PRESS: {
        COUNT_TYPE: REPS,
        EXERCISE_TYPE: COMPOUND_WEIGHT,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPOUND_REP_RANGE,
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BENT_OVER_LATERAL_LIFT: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BENT_OVER_SINGLE_ARM_BARBELL_ROW: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BICEP_CURL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.BURPEES: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CABLE_LATERAL_LIFT: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CABLE_PEC_FLIES: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CALF_RAISE: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CLEAN_AND_JERK: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CLOSE_GRIP_LAT_PULLDOWN: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.CONCENTRAION_CURL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DEADLIFT: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DEC_BENCH_PRESS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DEFICIT_PUSH_UPS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DELT_FLIES: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.DUMBBELL_PRESS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.FINGER_CURL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.FRONT_LIFT: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.FULL_CANS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.GOOD_MORNING: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.HAMMER_CURL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.HEX_BAR_DEADLIFT: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.INC_BENCH_PRESS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.INC_DUMBBELL_PRESS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.JUMPING_JACKS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.KETTLEBELL_FLIPS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LAT_PULLDOWN: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LAT_PULLDOWN_HANG: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LATERAL_LIFT: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LAWNMOWERS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_CURL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_EXTENSION: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_PRESS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_PRESS_CALF_RAISE: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LEG_RAISE: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LONG_HANG_DEADLIFT: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.LUNGES: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_BENCH_PRESS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_HIP_ABDUCTORS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_HIP_ADDUCTORS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_INCLINE_BENCH_PRESS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MACH_PEC_FLIES: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.MILITARY_PRESS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.NEUTRAL_GRIP_PULL_UP: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.OVERHEAD_TRICEP_EXTENSION: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PLANK: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PREACHER_CURL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PUSH_UPS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PUSH_UPS_PERFECT_DEVICE: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.PULLOVERS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.RES_LAT_PULLDOWN: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.RES_SEATED_ROW: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.RES_TRICEP_PUSHDOWN: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SEATED_ROW: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SEATED_ROW_WIDE_NATURAL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SIDE_LYING_EXTERNAL_ROTATION: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SIDE_PLANK: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SINGLE_ARM_FARMERS_CARRY: {
        COUNT_TYPE: STEPS,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        OPTIMAL_REP_RANGE: (40, 80),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SINGLE_LEG_LEG_CURL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SINGLE_LEG_LEG_EXTENSION: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SHRUGS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SKULLCRUSHERS: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.SQUATS: {
        COUNT_TYPE: REPS,
        EXERCISE_TYPE: COMPOUND_WEIGHT,
        TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        OPTIMAL_REP_RANGE: COMPOUND_REP_RANGE,
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
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.TRICEP_PUSHDOWN: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.UPWARD_CABLE_PEC_FLIES: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.WIDE_GRIP_PULL_UP: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.WRIST_CURL: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
    Exercise.WRIST_EXTENSION: {
        COUNT_TYPE: None,
        EXERCISE_TYPE: None,
        TENSILE_FOCUS: None,
        OPTIMAL_REP_RANGE: (None, None),
        MUSCLE_GROUPS_WORKED: {
            None: None,
        },
        MUSCLES_WORKED: {
            None: None,
        },
        ANTAGONIST_MUSCLES: None,
    },
}


# Ideal strength ratios:
# Tricep should be slightly stronger than bicep
# Hip abductors and adductors should be fairly close in strength