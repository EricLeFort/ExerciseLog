import numpy as np
import pandas as pd

from scipy.optimize import curve_fit
from scipy.ndimage import uniform_filter1d
from typing import Callable

from exercise_log.dataloader import ColumnName


EXTRAPOLATE_DAYS = 100
MIN_DAILY_ACTIVE_MINUTES = 22.5  # Weekly is 150, this is about 150/7
N_DAYS_TO_AVG = 8

class Trendsetter:
    @staticmethod
    def _f_log_curve(t, a, b, c):
        """This is a logaritmic function that Scipy's curve_fit will fit (using the variables given)"""
        return a * np.log(b * t) + c

    @staticmethod
    def _f_affine(t, a, b):
        """This is a linear function that Scipy's curve_fit will fit (using the variables given)"""
        return a*t + b

    @staticmethod
    def _get_padded_dates(df: pd.DataFrame, num_days_to_pad: int):
        """Computes a list of dates using the given dataframe padded with extra days at the end"""
        first_index = df.index[0]
        periods = df.shape[0] + num_days_to_pad
        padded_dates = pd.date_range(df.iloc[0][ColumnName.DATE], periods=periods, freq='1d')
        padded_dates = padded_dates.to_series(name=ColumnName.DATE).reset_index(drop=True)
        padded_dates.index = pd.RangeIndex(start=first_index, stop=first_index + periods)
        return padded_dates

    @staticmethod
    def _get_curve_of_best_fit(
        df: pd.DataFrame,
        f_to_fit: Callable,
        fitted_params: tuple,
        num_days_to_extrapolate: int
    ) -> np.ndarray:
        """Fits a trendline using the given functionm for the column specified by key in the given DataFrame"""
        padded_dates = Trendsetter._get_padded_dates(df, num_days_to_extrapolate)
        return f_to_fit(padded_dates.index, *fitted_params).to_numpy()

    @staticmethod
    def compute_n_sample_avg(data: pd.DataFrame, field: str, n_days_to_avg: int) -> np.ndarray:
        """Compute an average over the most recent N samples"""
        return uniform_filter1d(data[field], size=n_days_to_avg)

    @staticmethod
    def fit_linear(df: pd.DataFrame, field: str) -> np.ndarray:
        """
        Computes the line of best fit for the given field.

        Args:
            data (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
            field (str): The column name to fit
        Returns:
            A 2-tuple containing:
                m (float): The slope of the line of best fit
                b (float): The y-intercept of the line of best fit
        """
        fitted_params, _ = curve_fit(Trendsetter._f_affine, df.index, df[field])
        return fitted_params

    @staticmethod
    def fit_logarithmic(df: pd.DataFrame, field: str) -> np.ndarray:
        """
        Computes the logarithmic curve of best fit for the given field.

        Args:
            data (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
            field (str): The column name to fit
        Returns:
            A 3-tuple containing a, b, and, c of the equation: a * log(b * t) + c
        """
        fitted_params, _ = curve_fit(Trendsetter._f_log_curve, df.index, df[field])
        return fitted_params

    @staticmethod
    def get_line_of_best_fit(df: pd.DataFrame, field: str, extrapolate_days: int) -> np.ndarray:
        """
        Fits a linear trendline to the given field in the data. Returns the line of best fit from the start of the data
        until the end of the data plus the number of extrapolated days.

        Args:
            data (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
            field (str): The column name to fit
            extrapolate_days (int): The number of days to extrapolate the trend until
        Returns:
            An np.ndarray of values that belong to the trendline
        """
        nonnulls = df[df[field].notnull()]
        fitted_params = Trendsetter.fit_linear(nonnulls, field)
        return Trendsetter._get_curve_of_best_fit(nonnulls, Trendsetter._f_affine, fitted_params, extrapolate_days)

    @staticmethod
    def get_logarithmic_curve_of_best_fit(df: pd.DataFrame, field: str, extrapolate_days: int) -> np.ndarray:
        """
        Fits a logarithmic trendline of the given field. Returns the line of best fit from the start of the data
        until the end of the data plus the number of extrapolated days.

        Args:
            data (pd.DataFrame): The data to fit. It must contain a column with the name of the given field.
            field (str): The column name to fit
            extrapolate_days (int): The number of days to extrapolate the trend until
        Returns:
            An np.ndarray of values that belong to the trendline
        """
        nonnulls = df[df[field].notnull()]
        fitted_params = Trendsetter.fit_logarithmic(nonnulls, field)
        return Trendsetter._get_curve_of_best_fit(nonnulls, Trendsetter._f_log_curve, fitted_params, extrapolate_days)
