from collections import deque


def escape_maze(maze):
    if not isinstance(maze, list) or not 1 <= len(maze) <= 5:
        raise ValueError("Mreža mora imeti od 1 do 5 vrstic.")
    if any(
        not isinstance(row, list) or not 1 <= len(row) <= 5
        for row in maze
    ):
        raise ValueError("Vsaka vrstica mora biti seznam dolžine 1–5.")

    height, width = len(maze), len(maze[0])
    if any(len(row) != width for row in maze):
        raise ValueError("Mreža mora biti pravokotna.")
    if any(
        not isinstance(v, int) or isinstance(v, bool) or v not in (0, 1)
        for row in maze for v in row
    ):
        raise ValueError("Dovoljeni sta le celi števili 0 in 1, brez bool.")

    goal = (height - 1, width - 1)
    if maze[0][0] == 1 or maze[goal[0]][goal[1]] == 1:
        return None

    queue = deque([(0, 0)])
    parents = {(0, 0): None}
    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            break
        for nr, nc in sorted(((r - 1, c), (r + 1, c),
                              (r, c - 1), (r, c + 1))):
            if (
                0 <= nr < height and 0 <= nc < width
                and maze[nr][nc] == 0 and (nr, nc) not in parents
            ):
                parents[(nr, nc)] = (r, c)
                queue.append((nr, nc))

    if goal not in parents:
        return None
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parents[current]
    return path[::-1]


# Test 1: najkrajša leksikografska pot in nespremenjen original.
maze = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
original = [row[:] for row in maze]
assert escape_maze(maze) == [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
assert maze == original

# Test 2: robni primeri.
assert escape_maze([[0]]) == [(0, 0)]
assert escape_maze([[0, 1], [1, 0]]) is None
assert escape_maze([[1]]) is None

# Test 3: bool ni dovoljen.
try:
    escape_maze([[False]])
except ValueError:
    pass
else:
    raise AssertionError("Pričakovan ValueError.")
