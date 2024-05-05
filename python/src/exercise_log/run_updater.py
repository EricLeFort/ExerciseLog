"""Orchestrates the process of adding a workout."""

import datetime
import os
from functools import partial
from multiprocessing import Pool

import pandas as pd

from exercise_log.dataloader import CName, DataBox
from exercise_log.strength import Exercise
from exercise_log.trend import HealthTrends
from exercise_log.utils import TermColour
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


def build_health_visuals(health_trends: HealthTrends) -> None:
    """Build and save health metric visuals including workout frequency, resting heart rate, and weight."""
    options = PlotOptions(export_dir=ROOT_IMG_DIR, show_plot=False)
    print("Plotting workout frequency..")
    plot_workout_frequency(health_trends.get_workout_durations(), N_DAYS_TO_AVG, options)
    print("Plotting resting heart rate..")
    plot_resting_heart_rate(health_trends.health_metrics, health_trends.get_heart_rate_trendline(), options)
    print("Plotting weight..")
    plot_weight(health_trends.health_metrics, health_trends.get_weight_trendline(), options)
    print("Done plotting health metrics.")


def build_strength_visuals(workouts: pd.DataFrame, sets: pd.DataFrame) -> None:
    """Build and save the strength metric visuals for each individual exercise. Runs them in parallel."""
    num_workers = 5 * os.cpu_count()  # Should be a little faster if hyperthreading is enabled
    with Pool(num_workers) as p:
        partial_plot_strength = partial(plot_single_strength_visual, workouts=workouts, sets=sets)
        print("Loading strength sets data..")
        p.map(partial_plot_strength, sets[CName.EXERCISE].unique())
    print("Done plotting strength metrics.")


def plot_single_strength_visual(exercise: str, workouts: pd.DataFrame, sets: pd.DataFrame) -> None:
    """Plot the strength metric visual for the given exercise."""
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
    """Execute the data loading to metric visualization pipeline."""
    # Load data, build graphs, make predictions, save results
    databox = DataBox(ROOT_DATA_DIR)
    health_trends = HealthTrends(databox.get_all_workouts(), databox.get_health_metrics(), PREDS_DIR)
    build_health_visuals(health_trends)
    build_strength_visuals(databox.get_weight_training_workouts(), databox.get_weight_training_sets())
    health_trends.save_predictions()


if __name__ == "__main__":
    main()
