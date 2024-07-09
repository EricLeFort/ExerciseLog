"""Defines project-level constants for ExerciseLog."""

from typing import Union

# I'm treating this like "int" not like "Int" so I don't agree with the linter here
number = Union[float, int]  # Something like this should be part of the standard library IMO

DATE = "date"
MIN_DAILY_ACTIVE_MINUTES = 22.5  # Weekly recommended is 150, this is about 150/7

ROOT_ONTOLOGY_DIR = "../../ontology"

# Conversion ratios between units
KG_TO_LB = 2.20462
WATT_TO_KCAL_PER_HOUR = 0.86042065
