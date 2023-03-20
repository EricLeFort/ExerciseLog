import numpy as np
import pandas as pd

from pandas.core.generic import NDFrame  # This is the generic type that encompasses Series and DataFrame
from typing import List

from exercise_log.constants import number, DATE

def join_with_comma(items: List[str]):
    """Wrapper function to join a list of strs with commas"""
    return ",".join(items)


def convert_pd_to_np(obj: NDFrame) -> np.ndarray:
    return np.array(obj)[:, None]


def convert_mins_to_hour_mins(mins: number, _ = None) -> str:
    if mins < 60:
        return f"{int(mins)}m"
    hours, mins = int(mins // 60), int(mins % 60)
    return f"{hours}h {mins}m"


def get_padded_dates(df: pd.DataFrame, num_days_to_pad: int) -> pd.DataFrame:
    """Pads the dates in the Dataframe by the specified number of days"""
    first_index = df.index[0]
    periods = df.shape[0] + num_days_to_pad
    padded_dates = pd.date_range(df.iloc[0][DATE], periods=periods, freq='1d')
    padded_dates = padded_dates.to_series(name=DATE).reset_index(drop=True)
    padded_dates.index = pd.RangeIndex(start=first_index, stop=first_index + periods)
    return padded_dates
