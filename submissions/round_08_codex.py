def wildcard_match(text, pattern):
    if any(
        not isinstance(value, str) or len(value) > 20
        for value in (text, pattern)
    ):
        raise ValueError("Oba vhoda morata biti niza z največ 20 znaki.")
    if any(not ("a" <= char <= "z") for char in text):
        raise ValueError("text sme vsebovati samo črke a–z.")
    if any(
        not ("a" <= char <= "z") and char not in "?*"
        for char in pattern
    ):
        raise ValueError("pattern sme vsebovati samo a–z, ? in *.")

    matched = [True] + [False] * len(text)
    for token in pattern:
        current = [False] * (len(text) + 1)
        if token == "*":
            current[0] = matched[0]
        for j, char in enumerate(text, 1):
            if token == "*":
                current[j] = matched[j] or current[j - 1]
            else:
                current[j] = matched[j - 1] and (token == "?" or token == char)
        matched = current
    return matched[-1]


# Test 1: zvezdica, vprašaj in ujemanje celotnega besedila.
assert (
    wildcard_match("abbbc", "a*c"),
    wildcard_match("abc", "a?c"),
    wildcard_match("abc", "a*d"),
    wildcard_match("abc", "ab"),
) == (True, True, False, False)

# Test 2: prazna niza in zaporedne zvezdice.
assert (
    wildcard_match("", ""),
    wildcard_match("", "***"),
    wildcard_match("", "?"),
    wildcard_match("ab", "*?**?"),
) == (True, True, False, True)

# Test 3: neveljavni tipi, znaki in dolžine.
for text, pattern in (
    (None, "*"), ("A", "*"), ("a", "["),
    ("a" * 21, "*"), ("", "*" * 21),
):
    try:
        wildcard_match(text, pattern)
    except ValueError:
        pass
    else:
        raise AssertionError("Pričakovan ValueError.")
