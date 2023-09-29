import numpy as np

from exercise_log.dataloader import DataLoader, ColumnName
from exercise_log.strength import Exercise
from exercise_log.trend import Trendsetter
from exercise_log.utils import TermColour
from exercise_log.vis import plot_resting_heart_rate, plot_strength_over_time, plot_weight, plot_workout_frequency

ROOT_DATA_DIR = "data"
ROOT_IMG_DIR = "img"
EXTRAPOLATE_DAYS = 100
N_DAYS_TO_AVG = 28

SKIP_EXERCISE_PLOTS = {
    Exercise.FIFTH_POINT_OF_FLIGHT,
    Exercise.BURPEES,
    Exercise.DEFICIT_PUSH_UPS,
    Exercise.JUMPING_JACKS,
    Exercise.LEG_RAISE,
    Exercise.LAT_PULLDOWN_HANG,
    Exercise.PLANK,
    Exercise.SIDE_PLANK,
    Exercise.PUSH_UPS,
    Exercise.PUSH_UPS_PERFECT_DEVICE,
}

def main():
    # Load data
    health_metrics = DataLoader.load_health_metrics(ROOT_DATA_DIR)
    travel_days = DataLoader.load_travel_days(ROOT_DATA_DIR)
    walk_workouts = DataLoader.load_walk_workouts(ROOT_DATA_DIR)
    run_workouts = DataLoader.load_run_workouts(ROOT_DATA_DIR)
    bike_workouts = DataLoader.load_bike_workouts(ROOT_DATA_DIR)
    cardio_workouts = DataLoader.merge_cardio_workouts([walk_workouts, run_workouts, bike_workouts])
    weight_training_workouts = DataLoader.load_weight_training_workouts(ROOT_DATA_DIR)
    weight_training_sets = DataLoader.load_weight_training_sets(ROOT_DATA_DIR)
    all_workouts = DataLoader.load_all_workouts(cardio_workouts, weight_training_workouts, travel_days)

    # Fit relevant trendlines and plot data
    # n-day average over a week gives a sense of if I'm keeping above a relatively low baseline of 150 minutes/week
    n_day_avg_workout_duration = Trendsetter.compute_n_sample_avg(all_workouts, ColumnName.DURATION, N_DAYS_TO_AVG)
    weight_trendline = Trendsetter.get_line_of_best_fit(health_metrics, ColumnName.WEIGHT, EXTRAPOLATE_DAYS)
    heart_rate_trendline = Trendsetter.get_logarithmic_curve_of_best_fit(health_metrics, ColumnName.RESTING_HEART_RATE, EXTRAPOLATE_DAYS)
    plot_workout_frequency(all_workouts, n_day_avg_workout_duration, N_DAYS_TO_AVG, export_dir=ROOT_IMG_DIR, show_plot=False)
    plot_resting_heart_rate(all_workouts, health_metrics, heart_rate_trendline, EXTRAPOLATE_DAYS, export_dir=ROOT_IMG_DIR, show_plot=False)
    plot_weight(all_workouts, health_metrics, weight_trendline, EXTRAPOLATE_DAYS, export_dir=ROOT_IMG_DIR, show_plot=False)

    for exercise in weight_training_sets[ColumnName.EXERCISE].unique():
        if exercise in SKIP_EXERCISE_PLOTS:
            print(f"Manually skipping {exercise}.")
            continue
        print(f"Plotting {exercise}... ", end="")
        try:
            plot_strength_over_time(all_workouts, weight_training_sets, exercise, export_dir=ROOT_IMG_DIR, show_plot=False)
            print("done.")
        except ValueError as ve:
            TermColour.print_warning(f"SKIPPED: {str(ve)}.")


if __name__ == "__main__":
    main()
