# pylint: disable=protected-access
import unittest

from exercise_log.utils import StrEnum


class TestStrEnum(unittest.TestCase):
    def test_create_from_json(self) -> None:
        """Tests that a StrEnum can be created from a JSON as expected."""
        # pylint: disable=invalid-name
        TestEnum = StrEnum.create_from_json("../test/data/enum/sample_enum.json")  # noqa: N806

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
