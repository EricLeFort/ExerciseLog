from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Self

import numpy as np
import pandas as pd
from scipy.ndimage import uniform_filter1d
from scipy.optimize import curve_fit

from exercise_log.dataloader import CName
from exercise_log.utils import TermColour, get_padded_dates

EXTRAPOLATE_DAYS = 100
MIN_DAILY_ACTIVE_MINUTES = 22.5  # Weekly is 150, this is about 150/7
N_DAYS_TO_AVG = 8


class Trendsetter:
    @staticmethod
    def _f_log_curve(t: float, a: float, b: float, c: float) -> float:
        """Define a logaritmic function to be fit using Scipy's curve_fit (using the variables given)."""
        return a * np.log(b * t) + c

    @staticmethod
    def _f_affine(t: float, a: float, b: float) -> float:
        """Define a linear function to be fit using Scipy's curve_fit (using the variables given)."""
        return a * t + b

    @staticmethod
    def _get_curve_of_best_fit(
        df: pd.DataFrame,
        f_to_fit: Callable,
        fitted_params: tuple,
        num_days_to_extrapolate: int,
    ) -> np.ndarray:
        """Fit a trendline using the given functionm for the column specified by key in the given DataFrame."""
        padded_dates = get_padded_dates(df, num_days_to_extrapolate)
        return f_to_fit(padded_dates.index, *fitted_params).to_numpy()

    @staticmethod
    def compute_n_sample_avg(data: pd.DataFrame, field: str, n_days_to_avg: int) -> np.ndarray:
        """Compute an average over the most recent N samples."""
        return uniform_filter1d(data[field].astype("float64"), size=n_days_to_avg)

    @staticmethod
    def fit_linear(df: pd.DataFrame, field: str) -> np.ndarray:
        """
        Compute the line of best fit for the given field.

        Args:
            df (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
            field (str): The column name to fit
        Returns:
            A 2-tuple containing:
                m (float): The slope of the line of best fit
                b (float): The y-intercept of the line of best fit
        """
        (m, b), _ = curve_fit(Trendsetter._f_affine, df.index, df[field])
        return m, b

    @staticmethod
    def fit_logarithmic(df: pd.DataFrame, field: str) -> np.ndarray:
        """
        Compute the logarithmic curve of best fit for the given field.

        Args:
            df (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
            field (str): The column name to fit
        Returns:
            A 3-tuple containing a, b, and, c of the equation: a * log(b * t) + c
        """
        (a, b, c), _ = curve_fit(Trendsetter._f_log_curve, df.index, df[field])
        return a, b, c

    @staticmethod
    def get_line_of_best_fit(df: pd.DataFrame, field: str, extrapolate_days: int) -> np.ndarray:
        """
        Fit a linear trendline to the given field including padding for the number of extrapolated days.

        Args:
            df (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
            field (str): The column name to fit
            extrapolate_days (int): The number of days to extrapolate the trend until
        Returns:
            An np.ndarray of values that belong to the trendline
        """
        nonnulls = df[df[field].notna()]
        fitted_params = Trendsetter.fit_linear(nonnulls, field)
        return Trendsetter._get_curve_of_best_fit(nonnulls, Trendsetter._f_affine, fitted_params, extrapolate_days)

    @staticmethod
    def get_logarithmic_curve_of_best_fit(df: pd.DataFrame, field: str, extrapolate_days: int) -> np.ndarray:
        """
        Fit a logarithmic trendline to the given field including padding for the number of extrapolated days.

        Args:
            df (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
            field (str): The column name to fit
            extrapolate_days (int): The number of days to extrapolate the trend until
        Returns:
            An np.ndarray of values that belong to the trendline
        """
        nonnulls = df[df[field].notna()]
        fitted_params = Trendsetter.fit_logarithmic(nonnulls, field)
        return Trendsetter._get_curve_of_best_fit(nonnulls, Trendsetter._f_log_curve, fitted_params, extrapolate_days)


class HealthTrends:
    """Creates relevant trendlines and stores the results."""

    def __init__(
        self,
        all_workouts: pd.DataFrame,
        health_metrics: pd.DataFrame,
        preds_dir: str,
        extrapolate_days: int = EXTRAPOLATE_DAYS,
    ) -> None:
        """Initialize this HealthTrends using the given data. The actual trends are computed lazily."""
        self.all_workouts = all_workouts
        self.health_metrics = health_metrics
        self.extrapolate_days = extrapolate_days
        self.preds_dir = preds_dir

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

    def get_padded_dates(self, c_name: CName) -> pd.DataFrame:
        nonnulls = self.health_metrics[self.health_metrics[c_name].notna()]
        return get_padded_dates(nonnulls, self.extrapolate_days)

    def _save_data(self, data: pd.DataFrame, fname: str) -> None:
        """Save the given data, print an error if it fails."""
        if data is not None:
            data.to_csv(f"{self.preds_dir}/{fname}", index=False)
        else:
            TermColour.print_error(f"Data not saved to: {fname}, it was missing.")

    def save_predictions(self) -> None:
        """Save all available predictions to disk."""
        self._save_data(data=self.get_workout_durations(), fname="avg_workout_durations.csv")
        self._save_data(data=self.get_heart_rate_trendline(), fname="resting_heart_rate_trendline.csv")
        self._save_data(data=self.get_weight_trendline(), fname="weight_trendline.csv")


class ExerciseSummary:
    @classmethod
    def build_summary(cls, data: pd.DataFrame, start_date: date, end_date: date) -> Self:
        start_date, end_date = np.datetime64(start_date, "ns"), np.datetime64(end_date, "ns")
        data = data[start_date <= data[CName.DATE]]
        data = data[data[CName.DATE] <= end_date]
        return cls._build(data)

    @staticmethod
    def _build(data: pd.DataFrame) -> "ExerciseSummary":
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


@dataclass
class WeightTrainingSummary(ExerciseSummary):
    weight_moved: int
    set_count: int
    rep_count: int

    @staticmethod
    def _build(data: pd.DataFrame) -> "WeightTrainingSummary":
        weight_moved = int((data[CName.REPS] * data[CName.WEIGHT]).sum())
        set_count = data.shape[0]
        rep_count = data[CName.REPS].sum()
        return WeightTrainingSummary(weight_moved, set_count, rep_count)

    def __str__(self) -> str:
        return f"Lifting {self.weight_moved:,} lbs across {self.set_count:,} sets and {self.rep_count:,} reps."


@dataclass
class FootCardioSummary(ExerciseSummary):
    dist: float
    elv_gain: int

    @staticmethod
    def _build(data: pd.DataFrame) -> "FootCardioSummary":
        dist = round(data[CName.DISTANCE].sum(), 1)
        elv_gain = data[CName.ELEVATION].sum()
        return FootCardioSummary(dist, elv_gain)

    def __str__(self) -> str:
        return f"Moving my body by foot across {self.dist:,} km and up {self.elv_gain:,} m."


@dataclass
class BikeCardioSummary(ExerciseSummary):
    dist: float
    total_output: int

    @staticmethod
    def _build(data: pd.DataFrame) -> "BikeCardioSummary":
        dist = round(data[CName.DISTANCE].sum(), 1)
        total_output = round((data[CName.DURATION] * data[CName.AVG_WATT] / 1000).sum())
        return BikeCardioSummary(dist, total_output)

    def __str__(self) -> str:
        return f"Biking across {self.dist:,} km with a total output of {self.total_output:,} KJ."
