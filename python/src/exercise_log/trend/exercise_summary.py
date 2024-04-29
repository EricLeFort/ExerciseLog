"""A collection of dataclasses that store and pretty-print workout volume metrics of various forms of exercise."""

from dataclasses import dataclass
from datetime import date
from typing import Self

import numpy as np
import pandas as pd

from exercise_log.dataloader import CName


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
