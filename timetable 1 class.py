import random
from tabulate import tabulate

random.seed(1)

subs = ["maths", "social", "science", "language", "english"]
extra = ["art", "PT", "music"]
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# Empty table
timetable = [["" for i in range(6)] for j in range(5)]

# Iterating each row
for day_index in range(5):
    track_dups = [0] * 6  # A new hashmap for each row, to track dups
    # Iterating each column
    for period_index in range(6):
        while True:
            sub = random.choice(subs + extra)
            # The picked random choice is a subject
            if sub in subs:
                sub_index = subs.index(sub)
                # If the subject is already picked in the same row
                if not (any(ele > 1 for ele in track_dups) and track_dups[sub_index] == 1):
                    if track_dups[sub_index] <= 1:
                        timetable[day_index][period_index] = sub
                        track_dups[sub_index] += 1
                        break
            # The picked random choice is an extra subject
            else:
                # Check if an extra has already occured in that day
                if not any(period in extra for period in timetable[day_index]):
                    # Check if the extra is present in any of the previously generated days
                    if not any(sub in row for row in timetable):
                        timetable[day_index][period_index] = sub
                        break

print(tabulate(([days[d]] + ele for d, ele in enumerate(timetable)), tablefmt="fancy_grid"))
