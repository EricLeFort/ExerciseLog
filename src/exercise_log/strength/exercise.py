from exercise_log.utils import StrEnum
from exercise_log.strength.constants import (
    ANTAGONIST_MUSCLES,
    MUSCLE_GROUPS_WORKED,
    MUSCLES_WORKED,
)


class Exercise(StrEnum):
    """
    An Enum of the exercise names this system allows. It is not intended to be exhaustive, merely a reflection of the
    set of exercises currently present in the data. It helps prevent the addition of noise such as name variations
    (e.g. lateral lift vs. lateral raise, bicep curl vs. bicep curls) or typos.
    """
    FIFTH_POINT_OF_FLIGHT = "5th Point of Flight"
    ARNOLD_PRESS = "Arnold Press"
    BARBELL_BICEP_CURL = "Barbell Bicep Curl"
    BARBELL_CALF_RAISE = "Barbell Calf Raise"
    BARBELL_OVERHEAD_TRICEP_EXTENSION = "Barbell Overhead Tricep Extension"
    BENCH_PRESS = "Bench Press"
    BENT_OVER_LATERAL_LIFT = "Bent-Over Lateral Lift"
    BENT_OVER_SINGLE_ARM_BARBELL_ROW = "Bent-Over Single-Arm Barbell Row"
    BICEP_CURL = "Bicep Curl"
    BURPEES = "Burpees"
    CABLE_LATERAL_LIFT = "Cable Lateral Lift"
    CABLE_PEC_FLIES = "Cable Pec Flies"
    CALF_RAISE = "Calf Raise"
    CLEAN_AND_JERK = "Clean & Jerk"
    CLOSE_GRIP_LAT_PULLDOWN = "Close-Grip Lat Pulldown"
    CONCENTRAION_CURL = "Concentration Curl"
    DEADLIFT = "Deadlift"
    DEC_BENCH_PRESS = "Decline Bench Press"
    DELT_FLIES = "Delt Flies"
    DUMBBELL_PRESS = "Dumbbell Press"
    FINGER_CURL = "Finger Curl"
    FRONT_LIFT = "Front Lift"
    FULL_CANS = "Full Cans"
    HAMMER_CURL = "Hammer Curl"
    INC_BENCH_PRESS = "Incline Bench Press"
    INC_DUMBBELL_PRESS = "Incline Dumbbell Press"
    KETTLEBELL_FLIPS = "Kettlebell Flips"
    LAT_PULLDOWN = "Lat Pulldown"
    LAT_PULLDOWN_HANG = "Lat Pulldown Hang"
    LATERAL_LIFT = "Lateral Lift"
    LAWNMOWERS = "Lawnmowers"
    LEG_CURL = "Leg Curl"
    LEG_EXTENSION = "Leg Extension"
    LEG_PRESS = "Leg Press"
    LEG_PRESS_CALF_RAISE = "Leg Press Calf Raise"
    LEG_RAISE = "Leg Raise"
    LONG_HANG_DEADLIFT = "Long-Hang Deadlift"
    LUNGES = "Lunges"
    MACH_BENCH_PRESS = "Machine Bench Press"
    MACH_HIP_ABDUCTORS = "Machine Hip Abductors"
    MACH_HIP_ADDUCTORS = "Machine Hip Adductors"
    MACH_INCLINE_BENCH_PRESS = "Machine Incline Bench Press"
    MACH_PEC_FLIES = "Machine Pec Flies"
    MILITARY_PRESS = "Military Press"
    NEUTRAL_GRIP_PULL_UP= "Neutral-Grip Pull-Up"
    OVERHEAD_TRICEP_EXTENSION = "Overhead Tricep Extension"
    PLANK = "Plank"
    PREACHER_CURL = "Preacher Curl"
    PUSH_UPS = "Push-Ups"
    PUSH_UPS_PERFECT_DEVICE = "Push-Ups (Perfect Device)"
    PULLOVERS = "Pullovers"
    RES_LAT_PULLDOWN = "Resistance Lat Pulldown"
    RES_SEATED_ROW = "Resistance Seated Row"
    RES_TRICEP_PUSHDOWN = "Resistance Tricep Pushdown"
    SEATED_ROW = "Seated Row"
    SEATED_ROW_WIDE_NATURAL = "Seated Row (Wide-Natural Grip)"
    SIDE_LYING_EXTERNAL_ROTATION = "Side-Lying External Rotation"
    SIDE_PLANK = "Side-Plank"
    SINGLE_ARM_FARMERS_CARRY = "Single-Arm Farmer's Carry"
    SINGLE_LEG_LEG_CURL = "Single-Leg Leg Curl"
    SINGLE_LEG_LEG_EXTENSION = "Single-Leg Leg Extension"
    SHRUGS = "Shrugs"
    SKULLCRUSHERS = "Skullcrushers"
    SQUATS = "Squats"
    STRICT_PRESS = "Strict Press"
    TRICEP_PUSHDOWN = "Tricep Pushdown"
    UPWARD_CABLE_PEC_FLIES = "Upward Cable Pec Flies"
    WIDE_GRIP_PULL_UP = "Wide-Grip Pull-Up"
    WRIST_CURL = "Wrist Curl"
    WRIST_EXTENSION = "Wrist Extension"


class ExerciseType(StrEnum):
    CALISTHENIC = "Calisthenic"
    CARDIO = "Cardio"
    COMPOUND_LIFT = "Compound Lift"
    HIIT = "HIIT"
    ISOLATED_LIFT = "Isolated Lift"


class ExerciseInfo:
    """
    Stores metadata about an Exercise such as which muscles and muscle groups it works, which antagonist muscle is
    worked, and which ExerciseType it is.
    """
    def __init__(exercise: Exercise):
        """
        Initializes an ExerciseInfo by looking up the relevant data for the given Exercise.
        """
        info = exercise_info[exercise]

        self.muscles_worked = info[MUSCLES_WORKED]
        self.muscle_groups_worked = info[MUSCLE_GROUPS_WORKED]
        self.antagonist_muscles = info[ANTAGONIST_MUSCLES]
        self.exercise_type = info[EXERCISE_TYPE]
