def _fits(g, r, c, v):
    br, bc = r // 2 * 2, c // 2 * 2
    return (v not in g[r]
            and all(g[i][c] != v for i in range(4))
            and all(g[br + i][bc + j] != v for i in range(2) for j in range(2)))


def _units():
    rows = [[(r, c) for c in range(4)] for r in range(4)]
    cols = [[(r, c) for r in range(4)] for c in range(4)]
    boxes = [[(br + i, bc + j) for i in range(2) for j in range(2)]
             for br in (0, 2) for bc in (0, 2)]
    return rows + cols + boxes


def solve_sudoku(board):
    if not isinstance(board, list) or len(board) != 4:
        raise ValueError("Mreža mora biti seznam štirih seznamov")
    for row in board:
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError("Vsaka vrstica mora biti seznam s štirimi vrednostmi")
        for v in row:
            if type(v) is not int or not 0 <= v <= 4:  # izključi tudi bool
                raise ValueError(f"Neveljavna vrednost: {v!r}")

    g = [row[:] for row in board]  # kopija, original ostane nespremenjen
    for unit in _units():
        vals = [g[r][c] for r, c in unit if g[r][c]]
        if len(vals) != len(set(vals)):
            raise ValueError("Podvojene začetne številke")

    # Polja po vrsti (vrstica za vrstico), števke naraščajoče:
    # prva najdena rešitev je leksikografsko najmanjša.
    def backtrack(i):
        if i == 16:
            return True
        r, c = divmod(i, 4)
        if g[r][c]:
            return backtrack(i + 1)
        for v in range(1, 5):
            if _fits(g, r, c, v):
                g[r][c] = v
                if backtrack(i + 1):
                    return True
                g[r][c] = 0
        return False

    return g if backtrack(0) else None


# --- Testi ---
b = [[1, 0, 3, 4], [3, 4, 1, 0], [0, 1, 4, 3], [4, 3, 0, 1]]
assert solve_sudoku(b) == [[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]]
assert b[0][1] == 0  # original nespremenjen

assert solve_sudoku([[0, 0, 1, 2], [0, 4, 0, 0], [3, 0, 0, 0], [0, 0, 0, 0]]) is None

try:
    solve_sudoku([[1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    assert False, "Pričakovan ValueError"
except ValueError:
    pass
