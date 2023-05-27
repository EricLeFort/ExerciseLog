from enum import Enum
from typing import List

import numpy as np
import pandas as pd
from pandas.core.generic import NDFrame  # This is the generic type that encompasses Series and DataFrame

from exercise_log.constants import number, DATE


class TermColour(str, Enum):
    FAIL = '\033[91m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    OKBLUE = '\033[94m'
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print_warning(msg: str):
        print(f"{TermColour.WARNING}{msg}{TermColour.END}")

    @staticmethod
    def print_error(msg: str):
        print(f"{TermColour.FAIL}{msg}{TermColour.END}")

    @staticmethod
    def print_success(msg: str):
        print(f"{TermColour.OKGREEN}{msg}{TermColour.END}")


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
