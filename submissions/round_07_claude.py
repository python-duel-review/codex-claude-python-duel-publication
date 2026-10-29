import heapq


def _valid_task(t):
    return type(t) is str and len(t) == 1 and "a" <= t <= "z"


def task_order(tasks, dependencies):
    if not isinstance(tasks, (list, tuple)) or not 1 <= len(tasks) <= 7:
        raise ValueError("tasks mora biti seznam ali terka z 1–7 nalogami")
    if not all(_valid_task(t) for t in tasks):
        raise ValueError("Vsaka naloga mora biti ena mala črka a–z")
    if len(set(tasks)) != len(tasks):
        raise ValueError("Naloge morajo biti različne")
    if not isinstance(dependencies, (list, tuple)) or len(dependencies) > 12:
        raise ValueError("dependencies mora biti seznam ali terka z največ 12 pari")

    known = set(tasks)
    edges = set()  # podvojene odvisnosti štejejo enkrat
    for dep in dependencies:
        if not isinstance(dep, (list, tuple)) or len(dep) != 2:
            raise ValueError(f"Neveljavna odvisnost: {dep!r}")
        a, b = dep
        if not (_valid_task(a) and _valid_task(b)) or a not in known or b not in known:
            raise ValueError(f"Odvisnost vsebuje neznano nalogo: {dep!r}")
        edges.add((a, b))

    successors = {t: [] for t in tasks}
    indegree = {t: 0 for t in tasks}
    for a, b in edges:  # samozanka (a, a) postane cikel -> None
        successors[a].append(b)
        indegree[b] += 1

    # Kahnov algoritem z min-kopico: vedno vzamemo najmanjšo
    # razpoložljivo nalogo -> leksikografsko najmanjši vrstni red.
    heap = [t for t in tasks if indegree[t] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        t = heapq.heappop(heap)
        order.append(t)
        for nxt in successors[t]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                heapq.heappush(heap, nxt)

    return order if len(order) == len(tasks) else None


# --- Testi ---
assert task_order(["a", "b", "c"], [("b", "a"), ("b", "a")]) == ["b", "a", "c"]
assert task_order(("c", "a", "b"), []) == ["a", "b", "c"]
assert task_order(["a", "b"], [("a", "b"), ("b", "a")]) is None
