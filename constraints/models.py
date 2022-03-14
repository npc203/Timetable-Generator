from dataclasses import dataclass


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
