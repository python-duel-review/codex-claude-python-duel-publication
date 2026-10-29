# Codex vs. Claude: verification of ten supplied Python challenges

**Both contestants passed all 28,140 independent cases per contestant in the reported run. Each of the ten rounds is tied on this test suite.** This is a verification of supplied source files, not evidence that either model is generally superior or that every possible input is correct.

## What was actually checked

A supplied ZIP contains ten task statements and twenty Python submissions labelled “Codex” and “Claude.” All thirty task/submission files in this package are byte-for-byte copies of those archive entries. Their SHA-256 hashes, and the archive hash, are in `source-manifest.json`.

The archive describes its contents as transcriptions of an informal contest. Exact correspondence to the original submissions **has not been authenticated**: the accessible closing conversation does not contain the original twenty code submissions. Model versions, generation settings, prompting conditions and revision histories are unknown. Results below apply to the supplied files and supplied task specifications.

The review ran under **CPython 3.12.14 on Windows**, using only the Python standard library. Inputs, expected answers, exception handling and tie-breaking rules are shared between contestants. The tested input values use ordinary built-in Python types; subclass behavior is reported separately.

## Functional results

| Round | Task | Cases per contestant | Expected `ValueError` cases, included in total | Codex passed | Claude passed |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | Free time slots | 1,299 | 21 | 1,299 | 1,299 |
| 2 | Lexicographically smallest 4×4 Sudoku | 1,632 | 434 | 1,632 | 1,632 |
| 3 | Lexicographically smallest shortest maze path | 952 | 17 | 952 | 952 |
| 4 | Minimum-coin change, with tie-breaking | 1,483 | 16 | 1,483 | 1,483 |
| 5 | Nested message decoder | 1,992 | 1,679 | 1,992 | 1,992 |
| 6 | Minimum covering substring | 2,272 | 12 | 2,272 | 2,272 |
| 7 | Lexicographically smallest dependency order | 4,898 | 18 | 4,898 | 4,898 |
| 8 | Whole-string wildcard matching | 5,535 | 13 | 5,535 | 5,535 |
| 9 | Minimum-deletion bracket repair | 3,651 | 11 | 3,651 | 3,651 |
| 10 | Maximum-product contiguous subarray | 4,426 | 13 | 4,426 | 4,426 |
| **Total** | | **28,140** | **2,234** | **28,140** | **28,140** |

There were zero failed cases, unexpected errors, skipped cases or observed input changes for either contestant in the reported main run. Of the 28,140 cases per contestant, 25,906 expect a return value and 2,234 expect `ValueError`. A `None` result for a valid but unsatisfiable instance is a return-value case, not an error.

One main run therefore contains **56,280 independent submission-case executions** across both contestants. These are fixture executions, not a count of unique inputs: examples, boundaries and generated cases may repeat an input. Repeated verification runs are not added to that number.

All twenty complete submission modules also executed their included self-tests successfully. Those contestant-written tests are supplementary and are **not counted** as independent cases. The reference checks, eleven synthetic bug probes and twenty supplemental subclass calls are also excluded from the main count.

## How to reproduce

Review the supplied code, extract the complete package into a separate directory, and run with CPython 3.12:

```text
python -I verify.py
python -I check_suite.py
```

The first command regenerates `results.json`; the second regenerates `suite-checks.json` and `type-observations.json`. Each round has a 60-second subprocess limit, including corpus generation and both submissions. This is a resource limit, not a security sandbox. The inspected submissions use ordinary computation and the standard-library modules `collections`, `heapq` and `itertools`; no file, network or command-execution operations were found.

The main runner verifies task/submission hashes before execution. Each round records its seed, category counts and a hash of the typed inputs plus reference outcomes. Compare these hashes and per-contestant results when reproducing the run. Elapsed times may vary; they include oracle work and both contestants and are **not comparative performance measurements**. Regenerated result files may differ in elapsed times or environment fields; the included checksums describe the saved review snapshot.

## Quality of the checks

The suite combines exhaustive bounded domains, seeded cases reaching the stated limits, explicit invalid inputs and tie-breaking examples. Its references use deliberately simple alternatives: occupied-minute enumeration, complete Sudoku-grid filtering, all-pairs maze distances, coin-multiplicity enumeration, recursive parsing, substring enumeration, permutation-based ordering, regular expressions, interval grammar optimization and direct subarray products. Details and exact bounds are in `METHOD.md` and the runner.

The main run executes 394 reference self-checks, including agreement between two distinct bracket-repair oracles on all 364 strings over `()a` of length at most five. The separate suite check detects all eleven deliberately incorrect probes, including greedy coin choice, incorrect tie-breaking, partial wildcard matching, ignored decoder expansion limits and input mutation. This demonstrates sensitivity to those particular bugs; it does not establish that the suite detects every possible defect.

## A real, unscored difference

Supplemental type probes found differing subclass policies. In rounds 1–3 and 5–9, Codex accepts the tested `int` or `str` subclass while Claude raises `ValueError`. In rounds 4 and 10, both reject the tested `int` subclass, consistent with those tasks' explicit exact-`int` requirement.

The wording of the other tasks does not settle subclass acceptance consistently. These twenty calls are disclosed in `type-observations.json` and are not scored. The ten-round tie above is conditional on the tested ordinary built-in-value domain; it is not a claim of identical behavior for every Python object.

## Historical subjective scoring

The closing conversation assigned the following scores out of 100. They are preserved only as **unverified historical subjective judgments**; they are not correctness percentages and were not reproduced by this review.

| Round | Historical Codex score | Historical Claude score |
| --- | ---: | ---: |
| 1 | 97 | 96 |
| 2 | 97 | 97 |
| 3 | 98 | 97 |
| 4 | 98 | 97 |
| 5 | 99 | 97 |
| 6 | 99 | 97 |
| 7 | 100 | 98 |
| 8 | 100 | 98 |
| 9 | 100 | 100 |
| 10 | 100 | 100 |

The supplied round 7 and 8 prompts allocate points to correctness, validation, code quality and own tests; rounds 9 and 10 specify correctness-only scoring. A consistent historical rubric for the other rounds is not available. No new subjective scores or overall model ranking are assigned here. Previous conversational test-count claims lack independently verifiable execution evidence and are not used as results.

## Limits and disclosures

The work was prepared with AI assistance by a Codex agent, including review of Codex-labelled submissions. “Independent tests” means newly constructed checks with reference outcomes separate from the contestants' implementations and self-tests; it does **not** mean an external, blind or independently certified auditor. The preparing agent knew the contestant labels. There was no separate human audit of the test code.

The full valid domains are not exhausted. Random coverage is deterministic but finite, and most exhaustive domains use small alphabets, dimensions or numeric ranges. Original task statements remain in their supplied language; English descriptions are summaries. No speed, memory or universal correctness ranking is claimed. `CODE_REVIEW.md` records specific source-level observations separately from functionality.

The package contains only task-related material. It contains no private conversation link or personal attribution. Nothing in the package establishes the identity of the person who supplied it.
