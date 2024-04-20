import datetime
import os
from functools import partial
from multiprocessing import Pool

import pandas as pd

from exercise_log.dataloader import CName, ColumnName, DataLoader
from exercise_log.strength import Exercise
from exercise_log.trend import Trendsetter
from exercise_log.utils import TermColour, get_padded_dates
from exercise_log.vis import (
    PlotOptions,
    plot_resting_heart_rate,
    plot_strength_over_time,
    plot_weight,
    plot_workout_frequency,
)

ROOT_DATA_DIR = "../../data"
ROOT_IMG_DIR = "../../img"
PREDS_DIR = f"{ROOT_DATA_DIR}/preds"
EXTRAPOLATE_DAYS = 100
N_DAYS_TO_AVG = 28

PRIMARY_GYMS = {
    "Via 6 Gym": (datetime.date(year=2022, month=12, day=4), datetime.datetime.now(tz=datetime.UTC).date()),
}

SKIP_EXERCISE_PLOT_EXERCISES = {
    Exercise.FIFTH_POINT_OF_FLIGHT,
    Exercise.BURPEES,
    Exercise.DEFICIT_PUSH_UPS,
    Exercise.JUMPING_JACKS,
    Exercise.PARALLEL_BAR_LEG_RAISE,
    Exercise.LAT_PULLDOWN_HANG,
    Exercise.PLANK,
    Exercise.SIDE_PLANK,
    Exercise.PUSH_UPS,
    Exercise.PUSH_UPS_PERFECT_DEVICE,
    Exercise.SQUAT_WALKOUT,
}


class HealthTrends:
    """Creates relevant trendlines and stores the results."""

    def __init__(
        self,
        all_workouts: pd.DataFrame,
        health_metrics: pd.DataFrame,
        extrapolate_days: int = EXTRAPOLATE_DAYS,
    ):
        self.all_workouts = all_workouts
        self.health_metrics = health_metrics
        self.extrapolate_days = extrapolate_days

        self._workout_durations = None
        self._weight_trendline = None
        self._heart_rate_trendline = None

    def get_workout_durations(self) -> pd.DataFrame:
        """
        Access the n-day average workout duration, computing it if it hasn't been already.

        Note: n-day average gives a sense of whether its keeping above the recommended baseline of 150 mins/week
        """
        if self._workout_durations is None:
            data = Trendsetter.compute_n_sample_avg(self.all_workouts, CName.DURATION, N_DAYS_TO_AVG)
            column_dict = {
                CName.DATE: self.all_workouts[CName.DATE],
                CName.AVG_DURATION: data,
                CName.DURATION: self.all_workouts[CName.DURATION],
            }
            self._workout_durations = pd.DataFrame(column_dict)
        return self._workout_durations

    def get_weight_trendline(self) -> pd.DataFrame:
        """Access the linear trend of weight over time, first computing it if needed."""
        if self._weight_trendline is None:
            cname = CName.WEIGHT
            data = Trendsetter.get_line_of_best_fit(self.health_metrics, cname, self.extrapolate_days)
            self._weight_trendline = pd.DataFrame({CName.DATE: self.get_padded_dates(cname), cname: data})
        return self._weight_trendline

    def get_heart_rate_trendline(self) -> pd.DataFrame:
        """Access the logarithmic curve of best fit of resting heart rate over time, first computing it if needed."""
        if self._heart_rate_trendline is None:
            cname = CName.RESTING_HEART_RATE
            data = Trendsetter.get_logarithmic_curve_of_best_fit(self.health_metrics, cname, self.extrapolate_days)
            self._heart_rate_trendline = pd.DataFrame({CName.DATE: self.get_padded_dates(cname), cname: data})
        return self._heart_rate_trendline

    def get_padded_dates(self, c_name: ColumnName) -> pd.DataFrame:
        nonnulls = self.health_metrics[self.health_metrics[c_name].notna()]
        return get_padded_dates(nonnulls, self.extrapolate_days)

    @staticmethod
    def _save_data(data: pd.DataFrame, fname: str) -> None:
        """Save the given data, print an error if it fails."""
        if data is not None:
            data.to_csv(f"{PREDS_DIR}/{fname}", index=False)
        else:
            TermColour.print_error(f"Data not saved to: {fname}, it was missing.")

    def save_predictions(self) -> None:
        """Save all available predictions to disk."""
        HealthTrends._save_data(data=self.get_workout_durations(), fname="avg_workout_durations.csv")
        HealthTrends._save_data(data=self.get_heart_rate_trendline(), fname="resting_heart_rate_trendline.csv")
        HealthTrends._save_data(data=self.get_weight_trendline(), fname="weight_trendline.csv")


def build_health_visuals(health_trends: HealthTrends) -> None:
    options = PlotOptions(export_dir=ROOT_IMG_DIR, show_plot=False)
    plot_workout_frequency(health_trends.get_workout_durations(), N_DAYS_TO_AVG, options)
    plot_resting_heart_rate(health_trends.health_metrics, health_trends.get_heart_rate_trendline(), options)
    plot_weight(health_trends.health_metrics, health_trends.get_weight_trendline(), options)


def build_strength_visuals(workouts: pd.DataFrame, sets: pd.DataFrame) -> None:
    num_workers = 5 * os.cpu_count()  # Should be a little faster if hyperthreading is enabled
    with Pool(num_workers) as p:
        partial_plot_strength = partial(plot_single_strength_visual, workouts=workouts, sets=sets)
        p.map(partial_plot_strength, sets[CName.EXERCISE].unique())


def plot_single_strength_visual(exercise: str, workouts: pd.DataFrame, sets: pd.DataFrame) -> None:
    if exercise in SKIP_EXERCISE_PLOT_EXERCISES:
        print(f"Manually skipping {exercise}.")
        return

    print(f"Plotting {exercise}... ", end="")
    try:
        options = PlotOptions(export_dir=ROOT_IMG_DIR, show_plot=False)
        plot_strength_over_time(
            workouts,
            sets,
            exercise,
            PRIMARY_GYMS,
            options,
        )
        print("done.")
    except ValueError as ve:
        TermColour.print_warning(f"SKIPPED: {ve}.")


def main() -> None:
    # Load data
    health_metrics = DataLoader.load_health_metrics(ROOT_DATA_DIR)
    travel_days = DataLoader.load_travel_days(ROOT_DATA_DIR)
    walk_workouts = DataLoader.load_walk_workouts(ROOT_DATA_DIR)
    run_workouts = DataLoader.load_run_workouts(ROOT_DATA_DIR)
    bike_workouts = DataLoader.load_bike_workouts(ROOT_DATA_DIR)
    row_workouts = DataLoader.load_row_workouts(ROOT_DATA_DIR)
    stair_workouts = DataLoader.load_stair_workouts(ROOT_DATA_DIR)
    cardio_workouts = [
        walk_workouts,
        run_workouts,
        bike_workouts,
        row_workouts,
        stair_workouts,
    ]
    weight_training_workouts = DataLoader.load_weight_training_workouts(ROOT_DATA_DIR)
    weight_training_sets = DataLoader.load_weight_training_sets(ROOT_DATA_DIR)
    cardio_workouts = DataLoader.merge_cardio_workouts(cardio_workouts)
    all_workouts = DataLoader.load_all_workouts(cardio_workouts, weight_training_workouts, travel_days)

    # Build the graphs, save the predictions
    health_trends = HealthTrends(all_workouts, health_metrics)
    build_health_visuals(health_trends)
    build_strength_visuals(weight_training_workouts, weight_training_sets)
    health_trends.save_predictions()


if __name__ == "__main__":
    main()
