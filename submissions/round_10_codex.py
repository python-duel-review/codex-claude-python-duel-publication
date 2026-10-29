def max_product(nums):
    if not isinstance(nums, (list, tuple)) or not 1 <= len(nums) <= 10:
        raise ValueError("Vhod mora biti seznam ali terka dolžine 1–10.")
    if any(type(n) is not int or not -5 <= n <= 5 for n in nums):
        raise ValueError("Dovoljena so samo cela števila od -5 do 5, brez bool.")

    best = (nums[0], 0, 0)
    for start in range(len(nums)):
        product = 1
        for end in range(start, len(nums)):
            product *= nums[end]
            # Vrstni red pregledovanja zagotavlja pravilno izbiro ob izenačenju.
            if product > best[0]:
                best = (product, start, end)
    return best


# Test 1: največji zmnožek celotnega seznama.
assert max_product([2, -3, -2, 4]) == (48, 0, 3)

# Test 2: izenačenje in najzgodnejši začetek.
assert max_product([-2, 0, -1]) == (0, 0, 1)

# Test 3: največji zmnožek krajšega dela.
assert max_product([-2, -3, -4]) == (12, 1, 2)
