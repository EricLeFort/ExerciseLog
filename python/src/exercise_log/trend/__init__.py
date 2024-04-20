from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Self

import numpy as np
import pandas as pd
from scipy.ndimage import uniform_filter1d
from scipy.optimize import curve_fit

from exercise_log.dataloader import ColumnName
from exercise_log.utils import get_padded_dates

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
            data (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
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
            data (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
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
            data (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
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
            data (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
            field (str): The column name to fit
            extrapolate_days (int): The number of days to extrapolate the trend until
        Returns:
            An np.ndarray of values that belong to the trendline
        """
        nonnulls = df[df[field].notna()]
        fitted_params = Trendsetter.fit_logarithmic(nonnulls, field)
        return Trendsetter._get_curve_of_best_fit(nonnulls, Trendsetter._f_log_curve, fitted_params, extrapolate_days)


class ExerciseSummary:
    @classmethod
    def build_summary(cls, data: pd.DataFrame, start_date: date, end_date: date) -> Self:
        start_date, end_date = np.datetime64(start_date, "ns"), np.datetime64(end_date, "ns")
        data = data[start_date <= data[ColumnName.DATE]]
        data = data[data[ColumnName.DATE] <= end_date]
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
        weight_moved = int((data[ColumnName.REPS] * data[ColumnName.WEIGHT]).sum())
        set_count = data.shape[0]
        rep_count = data[ColumnName.REPS].sum()
        return WeightTrainingSummary(weight_moved, set_count, rep_count)

    def __str__(self) -> str:
        return f"Lifting {self.weight_moved:,} lbs across {self.set_count:,} sets and {self.rep_count:,} reps."


@dataclass
class FootCardioSummary(ExerciseSummary):
    dist: float
    elv_gain: int

    @staticmethod
    def _build(data: pd.DataFrame) -> "FootCardioSummary":
        dist = round(data[ColumnName.DISTANCE].sum(), 1)
        elv_gain = data[ColumnName.ELEVATION].sum()
        return FootCardioSummary(dist, elv_gain)

    def __str__(self) -> str:
        return f"Moving my body by foot across {self.dist:,} km and up {self.elv_gain:,} m."


@dataclass
class BikeCardioSummary(ExerciseSummary):
    dist: float
    total_output: int

    @staticmethod
    def _build(data: pd.DataFrame) -> "BikeCardioSummary":
        dist = round(data[ColumnName.DISTANCE].sum(), 1)
        total_output = round((data[ColumnName.DURATION] * data[ColumnName.AVG_WATT] / 1000).sum())
        return BikeCardioSummary(dist, total_output)

    def __str__(self) -> str:
        return f"Biking across {self.dist:,} km with a total output of {self.total_output:,} KJ."
