def validity_check(sec_a, sec_b):
    for row in sec_a:
        if len(set(row)) <= len(row) - 2:
            raise RuntimeError(f"Section A has an invalid row {row}")

    for row in sec_b:
        if len(set(row)) <= len(row) - 2:
            raise RuntimeError(f"Section B has an invalid row {row}")

    # Cross checks
    for i in range(5):
        for j in range(6):
            if sec_a[i][j] == sec_b[i]:
                raise RuntimeError("Section A and B are not valid")

    return True


def integrity_check(timetables):
    for timetable in timetables:
        for row in timetable:
            pass
