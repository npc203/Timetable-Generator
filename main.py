import random
from constraints import validate
from constraints.models import (
    Period,
    Subject,
)
import logging
from collections import defaultdict
from typing import Dict, List, Optional
from constants import primary_subs_raw, secondary_subs_raw

LOG = logging.getLogger("table_buddy.core.timetable")
NO_OF_TEACHERS = 40
NO_OF_PERIODS_PER_DAY = 6
NO_OF_WORKING_DAYS = 5
NO_OF_CLASSES = 10
SECTIONS = ["A", "B"]


def find_empty_slot(timetables, cell):
    """Find empty slot in timetables.

    Arguments:
    cell -- list of (class_index,day,period), passed by reference and mutated in place
    timetables -- 3d list of periods
    """
    for class_index in range(len(timetables)):
        for day in range(NO_OF_WORKING_DAYS):
            for period in range(NO_OF_PERIODS_PER_DAY):
                LOG.debug(day, period, len(timetables), len(timetables[0]), len(timetables[0][0]))
                if timetables[class_index][day][period] is None:
                    cell[0] = class_index
                    cell[1] = day
                    cell[2] = period
                    return True
    return False


class TimetableGenerator:
    def __init__(self, no_of_classes: int, subjects: Dict[int, List[Subject]]):
        self.no_of_classes = no_of_classes
        self.subjects = subjects
        self.timetables: List[List[List[Optional[Period]]]] = [
            [[None for _ in range(NO_OF_PERIODS_PER_DAY)] for i in range(NO_OF_WORKING_DAYS)]
            for j in range(self.no_of_classes * 2)
        ]  # Multiplied by 2 because of two sections

    def generate_timetables(self):
        """Generate timetable for school using backtracking"""

        cell: List[int] = [0, 0, 0]

        if not find_empty_slot(self.timetables, cell):
            return self.timetables

        curr_class = cell[0] // 2  # Multiplied by 2 because of two sections
        curr_day = cell[1]
        curr_period = cell[2]

        for sub in self.subjects[curr_class]:
            period = Period(sub, curr_day, curr_period)
            if validate(self.timetables[curr_class], period):
                self.timetables[curr_class][curr_day][curr_period] = period
                if self.generate_timetables():
                    return True

                self.timetables[curr_class][curr_day][curr_period] = None
        return False


if __name__ == "__main__":
    primary_subs: Dict[int, List[Subject]] = defaultdict(list)

    for standard in range(NO_OF_CLASSES):
        for sub in primary_subs_raw:
            primary_subs[standard].append(Subject(sub, f"{sub}_{standard}", standard))

    # secondary_subs: Dict[int, List[Subject]] = {}

    # for standard in range(6, 10):
    #     for sub in secondary_subs_raw:
    #         secondary_subs[standard].append(Subject(sub, f"{sub}_{standard}", standard))

    # print(*primary_subs, len(primary_subs), sep="\n")
    # print(*secondary_subs, len(secondary_subs), sep="\n")
    primary_classes = TimetableGenerator(5, primary_subs)
    final_table = primary_classes.generate_timetables()
    print(final_table)
