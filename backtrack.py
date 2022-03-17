import logging
from collections import defaultdict
from typing import Dict, List, Optional
import random

from rich.logging import RichHandler

from constants import *
from constraints import validate
from constraints.models import Period, Subject

# importing restrictions to register the various constraint classes
from restrictions import *

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
LOG = logging.getLogger("table_buddy.core.timetable")


# secondary_subs: Dict[int, List[Subject]] = {}

# for standard in range(6, 10):
#     for sub in secondary_subs_raw:
#         secondary_subs[standard].append(Subject(sub, f"{sub}_{standard}", standard))


def find_empty_slot(timetables, cell):
    """Find empty slot in timetables.

    Arguments:
    cell -- list of (class_index,day,period), passed by reference and mutated in place
    timetables -- 3d list of periods
    """
    for class_index in range(len(timetables)):
        for day in range(NO_OF_WORKING_DAYS):
            for period in range(NO_OF_PERIODS_PER_DAY):
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
            [[None] * NO_OF_PERIODS_PER_DAY for _ in range(NO_OF_WORKING_DAYS)]
            for _ in range(self.no_of_classes * 2)
        ]  # Multiplied by 2 because of two sections

    def generate_timetables(self):
        """Generate timetable for school using backtracking"""

        cell: List[int] = [0, 0, 0]

        if not find_empty_slot(self.timetables, cell):
            LOG.debug("No empty slot found")
            return self.timetables

        curr_class = cell[0]
        curr_day = cell[1]
        curr_period = cell[2]

        LOG.debug("Current cell: {}".format(cell))
        current_class_subjects = self.subjects[curr_class]
        # Iterating through current class subjects
        for sub in random.sample(current_class_subjects, len(current_class_subjects)):
            if validate(self.timetables, cell, sub):
                period = Period(sub, curr_day, curr_period)  # Creating period obj if it's valid
                LOG.debug("Chosen Subject: {}".format(sub.name))
                self.timetables[curr_class][curr_day][curr_period] = period
                if self.generate_timetables():
                    return True

                self.timetables[curr_class][curr_day][curr_period] = None
        return False

    def print_table(self, class_index=None):
        """Print timetable for a class or all classes"""

        final_str = ""

        def format_class(index, class_):
            nonlocal final_str
            final_str += f"Class: {index}\n"
            final_str += "-" * 20 + "\n"

            for day in class_:
                final_str += (
                    ", ".join("-" if period is None else period.subject.name for period in day)
                    + "\n"
                )
            final_str += "-" * 20 + "\n"
            return final_str

        if class_index is None:
            for index, class_ in enumerate(self.timetables):
                print(format_class(index, class_))
        else:
            print(format_class(class_index, self.timetables[class_index]))


if __name__ == "__main__":
    primary_classes = TimetableGenerator(5, primary_subs)

    ### Debug printing tables
    import threading, time

    class PrintThread(threading.Thread):
        def __init__(self, generator):
            super().__init__()
            self.generator = generator

        def run(self):
            while True:
                self.generator.print_table(0)
                time.sleep(5)

    thread = PrintThread(primary_classes)
    thread.daemon = True
    # thread.start()
    ### END Debug printing tables

    if primary_classes.generate_timetables():
        primary_classes.print_table()
    else:
        LOG.info("Timetable cannot generated with the given constraints")