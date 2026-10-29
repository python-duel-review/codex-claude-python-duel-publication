from collections import deque


def escape_maze(maze):
    if not isinstance(maze, list) or not 1 <= len(maze) <= 5:
        raise ValueError("Mreža mora biti seznam z 1–5 vrsticami")
    if not all(isinstance(row, list) for row in maze):
        raise ValueError("Vsaka vrstica mora biti seznam")
    cols = len(maze[0])
    if not 1 <= cols <= 5 or any(len(row) != cols for row in maze):
        raise ValueError("Mreža mora biti pravokotna z 1–5 stolpci")
    for row in maze:
        for v in row:
            if type(v) is not int or v not in (0, 1):  # izključi tudi bool
                raise ValueError(f"Neveljavna vrednost: {v!r}")

    rows = len(maze)
    start, goal = (0, 0), (rows - 1, cols - 1)
    if maze[0][0] or maze[rows - 1][cols - 1]:
        return None

    def neighbours(r, c):
        for nr, nc in ((r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)):
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                yield nr, nc

    # BFS od cilja: razdalja vsakega polja do cilja
    dist = {goal: 0}
    queue = deque([goal])
    while queue:
        cell = queue.popleft()
        for nb in neighbours(*cell):
            if nb not in dist:
                dist[nb] = dist[cell] + 1
                queue.append(nb)
    if start not in dist:
        return None

    # Vsak korak izberi najmanjšega soseda, ki je za 1 bližje cilju
    # -> leksikografsko najmanjša med najkrajšimi potmi.
    path = [start]
    while path[-1] != goal:
        cur = path[-1]
        path.append(min(nb for nb in neighbours(*cur)
                        if dist.get(nb) == dist[cur] - 1))
    return path


# --- Testi ---
assert escape_maze([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == \
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]

assert escape_maze([[0, 1], [1, 0]]) is None

try:
    escape_maze([[0, True], [0, 0]])
    assert False, "Pričakovan ValueError"
except ValueError:
    pass
