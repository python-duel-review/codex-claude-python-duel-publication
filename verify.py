"""Reproduce the review using only the Python standard library.

Run: python -I verify.py
Only run this bundle after reviewing its submissions. Subprocess timeouts are
resource limits, not security isolation. The supplied code has been inspected.
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import itertools as it
import json
import math
import platform
import random
import re
import runpy
import subprocess
import sys
import tempfile
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED = 314159
FUNCTIONS = ("", "free_slots", "solve_sudoku", "escape_maze", "best_change",
             "decode_message", "min_cover", "task_order", "wildcard_match",
             "repair_brackets", "max_product")


def require(condition):
    if not condition:
        raise ValueError("Outside the supplied task contract")


def integer(value, low, high):
    return type(value) is int and low <= value <= high


def letters(value, limit, extra=""):
    return (type(value) is str and len(value) <= limit
            and all("a" <= char <= "z" or char in extra for char in value))


def sequence(value):
    return type(value) in (list, tuple)


def slots(bookings, start, end):
    require(integer(start, 0, 1440) and integer(end, 0, 1440) and start < end)
    require(sequence(bookings) and len(bookings) <= 20)
    occupied = [False] * (end - start)
    for pair in bookings:
        require(sequence(pair) and len(pair) == 2)
        a, b = pair
        require(integer(a, start, end) and integer(b, start, end) and a < b)
        for minute in range(a, b):
            occupied[minute - start] = True
    result = []
    beginning = None
    for offset, busy in enumerate(occupied + [True]):
        if not busy and beginning is None:
            beginning = start + offset
        if busy and beginning is not None:
            result.append((beginning, start + offset))
            beginning = None
    return result


@lru_cache(None)
def completed_sudokus():
    """Enumerate complete row permutations; do not solve by cell backtracking."""
    rows = tuple(it.permutations(range(1, 5)))
    grids = []
    for first in rows:
        for second in rows:
            if any(first[c] == second[c] for c in range(4)):
                continue
            if any(len(set(first[c:c + 2] + second[c:c + 2])) != 4
                   for c in (0, 2)):
                continue
            for third in rows:
                if any(third[c] in (first[c], second[c]) for c in range(4)):
                    continue
                fourth = tuple(next(iter(set(range(1, 5))
                                         - {first[c], second[c], third[c]}))
                               for c in range(4))
                if len(set(fourth)) != 4:
                    continue
                if any(len(set(third[c:c + 2] + fourth[c:c + 2])) != 4
                       for c in (0, 2)):
                    continue
                grids.append(first + second + third + fourth)
    return tuple(sorted(grids))


def sudoku(board):
    require(type(board) is list and len(board) == 4)
    require(all(type(row) is list and len(row) == 4 for row in board))
    flat = tuple(value for row in board for value in row)
    require(all(integer(value, 0, 4) for value in flat))
    units = [tuple(board[r]) for r in range(4)]
    units += [tuple(board[r][c] for r in range(4)) for c in range(4)]
    units += [tuple(board[r + dr][c + dc] for dr in (0, 1) for dc in (0, 1))
              for r in (0, 2) for c in (0, 2)]
    require(all(len([v for v in unit if v]) == len({v for v in unit if v})
                for unit in units))
    for grid in completed_sudokus():
        if all(given == 0 or given == answer for given, answer in zip(flat, grid)):
            return [list(grid[i:i + 4]) for i in range(0, 16, 4)]
    return None


def maze(grid):
    require(type(grid) is list and 1 <= len(grid) <= 5)
    require(all(type(row) is list and 1 <= len(row) <= 5 for row in grid))
    height, width = len(grid), len(grid[0])
    require(all(len(row) == width for row in grid))
    require(all(integer(v, 0, 1) for row in grid for v in row))
    cells = [(r, c) for r in range(height) for c in range(width) if grid[r][c] == 0]
    start, goal = (0, 0), (height - 1, width - 1)
    if start not in cells or goal not in cells:
        return None
    # All-pairs Floyd-Warshall distances, independently of either BFS solution.
    index = {cell: i for i, cell in enumerate(cells)}
    size = len(cells)
    distances = [[100] * size for _ in cells]
    for i, (r, c) in enumerate(cells):
        distances[i][i] = 0
        for j, (s, t) in enumerate(cells):
            if abs(r - s) + abs(c - t) == 1:
                distances[i][j] = 1
    for k in range(size):
        for i in range(size):
            for j in range(size):
                distances[i][j] = min(distances[i][j],
                                      distances[i][k] + distances[k][j])
    target = index[goal]
    if distances[index[start]][target] == 100:
        return None
    result = [start]
    while result[-1] != goal:
        current = index[result[-1]]
        candidates = [cell for cell in cells if distances[current][index[cell]] == 1
                      and distances[index[cell]][target] == distances[current][target] - 1]
        result.append(min(candidates))
    return result


def change(coins, amount):
    require(sequence(coins) and 1 <= len(coins) <= 8)
    require(all(integer(coin, 1, 20) for coin in coins))
    require(len(set(coins)) == len(coins) and integer(amount, 0, 60))
    ordered = sorted(coins, reverse=True)

    @lru_cache(None)
    def enumerate_counts(index, remaining):
        if remaining == 0:
            return ()
        if index == len(ordered):
            return None
        coin = ordered[index]
        possibilities = []
        for count in range(remaining // coin + 1):
            rest = enumerate_counts(index + 1, remaining - count * coin)
            if rest is not None:
                possibilities.append((coin,) * count + rest)
        if not possibilities:
            return None
        shortest = min(map(len, possibilities))
        return max(p for p in possibilities if len(p) == shortest)

    answer = enumerate_counts(0, amount)
    return None if answer is None else list(answer)


def decode(text):
    require(type(text) is str and len(text) <= 60)

    def parse(pos, nested):
        pieces = []
        total = 0
        while pos < len(text) and text[pos] != "]":
            token = text[pos]
            if "a" <= token <= "z":
                piece, pos = token, pos + 1
            else:
                require("1" <= token <= "9" and pos + 1 < len(text)
                        and text[pos + 1] == "[")
                body, pos = parse(pos + 2, True)
                piece = body * int(token)
            total += len(piece)
            require(total <= 120)
            pieces.append(piece)
        if nested:
            require(pos < len(text) and text[pos] == "]")
            pos += 1
        else:
            require(pos == len(text))
        return "".join(pieces), pos

    return parse(0, False)[0]


def cover(text, required):
    require(letters(text, 40) and letters(required, 10))
    if not required:
        return ""
    needed = Counter(required)
    for length in range(1, len(text) + 1):
        for start in range(len(text) - length + 1):
            candidate = text[start:start + length]
            if not needed - Counter(candidate):
                return candidate
    return None


def ordering(tasks, dependencies):
    require(sequence(tasks) and 1 <= len(tasks) <= 7)
    require(all(letters(task, 1) and len(task) == 1 for task in tasks))
    require(len(set(tasks)) == len(tasks))
    require(sequence(dependencies) and len(dependencies) <= 12)
    edges = []
    for pair in dependencies:
        require(sequence(pair) and len(pair) == 2)
        require(all(type(task) is str and task in tasks for task in pair))
        edges.append(tuple(pair))
    for permutation in it.permutations(sorted(tasks)):
        positions = {task: i for i, task in enumerate(permutation)}
        if all(positions[a] < positions[b] for a, b in edges):
            return list(permutation)
    return None


@lru_cache(None)
def wildcard_expression(pattern):
    return re.compile("".join("[a-z]*" if token == "*" else
                              "[a-z]" if token == "?" else re.escape(token)
                              for token in pattern))


def wildcard(text, pattern):
    require(letters(text, 20) and letters(pattern, 20, "?*"))
    return wildcard_expression(pattern).fullmatch(text) is not None


def brackets(text):
    require(letters(text, 14, "()"))

    @lru_cache(None)
    def interval(left, right):
        if left == right:
            return ""
        token = text[left]
        if token not in "()":
            return token + interval(left + 1, right)
        candidates = [interval(left + 1, right)]
        if token == "(":
            for close in range(left + 1, right):
                if text[close] == ")":
                    candidates.append("(" + interval(left + 1, close) + ")"
                                      + interval(close + 1, right))
        return min(candidates, key=lambda value: (-len(value), value))

    return interval(0, len(text))


def product(nums):
    require(sequence(nums) and 1 <= len(nums) <= 10)
    require(all(integer(value, -5, 5) for value in nums))
    triples = [(math.prod(nums[i:j + 1]), i, j)
               for i in range(len(nums)) for j in range(i, len(nums))]
    return max(triples, key=lambda triple: (triple[0], -triple[1], -triple[2]))


REFERENCES = (None, slots, sudoku, maze, change, decode, cover, ordering,
              wildcard, brackets, product)


def strings(alphabet, maximum):
    for length in range(maximum + 1):
        for tokens in it.product(alphabet, repeat=length):
            yield "".join(tokens)


def corpus(round_number):
    rng = random.Random(SEED + round_number)
    cases = []

    def add(category, *args):
        cases.append((category, args))

    if round_number == 1:
        intervals = list(it.combinations(range(5), 2))
        for mask in range(1 << len(intervals)):
            selected = [intervals[i] for i in range(len(intervals)) if mask >> i & 1]
            add("exhaustive_interval_subsets", selected[::-1], 0, 4)
        for _ in range(250):
            start = rng.randrange(1440)
            end = rng.randint(start + 1, 1440)
            selected = [tuple(sorted(rng.sample(range(start, end + 1), 2)))
                        for _ in range(rng.randrange(21))]
            add("seeded_full_domain", tuple(selected) if rng.randrange(2) else selected, start, end)
        for args in (([], 0, 1440), ([(0, 1440)], 0, 1440),
                     ([(0, 1)] * 20, 0, 1440), ([[0, 1], [1, 1440]], 0, 1440)):
            add("boundary", *args)
        bad = [(None, 0, 1), ({}, 0, 1), ([], False, 1), ([], 0, True),
               ([], -1, 1), ([], 0, 1441), ([], 1, 1), ([], 2, 1),
               ([], 0.0, 1), ([], "0", 1), ([(0, 1)] * 21, 0, 1),
               ([None], 0, 1), ([(0,)], 0, 1), ([(0, 1, 2)], 0, 2),
               ([(False, 1)], 0, 1), ([(0, 1.0)], 0, 1), ([(1, 1)], 0, 2),
               ([(1, 0)], 0, 2), ([(-1, 1)], 0, 2), ([(0, 3)], 0, 2),
               (["ab"], 0, 2)]
    elif round_number == 2:
        for first in it.product(range(5), repeat=4):
            add("exhaustive_first_row", [list(first)] + [[0] * 4 for _ in range(3)])
        for grid in completed_sudokus():
            add("all_complete_solutions", [list(grid[i:i + 4]) for i in range(0, 16, 4)])
        for _ in range(400):
            grid = rng.choice(completed_sudokus())
            flat = [value if rng.random() < .45 else 0 for value in grid]
            add("seeded_solution_clues", [flat[i:i + 4] for i in range(0, 16, 4)])
        for _ in range(300):
            board = [[0] * 4 for _ in range(4)]
            for index in rng.sample(range(16), rng.randrange(1, 13)):
                r, c = divmod(index, 4)
                candidates = [v for v in range(1, 5) if v not in board[r]
                              and all(board[i][c] != v for i in range(4))
                              and all(board[r // 2 * 2 + dr][c // 2 * 2 + dc] != v
                                      for dr in (0, 1) for dc in (0, 1))]
                if candidates:
                    board[r][c] = rng.choice(candidates)
            add("seeded_locally_consistent_clues", board)
        add("given_unsatisfiable", [[0, 0, 1, 2], [0, 4, 0, 0], [3, 0, 0, 0], [0] * 4])
        bad = [(None,), ((),), ([],), ([[0] * 4] * 3,), ([[0] * 4] * 5,),
               ([(0,) * 4] * 4,), ([[0] * 3] + [[0] * 4] * 3,)]
        for value in (True, False, -1, 5, 1.0, "1", None, []):
            bad.append(([[value, 0, 0, 0]] + [[0] * 4 for _ in range(3)],))
        for a, b in ((0, 1), (0, 4), (0, 5)):
            flat = [0] * 16
            flat[a] = flat[b] = 1
            bad.append(([flat[i:i + 4] for i in range(0, 16, 4)],))
    elif round_number == 3:
        for height in range(1, 4):
            for width in range(1, 4):
                for mask in range(1 << (height * width)):
                    grid = [[(mask >> (r * width + c)) & 1 for c in range(width)]
                            for r in range(height)]
                    add("exhaustive_grids_up_to_3_by_3", grid)
        for _ in range(250):
            height, width = rng.randint(1, 5), rng.randint(1, 5)
            add("seeded_full_domain", [[int(rng.random() < .3) for _ in range(width)]
                                        for _ in range(height)])
        for height, width in ((1, 5), (5, 1), (5, 5)):
            add("maximum_open_dimensions", [[0] * width for _ in range(height)])
        bad = [(None,), ((),), ([],), ([[]],), ([[0]] * 6,), ([[0] * 6],),
               ([[0], [0, 0]],), ([(0,)],), ([0],)]
        bad += [([[value]],) for value in (True, False, -1, 2, 0.0, "0", None, [])]
    elif round_number == 4:
        for mask in range(1, 1 << 6):
            coins = [i + 1 for i in range(6) if mask >> i & 1]
            for amount in range(19):
                add("exhaustive_small_denominations", coins[::-1], amount)
        for _ in range(250):
            coins = rng.sample(range(1, 21), rng.randint(1, 8))
            add("seeded_full_domain", tuple(coins) if rng.randrange(2) else coins,
                rng.randint(0, 60))
        for coins in ([1], [20], list(range(1, 9)), list(range(13, 21)), [2, 3, 4]):
            for amount in (0, 1, 59, 60):
                add("boundary_and_ties", coins, amount)
        bad = [(None, 1), ({}, 1), ([], 1), (list(range(1, 10)), 1),
               ([1, 1], 1), ([0], 1), ([21], 1), ([True], 1), ([1.0], 1),
               ([[]], 1), (["1"], 1), ([1], True), ([1], -1), ([1], 61),
               ([1], 1.0), ([1], None)]
    elif round_number == 5:
        for text in strings("a1[]", 5):
            add("exhaustive_short_syntax", text)

        def expression(depth):
            parts = []
            for _ in range(rng.randrange(4)):
                if depth and rng.random() < .55:
                    parts.append(str(rng.randint(1, 9)) + "[" + expression(depth - 1) + "]")
                else:
                    parts.append(rng.choice("abz"))
            return "".join(parts)

        accepted = 0
        while accepted < 350:
            text = expression(4)
            if len(text) <= 60:
                add("seeded_grammar_including_overflow", text)
                accepted += 1
        for _ in range(250):
            add("seeded_raw_syntax", "".join(rng.choices("ab019[]Az", k=rng.randrange(61))))
        for text in ("2[" + "a" * 57 + "]", "3[" + "a" * 40 + "]",
                     "3[" + "a" * 41 + "]", "9[9[]]", "1[" * 20 + "]" * 20,
                     "9[9[9[9[9[9[a]]]]]]", "a" * 60, "2[a3[b]]", "2[a]3[b]"):
            add("length_nesting_and_grammar_boundaries", text)
        bad = [(value,) for value in (None, True, 1, [], b"a", "a" * 61,
               "0[a]", "10[a]", "2a", "[a]", "2[a", "a]", "A", "é", "١[a]",
               "2[ ]", "1[2]", "9[9[aa]]")]
    elif round_number == 6:
        for text in strings("ab", 6):
            for required in strings("ab", 3):
                add("exhaustive_binary_strings", text, required)
        for _ in range(350):
            add("seeded_full_domain", "".join(rng.choices("abcxyz", k=rng.randrange(41))),
                "".join(rng.choices("abcxyz", k=rng.randrange(11))))
        for args in (("a" * 40, "a" * 10), ("a" * 39 + "z", "z"),
                     ("baab", "ab"), ("adobecodebanc", "abc"), ("", "")):
            add("boundary_examples_and_ties", *args)
        bad = [(None, "a"), ("a", None), (True, "a"), ("a", []),
               ("a" * 41, ""), ("", "a" * 11), ("A", ""), ("", "A"),
               ("a1", "a"), ("é", "a"), ("a", " "), (b"a", "a")]
    elif round_number == 7:
        for n in range(1, 5):
            tasks = list("abcd"[:n])
            edges = list(it.product(tasks, repeat=2)) if n <= 3 else list(it.permutations(tasks, 2))
            for mask in range(1 << len(edges)):
                selected = [edge for i, edge in enumerate(edges) if mask >> i & 1]
                add("exhaustive_graphs", tasks[::-1], selected)
        for _ in range(250):
            tasks = rng.sample(list("abcdefgxyz"), rng.randint(1, 7))
            edges = [(rng.choice(tasks), rng.choice(tasks)) for _ in range(rng.randrange(13))]
            add("seeded_full_domain", tuple(tasks) if rng.randrange(2) else tasks,
                tuple(edges) if rng.randrange(2) else edges)
        for args in ((["a"], [("a", "a")]), (["c", "a", "b"], [("b", "a")] * 12),
                     (list("gfedcba"), []), (["a", "b"], [["a", "b"]])):
            add("boundary_duplicates_and_list_pairs", *args)
        bad = [(None, []), ([], []), (list("abcdefgh"), []), (["a", "a"], []),
               (["A"], []), (["ab"], []), ([[]], []), ([True], []),
               (["a"], None), (["a"], {}), (["a"], [("a", "a")] * 13),
               (["a"], [None]), (["a"], [("a",)]), (["a"], [("a", "a", "a")]),
               (["a"], [("a", "b")]), (["a"], [(["a"], "a")]),
               (["a"], [(None, "a")]), (["a"], ["aa"])]
    elif round_number == 8:
        for text in strings("ab", 3):
            for pattern in strings("ab?*", 4):
                add("exhaustive_short_texts_and_patterns", text, pattern)
        for _ in range(400):
            add("seeded_full_domain", "".join(rng.choices("abxyz", k=rng.randrange(21))),
                "".join(rng.choices("abxyz?*", k=rng.randrange(21))))
        for args in (("a" * 20, "*" * 20), ("a" * 20, "?" * 20),
                     ("a" * 20, "*a" * 10), ("a" * 19 + "b", "*a" * 10),
                     ("", "*" * 20), ("abc", "ab"), ("ab", "*?**?")):
            add("boundary_and_ties", *args)
        bad = [(None, "*"), ("a", None), (True, "*"), ("a", []),
               ("a" * 21, "*"), ("", "*" * 21), ("A", "*"), ("a", "["),
               ("?", "*"), ("é", "*"), ("a", "é"), ("a\n", "*"), (b"a", "*")]
    elif round_number == 9:
        for text in strings("()a", 7):
            add("exhaustive_short_bracket_texts", text)
        for _ in range(350):
            add("seeded_full_domain", "".join(rng.choices("()abz", k=rng.randrange(15))))
        for text in ("(" * 14, ")" * 14, "()" * 7, ")(" * 7, "(" * 7 + ")" * 7,
                     "a" * 14, "()())()", "a)b(c)d", "(a(b)c))(", ""):
            add("maximum_length_examples_and_ties", text)
        bad = [(value,) for value in (None, True, 1, [], b"()", "a" * 15, "A", "[a]", "é", "a b", "a\n")]
    else:
        for length in range(1, 6):
            for values in it.product(range(-2, 3), repeat=length):
                add("exhaustive_small_integer_arrays", list(values))
        for _ in range(500):
            values = [rng.randint(-5, 5) for _ in range(rng.randint(1, 10))]
            add("seeded_full_domain", tuple(values) if rng.randrange(2) else values)
        for values in ([0] * 10, [1] * 10, [-1] * 10, [5] * 10, [-5] * 10,
                       [-2, 0, -1], [-2, -3, -4], [2, -3, -2, 4]):
            add("maximum_length_and_ties", values)
        bad = [(value,) for value in (None, [], (), "123", {}, [0] * 11,
                                      [True], [False], [6], [-6], [1.0], ["1"], [[]])]
    for args in bad:
        add("explicit_invalid", *args)
    return cases


def strict_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) in (list, tuple):
        return len(a) == len(b) and all(strict_equal(x, y) for x, y in zip(a, b))
    return a == b


def encoded(value):
    if type(value) is tuple:
        return {"tuple": [encoded(item) for item in value]}
    if type(value) is list:
        return [encoded(item) for item in value]
    if type(value) is bytes:
        return {"bytes_hex": value.hex()}
    if type(value) is dict:
        return {key: encoded(item) for key, item in value.items()}
    return value


def outcome(reference, args):
    try:
        return {"kind": "return", "value": reference(*copy.deepcopy(args))}
    except ValueError:
        return {"kind": "ValueError"}


def brute_brackets(text):
    positions = [i for i, char in enumerate(text) if char in "()"]
    answers = []
    for mask in range(1 << len(positions)):
        deleted = {positions[i] for i in range(len(positions)) if mask >> i & 1}
        candidate = "".join(char for i, char in enumerate(text) if i not in deleted)
        balance = 0
        good = True
        for char in candidate:
            balance += (char == "(") - (char == ")")
            if balance < 0:
                good = False
                break
        if good and balance == 0:
            answers.append(candidate)
    return min(answers, key=lambda candidate: (-len(candidate), candidate))


def self_checks(number):
    manual = {
        1: [(([(10, 20), (18, 30), (40, 50)], 0, 60), [(0, 10), (30, 40), (50, 60)]),
            (([(0, 2), (2, 3)], 0, 4), [(3, 4)])],
        2: [(([[0] * 4 for _ in range(4)],),
             [[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]]),
            (([[0, 0, 1, 2], [0, 4, 0, 0], [3, 0, 0, 0], [0] * 4],), None)],
        3: [(([[0, 0], [0, 0]],), [(0, 0), (0, 1), (1, 1)]),
            (([[0, 1], [1, 0]],), None)],
        4: [(([1, 3, 4], 6), [3, 3]), (([2, 3, 4], 6), [4, 2]),
            (([4, 6], 5), None), (([4], 0), [])],
        5: [(("2[a3[b]]",), "abbbabbb"), (("2[]a",), "a"),
            (("3[ab]c",), "abababc")],
        6: [(("baab", "ab"), "ba"), (("aaabc", "aabc"), "aabc"),
            (("abc", "aabb"), None), (("", ""), "")],
        7: [((["a", "b", "c"], [("b", "a")]), ["b", "a", "c"]),
            ((["a"], [("a", "a")]), None)],
        8: [(("abc", "a?c"), True), (("abc", "ab"), False),
            (("", "**"), True), (("", "?"), False)],
        9: [(("a)b(c)d",), "ab(c)d"), (("()())()",), "(())()"),
            (("())(",), "()")],
        10: [(([2, -3, -2, 4],), (48, 0, 3)), (([-2, 0, -1],), (0, 0, 1)),
             (([-2, -3, -4],), (12, 1, 2))],
    }
    checks = 0
    for args, expected in manual[number]:
        if not strict_equal(REFERENCES[number](*args), expected):
            raise RuntimeError("Reference failed a hand-derived example")
        checks += 1
    if number == 2:
        grids = completed_sudokus()
        if len(grids) != 288 or len(set(grids)) != 288:
            raise RuntimeError("Unexpected complete Sudoku enumeration")
        checks += 1
    if number == 9:
        for text in strings("()a", 5):
            if brackets(text) != brute_brackets(text):
                raise RuntimeError("Interval oracle disagrees with deletion-mask oracle")
            checks += 1
    return checks


def source_inventory():
    inventory = {}
    allowed_imports = {"collections", "heapq", "itertools"}
    forbidden_calls = {"open", "exec", "eval", "compile", "__import__", "input", "breakpoint"}
    for path in sorted((ROOT / "submissions").iterdir()):
        if path.suffix not in (".py", ".md"):
            raise RuntimeError("Unexpected submission file")
        data = path.read_bytes()
        entry = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        if path.suffix == ".py":
            text = data.decode("utf-8")
            tree = ast.parse(text, filename=path.name)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                if isinstance(node, ast.ImportFrom):
                    imports.append(node.module or "")
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                        and node.func.id in forbidden_calls):
                    raise RuntimeError("Submission requires renewed side-effect review")
            if any(module not in allowed_imports for module in imports):
                raise RuntimeError("Submission requires renewed import review")
            entry.update(physical_lines=len(text.splitlines()), imports=sorted(set(imports)),
                         within_80_line_limit=len(text.splitlines()) <= 80)
        inventory[path.name] = entry
    return inventory


def run_round(number):
    started = time.perf_counter()
    checked = self_checks(number)
    cases = corpus(number)
    oracle = REFERENCES[number]
    expected = [outcome(oracle, args) for _, args in cases]
    for (category, _), answer in zip(cases, expected):
        if category == "explicit_invalid" and answer["kind"] != "ValueError":
            raise RuntimeError("Invalid fixture was not invalid under reference contract")
    digest = hashlib.sha256(json.dumps(
        [[category, encoded(args), encoded(answer)]
         for (category, args), answer in zip(cases, expected)],
        sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()
    report = {"round": number, "function": FUNCTIONS[number], "seed": SEED + number,
              "cases_per_contestant": len(cases), "cases_sha256": digest,
              "case_categories": dict(Counter(category for category, _ in cases)),
              "expected_ValueError_cases": sum(answer["kind"] == "ValueError" for answer in expected),
              "expected_return_cases": sum(answer["kind"] == "return" for answer in expected),
              "expected_None_cases": sum(answer["kind"] == "return" and answer["value"] is None
                                          for answer in expected),
              "oracle_self_checks": checked, "contestants": {}}
    for contestant in ("codex", "claude"):
        path = ROOT / "submissions" / f"round_{number:02d}_{contestant}.py"
        stats = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "input_mutations": 0,
                 "original_self_test_module": "not_run", "failures": []}
        # Executes the complete supplied module, including its own original tests.
        # Their assertions/calls are NOT counted as independent test cases.
        try:
            namespace = runpy.run_path(str(path), run_name="__audit__")
            function = namespace[FUNCTIONS[number]]
            stats["original_self_test_module"] = "passed"
        except Exception as error:
            stats["original_self_test_module"] = "failed:" + type(error).__name__
            stats["skipped"] = len(cases)
            report["contestants"][contestant] = stats
            continue
        for index, ((category, args), answer) in enumerate(zip(cases, expected), 1):
            arguments = copy.deepcopy(args)
            before = copy.deepcopy(arguments)
            actual, raised = None, None
            try:
                actual = function(*arguments)
            except Exception as error:
                raised = type(error).__name__
                error_is_valueerror = isinstance(error, ValueError)
            mutated = not strict_equal(arguments, before)
            stats["input_mutations"] += int(mutated)
            if answer["kind"] == "ValueError":
                good = raised is not None and error_is_valueerror
            else:
                good = raised is None and strict_equal(actual, answer["value"])
                if good and number == 2 and actual is not None:
                    good = actual is not arguments[0] and all(
                        row is not original_row for row in actual for original_row in arguments[0])
            good = good and not mutated
            category_key = "passed" if good else (
                "errors" if raised is not None and not error_is_valueerror else "failed")
            stats[category_key] += 1
            if not good and len(stats["failures"]) < 20:
                stats["failures"].append({"case_id": f"r{number:02d}-{index:06d}",
                    "category": category, "arguments": encoded(args), "expected": encoded(answer),
                    "actual": {"exception_type": raised} if raised else encoded(actual),
                    "input_mutated": mutated})
        report["contestants"][contestant] = stats
    report["elapsed_seconds_including_oracles_and_both_contestants"] = round(time.perf_counter() - started, 4)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", type=int, choices=range(1, 11))
    parser.add_argument("--output", default="results.json")
    options = parser.parse_args()
    destination = Path(options.output)
    if not destination.is_absolute():
        destination = ROOT / destination
    if options.worker:
        result = run_round(options.worker)
        destination.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        return 0
    started = time.perf_counter()
    inventory = source_inventory()
    frozen = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
    if {name: info["sha256"] for name, info in inventory.items()} != frozen["files_sha256"]:
        raise RuntimeError("Submission/task bytes differ from reviewed manifest")
    report = {"status": "completed", "published": False, "schema_version": 1,
              "environment": {"python": platform.python_version(),
                              "implementation": platform.python_implementation(),
                              "platform": platform.system(), "dependencies": "standard_library_only"},
              "base_seed": SEED, "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "source_archive_sha256": frozen["source_archive_sha256"],
              "source_inventory": inventory, "rounds": []}
    temporary_parts = tempfile.TemporaryDirectory(prefix="coding-duel-")
    working = Path(temporary_parts.name)
    for number in range(1, 11):
        part = working / f"round_{number:02d}.json"
        try:
            process = subprocess.run([sys.executable, "-I", str(Path(__file__).resolve()),
                "--worker", str(number), "--output", str(part)],
                cwd=ROOT, capture_output=True, text=True, timeout=60)
            if process.returncode:
                # Raw stderr may contain private absolute paths; do not include it.
                report["rounds"].append({"round": number, "status": "worker_error", "exit_code": process.returncode})
                report["status"] = "incomplete"
            else:
                result = json.loads(part.read_text(encoding="utf-8"))
                report["rounds"].append(result)
                if any(stats["original_self_test_module"] != "passed"
                       for stats in result["contestants"].values()):
                    report["status"] = "incomplete"
                print(f"Round {number:02d}: " + "; ".join(
                    f"{label} {stats['passed']}/{result['cases_per_contestant']} passed"
                    for label, stats in result["contestants"].items()), flush=True)
        except subprocess.TimeoutExpired:
            report["rounds"].append({"round": number, "status": "worker_timeout", "timeout_seconds": 60})
            report["status"] = "incomplete"
        destination.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    temporary_parts.cleanup()
    totals = {label: {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "input_mutations": 0}
              for label in ("codex", "claude")}
    for item in report["rounds"]:
        for label, stats in item.get("contestants", {}).items():
            for key in totals[label]:
                totals[label][key] += stats[key]
    report["totals_per_contestant"] = totals
    report["total_independent_submission_case_executions"] = sum(
        sum(stats[key] for key in ("passed", "failed", "errors")) for stats in totals.values())
    report["elapsed_seconds_including_process_startup"] = round(time.perf_counter() - started, 4)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "totals": totals}, sort_keys=True), flush=True)
    return int(report["status"] != "completed" or any(
        stats["failed"] or stats["errors"] for stats in totals.values()))


if __name__ == "__main__":
    raise SystemExit(main())
