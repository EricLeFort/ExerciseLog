import pickle
import unittest

from exercise_log.utils import StrEnum

TestEnum = StrEnum.create_from_json("../test/data/enum/sample_enum.json", __name__)


class TestStrEnum(unittest.TestCase):
    def test_create_from_json(self) -> None:
        """Tests that a StrEnum can be created from a JSON as expected."""
        try:
            a = TestEnum.A
            b = TestEnum.B
            c = TestEnum.C
        except ValueError:
            self.fail("Could not find one of the expected enums")

        self.assertNotEqual(TestEnum.__doc__, "No description available")
        self.assertEqual(a.value, "a", "Value of TestEnum.A was incorrect")
        self.assertEqual(b.value, "b", "Value of TestEnum.B was incorrect")
        self.assertEqual(c.value, "c", "Value of TestEnum.C was incorrect")
        self.assertEqual(len(TestEnum), 3, "More enums were found than expected: should only be 3.")

    def test_is_picklable(self) -> None:
        """Tests that a StrEnum can be pickled/unpickled correctly."""
        result = pickle.loads(pickle.dumps(TestEnum.A))  # noqa: S301
        self.assertEqual(TestEnum.A.value, result.value, "Original value and depickled value do not match")
