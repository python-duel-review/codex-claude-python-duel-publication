# Executed verification method

## Evidence and scope

The source evidence is one supplied ZIP. Its thirty task/submission entries were copied without edits into `submissions/`; the archive's introductory README is not included as a second report. `source-manifest.json` records all thirty entry hashes and the archive SHA-256. No algorithms, comments, tests or exception messages in those entries were corrected or rewritten.

The archive's transcription/authorship claims cannot be established from the available original messages. This review verifies the supplied files against the supplied specifications. No missing original source was reconstructed.

All twenty programs were read before execution. They consist of functions, ordinary imports and top-level self-tests. No file/network operations, subprocess calls or dynamic code execution were found. The runner also syntax-parses every submission and checks a narrow import/call list as an integrity aid; that list is not a general-purpose malicious-code detector.

## Contracts and counting

The reference validates the stated ranges, container shapes and ordinary built-in scalar types. `bool` is rejected where integer values are required. Numeric/character subclasses are outside the scored corpus because acceptance is not explicit consistently across tasks; they have separate recorded observations.

For every case, the runner deep-copies the arguments, calls the submission once, compares the result with type-sensitive equality or verifies `ValueError`, and checks arguments for observable changes even when an exception occurs. Sudoku results must also use a fresh outer grid and fresh row objects. The runner does not claim to detect temporary internal mutations that are restored before return.

Task-specific lexicographic rules are required by the supplied prompts and are part of expected answers. Inputs such as duplicate Sudoku clues, invalid syntax and an expansion exceeding the decoder's stated limit require `ValueError`. Valid but infeasible instances return `None` where specified.

One case is one independent fixture invocation of one submission. Its several assertions are not counted separately. Every fixture is used for both contestants. Case IDs are round number plus generation index. Counts are not deduplicated: repeated inputs can arise across categories. Module-level self-tests and supplementary checks are counted separately. The published totals represent one final main run, not a sum of reruns.

## Corpus and reference algorithms

All random generators use `random.Random(314159 + round_number)` and ordinary deterministic loops. Complete generators, explicit invalid fixtures and boundaries are in `verify.py`. Some generated syntactic or Sudoku cases are intentionally invalid and are classified by the reference outcome; they are not all return-value cases.

| Round | Systematic coverage | Seeded/additional coverage | Reference |
| --- | --- | --- | --- |
| 1 | All 1,024 subsets of the ten nonempty intervals with endpoints in 0…4, supplied in reverse order | 250 full-range fixtures, four boundaries, 21 explicit invalid cases | Mark each occupied integer minute and coalesce free runs |
| 2 | All 625 first-row assignments in 0…4 with other cells empty; all 288 enumerated complete 4×4 solutions | 400 sampled clue masks, 300 locally consistent clue constructions, one specified unsatisfiable board, 18 explicit invalid cases | Enumerate complete row permutations, filter column/box constraints, then select first compatible grid |
| 3 | All 682 binary grids for every shape from 1×1 through 3×3 | 250 sampled grids up to 5×5, three maximum-dimension open grids, 17 explicit invalid cases | Floyd–Warshall all-pairs distances and smallest distance-decreasing next coordinate |
| 4 | All 63 nonempty subsets of denominations 1…6, each with amounts 0…18: 1,197 fixtures | 250 full-range fixtures, 20 boundary/tie fixtures, 16 explicit invalid cases | Enumerate denomination multiplicities with memoization; minimize count, then maximize sorted tuple |
| 5 | All 1,365 strings over `a1[]` of length 0…5 | 350 generated expressions, 250 raw syntax samples, nine nesting/length fixtures, 18 explicit invalid cases | Recursive-descent parsing, with the stated 120-character output limit |
| 6 | All 127 texts over `ab` of length 0…6 paired with all 15 requirements of length 0…3: 1,905 fixtures | 350 full-range fixtures, five boundaries/examples, 12 explicit invalid cases | Enumerate substring length first, then starting position; compare character multiplicities |
| 7 | All directed graphs including self-loops on 1…3 labelled tasks; all 4,096 loop-free directed graphs on four tasks: 4,626 fixtures | 250 full-range fixtures including duplicate edges, four boundaries, 18 explicit invalid cases | Enumerate task permutations in lexicographic order, checking every precedence constraint |
| 8 | All 15 texts over `ab` of length 0…3 with all 341 patterns over `ab?*` of length 0…4: 5,115 fixtures | 400 full-range fixtures, seven boundary/tie fixtures, 13 explicit invalid cases | Translate tokens to a standard-library regular expression and require `fullmatch` |
| 9 | All 3,280 strings over `()a` of length 0…7 | 350 full-range fixtures, ten boundaries/examples, 11 explicit invalid cases | Memoized interval grammar: preserve letters, delete brackets or pair an opener with each eligible closer; optimize length then lexical order |
| 10 | All 3,905 arrays over −2…2 of lengths 1…5 | 500 full-range fixtures, eight maximum-length/tie fixtures, 13 explicit invalid cases | Compute each subarray's product independently with `math.prod`; maximize product then earliest indices |

These references were written separately from contestant submissions. Some underlying mathematical principles necessarily overlap; the maximum-product task in particular naturally admits the same direct enumeration. No claim is made that every reference is a wholly different algorithmic family.

## Reference and suite checks

There are 394 reference checks in the main run: hand-derived examples, a complete-grid Sudoku count/uniqueness check, and a second deletion-mask bracket oracle cross-checked against the interval oracle on every string over `()a` of length at most five. The count of 288 Sudoku completions is also the observed result of the included enumeration, not a contestant test count.

`check_suite.py` runs eleven synthetic incorrect implementations through the corpus. Ten demonstrate representative mistakes associated with the ten tasks; one returns the correct interval result while mutating its input. The check records the first detecting case and number of synthetic calls for each probe in `suite-checks.json`. It does not execute these mutants as contestant submissions or add their calls to the main count.

The same supplementary script invokes each contestant once per round using a scalar subclass. These twenty calls have no pass/fail rubric and are recorded in `type-observations.json`. Included original self-tests execute when a module is loaded; module completion is recorded, and assertion counts are not presented as independent tests.

## Runtime and reproducibility

The recorded runtime is CPython 3.12.14 on Windows, with no third-party dependencies. `python -I` enables isolated interpreter mode; it does not restrict filesystem or network access. Code inspection preceded execution. Each round runs in a separate process with a 60-second timeout covering reference checks, fixture generation and both submissions. The reported run had no worker failures or timeouts.

`results.json` records environment fields without usernames, hostnames or local paths; source hashes; runner hash; seeds; hashes of typed fixtures and outcomes; case categories; expected exception/return/`None` counts; original self-test module status; and per-contestant counts. Failure reporting is bounded to twenty examples per submission, although every case is counted. There were no failures in the recorded run.

Per-round scratch files use an automatically cleaned temporary directory. Reproduction updates results in the extracted review directory. Output file hashes and elapsed times can change after a rerun; fixture/outcome hashes and functional counts should agree when using the recorded interpreter and unchanged sources. The archive includes a SHA-256 snapshot list for the delivered files, excluding that list itself.

## Interpretation

The test-suite outcome is a ten-round tie over the disclosed ordinary built-in-value corpus. The result does not establish universal correctness, equal performance, exact authorship or general model quality. Unscored subclass differences, unverified source provenance, unknown model conditions and finite coverage remain explicit limitations. Subjective historical scores are not recomputed from these pass counts.
