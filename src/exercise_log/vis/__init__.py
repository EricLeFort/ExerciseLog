import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from typing import Optional

from exercise_log.constants import (
    DATE,
    DURATION,
    EXERCISE,
    MIN_DAILY_ACTIVE_MINUTES,
    RATING,
    REPS,
    RESTING_HEART_RATE,
    SET_TYPE_TO_REP_RANGE,
    WARMUP,
    WEIGHT,
)
from exercise_log.utils import convert_mins_to_hour_mins, convert_pd_to_np, get_padded_dates
from exercise_log.vis.constants import BOTTOM_OFFSET, RIGHT_OF_AXIS_X_COORD, NON_GRAPH_AREA_SCALER
from exercise_log.vis.utils import configure_x_axis_by_month, create_legend_and_title


def plot_workout_frequency(
    all_workouts: pd.DataFrame,
    n_day_avg_workout_duration: pd.DataFrame,
    n_days_to_avg: int,
    export_dir: Optional[str] = None,
    show_plot=True,
):
    NON_GRAPH_GCF_PERCENT = 0.1

    # Draw the main graph contents and setup the axes
    workout_durations_mins = all_workouts[DURATION] // 60
    plt.scatter(
        all_workouts[DATE],
        workout_durations_mins,
        s=5,
        label="Workout Duration",
    )
    plt.plot(
        convert_pd_to_np(all_workouts[DATE]),
        convert_pd_to_np(n_day_avg_workout_duration // 60),
        label=f"{n_days_to_avg}-Day Avg Daily Duration",
    )

    # Delineate the ideal minimum daily exercise threshold as a horizontal reference line
    plt.axhline(y=MIN_DAILY_ACTIVE_MINUTES, color='r', linestyle='-')
    y_percent_min_daily_active = MIN_DAILY_ACTIVE_MINUTES / max(workout_durations_mins)
    y_pos = y_percent_min_daily_active + NON_GRAPH_GCF_PERCENT
    plt.gcf().text(RIGHT_OF_AXIS_X_COORD, y_pos, "Target\nMinimum")

    # Set up axes
    ax = plt.gca()
    configure_x_axis_by_month(all_workouts)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(convert_mins_to_hour_mins))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    plt.grid(visible=True)
    plt.grid(visible=True, which="minor", linestyle="--", linewidth="0.25")

    # Scale up the plot
    fig = plt.gcf()
    fig.set_size_inches(15, 9)

    # Add in the surrounding information
    create_legend_and_title("Workout Frequency", reverse_labels=True)
    if export_dir:
        plt.savefig(f"{export_dir}/workout_frequency.png", bbox_inches="tight")
    if show_plot:
        plt.show()

def plot_resting_heart_rate(
    all_workouts: pd.DataFrame,
    health_metrics: pd.DataFrame,
    heart_rate_trendline: np.ndarray,
    n_days_to_extrapolate: int,
    export_dir: Optional[str] = None,
    show_plot=True,
):
    Y_MIN, Y_MAX = 45, 90

    nonnull_heart_rates = health_metrics[health_metrics[RESTING_HEART_RATE].notnull()]
    padded_dates = get_padded_dates(nonnull_heart_rates, n_days_to_extrapolate)
    plt.scatter(
        nonnull_heart_rates[DATE].to_numpy(),
        nonnull_heart_rates[RESTING_HEART_RATE].to_numpy(),
        s=5,
        label="Resting HR"
    )
    plt.plot(
        padded_dates.to_numpy(),
        heart_rate_trendline,
        linestyle="--",
        label="Projected Resting HR"
    )

    # Delineate various resting heart rate levels as horizontal reference lines
    resting_heart_rate_levels = {
        "Average": 72,
        "Above Average": 68,
        "Good": 63,
        "Excellent": 58,
        "Athlete": 50,
    }
    for text, hr in resting_heart_rate_levels.items():
        plt.axhline(y=hr, color='k', linestyle='--', linewidth="0.75")
        y_range = Y_MAX - Y_MIN
        y_pos = BOTTOM_OFFSET + (hr - Y_MIN) / (NON_GRAPH_AREA_SCALER*y_range)
        plt.gcf().text(RIGHT_OF_AXIS_X_COORD, y_pos, text)

    # Set up axes
    ax = plt.gca()
    configure_x_axis_by_month(all_workouts, end_padding_days=n_days_to_extrapolate)
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.set_ylim([Y_MIN, Y_MAX])
    plt.grid(visible=True)
    plt.grid(visible=True, which="minor", linestyle="--", linewidth="0.25")

    # Scale up the plot
    fig = plt.gcf()
    fig.set_size_inches(15, 9)

    # Add in the surrounding information
    create_legend_and_title("Resting Heart Rate", reverse_labels=True)
    if export_dir:
        plt.savefig(f"{export_dir}/resting_heart_rate.png", bbox_inches="tight")
    if show_plot:
        plt.show()


def plot_weight(
    all_workouts: pd.DataFrame,
    health_metrics: pd.DataFrame,
    weight_trendline: np.ndarray,
    n_days_to_extrapolate: int,
    export_dir: Optional[str] = None,
    show_plot=True,
):
    Y_MIN, Y_MAX = 180, 300

    nonnull_weights = health_metrics[health_metrics[WEIGHT].notnull()]
    padded_dates = get_padded_dates(nonnull_weights, n_days_to_extrapolate)
    plt.scatter(
        nonnull_weights[DATE].to_numpy(),
        nonnull_weights[WEIGHT].to_numpy(),
        s=5,
        label="Weight"
    )
    plt.plot(
        padded_dates.to_numpy(),
        weight_trendline,
        linestyle="--",
        label="Projected Weight"
    )

    # Delineate various resting heart rate levels as horizontal reference lines
    weight_levels = {
        "Healthy": 250,
        "Target": 200,
    }
    for text, weight in weight_levels.items():
        plt.axhline(y=weight, color='k', linestyle='--', linewidth="0.75")
        y_range = Y_MAX - Y_MIN
        y_pos = BOTTOM_OFFSET + (weight - Y_MIN) / (NON_GRAPH_AREA_SCALER*y_range)
        plt.gcf().text(RIGHT_OF_AXIS_X_COORD, y_pos, text)

    # Set up axes
    ax = plt.gca()
    configure_x_axis_by_month(all_workouts, end_padding_days=n_days_to_extrapolate)
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.set_ylim([Y_MIN, Y_MAX])
    plt.grid(visible=True)
    plt.grid(visible=True, which="minor", linestyle="--", linewidth="0.25")

    # Scale up the plot
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)

    # Add in the surrounding information
    create_legend_and_title("Weight", reverse_labels=True)
    if export_dir:
        plt.savefig(f"{export_dir}/weight.png", bbox_inches="tight")
    if show_plot:
        plt.show()



def plot_strength_over_time(
    all_workouts: pd.DataFrame,
    weight_training_sets: pd.DataFrame,
    exercise: str,
    export_dir: Optional[str] = None,
    show_plot=True,
):
    final_date = all_workouts[DATE].max()
    single_exercise = weight_training_sets[weight_training_sets[EXERCISE] == exercise]
    for set_type, rep_range in SET_TYPE_TO_REP_RANGE.items():
        sets = single_exercise[(rep_range[0] <= single_exercise[REPS]) & (single_exercise[REPS] <= rep_range[1])]

        # TODO filter out sets that shouldn't be counted (e.g. Leg Press from Earnscliffe rec center)
        # Filter to only the max weight set of this type for that day
        idx = sets.groupby(DATE)[WEIGHT].idxmax()
        sets = sets.loc[idx]

        # Filter out warmup sets
        sets = sets[sets[RATING] != WARMUP]

        if not sets.empty:
            last_weight = sets[WEIGHT].iloc[-1]
            sets = sets.append({DATE: final_date, WEIGHT: last_weight}, ignore_index=True)
            plt.scatter(
                sets[DATE],
                sets[WEIGHT],
                s=2,
                label=set_type,
            )
            plt.step(
                sets[DATE].to_numpy(),
                sets[WEIGHT].to_numpy(),
                where="post",
            )

    # Set up axes
    ax = plt.gca()
    configure_x_axis_by_month(all_workouts)
    chunk_of_range = (single_exercise[WEIGHT].max() - single_exercise[WEIGHT].min()) / 20
    y_step = max(1, round(chunk_of_range / 10) * 10)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5 * y_step))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(y_step))
    plt.grid(visible=True)
    plt.grid(visible=True, which="minor", linestyle="--", linewidth="0.25")

    # Add in the surrounding information
    if export_dir:
        plt.savefig(f"{export_dir}/strength/{exercise}.png", bbox_inches="tight")
    if show_plot:
        plt.show()
