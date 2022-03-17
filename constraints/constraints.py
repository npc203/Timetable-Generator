from .constraint_meta import ConstraintGroup, constraint, validate
from .models import Period, Subject
import logging

LOG = logging.getLogger("table_buddy.core.constraints")


class MinQuotas(ConstraintGroup):
    @constraint
    def current_day_quota(self, timetables, cell, subject) -> bool:
        """Can repeat twice in a day"""
        day_periods = timetables[cell[0]][cell[1]]
        if sum(subject.name == period.subject.name for period in day_periods if period) >= 2:
            LOG.debug(
                "%s %s %s"
                % (cell, subject.name, [i.subject.name if i else "NONE" for i in day_periods])
            )
            return False
        return True

    @constraint
    def weekly_period_quota(self, timetables, cell, subject) -> bool:
        return True


if __name__ == "__main__":
    print(validate([[[None]]], [0, 0, 0], Subject("a", "a", 1)))
