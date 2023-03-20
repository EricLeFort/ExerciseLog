import pandas as pd

from exercise_log.constants import (
    DATA_DURATION,
    DATE,
    DISTANCE,
    DURATION,
    ELEVATION,
    NOTES,
    PACE,
    RATE_OF_CLIMB,
    RESTING_HEART_RATE,
    WEIGHT,
    WORKOUT_TYPE,
)
from exercise_log.utils import join_with_comma


ROOT_DATA_DIR = "../data/"


class DataLoader:
    @staticmethod
    def _load_and_clean_data(fname: str) -> pd.DataFrame:
        """
        Loads the CSV at the given fname and cleans up the data (convert date/times to proper types, NA -> "", etc.)
        """
        df = pd.read_csv(fname)
        df[DATE] = pd.to_datetime(df[DATE])
        if DATA_DURATION in df:
            df[DATA_DURATION] = pd.to_timedelta(df[DATA_DURATION])
            df[DATA_DURATION] = df[DATA_DURATION].apply(lambda x: int(x.total_seconds()))
            df.rename(columns={DATA_DURATION: DURATION}, inplace=True)
        if NOTES in df:
            df[NOTES] = df[NOTES].fillna("")
        return df

    def _det_workout_type(joined_workout_types: str):
        """Determines the workout type given all of the comma-joined workout types for a given day."""
        result = ""
        for w_type in joined_workout_types.split(","):
            if not result:
                result = w_type
            if result and w_type != result:
                return "Mixed"
        return result

    def _compute_total_durations(
        all_workouts: pd.DataFrame,
        cardio_workouts: pd.DataFrame,
        weight_training_workouts: pd.DataFrame,
        travel_days: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Computes the total daily workout duration for each day.

        Note: there can be more than one per day or rest days, this smooths that out.
        """
        total_durations = pd.concat([
            weight_training_workouts.groupby(DATE)[DURATION].agg(sum),
            cardio_workouts.groupby(DATE)[DURATION].agg(sum),
            travel_days.groupby(DATE)[DURATION].agg(sum),
        ]).groupby(DATE).agg(sum)
        total_durations.index = pd.DatetimeIndex(total_durations.index)
        return total_durations.reindex(all_workouts.index, fill_value=0)

    def _compute_workout_types(
        all_workouts: pd.DataFrame,
        cardio_workouts: pd.DataFrame,
        weight_training_workouts: pd.DataFrame,
        travel_days: pd.DataFrame,
    ) -> pd.DataFrame:
        """Computes the daily workout type for each day"""
        workout_types = pd.concat([
            weight_training_workouts.groupby(DATE)[WORKOUT_TYPE].agg(join_with_comma),
            cardio_workouts.groupby(DATE)[WORKOUT_TYPE].agg(join_with_comma),
            travel_days.groupby(DATE)[WORKOUT_TYPE].agg(join_with_comma),
        ]).groupby(DATE).agg(join_with_comma)
        workout_types = workout_types.apply(DataLoader._det_workout_type)
        workout_types.index = pd.DatetimeIndex(workout_types.index)
        return workout_types.reindex(all_workouts.index, fill_value="Rest Day")

    @staticmethod
    def load_health_metrics():
        health_metrics = DataLoader._load_and_clean_data(f"{ROOT_DATA_DIR}health_metrics.csv")

        # Filter out any empty rows from the health metrics
        return health_metrics[health_metrics[WEIGHT].notnull() | health_metrics[RESTING_HEART_RATE].notnull()]

    @staticmethod
    def load_travel_days():
        travel_days = DataLoader._load_and_clean_data(f"{ROOT_DATA_DIR}travel_days.csv")
        # Filling in an explicit workout type since its implicit for travel days
        travel_days[WORKOUT_TYPE] = "Travel"
        return travel_days

    @staticmethod
    def load_cardio_workouts():
        cardio_workouts = DataLoader._load_and_clean_data(f"{ROOT_DATA_DIR}cardio_workouts.csv")

        # Populate computed fields
        cardio_workouts[PACE] = cardio_workouts[DISTANCE] / cardio_workouts[DURATION]
        cardio_workouts[PACE] = cardio_workouts[PACE] * 1000                            # Convert from km/s to m/s
        cardio_workouts[RATE_OF_CLIMB] = cardio_workouts[ELEVATION] / cardio_workouts[DURATION]
        cardio_workouts[RATE_OF_CLIMB] = cardio_workouts[RATE_OF_CLIMB] * (60 * 60)     # Convert from m/s to m/h
        return cardio_workouts

    @staticmethod
    def load_weight_training_workouts():
        return DataLoader._load_and_clean_data(f"{ROOT_DATA_DIR}weight_training_workouts.csv")

    @staticmethod
    def load_weight_training_sets():
        return DataLoader._load_and_clean_data(f"{ROOT_DATA_DIR}weight_training_sets.csv")

    @staticmethod
    def load_all_workouts(cardio_workouts: pd.DataFrame, weight_training_workouts: pd.DataFrame, travel_days: pd.DataFrame):
        # Will be used to pad all datasets to have consistent dates
        all_dates = pd.concat([cardio_workouts[DATE], weight_training_workouts[DATE], travel_days[DATE]])

        # Initialize the dataframe including all dates spanning the range of the data (rest days are missing in the workout data)
        all_workouts = pd.DataFrame()
        all_workouts[DATE] = pd.date_range(all_dates.min(), all_dates.max())
        all_workouts = all_workouts.set_index(DATE)

        # Populate computed fields
        all_workouts[DURATION] = DataLoader._compute_total_durations(
            all_workouts,
            cardio_workouts,
            weight_training_workouts,
            travel_days
        )
        all_workouts[WORKOUT_TYPE] = DataLoader._compute_workout_types(
            all_workouts,
            cardio_workouts,
            weight_training_workouts,
            travel_days
        )
        return all_workouts.reset_index()
