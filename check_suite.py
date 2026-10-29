"""Check that the corpus detects representative, deliberately incorrect algorithms.

These are synthetic probes, not contestant submissions or contestant test counts.
Run: python -I check_suite.py
"""
import copy
import importlib.util
import itertools
import json
import math
import re
import runpy
import sys
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("audit_verify", ROOT / "verify.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def no_partial_gaps(bookings, start, end):
    return [] if bookings else [(start, end)]


def largest_sudoku(board):
    flat = [value for row in board for value in row]
    for grid in reversed(audit.completed_sudokus()):
        if all(not clue or clue == answer for clue, answer in zip(flat, grid)):
            return [list(grid[i:i + 4]) for i in range(0, 16, 4)]
    return None


def reverse_maze_ties(maze):
    height, width = len(maze), len(maze[0])
    goal = height - 1, width - 1
    if maze[0][0] or maze[-1][-1]:
        return None
    queue = deque([[(0, 0)]])
    seen = {(0, 0)}
    while queue:
        path = queue.popleft()
        r, c = path[-1]
        if (r, c) == goal:
            return path
        for cell in sorted(((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)), reverse=True):
            x, y = cell
            if 0 <= x < height and 0 <= y < width and not maze[x][y] and cell not in seen:
                seen.add(cell)
                queue.append(path + [cell])
    return None


def greedy_coins(coins, amount):
    answer = []
    for coin in sorted(coins, reverse=True):
        count, amount = divmod(amount, coin)
        answer.extend([coin] * count)
    return None if amount else answer


def unlimited_decoder(text):
    audit.require(type(text) is str and len(text) <= 60)
    while True:
        updated = re.sub(r"([1-9])\[([a-z]*)\]", lambda m: m[2] * int(m[1]), text)
        if updated == text:
            audit.require(all("a" <= char <= "z" for char in updated))
            return updated
        text = updated
        if len(text) > 2000:
            # Deliberately accepts excessive expansion, without allocating huge strings.
            return "incorrectly accepted expansion"


def latest_cover(text, required):
    if not required:
        return ""
    needed = Counter(required)
    for length in range(1, len(text) + 1):
        for start in reversed(range(len(text) - length + 1)):
            candidate = text[start:start + length]
            if not needed - Counter(candidate):
                return candidate
    return None


def largest_order(tasks, dependencies):
    for order in itertools.permutations(sorted(tasks, reverse=True)):
        position = {task: i for i, task in enumerate(order)}
        if all(position[a] < position[b] for a, b in dependencies):
            return list(order)
    return None


def partial_wildcard(text, pattern):
    return audit.wildcard_expression(pattern).search(text) is not None


def largest_bracket_tie(text):
    positions = [i for i, char in enumerate(text) if char in "()"]
    best = ""
    for mask in range(1 << len(positions)):
        removed = {positions[i] for i in range(len(positions)) if mask >> i & 1}
        candidate = "".join(char for i, char in enumerate(text) if i not in removed)
        balance = 0
        good = True
        for char in candidate:
            balance += (char == "(") - (char == ")")
            if balance < 0:
                good = False
                break
        if good and balance == 0 and (len(candidate), candidate) > (len(best), best):
            best = candidate
    return best


def latest_product_tie(nums):
    return max((math.prod(nums[i:j + 1]), i, j)
               for i in range(len(nums)) for j in range(i, len(nums)))


def mutating_slots(bookings, start, end):
    result = audit.slots(bookings, start, end)
    if type(bookings) is list:
        bookings.clear()
    return result


PROBES = [
    (1, "ignores_partial_free_intervals", no_partial_gaps),
    (2, "largest_instead_of_smallest_sudoku", largest_sudoku),
    (3, "reverse_lexicographic_shortest_path", reverse_maze_ties),
    (4, "greedy_coin_selection", greedy_coins),
    (5, "decoder_ignores_expansion_limit", unlimited_decoder),
    (6, "latest_instead_of_earliest_cover", latest_cover),
    (7, "largest_instead_of_smallest_task_order", largest_order),
    (8, "partial_instead_of_whole_text_match", partial_wildcard),
    (9, "largest_instead_of_smallest_bracket_repair", largest_bracket_tie),
    (10, "latest_instead_of_earliest_product_indices", latest_product_tie),
    (1, "mutates_booking_input_after_computing_correct_output", mutating_slots),
]


def observe_subclasses():
    """Record an ambiguous contract boundary without scoring either interpretation."""
    class DerivedInteger(int):
        pass

    class DerivedText(str):
        pass

    arguments = {
        1: ([], DerivedInteger(0), 1),
        2: ([[DerivedInteger(0), 0, 0, 0]] + [[0] * 4 for _ in range(3)],),
        3: ([[DerivedInteger(0)]],),
        4: ([DerivedInteger(1)], 1),
        5: (DerivedText("a"),),
        6: (DerivedText("a"), "a"),
        7: ([DerivedText("a")], []),
        8: (DerivedText("a"), "*"),
        9: (DerivedText("a"),),
        10: ([DerivedInteger(1)],),
    }
    observations = []
    for number, args in arguments.items():
        entry = {"round": number, "probe": "str_subclass" if 5 <= number <= 9 else "int_subclass",
                 "scored": False, "outcomes": {}}
        for label in ("codex", "claude"):
            module = runpy.run_path(str(ROOT / "submissions" / f"round_{number:02d}_{label}.py"))
            try:
                module[audit.FUNCTIONS[number]](*copy.deepcopy(args))
                status = "accepted"
            except Exception as error:
                status = type(error).__name__
            entry["outcomes"][label] = status
        observations.append(entry)
    result = {"scored": False, "reason": "Subclass policy is not consistently explicit in the supplied task wording.",
              "supplementary_submission_calls": 20, "observations": observations}
    (ROOT / "type-observations.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


def main():
    datasets = {}
    reports = []
    for number, name, function in PROBES:
        if number not in datasets:
            cases = audit.corpus(number)
            datasets[number] = [(category, args, audit.outcome(audit.REFERENCES[number], args))
                                for category, args in cases]
        detected = None
        calls = 0
        for index, (category, args, expected) in enumerate(datasets[number], 1):
            # Except for the decoder's overflow probe, target semantic mistakes
            # on valid inputs rather than irrelevant missing input validators.
            if expected["kind"] == "ValueError" and number != 5:
                continue
            arguments = copy.deepcopy(args)
            before = copy.deepcopy(arguments)
            calls += 1
            try:
                actual = function(*arguments)
                good = expected["kind"] == "return" and audit.strict_equal(actual, expected["value"])
            except ValueError:
                good = expected["kind"] == "ValueError"
            mutated = not audit.strict_equal(arguments, before)
            if not good or mutated:
                detected = {"case_id": f"r{number:02d}-{index:06d}", "category": category,
                            "arguments": audit.encoded(args), "input_mutation_detected": mutated}
                break
        reports.append({"round": number, "synthetic_bug": name, "detected": detected is not None,
                        "synthetic_function_calls": calls, "first_detecting_case": detected})
    result = {"all_detected": all(item["detected"] for item in reports),
              "synthetic_probes": len(reports), "contestant_cases_in_this_check": 0,
              "probes": reports}
    (ROOT / "suite-checks.json").write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    observe_subclasses()
    print(json.dumps({"synthetic_probes": len(reports), "detected": sum(item["detected"] for item in reports)}))
    return int(not result["all_detected"])


if __name__ == "__main__":
    raise SystemExit(main())
