"""Contains logic relating to the loading and transformation of ExerciseLog data."""

import csv

import numpy as np
import pandas as pd

from exercise_log.constants import ROOT_ONTOLOGY_DIR
from exercise_log.strength import Exercise
from exercise_log.utils import StrEnum, join_with_comma

# Dynamically create the ColumnNames enum using a shared definition
ColumnName = StrEnum.create_from_json(f"{ROOT_ONTOLOGY_DIR}/enum/dataloader/columns.json", __name__)


# This is just for convenience since ColumnName is a long string
CName = ColumnName
LONG = "Int64"


class DataBox:
    """A manager for gathering and logically grouping relevant data being loaded."""

    def __init__(self, root_data_dir: str) -> None:
        """Initialize this DataBox. The contained data is all computed lazily."""
        self.root_data_dir = root_data_dir

        # Base datasets
        self._health_metrics = None
        self._travel_days = None
        self._walk_workouts = None
        self._run_workouts = None
        self._bike_workouts = None
        self._row_workouts = None
        self._stair_workouts = None
        self._weight_training_workouts = None
        self._weight_training_sets = None

        # Aggregate datasets
        self._cardio_workouts = None
        self._all_workouts = None

    def get_health_metrics(self) -> pd.DataFrame:
        """Access the health metrics dataset and loads it if it hasn't been yet."""
        if self._health_metrics is None:
            self._health_metrics = DataLoader.load_health_metrics(self.root_data_dir)
        return self._health_metrics

    def get_travel_days(self) -> pd.DataFrame:
        """Access the travel days dataset, loading it if necessary."""
        if self._travel_days is None:
            self._travel_days = DataLoader.load_travel_days(self.root_data_dir)
        return self._travel_days

    def get_walk_workouts(self) -> pd.DataFrame:
        """Access the walk workouts dataset, loading it if necessary."""
        if self._walk_workouts is None:
            self._walk_workouts = DataLoader.load_walk_workouts(self.root_data_dir)
        return self._walk_workouts

    def get_run_workouts(self) -> pd.DataFrame:
        """Access the run workouts dataset, loading it if necessary."""
        if self._run_workouts is None:
            self._run_workouts = DataLoader.load_run_workouts(self.root_data_dir)
        return self._run_workouts

    def get_bike_workouts(self) -> pd.DataFrame:
        """Access the bike workouts dataset, loading it if necessary."""
        if self._bike_workouts is None:
            self._bike_workouts = DataLoader.load_bike_workouts(self.root_data_dir)
        return self._bike_workouts

    def get_row_workouts(self) -> pd.DataFrame:
        """Access the row workouts dataset, loading it if necessary."""
        if self._row_workouts is None:
            self._row_workouts = DataLoader.load_row_workouts(self.root_data_dir)
        return self._row_workouts

    def get_stair_workouts(self) -> pd.DataFrame:
        """Access the stair workouts dataset, loading it if necessary."""
        if self._stair_workouts is None:
            self._stair_workouts = DataLoader.load_stair_workouts(self.root_data_dir)
        return self._stair_workouts

    def get_weight_training_workouts(self) -> pd.DataFrame:
        """Access the weight training workouts dataset, loading it if necessary."""
        if self._weight_training_workouts is None:
            self._weight_training_workouts = DataLoader.load_weight_training_workouts(self.root_data_dir)
        return self._weight_training_workouts

    def get_weight_training_sets(self) -> pd.DataFrame:
        """Access the weight training sets dataset, loading it if necessary."""
        if self._weight_training_sets is None:
            self._weight_training_sets = DataLoader.load_weight_training_sets(self.root_data_dir)
        return self._weight_training_sets

    def get_cardio_workouts(self) -> pd.DataFrame:
        """Access the cardio workouts dataset (an aggregate of other datasets), loading them if necessary."""
        if self._cardio_workouts is None:
            workouts = [
                self.get_walk_workouts(),
                self.get_run_workouts(),
                self.get_bike_workouts(),
                self.get_row_workouts(),
                self.get_stair_workouts(),
            ]
            self._cardio_workouts = DataLoader.merge_on_common_columns(workouts)
        return self._cardio_workouts

    def get_all_workouts(self) -> pd.DataFrame:
        """Access the all workouts dataset (an aggregate of other datasets), loading them if necessary."""
        if self._all_workouts is None:
            self._all_workouts = DataLoader.load_all_workouts(
                self.get_cardio_workouts(),
                self.get_weight_training_workouts(),
                self.get_travel_days(),
            )
        return self._all_workouts


class DataLoader:
    """Responsible for loading small datasets that fit in memory."""

    @staticmethod
    def _load_and_clean_data(fname: str) -> pd.DataFrame:
        """Load the CSV and cleans up the data (convert date/times to proper types, NA -> "", etc)."""
        df = pd.read_csv(fname)

        # Clean the data
        df[CName.DATE] = pd.to_datetime(df[CName.DATE], format="%d-%b-%Y")
        df = df.sort_values(CName.DATE, ignore_index=True)
        if CName.DATA_DURATION in df:
            df[CName.DATA_DURATION] = pd.to_timedelta(df[CName.DATA_DURATION])
            df[CName.DATA_DURATION] = df[CName.DATA_DURATION].apply(
                lambda x: np.nan if pd.isna(x) else x.total_seconds(),
            )
            df[CName.DATA_DURATION] = df[CName.DATA_DURATION].astype(LONG)
            df = df.rename(columns={CName.DATA_DURATION: CName.DURATION})
        if CName.NOTES in df:
            df[CName.NOTES] = df[CName.NOTES].fillna("")

        # Validate the data
        DataLoader._validate_csv(fname)
        if CName.EXERCISE in df:
            DataLoader._validate_exercises(df, fname)

        return df

    @staticmethod
    def _validate_csv(fname: str) -> None:
        with open(fname, encoding="utf-8") as f:
            reader = csv.reader(f)

            try:
                headers = next(reader)

                # Ensure the data is not ragged
                for row in reader:
                    if len(row) != len(headers):
                        msg = f'File {fname} is ragged at row {reader.line_num}: "{row}"'
                        raise ValueError(msg)
            except StopIteration as e:
                msg = f"CSV at {fname} was empty."
                raise ValueError(msg) from e

    @staticmethod
    def _validate_exercises(df: pd.DataFrame, fname: str) -> None:
        # Disabling linting, this is needed bc Pandas is fussy; "some_exercise in Exercise" ought to work but doesn't
        exercise_map = Exercise._value2member_map_  # noqa: SLF001
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
    def _det_workout_type(joined_workout_types: str) -> str:
        """Determine the workout type given all of the comma-joined workout types for a given day."""
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
        Compute the total daily workout duration for each day.

        Note: there can be more than one per day or rest days, this smooths that out.
        """
        agg_dict = {CName.DURATION: ["sum"]}
        total_durations = [
            weight_training_workouts.groupby(CName.DATE).agg(agg_dict),
            cardio_workouts.groupby(CName.DATE).agg(agg_dict),
            travel_days.groupby(CName.DATE).agg(agg_dict),
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
        """Compute the daily workout type for each day."""
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
    def _clean_cardio_workout(fname: str) -> pd.DataFrame:
        workouts = DataLoader._load_and_clean_data(fname)
        workouts[CName.AVG_HEART_RATE] = workouts[CName.AVG_HEART_RATE].astype(LONG)
        workouts[CName.MAX_HEART_RATE] = workouts[CName.MAX_HEART_RATE].astype(LONG)
        return workouts

    @staticmethod
    def _get_all_dates(workouts: list[pd.DataFrame]) -> pd.DataFrame:
        """
        Build a pd.DataFrame with all of the dates in the given DataFrames.

        Returns:
            The new pd.DataFrame
        """
        return pd.concat([workout[CName.DATE] for workout in workouts])

    @staticmethod
    def load_health_metrics(root_data_dir: str) -> pd.DataFrame:
        """Load the health metrics dataset, filtering out days where both weight and resting heart rate are missing."""
        health_metrics = DataLoader._load_and_clean_data(f"{root_data_dir}/health_metrics.csv")

        # Filter out any empty rows from the health metrics
        return health_metrics[health_metrics[CName.WEIGHT].notna() | health_metrics[CName.RESTING_HEART_RATE].notna()]

    @staticmethod
    def load_travel_days(root_data_dir: str) -> pd.DataFrame:
        """Load the travel days dataset."""
        travel_days = DataLoader._load_and_clean_data(f"{root_data_dir}/travel_days.csv")
        # Filling in an explicit workout type since its implicit for travel days
        travel_days[CName.WORKOUT_TYPE] = "Travel"
        return travel_days

    @staticmethod
    def load_walk_workouts(root_data_dir: str) -> pd.DataFrame:
        """Load the walk workouts dataset."""
        return DataLoader._load_foot_workouts(root_data_dir, "walks.csv")

    @staticmethod
    def load_run_workouts(root_data_dir: str) -> pd.DataFrame:
        """Load the run workouts dataset."""
        return DataLoader._load_foot_workouts(root_data_dir, "runs.csv")

    @staticmethod
    def _load_foot_workouts(root_data_dir: str, fname: str) -> pd.DataFrame:
        workouts = DataLoader._clean_cardio_workout(f"{root_data_dir}/{fname}")
        workouts[CName.STEPS] = workouts[CName.STEPS].astype(LONG)
        return workouts

    @staticmethod
    def load_bike_workouts(root_data_dir: str) -> pd.DataFrame:
        """Load the bike workouts dataset."""
        return DataLoader._load_spin_workouts(root_data_dir, "bikes.csv")

    @staticmethod
    def load_row_workouts(root_data_dir: str) -> pd.DataFrame:
        """Load the row workouts dataset."""
        return DataLoader._load_spin_workouts(root_data_dir, "rows.csv")

    @staticmethod
    def _load_spin_workouts(root_data_dir: str, fname: str) -> pd.DataFrame:
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
    def load_weight_training_workouts(root_data_dir: str) -> pd.DataFrame:
        """Load the weight training workouts dataset."""
        return DataLoader._load_and_clean_data(f"{root_data_dir}/weight_training_workouts.csv")

    @staticmethod
    def load_weight_training_sets(root_data_dir: str) -> pd.DataFrame:
        """Load the weight training sets dataset."""
        return DataLoader._load_and_clean_data(f"{root_data_dir}/weight_training_sets.csv")

    @staticmethod
    def load_stair_workouts(root_data_dir: str) -> pd.DataFrame:
        """Load the stair workouts dataset."""
        workouts = DataLoader._clean_cardio_workout(f"{root_data_dir}/stairs.csv")
        workouts[CName.FLIGHTS_UP] = workouts[CName.FLIGHTS_UP].astype("Int64")
        workouts[CName.FLIGHTS_DOWN] = workouts[CName.FLIGHTS_DOWN].astype("Int64")
        workouts[CName.DISTANCE] = np.nan  # Distance is unknown but I don't want to ruin merging of cardio workouts
        return workouts

    @staticmethod
    def load_dashes(root_data_dir: str) -> pd.DataFrame:
        """Load the dashes dataset."""
        return DataLoader._load_and_clean_data(f"{root_data_dir}/dashes.csv")

    @staticmethod
    def load_rate_of_climb(root_data_dir: str) -> pd.DataFrame:
        """Load the rate of climb dataset."""
        return DataLoader._load_and_clean_data(f"{root_data_dir}/rate_of_climb.csv")

    @staticmethod
    def load_walk_backwards(root_data_dir: str) -> pd.DataFrame:
        """Load the walk backwards dataset."""
        return DataLoader._load_and_clean_data(f"{root_data_dir}/walk_backwards.csv")

    @staticmethod
    def merge_on_common_columns(workouts: list[pd.DataFrame]) -> pd.DataFrame:
        """Merge all of the given pd.DataFrames, only keeping common fields."""
        workouts = pd.concat(workouts, join="inner")  # Use inner so we only preserve the common fields
        return workouts.reset_index(drop=True)

    @staticmethod
    def load_all_workouts(
        cardio_workouts: pd.DataFrame,
        weight_training_workouts: pd.DataFrame,
        travel_days: pd.DataFrame,
    ) -> pd.DataFrame:
        """Load all of the workouts datasets and merges them into a single dataset."""
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
        Add computed metrics to the cardio workouts DataFrame.

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
            if CName.DISTANCE in cardio_workouts:
                # Scale down from km, then round to the nearest 5%
                cardio_workouts[CName.AVG_GRADE] = cardio_workouts[CName.ELEVATION] / cardio_workouts[CName.DISTANCE]
                cardio_workouts[CName.AVG_GRADE] = cardio_workouts[CName.AVG_GRADE] / 1000
                cardio_workouts[CName.AVG_GRADE] = (cardio_workouts[CName.AVG_GRADE] * 20).round(1) * 0.05
        if CName.STEPS in cardio_workouts:  # Skip this metric for workouts like biking where steps aren't tracked
            # Convert km to m
            cardio_workouts[CName.STEP_SIZE] = cardio_workouts[CName.DISTANCE] / cardio_workouts[CName.STEPS]
            cardio_workouts[CName.STEP_SIZE] = (cardio_workouts[CName.STEP_SIZE] * 1000).round(2)
