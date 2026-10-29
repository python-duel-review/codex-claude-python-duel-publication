from itertools import combinations


def _balanced(s):
    depth = 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def repair_brackets(text):
    if type(text) is not str:
        raise ValueError("Vhod mora biti niz (str)")
    if len(text) > 14:
        raise ValueError("Vhod je daljši od 14 znakov")
    for ch in text:
        if not ("a" <= ch <= "z" or ch in "()"):
            raise ValueError(f"Neveljaven znak: {ch!r}")

    # Najmanjše število odstranitev: neujemajoči ')' + preostali '('
    open_count = bad_close = 0
    for ch in text:
        if ch == "(":
            open_count += 1
        elif ch == ")":
            if open_count:
                open_count -= 1
            else:
                bad_close += 1
    k = open_count + bad_close
    if k == 0:
        return text

    # Največ 14 znakov -> preizkusimo vse izbire k oklepajev za odstranitev
    positions = [i for i, ch in enumerate(text) if ch in "()"]
    best = None
    for removed in combinations(positions, k):
        drop = set(removed)
        candidate = "".join(ch for i, ch in enumerate(text) if i not in drop)
        if _balanced(candidate) and (best is None or candidate < best):
            best = candidate
    return best


# --- Testi ---
assert repair_brackets("a)b(c)d") == "ab(c)d"
assert repair_brackets("())(") == "()"
assert repair_brackets("()())()") == "(())()" and repair_brackets("") == ""
