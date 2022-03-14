from .constraint_meta import ConstraintGroup, constraint, validate
from .models import Period, Subject
import random


class ConstraintMain(ConstraintGroup):
    @constraint
    def current_day_quota(self, timetable, period) -> bool:
        return random.choice([True, False])

    @constraint
    def weekly_period_quota(self, timetable, period) -> bool:
        return random.choice([True, False])


class C1(ConstraintGroup):
    @constraint
    def combulate(self, timetable, period) -> bool:
        return random.choice([True, False])


if __name__ == "__main__":
    a = ConstraintMain()
    b = C1()
    print(validate([[None]], Period(Subject("a", "a", 1), 1, 1)))
