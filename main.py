from dataclasses import dataclass
import random

NO_OF_TEACHERS = 40
NO_OF_PERIODS_PER_DAY = 6
CLASSES = 10
SECTIONS = ["A", "B"]


@dataclass
class Subject:
    name: str
    id: str
    standard: str


@dataclass
class Period:
    subject: Subject
    day: int
    period: int


primary_subs_raw = ["English", "Language", "Maths", "Science", "Social Science"]
primary_subs = []

for standard in range(1, 6):
    for sub in primary_subs_raw:
        primary_subs.append(Subject(sub, f"{sub}_{standard}", str(standard)))

# TODO add PT
# primary_subs.append(Subject("PT", "PT-Common", "1"))

secondary_subs_raw = [
    "Prose-1",
    "Poetry-1",
    "Grammar-2",
    "Prose-2",
    "Physics",
    "Chemistry",
    "Biology",
    "Algebra",
    "Trignometry",
    "Geometry",
    "History",
    "Civics",
    "Geography",
    "PT",
]
secondary_subs = []

for standard in range(6, 10):
    for sub in secondary_subs_raw:
        secondary_subs.append(Subject(sub, f"{sub}_{standard}", str(standard)))

print(*primary_subs, len(primary_subs), sep="\n")
print(*secondary_subs, len(secondary_subs), sep="\n")


class Constraint:
    # TODO add more constraints
    def __init__(self) -> None:
        pass

    def validate(self, *args) -> bool:
        return all(
            getattr(self, func)(*args) for func in dir(self) if func.startswith("constraint_")
        )

    def constraint_prev(self, timetable, periods, period, day) -> bool:
        return random.choice([True, False])


def check_constraints(timetable, periods, period, day) -> bool:
    """Check if the period is valid"""
    return Constraint().validate(timetable, periods, period, day)


def generate_timetable():
    """Generate timetable for school using backtracking"""
    timetables = []
    # Primary
    for class_ in range(1, 6):
        for section in SECTIONS:
            timetable = []

            # Mon to Fri
            for day in range(1, 6):
                periods = []
                for period in range(1, NO_OF_PERIODS_PER_DAY + 1):
                    subject = random.choice(primary_subs)
                    if check_constraints(timetable, periods, period, day):
                        periods.append(
                            (
                                f"{class_} {section}",
                                subject,
                                day,
                                period,
                            )
                        )
                    else:
                        # TODO add recurision logic
                        pass
                timetable.append(periods)
            print(*timetable, sep="\n")


generate_timetable()
