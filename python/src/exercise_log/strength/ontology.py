from exercise_log.strength import CountType, ExerciseType, TensileFocus
from exercise_log.strength.anatomy import MuscleGroup, Muscle
from exercise_log.strength.constants import INHERITS_FROM
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
# Tricep:bicep
#    * low range: maybe 3:4 (elbow injury study in baseball players pubmed.ncbi.nlm.nih.gov/20231742)
#    * upper range: not known but let's assume the inverse, 4:3
#    * ideal: somewhere around 1:1
# Hamstring:Quads
#    * low range: 1:2
#    * upper range: 1:1 (or even higher maybe? Not really mentioned)
#    * ideal: >= 3:5
#    * This is a lot more studied than bicep:triceps or hip abd:hip add
#    * Measurements include rate of motion (i.e. degrees per second) -- faster favours the hamstrings relatively
# Trunk Flexion:Extension
#    * low range: 1:2?
#    * upper range: 7:10?
#    * ideal: 3:5 www.ncbi.nlm.nih.gov/pmc/articles/PMC5833971/
# Hip abductors and adductors should be fairly close in strength (note: soccer players tend to have more strength on their dominant leg)
#    * low range: 4:5, not clear there is one but let's assume the inverse
#    * upper range: 5:4 seems likely (journals.humankinetics.com/view/journals/jsr/29/1/article-p116.xml + journals.sagepub.com/doi/10.1177/0363546510378081)
#    * ideal: somewhere around 1:1
# Hip Flexor:Extensor
#    * Nominal typical range: 11:20 to 3:4 (www.ncbi.nlm.nih.gov/pmc/articles/PMC7727414/pdf/ijspt-15-967.pdf)
#    * low range: 1:2?
#    * upper range: 3:4?
#    * ideal: 11:20?
# Hip Internal(medial):External(lateral) Rotation
#    * low range: 10:11?, not clear there is one but let's assume the inverse
#    * upper range: 11:10?, more may lead to PFPS injuries (web.archive.org/web/20190308153356id_/http://pdfs.semanticscholar.org/f531/d7163d65c82a5301e505affe72c5c9ca8b7a.pdf)
#    * ideal: 1:1


INHERITS_FROM = "Inherits From"


class Field(StrEnum):
    """
    Enumerates over the fields present in an ExerciseInfo.

    COUNT_TYPE - The way to count this exercise. An isometric movement is measured in seconds, a compound lift in reps.
    EXERCISE_TYPE - The type of exercise. E.g. compound weight lifting, calisthenics, etc.
    IS_UNILATERAL - Whether the exercise uses a single limb at a time. E.g. alternating bicep curls, single-leg leg curls
    IS_LIMB_INDEPENDENT - Whether the exercise works limbs independently. E.g. cable flies are bilateral + limb independent
    REQUIRES_MACHINE - Whether a machine in required. Useful for knowing if an exercise can be compared across gyms.
    TENSILE_FOCUS - The type of muscle contraction happening during the primary portion of the lift.
    OPTIMAL_REP_RANGE - A bound of the ideal count for this exercise. They are just guiding values, not strict rules.
    MUSCLE_GROUPS_WORKED - A dict from the major muscle groups worked to a % activation of that muscle group.
      e.g. biceps are involved in pec flies but their activation percentage is much lower than that of the pecs
    MUSCLES_WORKED - A dict from the muscles worked to a % activation of that muscle.
    ANTAGONIST_MUSCLES - A set the antagonist muscles for the movement. Useful for root causing instability issues.
    """
    ANTAGONIST_MUSCLES = "Antagonist Muscles"
    COUNT_TYPE = "Count Type"
    EXERCISE_TYPE = "Excercise Type"
    IS_LIMB_INDEPENDENT = "Is Limb Independent"
    IS_UNILATERAL = "Is Unilateral"
    MUSCLE_GROUPS_WORKED = "Muscle Groups Worked"
    MUSCLES_WORKED = "Muscles Worked"
    OPTIMAL_REP_RANGE = "Optimal Rep Range"
    REQUIRES_MACHINE = "Requires Machine"
    TENSILE_FOCUS = "Tensile Focus"


class ExerciseInfoMeta(type):
    def __len__(cls):
        return len(EXERCISE_INFO)

    def __contains__(self, item):
        return item in EXERCISE_INFO


# TODO this should really be a parameterized singleton
class ExerciseInfo(metaclass=ExerciseInfoMeta):
    """
    Stores metadata about an Exercise such as which muscles and muscle groups it works, which antagonist muscle is
    worked, and which ExerciseType it is.

    Supports inheritance amongst data in related exercises. E.g. CONCENTRATION_CURL -> PREACHER_CURL -> BICEP_CURL
    """
    def __init__(self, exercise: Exercise):
        """
        Initializes an ExerciseInfo by looking up the relevant data for the given Exercise.
        """
        info = EXERCISE_INFO[exercise]

        self.count_type = CountType[ExerciseInfo._get_field(exercise, Field.COUNT_TYPE)]
        self.exercise_type = ExerciseType[ExerciseInfo._get_field(exercise, Field.EXERCISE_TYPE)]
        self.requires_machine = ExerciseInfo._get_field(exercise, Field.REQUIRES_MACHINE)
        self.tensile_focus = TensileFocus[ExerciseInfo._get_field(exercise, Field.TENSILE_FOCUS)]
        self.optimal_rep_range = ExerciseInfo._get_field(exercise, Field.OPTIMAL_REP_RANGE)

        self.muscles_worked = ExerciseInfo._get_field(exercise, Field.MUSCLES_WORKED)
        self.muscle_groups_worked = ExerciseInfo._get_field(exercise, Field.MUSCLE_GROUPS_WORKED)
        self.antagonist_muscles = ExerciseInfo._get_field(exercise, Field.ANTAGONIST_MUSCLES)

        self._fatigue_factor = None


    @staticmethod
    def _get_field(exercise: str, field: Field):
        """
        Retrieves the field from this exercise's dict if it exists.
        If it doesn't exist, it works its way up the INHERITS_FROM chain until it finds it.

        Raises:
            ValueError: If the field is not present in the EXERCISE_INFO dict.
        """
        info = EXERCISE_INFO[exercise]
        result = info.get(field)
        if result is not None:
            return result
        if INHERITS_FROM not in info:
            raise ValueError(f'Unexpected error: Exercise "{exercise}" is missing field "{field}".')

        return ExerciseInfo._get_field(info[INHERITS_FROM], field)


    def get_fatigue_factor(self):
        if self._fatigue_factor is not None:
            return self._fatigue_factor
        # TODO write logic to estimate "FATIGUE_FACTOR - The amount of systemic fatigue accumulated by the exercise. Useful for session planning."
        #      This is basically just a summation for every muscle worked dependant on
        #         1. muscle size/energy requirement,
        #         2. % activation of that muscle,
        #         3. systemic fatigue (e.g. using every single muscle is more fatiguing than just the summation of the individual muscles)
        #      Slightly higher fatigue for unilateral lifts bc the systemic time under tension is longer
        #      Sessions/programs should also factor in unilateral percentages since it's the best way to avoid imbalances
        pass


# TODO: come back later and fill in:
#.        * set of strings of antagonist muscles for each exercise
#         * percentages for muscles/groups worked (should be as a percentage of that muscle's effort)
# TODO: add info about the capacity of a muscle/muscle group (e.g. biceps/triceps can handle more volume than quads)

#This is a large data field containing metadata about the various exercises logged in this repo.
EXERCISE_INFO = {
    Exercise.FIFTH_POINT_OF_FLIGHT: {
        Field.COUNT_TYPE: CountType.SECONDS,
        Field.EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        Field.OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.QUADS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.ARNOLD_PRESS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.BARBELL_BICEP_CURL: {
        INHERITS_FROM: Exercise.BICEP_CURL,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
    },
    Exercise.BARBELL_CALF_RAISE: {
        INHERITS_FROM: Exercise.CALF_RAISE,
        Field.REQUIRES_MACHINE: False,
    },
    Exercise.BARBELL_LUNGES: {
        INHERITS_FROM: Exercise.LUNGES,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.BARBELL_OVERHEAD_TRICEP_EXTENSION: {
        INHERITS_FROM: Exercise.OVERHEAD_TRICEP_EXTENSION,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
    },
    Exercise.BENCH_PRESS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.BENT_OVER_LATERAL_LIFT: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.BENT_OVER_SINGLE_ARM_BARBELL_ROW: {
        INHERITS_FROM: Exercise.LAWNMOWERS,
    },
    Exercise.BICEP_CURL: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.BURPEES: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.PLYOMETRIC,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.EXPLOSIVE,
        Field.OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.CABLE_LATERAL_LIFT: {
        INHERITS_FROM: Exercise.LATERAL_LIFT,
        Field.REQUIRES_MACHINE: True,
    },
    Exercise.CABLE_LYING_HIP_FLEXORS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.QUADS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.CABLE_PEC_FLIES: {
        INHERITS_FROM: Exercise.MACH_PEC_FLIES,
        Field.IS_LIMB_INDEPENDENT: True,
    },
    Exercise.CALF_RAISE: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.CLEAN_AND_JERK: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.EXPLOSIVE,
        Field.OPTIMAL_REP_RANGE: EXPLOSIVE_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.CLOSE_GRIP_LAT_PULLDOWN: {
        INHERITS_FROM: Exercise.LAT_PULLDOWN,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.CONCENTRATION_CURL: {
        INHERITS_FROM: Exercise.PREACHER_CURL,
    },
    Exercise.DEADLIFT: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.DEC_BENCH_PRESS: {
        INHERITS_FROM: Exercise.BENCH_PRESS,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.DEFICIT_PUSH_UPS: {
        INHERITS_FROM: Exercise.PUSH_UPS,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.DELT_FLIES: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.DUMBBELL_PRESS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.FINGER_CURL: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.FOREARMS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.FRONT_LIFT: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.FULL_CANS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: ROTATOR_CUFF_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.ROTATOR_CUFF: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.GOOD_MORNING: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.HAMMER_CURL: {
        INHERITS_FROM: Exercise.BICEP_CURL,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.HEX_BAR_DEADLIFT: {
        INHERITS_FROM: Exercise.DEADLIFT,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.INC_BENCH_PRESS: {
        INHERITS_FROM: Exercise.BENCH_PRESS,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.INC_DUMBBELL_PRESS: {
        INHERITS_FROM: Exercise.DUMBBELL_PRESS,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.JUMPING_JACKS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.PLYOMETRIC,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.EXPLOSIVE,
        Field.OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ABDUCTORS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.KETTLEBELL_FLIPS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.FOREARMS,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LAT_PULLDOWN: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LAT_PULLDOWN_HANG: {
        INHERITS_FROM: Exercise.LAT_PULLDOWN,
        Field.COUNT_TYPE: CountType.SECONDS,
        Field.EXERCISE_TYPE: ExerciseType.WEIGHTED_COMPOUND_ISOMETRIC,
        Field.TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        Field.OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LAT_PUSHDOWN: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.TRICEPS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LATERAL_LIFT: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LAWNMOWERS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LEG_CURL: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.CALVES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.HIP_FLEXORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LEG_EXTENSION: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.QUADS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LEG_PRESS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.CALVES: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ABDUCTORS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.QUADS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LEG_PRESS_CALF_RAISE: {
        INHERITS_FROM: Exercise.CALF_RAISE,
    },
    Exercise.PARALLEL_BAR_LEG_RAISE: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.HIP_ABDUCTORS: None,
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LONG_HANG_DEADLIFT: {
        INHERITS_FROM: Exercise.DEADLIFT,
        Field.COUNT_TYPE: CountType.SECONDS,
        Field.EXERCISE_TYPE: ExerciseType.WEIGHTED_COMPOUND_ISOMETRIC,
        Field.TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        Field.OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.LUNGES: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.MACH_BENCH_PRESS: {
        INHERITS_FROM: Exercise.BENCH_PRESS,
        Field.REQUIRES_MACHINE: True,
    },
    Exercise.MACH_HIP_ABDUCTORS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.HIP_ABDUCTORS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.MACH_HIP_ADDUCTORS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: LOWER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.HIP_FLEXORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.MACH_INCLINE_BENCH_PRESS: {
        INHERITS_FROM: Exercise.MACH_BENCH_PRESS,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.MACH_PEC_FLIES: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.MILITARY_PRESS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.NEUTRAL_GRIP_PULL_UP: {
        INHERITS_FROM: Exercise.WIDE_GRIP_PULL_UP,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.OVERHEAD_TRICEP_EXTENSION: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.TRICEPS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.PLANK: {
        Field.COUNT_TYPE: CountType.SECONDS,
        Field.EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        Field.OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.PECS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.PREACHER_CURL: {
        INHERITS_FROM: Exercise.BICEP_CURL,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.BICEPS: None,
            MuscleGroup.FOREARMS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.PUSH_UPS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: CALI_PLYO_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.PUSH_UPS_PERFECT_DEVICE: {
        INHERITS_FROM: Exercise.PUSH_UPS,
    },
    Exercise.PULLOVERS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.RES_LAT_PULLDOWN: {
        INHERITS_FROM: Exercise.LAT_PULLDOWN,
    },
    Exercise.RES_SEATED_ROW: {
        INHERITS_FROM: Exercise.SEATED_ROW,
    },
    Exercise.RES_TRICEP_PUSHDOWN: {
        INHERITS_FROM: Exercise.TRICEP_PUSHDOWN,
    },
    Exercise.SEATED_ROW: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.SEATED_ROW_WIDE_NATURAL: {
        INHERITS_FROM: Exercise.SEATED_ROW,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.SIDE_LYING_EXTERNAL_ROTATION: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: ROTATOR_CUFF_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.SIDE_PLANK: {
        Field.COUNT_TYPE: CountType.SECONDS,
        Field.EXERCISE_TYPE: ExerciseType.CALISTHENIC,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        Field.OPTIMAL_REP_RANGE: ISOMETRIC_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.HIP_ABDUCTORS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.SINGLE_ARM_FARMERS_CARRY: {
        Field.COUNT_TYPE: CountType.STEPS,
        Field.EXERCISE_TYPE: ExerciseType.WEIGHTED_COMPOUND_ISOMETRIC,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        Field.OPTIMAL_REP_RANGE: STEP_BASED_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.HIP_FLEXORS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.SINGLE_LEG_LEG_CURL: {
        INHERITS_FROM: Exercise.LEG_CURL,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
    },
    Exercise.SINGLE_LEG_LEG_EXTENSION: {
        INHERITS_FROM: Exercise.LEG_EXTENSION,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
    },
    Exercise.SHRUGS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.SKULLCRUSHERS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.SQUATS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.SQUAT_WALKOUT: {
        INHERITS_FROM: Exercise.SQUATS,
        Field.EXERCISE_TYPE: ExerciseType.WEIGHTED_COMPOUND_ISOMETRIC,
        Field.TENSILE_FOCUS: TensileFocus.ISOMETRIC,
        Field.OPTIMAL_REP_RANGE: NERVOUS_SYSTEM_WEIGHTING,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.CALVES: None,
            MuscleGroup.GLUTES: None,
            MuscleGroup.HAMSTRINGS: None,
            MuscleGroup.HIP_ADDUCTORS: None,
            MuscleGroup.QUADS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.STRICT_PRESS: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: COMPLEX_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.TRICEP_PUSHDOWN: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: True,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.TRICEP_PUSHDOWN_V_BAR: {
        INHERITS_FROM: Exercise.TRICEP_PUSHDOWN,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.TRICEPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.UPWARD_CABLE_PEC_FLIES: {
        INHERITS_FROM: Exercise.MACH_PEC_FLIES,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.PECS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.WIDE_GRIP_PULL_UP: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.COMPOUND_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: False,
        Field.IS_LIMB_INDEPENDENT: False,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: SIMPLE_COMPOUND_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.ABS: None,
            MuscleGroup.BICEPS: None,
            MuscleGroup.DELTS: None,
            MuscleGroup.FOREARMS: None,
            MuscleGroup.LATS: None,
            MuscleGroup.RHOMBOIDS: None,
            MuscleGroup.ROTATOR_CUFF: None,
            MuscleGroup.SERRATUS: None,
            MuscleGroup.SPINAL_ERECTORS: None,
            MuscleGroup.TRAPS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.WRIST_CURL: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.FOREARMS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
    Exercise.WRIST_EXTENSION: {
        Field.COUNT_TYPE: CountType.REPS,
        Field.EXERCISE_TYPE: ExerciseType.ISOLATED_LIFT,
        Field.REQUIRES_MACHINE: False,
        Field.IS_UNILATERAL: True,
        Field.IS_LIMB_INDEPENDENT: True,
        Field.TENSILE_FOCUS: TensileFocus.CONCENTRIC,
        Field.OPTIMAL_REP_RANGE: UPPER_ISOLATED_REP_RANGE,
        Field.MUSCLE_GROUPS_WORKED: {
            MuscleGroup.FOREARMS: None,
        },
        Field.MUSCLES_WORKED: {
            None: None,
        },
        Field.ANTAGONIST_MUSCLES: {None},
    },
}
