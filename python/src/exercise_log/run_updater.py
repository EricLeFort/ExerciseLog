from datetime import date

import pandas as pd

from exercise_log.dataloader import CName, ColumnName, DataLoader
from exercise_log.strength import Exercise
from exercise_log.trend import Trendsetter
from exercise_log.utils import TermColour, get_padded_dates
from exercise_log.vis import plot_resting_heart_rate, plot_strength_over_time, plot_weight, plot_workout_frequency

ROOT_DATA_DIR = "data"
ROOT_IMG_DIR = "img"
PREDS_DIR = f"{ROOT_DATA_DIR}/preds"
EXTRAPOLATE_DAYS = 100
N_DAYS_TO_AVG = 28

PRIMARY_GYMS = {
    "Via 6 Gym": (date(year=2022, month=12, day=4), date.today()),
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
    """Creates relevant trendlines and stores the results"""

    def __init__(self, all_workouts: pd.DataFrame, health_metrics: pd.DataFrame):
        self.all_workouts = all_workouts
        self.health_metrics = health_metrics

        self._avg_workout_duration = None
        self._weight_trendline = None
        self._heart_rate_trendline = None

    def get_avg_workout_duration(self):
        """
        Returns the n-day average workout duration, computing it if it hasn't been already.

        Note: n-day average gives a sense of whether its keeping above the recommended baseline of 150 mins/week
        """
        if self._avg_workout_duration is None:
            self._avg_workout_duration = Trendsetter.compute_n_sample_avg(
                self.all_workouts,
                CName.DURATION,
                N_DAYS_TO_AVG,
            )
        return self._avg_workout_duration

    def get_weight_trendline(self):
        """Returns the linear trend of weight over time, first computing it if needed."""
        if self._weight_trendline is None:
            self._weight_trendline = Trendsetter.get_line_of_best_fit(
                self.health_metrics,
                CName.WEIGHT,
                EXTRAPOLATE_DAYS,
            )
        return self._weight_trendline

    def get_heart_rate_trendline(self):
        """Returns the logarithmic curve of best fit of resting heart rate over time, first computing it if needed."""
        if self._heart_rate_trendline is None:
            self._heart_rate_trendline = Trendsetter.get_logarithmic_curve_of_best_fit(
                self.health_metrics,
                CName.RESTING_HEART_RATE,
                EXTRAPOLATE_DAYS,
            )
        return self._heart_rate_trendline

    def get_padded_dates(self, c_name: ColumnName):
        nonnulls = self.health_metrics[self.health_metrics[c_name].notnull()]
        return get_padded_dates(nonnulls, EXTRAPOLATE_DAYS)

    @staticmethod
    def _save_data(data: pd.DataFrame, dates: pd.DataFrame, c_name: str, fname: str):
        """Just a simple wrapper around some repeated functionality"""
        if data is not None:
            df = pd.DataFrame({CName.DATE: dates, c_name: data})
            df.to_csv(f"{PREDS_DIR}/{fname}", index=False)

    def save_predictions(self):
        """Save all available predictions to disk."""
        HealthTrends._save_data(
            data=self.get_avg_workout_duration(),
            dates=self.all_workouts[CName.DATE],
            c_name=CName.DURATION,
            fname="avg_workout_durations.csv",
        )
        HealthTrends._save_data(
            data=self.get_heart_rate_trendline(),
            dates=self.get_padded_dates(CName.RESTING_HEART_RATE),
            c_name=CName.RESTING_HEART_RATE,
            fname="resting_heart_rate_trendline.csv",
        )
        HealthTrends._save_data(
            data=self.get_weight_trendline(),
            dates=self.get_padded_dates(CName.WEIGHT),
            c_name=CName.WEIGHT,
            fname="weight_trendline.csv",
        )


def build_health_visuals(health_trends: HealthTrends):
    plot_workout_frequency(
        health_trends.all_workouts,
        health_trends.get_avg_workout_duration(),
        N_DAYS_TO_AVG,
        export_dir=ROOT_IMG_DIR,
        show_plot=False,
    )
    plot_resting_heart_rate(
        health_trends.all_workouts,
        health_trends.health_metrics,
        health_trends.get_heart_rate_trendline(),
        EXTRAPOLATE_DAYS,
        export_dir=ROOT_IMG_DIR,
        show_plot=False,
    )
    plot_weight(
        health_trends.health_metrics,
        health_trends.get_weight_trendline(),
        EXTRAPOLATE_DAYS,
        export_dir=ROOT_IMG_DIR,
        show_plot=False,
    )


def build_strength_visuals(weight_training_workouts: pd.DataFrame, weight_training_sets: pd.DataFrame):
    weight_training_sets = DataLoader.load_weight_training_sets(ROOT_DATA_DIR)
    for exercise in weight_training_sets[CName.EXERCISE].unique():
        if exercise in SKIP_EXERCISE_PLOT_EXERCISES:
            print(f"Manually skipping {exercise}.")
            continue
        print(f"Plotting {exercise}... ", end="")
        try:
            plot_strength_over_time(
                weight_training_workouts,
                weight_training_sets,
                exercise,
                PRIMARY_GYMS,
                export_dir=ROOT_IMG_DIR,
                show_plot=False,
            )
            print("done.")
        except ValueError as ve:
            TermColour.print_warning(f"SKIPPED: {str(ve)}.")


def main():
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
