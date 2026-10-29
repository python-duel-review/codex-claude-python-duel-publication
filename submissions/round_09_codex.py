def repair_brackets(text):
    if not isinstance(text, str) or len(text) > 14:
        raise ValueError("Vhod mora biti niz z največ 14 znaki.")
    if any(
        not ("a" <= char <= "z") and char not in "()"
        for char in text
    ):
        raise ValueError("Dovoljene so samo male črke a–z in oklepaji.")

    best = ""

    def search(index, balance, candidate):
        nonlocal best
        if index == len(text):
            if balance == 0 and (
                len(candidate) > len(best)
                or (len(candidate) == len(best) and candidate < best)
            ):
                best = candidate
            return

        char = text[index]
        if char in "()":
            search(index + 1, balance, candidate)

        if char == "(":
            search(index + 1, balance + 1, candidate + char)
        elif char == ")":
            if balance > 0:
                search(index + 1, balance - 1, candidate + char)
        else:
            search(index + 1, balance, candidate + char)

    search(0, 0, "")
    return best


# Test 1: črke ostanejo nespremenjene.
assert repair_brackets("a)b(c)d") == "ab(c)d"

# Test 2: leksikografska izbira med optimalnimi rešitvami.
assert repair_brackets("()())()") == "(())()"

# Test 3: napačen vrstni red, same črke in prazen niz.
assert [repair_brackets(t) for t in ("())(", "abc", "")] == ["()", "abc", ""]
