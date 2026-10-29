def solve_sudoku(board):
    if (
        not isinstance(board, list) or len(board) != 4
        or any(not isinstance(row, list) or len(row) != 4 for row in board)
    ):
        raise ValueError("Pričakovan je seznam štirih seznamov dolžine 4.")
    if any(
        not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 4
        for row in board for v in row
    ):
        raise ValueError("Dovoljena so cela števila 0–4, brez bool.")

    grid = [row[:] for row in board]
    rows = [set() for _ in range(4)]
    cols = [set() for _ in range(4)]
    boxes = [set() for _ in range(4)]

    for r in range(4):
        for c in range(4):
            v = grid[r][c]
            if v == 0:
                continue
            b = (r // 2) * 2 + c // 2
            if v in rows[r] or v in cols[c] or v in boxes[b]:
                raise ValueError("Podvojena začetna številka.")
            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)

    def search(pos):
        if pos == 16:
            return True
        r, c = divmod(pos, 4)
        if grid[r][c]:
            return search(pos + 1)
        b = (r // 2) * 2 + c // 2
        for v in range(1, 5):
            if v in rows[r] or v in cols[c] or v in boxes[b]:
                continue
            grid[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)
            if search(pos + 1):
                return True
            rows[r].remove(v)
            cols[c].remove(v)
            boxes[b].remove(v)
            grid[r][c] = 0
        return False

    return grid if search(0) else None


# Test 1: primer in nespremenjen original.
board = [[1, 0, 3, 4], [3, 4, 1, 0], [0, 1, 4, 3], [4, 3, 0, 1]]
original = [row[:] for row in board]
expected = [[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]]
assert solve_sudoku(board) == expected and board == original

# Test 2: leksikografsko najmanjša med več rešitvami.
assert solve_sudoku([[0] * 4 for _ in range(4)]) == expected

# Test 3: bool ni dovoljen.
try:
    solve_sudoku([[True, 0, 0, 0]] + [[0] * 4 for _ in range(3)])
except ValueError:
    pass
else:
    raise AssertionError("Pričakovan ValueError.")
