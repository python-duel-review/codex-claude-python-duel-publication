def best_change(coins, amount):
    if not isinstance(coins, (list, tuple)) or not 1 <= len(coins) <= 8:
        raise ValueError("coins mora biti seznam ali terka z 1–8 vrednostmi")
    for c in coins:
        if type(c) is not int or not 1 <= c <= 20:  # izključi tudi bool
            raise ValueError(f"Neveljaven kovanec: {c!r}")
    if len(set(coins)) != len(coins):
        raise ValueError("Vrednosti kovancev morajo biti različne")
    if type(amount) is not int or not 0 <= amount <= 60:
        raise ValueError(f"Neveljaven znesek: {amount!r}")

    INF = float("inf")
    # dp[a] = najmanjše število kovancev za znesek a
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    if dp[amount] == INF:
        return None

    # Rekonstrukcija: vsakič vzemi največji kovanec, ki ohrani optimum.
    # Tako je seznam padajoč in leksikografsko največji.
    order = sorted(coins, reverse=True)  # kopija, vhod ostane nespremenjen
    result, rem = [], amount
    while rem:
        for c in order:
            if c <= rem and dp[rem - c] == dp[rem] - 1:
                result.append(c)
                rem -= c
                break
    return result


# --- Testi ---
assert best_change([1, 3, 4], 6) == [3, 3]
assert best_change((2, 3, 4), 6) == [4, 2]
assert best_change([4, 6], 5) is None
