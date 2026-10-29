def max_product(nums):
    if not isinstance(nums, (list, tuple)) or not 1 <= len(nums) <= 10:
        raise ValueError("Vhod mora biti seznam ali terka z 1–10 števili")
    for x in nums:
        if type(x) is not int or not -5 <= x <= 5:  # izključi tudi bool
            raise ValueError(f"Neveljavna vrednost: {x!r}")

    best = None  # (zmnožek, začetek, konec)
    # Začetek in konec naraščata; posodobimo le pri strogo večjem zmnožku,
    # zato pri izenačenju ostane najmanjši začetek, nato najmanjši konec.
    for start in range(len(nums)):
        product = 1
        for end in range(start, len(nums)):
            product *= nums[end]
            if best is None or product > best[0]:
                best = (product, start, end)
    return best


# --- Testi ---
assert max_product([2, -3, -2, 4]) == (48, 0, 3)
assert max_product((-2, 0, -1)) == (0, 0, 1)
assert max_product([-2, -3, -4]) == (12, 1, 2)
