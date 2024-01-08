from typing import Union

# pylint: disable=invalid-name
# I'm treating this like "int" not like "Int" so I don't agree with the linter here
number = Union[float, int]  # Something like this should be part of the standard library IMO
# pylint: enable=invalid-name

DATE = "date"
MIN_DAILY_ACTIVE_MINUTES = 22.5  # Weekly recommended is 150, this is about 150/7

ROOT_ONTOLOGY_DIR = "../../ontology"
