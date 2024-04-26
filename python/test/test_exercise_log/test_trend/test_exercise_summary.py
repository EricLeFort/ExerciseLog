import datetime
import unittest
from collections.abc import Callable
from datetime import date, timedelta
from random import randint, uniform

import pandas as pd

from exercise_log.dataloader import ColumnName as CName
from exercise_log.trend.exercise_summary import (
    BikeCardioSummary,
    ExerciseSummary,
    FootCardioSummary,
    WeightTrainingSummary,
)


def _test_four_scenarios(
    tester: unittest.TestCase,
    f_gen_data: Callable[[int], pd.DataFrame],
    f_assert_summary: Callable[[unittest.TestCase, pd.DataFrame, tuple[date, date]], None],
) -> None:
    num_entries = randint(5, 20)
    num_exclude = randint(1, num_entries // 2 - 1)
    start, end = 0, num_entries - 1
    data = f_gen_data(num_entries)

    # Scenario 1: include all dates
    f_assert_summary(tester, data, (start, end))

    # Scenario 2: exclude some of the first dates
    f_assert_summary(tester, data, (num_exclude, end))

    # Scenario 3: exclude some of the last dates
    f_assert_summary(tester, data, (start, end - num_exclude))

    # Scenario 4: exclude some of the last dates
    f_assert_summary(tester, data, (num_exclude, end - num_exclude))


def _gen_random_foot_cardio_data(num_entries: int) -> pd.DataFrame:
    data = _init_dataframe(num_entries)
    data[CName.AVG_WATT] = [randint(100, 1000) for _ in range(num_entries)]
    data[CName.DISTANCE] = [round(uniform(0.1, 100), 2) for _ in range(num_entries)]
    data[CName.ELEVATION] = [0] + [randint(1, 1000) for _ in range(num_entries - 2)] + [0]
    return data


def _gen_random_weight_training_data(num_entries: int) -> pd.DataFrame:
    data = _init_dataframe(num_entries)
    data[CName.REPS] = [randint(1, 100) for _ in range(num_entries)]
    data[CName.WEIGHT] = [0] + [round(uniform(1, 1000), 1) for _ in range(num_entries - 2)] + [0]
    return data


def _init_dataframe(num_entries: int) -> pd.DataFrame:
    today = datetime.datetime.now(tz=datetime.UTC).date()
    dates = [today - timedelta(i) for i in range(num_entries)][::-1]
    durations = [randint(0, 20000) for _ in range(num_entries)]
    data = pd.DataFrame({CName.DATE: dates, CName.DURATION: durations})
    data[CName.DATE] = pd.to_datetime(data[CName.DATE])
    return data


def _assert_foot_cardio_summary(tester: unittest.TestCase, data: pd.DataFrame, idx_range: tuple[date, date]) -> None:
    first_idx, last_idx = idx_range
    filtered_data = data.iloc[first_idx : last_idx + 1]
    total_dist = round((filtered_data[CName.DISTANCE].sum()), 1)
    total_elevation = sum(filtered_data[CName.ELEVATION])
    expected_str = f"Moving my body by foot across {total_dist:,} km and up {total_elevation:,} m."
    _assert_summary(tester, data, FootCardioSummary.build_summary, idx_range, expected_str)


def _assert_bike_cardio_summary(tester: unittest.TestCase, data: pd.DataFrame, idx_range: tuple[date, date]) -> None:
    first_idx, last_idx = idx_range
    filtered_data = data.iloc[first_idx : last_idx + 1]
    total_dist = round(filtered_data[CName.DISTANCE].sum(), 1)
    total_output = round((filtered_data[CName.DURATION] * filtered_data[CName.AVG_WATT] / 1000).sum())
    expected_str = f"Biking across {total_dist:,} km with a total output of {total_output:,} KJ."
    _assert_summary(tester, data, BikeCardioSummary.build_summary, idx_range, expected_str)


def _assert_weight_training_summary(
    tester: unittest.TestCase,
    data: pd.DataFrame,
    idx_range: tuple[date, date],
) -> None:
    first_idx, last_idx = idx_range
    filtered_data = data.iloc[first_idx : last_idx + 1]
    weight_moved = int((filtered_data[CName.REPS] * filtered_data[CName.WEIGHT]).sum())
    set_count = filtered_data.shape[0]
    rep_count = filtered_data[CName.REPS].sum()
    expected_str = f"Lifting {weight_moved:,} lbs across {set_count:,} sets and {rep_count:,} reps."
    _assert_summary(tester, data, WeightTrainingSummary.build_summary, idx_range, expected_str)


def _assert_summary(
    tester: unittest.TestCase,
    data: pd.DataFrame,
    summary_builder: Callable[[pd.DataFrame, date, date], ExerciseSummary],
    idx_range: tuple[int, int],
    expected_str: str,
) -> None:
    first_idx, last_idx = idx_range
    date_range = [data.iloc[first_idx][CName.DATE], data.iloc[last_idx][CName.DATE]]
    summary = summary_builder(data, *date_range)
    tester.assertEqual(expected_str, str(summary))


class TestExerciseSummary(unittest.TestCase):
    def test_bike_cardio_summary_pretty_print(self) -> None:
        _test_four_scenarios(self, _gen_random_foot_cardio_data, _assert_bike_cardio_summary)

    def test_foot_cardio_summary_pretty_print__include_all(self) -> None:
        _test_four_scenarios(self, _gen_random_foot_cardio_data, _assert_foot_cardio_summary)

    def test_weight_training_summary_pretty_print(self) -> None:
        _test_four_scenarios(self, _gen_random_weight_training_data, _assert_weight_training_summary)
