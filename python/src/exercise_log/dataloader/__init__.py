import csv
from typing import List

import numpy as np
import pandas as pd

from exercise_log.constants import ROOT_ONTOLOGY_DIR
from exercise_log.strength import Exercise
from exercise_log.utils import StrEnum, join_with_comma

# Dynamically create the ColumnNames enum using a shared definition
ColumnName = StrEnum.create_from_json(f"{ROOT_ONTOLOGY_DIR}/enum/columns.json", "ColumnName")


# This is just for convenience since ColumnName is a long string
CName = ColumnName
LONG = "Int64"


class DataLoader:
    @staticmethod
    def _load_and_clean_data(fname: str) -> pd.DataFrame:
        """
        Loads the CSV at the given fname and cleans up the data (convert date/times to proper types, NA -> "", etc.)
        """
        df = pd.read_csv(fname)

        # Clean the data
        df[CName.DATE] = pd.to_datetime(df[CName.DATE], format="%d-%b-%Y")
        df = df.sort_values(CName.DATE, ignore_index=True)
        if CName.DATA_DURATION in df:
            df[CName.DATA_DURATION] = pd.to_timedelta(df[CName.DATA_DURATION])
            df[CName.DATA_DURATION] = df[CName.DATA_DURATION].apply(
                lambda x: np.nan if pd.isnull(x) else x.total_seconds()
            )
            df[CName.DATA_DURATION] = df[CName.DATA_DURATION].astype(LONG)
            df.rename(columns={CName.DATA_DURATION: CName.DURATION}, inplace=True)
        if CName.NOTES in df:
            df[CName.NOTES] = df[CName.NOTES].fillna("")

        # Validate the data
        DataLoader._validate_csv(fname)
        if CName.EXERCISE in df:
            DataLoader._validate_exercises(df, fname)

        return df

    @staticmethod
    def _validate_csv(fname: str):
        with open(fname, "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            try:
                headers = next(reader)

                # Ensure the data is not ragged
                for row in reader:
                    if len(row) != len(headers):
                        raise ValueError(f'File is ragged at row {reader.line_num}: "{row}"')
            except StopIteration as e:
                raise ValueError(f"CSV at {fname} was empty.") from e

    @staticmethod
    def _validate_exercises(df: pd.DataFrame, fname: str):
        # Disabling pylint, this is needed bc Pandas is fussy; "some_exercise in Exercise" ought to work but doesn't
        exercise_map = Exercise._value2member_map_  # pylint: disable=protected-access
        if df[CName.EXERCISE].isin(exercise_map).all():
            return

        first_invalid_idx = df[~df[CName.EXERCISE].isin(exercise_map)].index.tolist()[0]
        first_invalid = df[CName.EXERCISE][first_invalid_idx]

        possible_valid = first_invalid[:-1]
        base_msg = f'"{first_invalid}" at row {first_invalid_idx + 2} in {fname} is not an expected exercise'
        if possible_valid in exercise_map:
            raise ValueError(base_msg + f', did you mean "{possible_valid}"')
        raise ValueError(base_msg)

    @staticmethod
    def _det_workout_type(joined_workout_types: str):
        """Determines the workout type given all of the comma-joined workout types for a given day."""
        result = ""
        for w_type in joined_workout_types.split(","):
            if not result:
                result = w_type
            if result and w_type != result:
                return "Mixed"
        return result

    @staticmethod
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
        total_durations = [
            weight_training_workouts.groupby(CName.DATE)[CName.DURATION].agg("sum"),
            cardio_workouts.groupby(CName.DATE)[CName.DURATION].agg("sum"),
            travel_days.groupby(CName.DATE)[CName.DURATION].agg("sum"),
        ]
        total_durations = pd.concat(total_durations).groupby(CName.DATE).agg("sum")
        total_durations.index = pd.DatetimeIndex(total_durations.index)
        return total_durations.reindex(all_workouts.index, fill_value=0)

    @staticmethod
    def _compute_workout_types(
        all_workouts: pd.DataFrame,
        cardio_workouts: pd.DataFrame,
        weight_training_workouts: pd.DataFrame,
        travel_days: pd.DataFrame,
    ) -> pd.DataFrame:
        """Computes the daily workout type for each day"""
        workout_types = [
            weight_training_workouts.groupby(CName.DATE)[CName.WORKOUT_TYPE].agg(join_with_comma),
            cardio_workouts.groupby(CName.DATE)[CName.WORKOUT_TYPE].agg(join_with_comma),
            travel_days.groupby(CName.DATE)[CName.WORKOUT_TYPE].agg(join_with_comma),
        ]
        workout_types = pd.concat(workout_types).groupby(CName.DATE).agg(join_with_comma)
        workout_types = workout_types.apply(DataLoader._det_workout_type)
        workout_types.index = pd.DatetimeIndex(workout_types.index)
        return workout_types.reindex(all_workouts.index, fill_value="Rest Day")

    @staticmethod
    def _clean_cardio_workout(fname: str):
        workouts = DataLoader._load_and_clean_data(fname)
        workouts[CName.AVG_HEART_RATE] = workouts[CName.AVG_HEART_RATE].astype(LONG)
        workouts[CName.MAX_HEART_RATE] = workouts[CName.MAX_HEART_RATE].astype(LONG)
        return workouts

    @staticmethod
    def _get_all_dates(workouts: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Builds a pd.DataFrame with all of the dates in the given DataFrames

        Returns:
            The new pd.DataFrame
        """
        return pd.concat([workout[CName.DATE] for workout in workouts])

    @staticmethod
    def load_health_metrics(root_data_dir: str):
        health_metrics = DataLoader._load_and_clean_data(f"{root_data_dir}/health_metrics.csv")

        # Filter out any empty rows from the health metrics
        return health_metrics[
            health_metrics[CName.WEIGHT].notnull() | health_metrics[CName.RESTING_HEART_RATE].notnull()
        ]

    @staticmethod
    def load_travel_days(root_data_dir: str):
        travel_days = DataLoader._load_and_clean_data(f"{root_data_dir}/travel_days.csv")
        # Filling in an explicit workout type since its implicit for travel days
        travel_days[CName.WORKOUT_TYPE] = "Travel"
        return travel_days

    @staticmethod
    def load_walk_workouts(root_data_dir: str):
        return DataLoader._load_foot_workouts(root_data_dir, "walks.csv")

    @staticmethod
    def load_run_workouts(root_data_dir: str):
        return DataLoader._load_foot_workouts(root_data_dir, "runs.csv")

    @staticmethod
    def _load_foot_workouts(root_data_dir: str, fname: str):
        workouts = DataLoader._clean_cardio_workout(f"{root_data_dir}/{fname}")
        workouts[CName.STEPS] = workouts[CName.STEPS].astype(LONG)
        return workouts

    @staticmethod
    def load_bike_workouts(root_data_dir: str):
        return DataLoader._load_spin_workouts(root_data_dir, "bikes.csv")

    @staticmethod
    def load_row_workouts(root_data_dir: str):
        return DataLoader._load_spin_workouts(root_data_dir, "rows.csv")

    @staticmethod
    def _load_spin_workouts(root_data_dir: str, fname: str):
        workouts = DataLoader._clean_cardio_workout(f"{root_data_dir}/{fname}")
        if CName.AVG_CADENCE_BIKE in workouts:
            avg_cadence = CName.AVG_CADENCE_BIKE
            max_cadence = CName.MAX_CADENCE_BIKE
        else:
            avg_cadence = CName.AVG_CADENCE_ROW
            max_cadence = CName.MAX_CADENCE_ROW
        workouts[avg_cadence] = workouts[avg_cadence].astype(LONG)
        workouts[max_cadence] = workouts[max_cadence].astype(LONG)
        workouts[CName.AVG_WATT] = workouts[CName.AVG_WATT].astype(LONG)
        workouts[CName.MAX_WATT] = workouts[CName.MAX_WATT].astype(LONG)
        return workouts

    @staticmethod
    def load_weight_training_workouts(root_data_dir: str):
        return DataLoader._load_and_clean_data(f"{root_data_dir}/weight_training_workouts.csv")

    @staticmethod
    def load_weight_training_sets(root_data_dir: str):
        return DataLoader._load_and_clean_data(f"{root_data_dir}/weight_training_sets.csv")

    @staticmethod
    def load_stair_workouts(root_data_dir: str):
        workouts = DataLoader._clean_cardio_workout(f"{root_data_dir}/stairs.csv")
        workouts[CName.FLIGHTS_UP] = workouts[CName.FLIGHTS_UP].astype("Int64")
        workouts[CName.FLIGHTS_DOWN] = workouts[CName.FLIGHTS_DOWN].astype("Int64")
        workouts[CName.DISTANCE] = np.nan  # Distance is unknown but I don't want to ruin merging of cardio workouts
        return workouts

    @staticmethod
    def load_dashes(root_data_dir: str):
        return DataLoader._load_and_clean_data(f"{root_data_dir}/dashes.csv")

    @staticmethod
    def load_rate_of_climb(root_data_dir: str):
        return DataLoader._load_and_clean_data(f"{root_data_dir}/rate_of_climb.csv")

    @staticmethod
    def load_walk_backwards(root_data_dir: str):
        return DataLoader._load_and_clean_data(f"{root_data_dir}/walk_backwards.csv")

    @staticmethod
    def merge_cardio_workouts(workouts: List[pd.DataFrame]) -> pd.DataFrame:
        cardio_workouts = pd.concat(workouts, join="inner")  # Use inner so we only preserve the common fields
        return cardio_workouts.reset_index(drop=True)

    @staticmethod
    def load_all_workouts(
        cardio_workouts: pd.DataFrame,
        weight_training_workouts: pd.DataFrame,
        travel_days: pd.DataFrame,
    ):
        # Will be used to pad all datasets to have consistent dates
        all_dates = DataLoader._get_all_dates([cardio_workouts, weight_training_workouts, travel_days])

        # Initialize the dataframe including all dates spanning the range of the data
        # (rest days are missing in the workout data)
        all_workouts = pd.DataFrame()
        all_workouts[CName.DATE] = pd.date_range(all_dates.min(), all_dates.max())
        all_workouts = all_workouts.sort_values(CName.DATE, ignore_index=True)
        all_workouts = all_workouts.set_index(CName.DATE)

        # Populate computed fields
        all_workouts[CName.DURATION.value] = DataLoader._compute_total_durations(
            all_workouts,
            cardio_workouts,
            weight_training_workouts,
            travel_days,
        )
        all_workouts[CName.WORKOUT_TYPE.value] = DataLoader._compute_workout_types(
            all_workouts,
            cardio_workouts,
            weight_training_workouts,
            travel_days,
        )
        return all_workouts.reset_index()

    @staticmethod
    def add_computed_cardio_metrics(cardio_workouts: pd.DataFrame) -> None:
        """
        Adds computed metrics to the cardio workouts DataFrame.

        Added metrics include:
            * pace (m/s)
            * rate of climb (m/h)
            * step size (m)

        Args:
            cardio_workouts (pd.DataFrame): The cardio workouts dataframe to add the columns to
        """
        # Convert km/s to m/s
        if CName.DISTANCE in cardio_workouts and CName.DURATION in cardio_workouts:
            cardio_workouts[CName.PACE] = cardio_workouts[CName.DISTANCE] / cardio_workouts[CName.DURATION]
            cardio_workouts[CName.PACE] = (cardio_workouts[CName.PACE] * 1000).round(2)
        if CName.ELEVATION in cardio_workouts:  # Skip this metric for workouts where elevation isn't tracked
            # Convert m/s to m/h
            cardio_workouts[CName.RATE_OF_CLIMB] = cardio_workouts[CName.ELEVATION] / cardio_workouts[CName.DURATION]
            cardio_workouts[CName.RATE_OF_CLIMB] = cardio_workouts[CName.RATE_OF_CLIMB] * (60 * 60)
            cardio_workouts[CName.RATE_OF_CLIMB] = cardio_workouts[CName.RATE_OF_CLIMB].round(0).astype(LONG)
        if CName.STEPS in cardio_workouts:  # Skip this metric for workouts like biking where steps aren't tracked
            # Convert km to m
            cardio_workouts[CName.STEP_SIZE] = cardio_workouts[CName.DISTANCE] / cardio_workouts[CName.STEPS]
            cardio_workouts[CName.STEP_SIZE] = (cardio_workouts[CName.STEP_SIZE] * 1000).round(2)
