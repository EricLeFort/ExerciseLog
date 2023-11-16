from datetime import timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from exercise_log.constants import DATE
from exercise_log.vis.constants import ABOVE_TABLE


def show_gcf_corners(plot: plt):
    """Shows the corners of the current plot by displaying x's"""
    plot.gcf().text(0, 0, "x")
    plot.gcf().text(1, 0, "x")
    plot.gcf().text(0, 1, "x")
    plot.gcf().text(1, 1, "x")


def configure_x_axis_by_month(all_workouts: pd.DataFrame, start_padding_days: int = 1, end_padding_days: int = 1):
    """Sets the current axes x-axis to major tick by month, minor tick on Sundays, and have MMM-YYYY major labels."""
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.SU))
    plt.xlim(
        all_workouts[DATE][0] - timedelta(days=start_padding_days),
        all_workouts[DATE].tail(1) + timedelta(days=end_padding_days),
    )


def create_legend_and_title(title: str, reverse_labels: bool = False, ncol: int = 2):
    """Adds a legend and title centered above the current plot"""
    plt.title(title, y=ABOVE_TABLE)
    handles, labels = plt.gca().get_legend_handles_labels()
    if reverse_labels:
        handles, labels = handles[::-1], labels[::-1]
    plt.legend(handles, labels, bbox_to_anchor=(0.5, ABOVE_TABLE), loc="upper center", frameon=False, ncol=ncol)
