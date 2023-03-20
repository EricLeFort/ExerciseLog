import numpy as np
import pandas as pd

from scipy.optimize import curve_fit
from scipy.ndimage import uniform_filter1d
from typing import Callable

from exercise_log.constants import (
    DATE,
    DURATION,
    RESTING_HEART_RATE,
    WEIGHT,
)

EXTRAPOLATE_DAYS = 100
MIN_DAILY_ACTIVE_MINUTES = 22.5  # Weekly is 150, this is about 150/7
N_DAYS_TO_AVG = 8

class Trendsetter:
    def _f_log_curve(t, a, b, c):
        """This is a logaritmic function that Scipy's curve_fit will fit (using the variables given)"""
        return a * np.log(b * t) + c

    def _f_affine(t, a, b):
        """This is a linear function that Scipy's curve_fit will fit (using the variables given)"""
        return a*t + b

    def _get_padded_dates(df: pd.DataFrame, num_days_to_pad: int):
        """Pads the """
        first_index = df.index[0]
        periods = df.shape[0] + num_days_to_pad
        padded_dates = pd.date_range(df.iloc[0][DATE], periods=periods, freq='1d')
        padded_dates = padded_dates.to_series(name=DATE).reset_index(drop=True)
        padded_dates.index = pd.RangeIndex(start=first_index, stop=first_index + periods)
        return padded_dates

    def _compute_trendline(df: pd.DataFrame, key: str, f_to_fit: Callable, num_days_to_extrapolate: int) -> np.ndarray:
        """Fits a trendline using the given functionm for the column specified by key in the given DataFrame"""
        nonnulls = df[df[key].notnull()]
        x = nonnulls.index
        y = nonnulls[key]
        fitted_params, _ = curve_fit(f_to_fit, x, y)
        padded_dates = Trendsetter._get_padded_dates(nonnulls, num_days_to_extrapolate)
        return f_to_fit(padded_dates.index, *fitted_params).to_numpy()

    def compute_n_sample_avg(data: pd.DataFrame, field: str, n_days_to_avg: int) -> np.ndarray:
        """Compute an average over the most recent N samples"""
        return uniform_filter1d(data[field], size=n_days_to_avg)

    def fit_linear(data: pd.DataFrame, field: str, extrapolate_days: int) -> np.ndarray:
        return Trendsetter._compute_trendline(data, field, Trendsetter._f_affine, extrapolate_days)

    def fit_logarithmic(data: pd.DataFrame, field: str, extrapolate_days: int) -> np.ndarray:
        return Trendsetter._compute_trendline(data, field, Trendsetter._f_log_curve, extrapolate_days)
