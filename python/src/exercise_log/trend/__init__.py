"""Contains logic relating to projecting simple trends."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta

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
    """A static object containing logic for simple trend-fitting using curves-of-best-fit."""

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
    def get_line_of_best_fit(df: pd.DataFrame, field: str, extrapolate_days: int = 0) -> np.ndarray:
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
    def get_logarithmic_curve_of_best_fit(df: pd.DataFrame, field: str, extrapolate_days: int = 0) -> np.ndarray:
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


class Trend(ABC):
    """An abstract class that uses datespans, a dataset, and a number of days to extrapolate to fit a trend."""

    def __init__(self, datespans: list[tuple[date]], health_metrics: pd.DataFrame, extrapolate_days: int) -> None:
        """Initialize this Trend with the relevant data. The trendline itself is computed lazily."""
        self.datespans = [(pd.to_datetime(start), pd.to_datetime(end)) for start, end in datespans]
        self.health_metrics = health_metrics
        self.extrapolate_days = extrapolate_days

        self._trendline = None

    @abstractmethod
    def get_trendline(self) -> pd.DataFrame:
        """Retrieve this Trend's trendline, computing it if necessary. Must be implemented by child classes."""
        raise NotImplementedError


class WeightTrend(Trend):
    """A Trend that predicts weight over time. Assumes each datespan contains a linear pattern of weight change."""

    def __init__(self, datespans: list[tuple[date]], health_metrics: pd.DataFrame, extrapolate_days: int) -> None:
        """Initialize this WeightTrend. Removes any null rows from the health_metrics."""
        nonnulls = health_metrics[health_metrics[CName.WEIGHT].notna()]
        super().__init__(datespans, nonnulls, extrapolate_days)

    def get_trendline(self) -> pd.DataFrame:
        """Retrieve this WeightTrend's trendline, computing it if necessary."""
        if self._trendline is None:
            cname = CName.WEIGHT
            lookback_days = 20

            # First section doesn't need a lookback
            metrics_slice = self.health_metrics[self.health_metrics[CName.DATE].between(*self.datespans[0])]
            y = [Trendsetter.get_line_of_best_fit(metrics_slice, cname)]
            for span in self.datespans[1:-1]:
                start_date = span[0] - timedelta(days=lookback_days)
                end_date = span[1] + timedelta(days=lookback_days)
                metrics_slice = self.health_metrics[self.health_metrics[CName.DATE].between(start_date, end_date)]
                line_of_fit = Trendsetter.get_line_of_best_fit(metrics_slice, cname)
                y.append(line_of_fit[lookback_days:-lookback_days])

            # The last section extrapolates a trend
            (start_date, end_date) = self.datespans[-1]
            start_date -= timedelta(days=lookback_days)
            metrics_slice = self.health_metrics[self.health_metrics[CName.DATE].between(start_date, end_date)]
            line_of_fit = Trendsetter.get_line_of_best_fit(metrics_slice, cname, self.extrapolate_days)
            y.append(line_of_fit[lookback_days:])

            # Combine all pieces into a single prediction
            y = np.concatenate(y)
            padded_dates = get_padded_dates(self.health_metrics, self.extrapolate_days)
            self._trendline = pd.DataFrame({CName.DATE: padded_dates, cname: y})
        return self._trendline


class HeartRateTrend(Trend):
    """
    A Trend that predicts resting heart rate (RHR) over time.

    Assumes the first datespan covers a logarithmic decrease in RHR and subsequent datespans are linear patterns of
    change. The first datespan is meant to capture the period of going from untrained to trained.
    """

    def __init__(self, datespans: list[tuple[date]], health_metrics: pd.DataFrame, extrapolate_days: int) -> None:
        """Initialize this HeartRateTrend. Removes any null rows from the health_metrics."""
        nonnulls = health_metrics[health_metrics[CName.RESTING_HEART_RATE].notna()]
        super().__init__(datespans, nonnulls, extrapolate_days)

    def get_trendline(self) -> pd.DataFrame:
        """
        Retrieve the heart rate trendline, computing it if necessary.

        First projects a log curve while going from untrained to trained, then projects linearly onward from there.

        There's better ways to fit the process of slowly becoming detrained or of becoming incrementally more trained
        but this can be improved in the future.
        """
        if self._trendline is None:
            cname = CName.RESTING_HEART_RATE
            lookback_days = 100
            first_slice = self.health_metrics[self.health_metrics[CName.DATE].between(*self.datespans[0])]
            untrained_to_trained = Trendsetter.get_logarithmic_curve_of_best_fit(first_slice, cname)

            # Start fitting this section from a little before it starts so that it fits more cleanly.
            span = (self.datespans[1][0] - timedelta(days=lookback_days), self.datespans[1][1])
            second_slice = self.health_metrics[self.health_metrics[CName.DATE].between(*span)]
            training = Trendsetter.get_line_of_best_fit(second_slice, cname, self.extrapolate_days)
            training = training[lookback_days:]

            # Combine both pieces into a single prediction
            y = np.concatenate([untrained_to_trained, training])
            padded_dates = get_padded_dates(self.health_metrics, self.extrapolate_days)
            self._trendline = pd.DataFrame({CName.DATE: padded_dates, cname: y})
        return self._trendline


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

        fmt = "%Y-%m-%d"
        first_weight_loss_end_date = datetime.strptime("2024-01-06", fmt).astimezone(UTC).date()
        first_weight_maintenance_end_date = datetime.strptime("2024-03-05", fmt).astimezone(UTC).date()

        nonnulls = self.health_metrics[self.health_metrics[CName.WEIGHT].notna()]
        first_date = nonnulls[CName.DATE].min()
        last_date = nonnulls[CName.DATE].max()
        datespans = [
            (first_date, first_weight_loss_end_date),
            (first_weight_loss_end_date, first_weight_maintenance_end_date),
            (first_weight_maintenance_end_date, last_date),
        ]
        self._weight_trend = WeightTrend(datespans, self.health_metrics, self.extrapolate_days)

        nonnulls = self.health_metrics[self.health_metrics[CName.RESTING_HEART_RATE].notna()]
        first_date = nonnulls[CName.DATE].min()
        last_date = nonnulls[CName.DATE].max()
        trained_date = datetime.strptime("2024-01-01", fmt).astimezone(UTC).date()
        datespans = [
            (first_date, trained_date),
            (trained_date, last_date),
        ]
        self._heart_rate_trend = HeartRateTrend(datespans, self.health_metrics, self.extrapolate_days)

        self._workout_durations = None

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
        return self._weight_trend.get_trendline()

    def get_heart_rate_trendline(self) -> pd.DataFrame:
        """Access the logarithmic curve of best fit of resting heart rate over time, first computing it if needed."""
        return self._heart_rate_trend.get_trendline()

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
