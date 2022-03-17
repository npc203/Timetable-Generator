import logging

from constants import NO_OF_PERIODS_PER_DAY, NO_OF_WORKING_DAYS, primary_subs
from constraints import Cell, ConstraintGroup, Subject, constraint, validate

LOG = logging.getLogger("table_buddy.core.constraints")


class MinQuotas(ConstraintGroup):
    @constraint
    def current_day_quota(self, timetables, cell, subject) -> bool:
        """Can repeat twice in a day"""
        day_periods = timetables[cell[0]][cell[1]]  # get the current day periods
        if sum(subject.name == period.subject.name for period in day_periods if period) >= 2:
            LOG.debug(
                "%s %s %s"
                % (cell, subject.name, [i.subject.name if i else "NONE" for i in day_periods])
            )
            return False
        return True

    @constraint
    def weekly_period_quota(self, timetables, cell, subject) -> bool:
        """Should occur atleast once a week and not more than 7 times"""
        if cell[2] == NO_OF_PERIODS_PER_DAY - 1:  # last period of the day
            class_timetable = timetables[cell[0]]

            for check_sub in primary_subs[cell[0]]:  # get all current class timetables
                total_occurences_in_week = 0
                for day in class_timetable:
                    total_occurences_in_week += sum(
                        check_sub.name == period.subject.name for period in day if period
                    )
                if not (7 >= total_occurences_in_week >= 1):
                    return False

        return True


if __name__ == "__main__":
    print(validate([[[None]]], [0, 0, 0], Subject("a", "a", 1)))
