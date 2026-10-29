from collections import Counter


def min_cover(text, required):
    for value, limit in ((text, 40), (required, 10)):
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError("Neveljaven tip ali predolg niz.")
        if any(not ("a" <= char <= "z") for char in value):
            raise ValueError("Dovoljene so samo male črke a–z.")

    if not required:
        return ""

    needed = Counter(required)
    missing = len(required)
    left = 0
    best_start, best_length = 0, len(text) + 1

    for right, char in enumerate(text, 1):
        if needed[char] > 0:
            missing -= 1
        needed[char] -= 1

        while missing == 0:
            if right - left < best_length:
                best_start, best_length = left, right - left
            outgoing = text[left]
            needed[outgoing] += 1
            if needed[outgoing] > 0:
                missing += 1
            left += 1

    if best_length > len(text):
        return None
    return text[best_start:best_start + best_length]


# Test 1: najkrajši ustrezen del.
assert min_cover("adobecodebanc", "abc") == "banc"

# Test 2: ponovitve in izbira najzgodnejšega začetka.
assert (min_cover("aaabc", "aabc"), min_cover("baab", "ab")) == ("aabc", "ba")

# Test 3: manjkajoče črke in prazna zahteva.
assert (min_cover("abc", "aabb"), min_cover("", "")) == (None, "")
