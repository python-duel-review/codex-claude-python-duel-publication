def _check_time(x):
    # type(...) is int izključi bool (bool je podrazred int)
    if type(x) is not int or not 0 <= x <= 1440:
        raise ValueError(f"Neveljaven čas: {x!r}")


def free_slots(bookings, start, end):
    _check_time(start)
    _check_time(end)
    if start >= end:
        raise ValueError("Veljati mora start < end")
    if not isinstance(bookings, (list, tuple)) or len(bookings) > 20:
        raise ValueError("bookings mora biti seznam ali terka z največ 20 intervali")

    intervals = []
    for b in bookings:
        if not isinstance(b, (list, tuple)) or len(b) != 2:
            raise ValueError(f"Neveljaven interval: {b!r}")
        s, e = b
        _check_time(s)
        _check_time(e)
        if not start <= s < e <= end:
            raise ValueError(f"Interval {b!r} ni veljaven ali ni znotraj [{start}, {end})")
        intervals.append((s, e))

    result = []
    cursor = start  # konec dosedanje zasedenosti
    for s, e in sorted(intervals):
        if s > cursor:  # s == cursor pomeni stik -> ni vrzeli
            result.append((cursor, s))
        cursor = max(cursor, e)
    if cursor < end:
        result.append((cursor, end))
    return result


# --- Testi ---
assert free_slots([(10, 20), (18, 30), (40, 50)], 0, 60) == [(0, 10), (30, 40), (50, 60)]
assert free_slots([(5, 10), (0, 5)], 0, 10) == []  # neurejeni, stikajoči se intervali

try:
    free_slots([(True, 5)], 0, 10)
    assert False, "Pričakovan ValueError"
except ValueError:
    pass
