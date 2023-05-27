import numpy as np

from exercise_log.constants import *
from exercise_log.dataloader import DataLoader
from exercise_log.trend import Trendsetter
from exercise_log.utils import TermColour
from exercise_log.vis import plot_resting_heart_rate, plot_strength_over_time, plot_weight, plot_workout_frequency

ROOT_DATA_DIR = "data"
ROOT_IMG_DIR = "img"
EXTRAPOLATE_DAYS = 100
N_DAYS_TO_AVG = 8

def main():
    # Load data
    health_metrics = DataLoader.load_health_metrics(ROOT_DATA_DIR)
    travel_days = DataLoader.load_travel_days(ROOT_DATA_DIR)
    cardio_workouts = DataLoader.load_cardio_workouts(ROOT_DATA_DIR)
    weight_training_workouts = DataLoader.load_weight_training_workouts(ROOT_DATA_DIR)
    weight_training_sets = DataLoader.load_weight_training_sets(ROOT_DATA_DIR)
    all_workouts = DataLoader.load_all_workouts(cardio_workouts, weight_training_workouts, travel_days)

    # Fit relevant trendlines and plot data
    # n-day average over a week gives a sense of if I'm keeping above a relatively low baseline of 150 minutes/week
    n_day_avg_workout_duration = Trendsetter.compute_n_sample_avg(all_workouts, DURATION, N_DAYS_TO_AVG)
    weight_trendline = Trendsetter.fit_linear(health_metrics, WEIGHT, EXTRAPOLATE_DAYS)
    heart_rate_trendline = Trendsetter.fit_logarithmic(health_metrics, RESTING_HEART_RATE, EXTRAPOLATE_DAYS)
    plot_workout_frequency(all_workouts, n_day_avg_workout_duration, N_DAYS_TO_AVG, export_dir=ROOT_IMG_DIR, show_plot=False)
    plot_resting_heart_rate(all_workouts, health_metrics, heart_rate_trendline, EXTRAPOLATE_DAYS, export_dir=ROOT_IMG_DIR, show_plot=False)
    plot_weight(all_workouts, health_metrics, weight_trendline, EXTRAPOLATE_DAYS, export_dir=ROOT_IMG_DIR, show_plot=False)

    for exercise in weight_training_sets[EXERCISE].unique():
        print(f"Plotting {exercise}... ", end="")
        try:
            plot_strength_over_time(all_workouts, weight_training_sets, exercise, export_dir=ROOT_IMG_DIR, show_plot=False)
            print("done.")
        except ValueError as ve:
            TermColour.print_warning(f"SKIPPED: {str(ve)}.")


if __name__ == "__main__":
    main()
