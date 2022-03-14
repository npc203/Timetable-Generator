from functools import wraps
from typing import List, Optional
from .models import Period
import weakref


def constraint(func):
    @wraps(func)
    def inner(self, timetable: List[List[Optional[Period]]], period: Period):
        return func(self, timetable, period)

    # One way to track decorators
    inner.is_constraint = True
    return inner


class ConstraintGroup:
    instances = []

    def __init__(self, name=None):
        self.__class__.instances.append(weakref.proxy(self))


def validate(timetable: List[List[Optional[Period]]], period: Period) -> bool:
    """Function that takes the whole timetable and the current period to check all registered constraints.
    Note: It's called by reference so don't make inplace changes in constraints"""
    for group in ConstraintGroup.instances:
        for func in dir(group):
            if hasattr(getattr(group, func), "is_constraint"):
                if not getattr(group, func)(timetable, period):
                    return False
    return True
