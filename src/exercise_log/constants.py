from typing import Union

number = Union[float, int]               # Something like this should be part of the standard library IMO

# Column names
DATE = "date"
WORKOUT_TYPE = "workout_type"
DATA_DURATION = "duration(HH:mm:ss)"     # This is the human-readable version -- it'll be dropped during processing
DURATION = "duration(s)"                 # Convert the human-readable durations to seconds for computational simplicity
DISTANCE = "distance(km)"
STEPS = "steps"
ELEVATION = "elevation(m)"
AVG_HEART_RATE = "avg_heart_rate"
MAX_HEART_RATE = "max_heart_rate"
RESTING_HEART_RATE = "resting_heart_rate(bpm)"
NOTES = "notes"
LOCATION = "location"
EXERCISE = "exercise"
REPS = "reps"
WEIGHT = "weight(lbs)"
RATING = "rating"
PACE = "pace (m/s)"
RATE_OF_CLIMB = "rate of climb (m/h)"

# Ratings
WARMUP = "warm-up"

# Workout Types
WALK_TREADMILL = "walk (treadmill)"
WALK_OUTDOOR = "walk (outdoor)"
BIKE_STATIONARY = "bike (stationary)"

# Health constants
MIN_DAILY_ACTIVE_MINUTES = 22.5  # Weekly recommended is 150, this is about 150/7

EXPECTED_EXERCISES = {
    "5th Point of Flight",
    "Arnold Press",
    "Barbell Bicep Curl",
    "Barbell Military Press",
    "Barbell Overhead Tricep Extension",
    "Bench Press",
    "Bent-Over Single-Arm Barbell Row",
    "Bicep Curl",
    "Cable Lateral Lift",
    "Cable Pec Flies",
    "Calf Raise",
    "Clean & Jerk",
    "Close-Grip Lat Pulldown",
    "Concentration Curl",
    "Deadlift",
    "Delt Flies",
    "Dumbell Press",
    "Front Lift",
    "Hammer Curl",
    "Incline Dumbell Press",
    "Lat Pulldown",
    "Lateral Lift",
    "Lawnmowers",
    "Leg Curl",
    "Leg Extension",
    "Leg Press",
    "Leg Raise",
    "Lunges",
    "Machine Bench Press",
    "Machine Pec Flies",
    "Machine Upward Bench Press",
    "Military Press",
    "Overhead Barbell Tricep Extension",
    "Overhead Tricep Extension",
    "Pec Flies",
    "Plank",
    "Preacher Curl",
    "Push-Ups",
    "Push-Ups (Perfect Device)",
    "Resistance Lat Pulldown",
    "Resistance Seated Row",
    "Resistance Tricep Pushdown",
    "Seated Row",
    "Shrugs",
    "Skullcrushers",
    "Squats",
    "Tricep Pushdown",
    "Upward Bench Press",
    "Upward Cable Pec Flies",
    "Upward Dumbell Bench Press",
    "Upward Dumbell Press",
}

SET_TYPE_TO_REP_RANGE = {
    "one_rm": (1, 1),
    "strength": (2, 7),
    "hypertrophy": (8, 14),
    "endurance": (15, float("inf")),
}
