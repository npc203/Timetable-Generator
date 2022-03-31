import copy
import sys
import unittest

from timetable_generator.constants import primary_subs

# Hack to get the correct path working
sys.path.append("..")
from timetable_generator.backtrack import TimetableGenerator


def cleanup_timetable_to_names(timetable):
    for i in range(5):
        for j in range(6):
            if timetable[i][j] is not None:
                timetable[i][j] = timetable[i][j].subject.name
    return timetable


class ValidityChecks(unittest.TestCase):
    def setUp(self) -> None:
        primary_classes = TimetableGenerator(5, primary_subs)
        primary_classes.generate_timetables()
        self.t = copy.deepcopy(primary_classes.timetables)

    def test_validity_check(self):
        """Main basic validity check"""
        for class_index in range(0, 10, 2):
            self.validity_check(
                cleanup_timetable_to_names(self.t[class_index]),
                cleanup_timetable_to_names(self.t[class_index + 1]),
            )

    def validity_check(self, sec_a, sec_b):
        for row in sec_a:
            self.assertGreater(len(set(row)), len(row) - 2, f"Section A has an invalid row {row}")

        for row in sec_b:
            self.assertGreater(len(set(row)), len(row) - 2, f"Section B has an invalid row {row}")

        # Cross section checks
        for i in range(5):
            for j in range(6):
                self.assertNotEqual(
                    sec_a[i][j], sec_b[i][j], f"Section A and B have same values at {i},{j}"
                )

        return True


if __name__ == "__main__":
    unittest.main()
