def best_change(coins, amount):
    if type(amount) is not int or not 0 <= amount <= 60:
        raise ValueError("amount mora biti int od 0 do 60.")
    if not isinstance(coins, (list, tuple)) or not 1 <= len(coins) <= 8:
        raise ValueError("coins mora biti seznam ali terka dolžine 1–8.")
    if any(type(c) is not int or not 1 <= c <= 20 for c in coins):
        raise ValueError("Vrednosti kovancev morajo biti int od 1 do 20.")
    if len(set(coins)) != len(coins):
        raise ValueError("Vrednosti kovancev morajo biti različne.")

    denominations = sorted(coins, reverse=True)
    unreachable = 61
    counts = [0] + [unreachable] * amount

    for total in range(1, amount + 1):
        for coin in denominations:
            if coin <= total:
                counts[total] = min(counts[total], counts[total - coin] + 1)

    if counts[amount] == unreachable:
        return None

    result = []
    remaining = amount
    while remaining:
        # Največji kovanec, ki še omogoča optimalno število kovancev.
        for coin in denominations:
            if coin <= remaining and counts[remaining - coin] + 1 == counts[remaining]:
                result.append(coin)
                remaining -= coin
                break
    return result


# Test 1: najmanjše število kovancev in nespremenjen vhod.
coins = [1, 3, 4]
assert best_change(coins, 6) == [3, 3] and coins == [1, 3, 4]

# Test 2: leksikografsko največja optimalna rešitev.
assert best_change([2, 3, 4], 6) == [4, 2]

# Test 3: nedosegljiv znesek in ničla.
assert (best_change([4, 6], 5), best_change([4, 6], 0)) == (None, [])
