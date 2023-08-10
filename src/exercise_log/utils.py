import os

from enum import Enum
from typing import Any, List, Optional

import numpy as np
import pandas as pd
from pandas.core.generic import NDFrame  # This is the generic type that encompasses Series and DataFrame

from exercise_log.constants import number, DATE


UTF8 = "utf-8"
NEWLINE = "\n"
CR = b"\r"
LF = b"\n"


class StrEnum(str, Enum):
    def __contains__(self: "StrEnum", item: Any) -> bool:
        """
        Checks if the given item is a member of this enum.

        Note: this is a little hacky due to the access to a private member but the alternative is try-casting which is
        ~8x slower.

        Args:
            item (Any): The item to check for membership
        """
        return item in self._value2member_map_


class TermColour(StrEnum):
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


def invert_csv_rows(
    fname: str,
    has_header_row: Optional[bool] = False,
    output_fname: Optional[str] = None,
    encoding: str = UTF8,
) -> None:
    """
    Inverts the rows of a csv so that the last row is first, the second last row is second, and so on. The inverted csv
    is then written to a new file. By default "x" or "x.csv" -> "x_inverted.csv".

    Args:
        path (str): The path to the csv file to invert
        has_header_row (Optional[str]): Whether the csv has a header row that should be maintained by this function.
        output_fname (Optional[str]): The new path to write the inverted csv to
    """
    # Note: working backwards from the input file rather than injecting into the first row of the output file even
    #       though it's messier bc I assume it's faster for data allocation reasons. I didn't validate this though.
    # Note: In Python, "\n" is the correct way to refer to a new line on all OS's.
    if encoding != UTF8:
        raise NotImplementedError("This function currently only supports utf-8")

    if not output_fname:
        output_fname = fname.rsplit(".csv")[0] + "_inverted.csv"

    # Start with the header row if it exists since it needs to remain at the top of the file
    output_strategy = "wb"
    if has_header_row:
        output_strategy = "ab"
        with open(fname, "r", encoding=encoding) as f_in:
            with open(output_fname, "w", encoding=encoding) as f_out:
                header = f_in.readline()
                f_out.write(header)
                f_out.write(NEWLINE)

    line_breaks = {CR, LF}
    with open(fname, "rb") as f_in:
        with open(output_fname, output_strategy) as f_out:
            # Move to an offset of 0 bytes from the end of the file
            f_in.seek(0, os.SEEK_END)

            # Work backwards and write a line every time a line break is found
            line = b""
            while f_in.tell() > 1:               # tell() gives the current position in the file
                f_in.seek(-2, os.SEEK_CUR)       # Move 2 bytes back to read the previous byte
                byte = f_in.read(1)              # Read a single byte, moving the pointer forward by one
                line = byte + line
                if byte in line_breaks:
                    # Write the bytes from this line
                    f_out.write(line[1:])
                    line_break = line[0:1]
                    line = b""

                    # Now write whichever line break was used to terminate the line
                    if byte == LF:
                        f_in.seek(-2, 1)
                        byte = f_in.read(1)
                        if byte == CR:
                            line_break = byte + line_break
                        else:
                            f_in.seek(1, 1)      # We still need this byte if it's not CR, reset the pointer
                    f_out.write(line_break)

            # Skip the last line if it's a header since it's already been written
            if not has_header_row:
                f_out.write(line)
