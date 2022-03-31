import logging
import random
from typing import Dict, List, Optional

import tabulate

from .constants import *
from .constraints import validate
from .constraints.models import Period, Subject
import roman

# importing restrictions to register the various constraint classes
from .restrictions import *

LOG = logging.getLogger("table_buddy.core.timetable")

# Bad seed that takes a lot of time to generate
# random.seed(1)

# Good seed (TODO change)
random.seed(3)


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
            for _ in range(self.no_of_classes * NO_OF_SECTIONS)
        ]  # No of classes * No of sections

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

        def format_class(index, class_):
            final_str = ""
            final_str += f"Class: {index}\n"

            data = []
            for day in class_:
                data.append(["-" if period is None else period.subject.name for period in day])

            final_str += (
                tabulate.tabulate(
                    data,
                    headers=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    tablefmt="fancy_grid",
                )
                + "\n"
            )
            return final_str

        if class_index is None:
            for index, class_ in enumerate(self.timetables):
                print(format_class(index, class_))
        else:
            print(format_class(class_index, self.timetables[class_index]))


def generate() -> Dict[tuple, List[List[Period]]]:
    """Generate timetable for school using backtracking"""
    LOG.info("Generating timetable for all classes at once.")
    class_objs = (TimetableGenerator(5, primary_subs), TimetableGenerator(5, secondary_subs))
    final_timetable = {}
    class_no = 0
    for class_obj in class_objs:
        class_obj.generate_timetables()
        for timetable in class_obj.timetables:
            final_timetable[
                (roman.toRoman(int(class_no * 0.5 + 1)), ("A" if class_no % 2 == 0 else "B"))
            ] = timetable
            class_no += 1
    LOG.debug("Done")
    return final_timetable


if __name__ == "__main__":
    print(generate())
    # primary_classes = TimetableGenerator(5, primary_subs)

    # ### Debug printing tables
    # import threading, time

    # class PrintThread(threading.Thread):
    #     def __init__(self, generator):
    #         super().__init__()
    #         self.generator = generator

    #     def run(self):
    #         while True:
    #             self.generator.print_table(0)
    #             time.sleep(5)

    # thread = PrintThread(primary_classes)
    # thread.daemon = True
    # thread.start()
    ### END Debug printing tables

    # if primary_classes.generate_timetables():
    #     primary_classes.print_table()
    # else:
    #     LOG.info("Timetable cannot generated with the given constraints")
