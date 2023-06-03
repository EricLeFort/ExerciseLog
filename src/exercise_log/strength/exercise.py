from enum import Enum
from typing import Any


class Exercise(str, Enum):
    FIFTH_POINT_OF_FLIGHT = "5th Point of Flight"
    ARNOLD_PRESS = "Arnold Press"
    BARBELL_BICEP_CURL = "Barbell Bicep Curl"
    BARBELL_OVERHEAD_TRICEP_EXTENSION = "Barbell Overhead Tricep Extension"
    BENCH_PRESS = "Bench Press"
    BENT_OVER_SINGLE_ARM_BARBELL_ROW = "Bent-Over Single-Arm Barbell Row"
    BICEP_CURL = "Bicep Curl"
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
    FRONT_LIFT = "Front Lift"
    FULL_CANS = "Full Cans"
    HAMMER_CURL = "Hammer Curl"
    INC_BENCH_PRESS = "Incline Bench Press"
    INC_DUMBBELL_PRESS = "Incline Dumbbell Press"
    LAT_PULLDOWN = "Lat Pulldown"
    LAT_PULLDOWN_HANG = "Lat Pulldown Hang"
    LATERAL_LIFT = "Lateral Lift"
    LAWNMOWERS = "Lawnmowers"
    LEG_CURL = "Leg Curl"
    LEG_EXTENSION = "Leg Extension"
    LEG_PRESS = "Leg Press"
    LEG_RAISE = "Leg Raise"
    LONG_HANG_DEADLIFT = "Long-Hang Deadlift"
    LUNGES = "Lunges"
    MACH_BENCH_PRESS = "Machine Bench Press"
    MACH_INCLINE_BENCH_PRESS = "Machine Incline Bench Press"
    MACH_PEC_FLIES = "Machine Pec Flies"
    MILITARY_PRESS = "Military Press"
    OVERHEAD_TRICEP_EXTENSION = "Overhead Tricep Extension"
    PEC_FLIES = "Pec Flies"
    PLANK = "Plank"
    PREACHER_CURL = "Preacher Curl"
    PUSH_UPS = "Push-Ups"
    PUSH_UPS_PERFECT_DEVICE = "Push-Ups (Perfect Device)"
    PULLOVERS = "Pullovers"
    RES_LAT_PULLDOWN = "Resistance Lat Pulldown"
    RES_SEATED_ROW = "Resistance Seated Row"
    RES_TRICEP_PUSHDOWN = "Resistance Tricep Pushdown"
    SEATED_ROW = "Seated Row"
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

    def __contains__(item: Any):
        """
        Checks if the given item is a member of this Exercise enum.

        Note: this is a little hacky due to the access to a private member but the alternative is try-casting which is
        ~8x slower.

        Args:
            item (Any): The item to check for membership
        """
        return item in Exercise._value2member_map_
