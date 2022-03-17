from dataclasses import dataclass
from enum import Enum


class Cell(Enum):
    CLASS = 0
    DAY = 1
    PERIOD = 2


@dataclass(frozen=True)
class Subject:
    name: str
    id: str
    standard: int


@dataclass
class Period:
    subject: Subject
    day: int
    period: int
