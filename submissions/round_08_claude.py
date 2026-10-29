def _check(s, name, allowed_extra):
    if type(s) is not str:
        raise ValueError(f"{name} mora biti niz (str)")
    if len(s) > 20:
        raise ValueError(f"{name} je daljši od 20 znakov")
    for ch in s:
        if not ("a" <= ch <= "z" or ch in allowed_extra):
            raise ValueError(f"Neveljaven znak {ch!r} v {name}")


def wildcard_match(text, pattern):
    _check(text, "text", "")
    _check(pattern, "pattern", "?*")

    n, m = len(text), len(pattern)
    # dp[i][j]: ali se text[:i] ujema s pattern[:j]
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for j in range(1, m + 1):
        if pattern[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]  # zvezdica se lahko ujema s praznim nizom

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            p = pattern[j - 1]
            if p == "*":
                # prazno ujemanje  ALI  zvezdica pogoltne še en znak
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p == "?" or p == text[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[n][m]


# --- Testi ---
assert wildcard_match("abbbc", "a*c") is True
assert wildcard_match("abc", "a?c") is True and wildcard_match("abc", "a*d") is False
assert wildcard_match("", "**") is True and wildcard_match("", "?") is False
