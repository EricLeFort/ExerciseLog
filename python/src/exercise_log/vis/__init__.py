from datetime import date
from typing import Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import ticker

from exercise_log.constants import MIN_DAILY_ACTIVE_MINUTES
from exercise_log.dataloader import ColumnName
from exercise_log.strength import SetRating, SetType
from exercise_log.strength.ontology import ExerciseInfo
from exercise_log.utils import convert_mins_to_hour_mins, convert_pd_to_np, get_padded_dates
from exercise_log.vis.constants import BOTTOM_OFFSET, NON_GRAPH_AREA_SCALER, RIGHT_OF_AXIS_X_COORD
from exercise_log.vis.utils import configure_x_axis_by_month, create_legend_and_title

WEIGHT_LEVELS = {
    "Healthy": 250,
    "Target": 200,
}
RESTING_HEART_RATE_LEVELS = {
    "Poor": 82,
    "Average": 72,
    "Above Average": 68,
    "Good": 63,
    "Excellent": 58,
    "Athlete": 50,
}


def plot_workout_frequency(
    all_workouts: pd.DataFrame,
    n_day_avg_workout_duration: pd.DataFrame,
    n_days_to_avg: int,
    export_dir: Optional[str] = None,
    show_plot=True,
):
    non_graph_gcf_percent = 0.1
    workout_frequency_bottom_offset = 0.03
    y_min, y_max = 0, 180  # Setting a 3 hour max since there's a few backpacking days that mess up the scale

    # Draw the main graph contents and setup the axes
    workout_durations_mins = all_workouts[ColumnName.DURATION] // 60
    plt.scatter(
        all_workouts[ColumnName.DATE],
        workout_durations_mins,
        s=5,
        label="Workout Duration",
    )
    plt.plot(
        convert_pd_to_np(all_workouts[ColumnName.DATE]),
        convert_pd_to_np(n_day_avg_workout_duration // 60),
        label=f"{n_days_to_avg}-Day Avg Daily Duration",
    )

    # Delineate the ideal minimum daily exercise threshold as a horizontal reference line
    plt.axhline(y=MIN_DAILY_ACTIVE_MINUTES, color="r", linestyle="-")
    y_percent_min_daily_active = (MIN_DAILY_ACTIVE_MINUTES / y_max) - workout_frequency_bottom_offset
    y_pos = y_percent_min_daily_active + non_graph_gcf_percent
    plt.gcf().text(RIGHT_OF_AXIS_X_COORD, y_pos, "Target\nMinimum")

    # Set up axes
    ax = plt.gca()
    configure_x_axis_by_month(all_workouts)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(convert_mins_to_hour_mins))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.set_ylim([y_min, y_max])
    plt.grid(visible=True)
    plt.grid(visible=True, which="minor", linestyle="--", linewidth="0.25")

    # Scale up the plot
    plt.gcf().set_size_inches(15, 9)

    # Add in the surrounding information
    create_legend_and_title("Workout Frequency", reverse_labels=True)
    if export_dir:
        plt.savefig(f"{export_dir}/workout_frequency.png", bbox_inches="tight")
    if show_plot:
        plt.show()
    plt.clf()


def plot_resting_heart_rate(
    all_workouts: pd.DataFrame,
    health_metrics: pd.DataFrame,
    heart_rate_trendline: np.ndarray,
    n_days_to_extrapolate: int,
    export_dir: Optional[str] = None,
    show_plot=True,
):  # pylint: disable=too-many-arguments
    y_min, y_max = 45, 90

    nonnull_heart_rates = health_metrics[health_metrics[ColumnName.RESTING_HEART_RATE].notnull()]
    padded_dates = get_padded_dates(nonnull_heart_rates, n_days_to_extrapolate)
    plt.scatter(
        nonnull_heart_rates[ColumnName.DATE].to_numpy(),
        nonnull_heart_rates[ColumnName.RESTING_HEART_RATE].to_numpy(),
        s=5,
        label="Resting HR",
    )
    plt.plot(
        padded_dates.to_numpy(),
        heart_rate_trendline,
        linestyle="--",
        label="Projected Resting HR",
    )

    # Delineate various resting heart rate levels as horizontal reference lines
    for text, hr in RESTING_HEART_RATE_LEVELS.items():
        plt.axhline(y=hr, color="k", linestyle="--", linewidth="0.75")
        y_range = y_max - y_min
        y_pos = BOTTOM_OFFSET + (hr - y_min) / (NON_GRAPH_AREA_SCALER * y_range)
        plt.gcf().text(RIGHT_OF_AXIS_X_COORD, y_pos, text)

    # Set up axes
    ax = plt.gca()
    configure_x_axis_by_month(all_workouts, end_padding_days=n_days_to_extrapolate)
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.set_ylim([y_min, y_max])
    plt.grid(visible=True)
    plt.grid(visible=True, which="minor", linestyle="--", linewidth="0.25")

    # Scale up the plot
    plt.gcf().set_size_inches(15, 9)

    # Add in the surrounding information
    create_legend_and_title("Resting Heart Rate", reverse_labels=True)
    if export_dir:
        plt.savefig(f"{export_dir}/resting_heart_rate.png", bbox_inches="tight")
    if show_plot:
        plt.show()
    plt.clf()


def plot_weight(
    health_metrics: pd.DataFrame,
    weight_trendline: np.ndarray,
    n_days_to_extrapolate: int,
    export_dir: Optional[str] = None,
    show_plot=True,
):
    y_min, y_max = 180, 305

    nonnull_weights = health_metrics[health_metrics[ColumnName.WEIGHT].notnull()]
    padded_dates = get_padded_dates(nonnull_weights, n_days_to_extrapolate)
    plt.scatter(
        nonnull_weights[ColumnName.DATE].to_numpy(),
        nonnull_weights[ColumnName.WEIGHT].to_numpy(),
        s=5,
        label="Weight",
    )
    plt.plot(
        padded_dates.to_numpy(),
        weight_trendline,
        linestyle="--",
        label="Projected Weight",
    )

    # Delineate various resting heart rate levels as horizontal reference lines
    for text, weight in WEIGHT_LEVELS.items():
        plt.axhline(y=weight, color="k", linestyle="--", linewidth="0.75")
        y_range = y_max - y_min
        y_pos = BOTTOM_OFFSET + (weight - y_min) / (NON_GRAPH_AREA_SCALER * y_range)
        plt.gcf().text(RIGHT_OF_AXIS_X_COORD, y_pos, text)

    # Set up axes
    ax = plt.gca()
    configure_x_axis_by_month(nonnull_weights, end_padding_days=n_days_to_extrapolate)
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.set_ylim([y_min, y_max])
    plt.grid(visible=True)
    plt.grid(visible=True, which="minor", linestyle="--", linewidth="0.25")

    # Scale up the plot
    plt.gcf().set_size_inches(18.5, 10.5)

    # Add in the surrounding information
    create_legend_and_title("Weight", reverse_labels=True)
    if export_dir:
        plt.savefig(f"{export_dir}/weight.png", bbox_inches="tight")
    if show_plot:
        plt.show()
    plt.clf()


def plot_strength_over_time(
    workouts: pd.DataFrame,
    weight_training_sets: pd.DataFrame,
    exercise: str,
    primary_gyms: Dict[str, Tuple[date, date]],
    export_dir: Optional[str] = None,
    show_plot=True,
):  # pylint: disable=too-many-arguments
    single_exercise = weight_training_sets[weight_training_sets[ColumnName.EXERCISE] == exercise]
    for set_type in SetType:
        rep_range = set_type.get_rep_range()
        sets = single_exercise[
            (rep_range[0] <= single_exercise[ColumnName.REPS]) & (single_exercise[ColumnName.REPS] <= rep_range[1])
        ]

        # Filter out sets with ratings that should be ignored
        sets = sets[sets[ColumnName.RATING] != SetRating.WARMUP]
        sets = sets[~sets[ColumnName.RATING].str.startswith(SetRating.BAD)]
        sets = sets[~sets[ColumnName.RATING].str.startswith(SetRating.FAILURE)]
        sets = sets[sets[ColumnName.RATING] != SetRating.FUN]
        sets = sets[sets[ColumnName.RATING] != SetRating.DELOAD]

        # Filter out sets using machines in non-primary gyms
        workouts = workouts[workouts[ColumnName.LOCATION].isin(primary_gyms)]
        # TODO also filter out sets that are from a primary gym but *not* in the time period when it was primary
        sets = sets[
            sets[ColumnName.DATE].isin(workouts[ColumnName.DATE])
            | ~sets[ColumnName.EXERCISE].apply(lambda exercise: ExerciseInfo(exercise).requires_machine)
        ]
        sets = sets[sets[ColumnName.DATE].isin(workouts[ColumnName.DATE])]

        # Filter to only the max weight set of this type for that day
        idx = sets.groupby(ColumnName.DATE)[ColumnName.WEIGHT].idxmax()
        sets = sets.loc[idx]

        # Only bother with plotting when there's 3+ sets available
        if len(sets) > 2:
            final_row = pd.DataFrame(
                {
                    ColumnName.DATE: [workouts[ColumnName.DATE].max()],
                    ColumnName.WEIGHT: [sets[ColumnName.WEIGHT].iloc[-1]],
                }
            )
            sets = pd.concat([sets, final_row], ignore_index=True)
            plt.scatter(
                sets[ColumnName.DATE],
                sets[ColumnName.WEIGHT],
                s=2,
                label=set_type,
            )
            plt.step(
                sets[ColumnName.DATE].to_numpy(),
                sets[ColumnName.WEIGHT].to_numpy(),
                where="post",
            )

    # All of the set types were skipped due to insufficient data, skip this plot entirely
    if not plt.gca().has_data():
        raise ValueError("Not enough good sets")

    # Set up axes
    ax = plt.gca()
    configure_x_axis_by_month(workouts)
    chunk_of_range = (single_exercise[ColumnName.WEIGHT].max() - single_exercise[ColumnName.WEIGHT].min()) / 20
    y_step = max(1, round(chunk_of_range / 10) * 10)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5 * y_step))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(y_step))
    plt.grid(visible=True)
    plt.grid(visible=True, which="minor", linestyle="--", linewidth="0.25")

    # Add in the surrounding information
    create_legend_and_title(exercise, reverse_labels=True)
    if export_dir:
        plt.savefig(f"{export_dir}/strength/{exercise}.png", bbox_inches="tight")
    if show_plot:
        plt.show()
    plt.clf()
