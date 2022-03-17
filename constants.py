from typing import Dict, List
from constraints import Subject
from collections import defaultdict

NO_OF_TEACHERS = 40
NO_OF_PERIODS_PER_DAY = 6
NO_OF_WORKING_DAYS = 5
NO_OF_CLASSES = 10
NO_OF_SECTIONS = 2


primary_subs_raw = ["English", "Language", "Maths", "Science", "Social Science"]
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

# Generate Subject Objects
primary_subs: Dict[int, List[Subject]] = defaultdict(list)
for standard in range(NO_OF_CLASSES):
    for sub in primary_subs_raw:
        primary_subs[standard].append(Subject(sub, f"{sub}_{standard}", standard))
