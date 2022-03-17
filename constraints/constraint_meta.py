from functools import wraps
from typing import Any, Callable, List, Optional
from .models import Period, Subject
import weakref


def constraint(func: Callable[[Any, List[List[List[Optional[Period]]]], List, Subject], bool]):
    @wraps(func)
    def inner(timetables, cell, subject):
        return func(object, timetables, cell, subject)

    # One way to track decorators
    inner.is_constraint = True
    return inner


class ConstraintGroup:
    constraints = []

    def __init_subclass__(cls):
        ConstraintGroup.update(cls)

    @classmethod
    def update(cls, arg_cls):
        cls.constraints.extend(
            [c for c in arg_cls.__dict__.values() if hasattr(c, "is_constraint")]
        )


def validate(timetables: List[List[List[Optional[Period]]]], cell: List, subject: Subject) -> bool:
    """Function that takes the whole timetable and the current period to check all registered constraints.
    Note: It's called by reference so don't make inplace changes in constraints"""
    for constraint in ConstraintGroup.constraints:
        if not constraint(timetables, cell, subject):
            return False
    return True
