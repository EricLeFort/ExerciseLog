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

# Workout Types
WALK_TREADMILL = "walk (treadmill)"
WALK_OUTDOOR = "walk (outdoor)"
BIKE_STATIONARY = "bike (stationary)"

# Health constants
MIN_DAILY_ACTIVE_MINUTES = 22.5  # Weekly recommended is 150, this is about 150/7