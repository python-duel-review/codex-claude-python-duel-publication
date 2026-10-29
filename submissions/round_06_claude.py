from collections import Counter


def _check(s, name, max_len):
    if type(s) is not str:
        raise ValueError(f"{name} mora biti niz (str)")
    if len(s) > max_len:
        raise ValueError(f"{name} je daljši od {max_len} znakov")
    if any(not "a" <= ch <= "z" for ch in s):
        raise ValueError(f"{name} sme vsebovati samo male črke a–z")


def min_cover(text, required):
    _check(text, "text", 40)
    _check(required, "required", 10)
    if not required:
        return ""

    need = Counter(required)
    missing = len(required)      # koliko zahtevanih znakov še manjka
    window = Counter()
    best = None                  # (začetek, konec)
    left = 0
    for right, ch in enumerate(text):
        window[ch] += 1
        if window[ch] <= need[ch]:
            missing -= 1
        while missing == 0:
            # Strogo krajše -> pri enaki dolžini ostane najzgodnejši začetek
            if best is None or right + 1 - left < best[1] - best[0]:
                best = (left, right + 1)
            out = text[left]
            window[out] -= 1
            if window[out] < need[out]:
                missing += 1
            left += 1

    return None if best is None else text[best[0]:best[1]]


# --- Testi ---
assert min_cover("adobecodebanc", "abc") == "banc"
assert min_cover("aaabc", "aabc") == "aabc"
assert min_cover("abc", "aabb") is None
