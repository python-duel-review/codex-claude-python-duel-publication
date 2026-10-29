from heapq import heapify, heappop, heappush


def task_order(tasks, dependencies):
    if not isinstance(tasks, (list, tuple)) or not 1 <= len(tasks) <= 7:
        raise ValueError("tasks mora vsebovati od 1 do 7 nalog.")
    if any(
        not isinstance(t, str) or len(t) != 1 or not ("a" <= t <= "z")
        for t in tasks
    ):
        raise ValueError("Naloge morajo biti posamezne male črke a–z.")
    if len(set(tasks)) != len(tasks):
        raise ValueError("Naloge se ne smejo ponavljati.")
    if (
        not isinstance(dependencies, (list, tuple))
        or len(dependencies) > 12
    ):
        raise ValueError("dependencies mora biti seznam ali terka do 12 parov.")

    successors = {t: set() for t in tasks}
    indegree = {t: 0 for t in tasks}
    for pair in dependencies:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError("Odvisnost mora biti par nalog.")
        if any(not isinstance(t, str) or t not in successors for t in pair):
            raise ValueError("Odvisnost vsebuje neznano ali neveljavno nalogo.")
        a, b = pair
        if b not in successors[a]:
            successors[a].add(b)
            indegree[b] += 1

    ready = [t for t in tasks if indegree[t] == 0]
    heapify(ready)
    result = []
    while ready:
        task = heappop(ready)
        result.append(task)
        for following in successors[task]:
            indegree[following] -= 1
            if indegree[following] == 0:
                heappush(ready, following)

    return result if len(result) == len(tasks) else None


# Test 1: leksikografski vrstni red, podvojene povezave in nespremenjen vhod.
tasks = ["c", "a", "b"]
dependencies = [("b", "a"), ("b", "a")]
original = (tasks[:], dependencies[:])
assert task_order(tasks, dependencies) == ["b", "a", "c"]
assert (tasks, dependencies) == original

# Test 2: cikel.
assert task_order(["a", "b"], [("a", "b"), ("b", "a")]) is None

# Test 3: neveljaven, nehashabilen element sproži ValueError.
try:
    task_order(["a"], [(["a"], "a")])
except ValueError:
    pass
else:
    raise AssertionError("Pričakovan ValueError.")
