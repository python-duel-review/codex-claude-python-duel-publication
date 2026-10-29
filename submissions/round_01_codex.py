def free_slots(bookings, start, end):
    def valid_time(value):
        return (
            isinstance(value, int)
            and not isinstance(value, bool)
            and 0 <= value <= 1440
        )

    if not valid_time(start) or not valid_time(end) or start >= end:
        raise ValueError("Neveljavni meji časovnega okna.")

    if not isinstance(bookings, (list, tuple)) or len(bookings) > 20:
        raise ValueError("bookings mora biti seznam ali terka do 20 intervalov.")

    intervals = []
    for interval in bookings:
        if not isinstance(interval, (list, tuple)) or len(interval) != 2:
            raise ValueError("Interval mora vsebovati začetek in konec.")
        a, b = interval
        if not valid_time(a) or not valid_time(b):
            raise ValueError("Časi morajo biti cela števila od 0 do 1440.")
        if not start <= a < b <= end:
            raise ValueError("Interval mora biti veljaven in znotraj okna.")
        intervals.append((a, b))

    result = []
    cursor = start
    for a, b in sorted(intervals):
        if a > cursor:
            result.append((cursor, a))
        cursor = max(cursor, b)
    if cursor < end:
        result.append((cursor, end))
    return result


# Test 1: prekrivanje
assert free_slots([(10, 20), (18, 30), (40, 50)], 0, 60) == [
    (0, 10), (30, 40), (50, 60)
]

# Test 2: neurejeni, stikajoči se intervali
assert free_slots([(20, 30), (10, 20)], 0, 40) == [(0, 10), (30, 40)]

# Test 3: bool ni dovoljen čas
try:
    free_slots([(False, 10)], 0, 60)
except ValueError:
    pass
else:
    raise AssertionError("Pričakovan ValueError.")
