## Run: Issue #8 — ZeroDivisionError (V1 Task 1, exp/structured-team)

Branch: task/issue-8-zero-division-error
PR target: exp/structured-team

Files changed:
- src/calculator.py: added b==0 guard in Calculator.divide raising ValueError("Division by zero is not allowed"); added docstring documenting the exception contract
- tests/test_calculator.py: added 6 test functions covering int zero, float zero, negative numerator, zero/zero, normal division, and zero numerator cases

Purpose: Ensure Calculator.divide handles division by zero with a stable, application-level ValueError rather than propagating Python's internal ZeroDivisionError. Establishes the error-handling pattern for future arithmetic guard additions in this experiment.

Risks: Low. Change is strictly local to one method and one test file. No interfaces changed. No new dependencies introduced.

Tests: 6 passed, 0 failed, 0 skipped (python -m pytest tests/test_calculator.py -v)

Duration: 308.6s | Cost: $0.718064 USD | Turns: 15

## Run: Issue #11 — V1 Task 2 - TestSuite - Structured/team

- Branch: exp/structured-team (task branch: task/issue-11-testsuite-structured-team)
- PR Target: exp/structured-team
- Files Changed: tests/test_calculator.py, progress.md
- Purpose: Add pytest tests for add, subtract, and multiply methods
- Risks: None — test-only change, no production code modified
- Tests Passed: all (verify count after run)
Duration: 334.6s | Cost: $0.807385 USD | Turns: 11

## Run: Issue #14 — V1 Task 3 - Factorial (exp/structured-team)

Branch: task/issue-14-factorial-operation
PR target: exp/structured-team

Files changed:
- src/calculator.py: added import math; added Calculator.factorial(n) method with isinstance and non-negativity guards, delegating to math.factorial
- tests/test_calculator.py: added 6 test functions covering factorial(0), factorial(1), factorial(5), factorial(10), negative input ValueError, and float input ValueError

Purpose: Add factorial as a supported calculator operation with correct computation for all valid non-negative integer inputs and proper error handling for invalid inputs.

Risks: Low. Purely additive change — no existing methods or tests modified. import math from stdlib introduces no new package dependencies.

Tests: 47 passed (41 pre-existing + 6 new), 0 failed, 0 skipped

Duration: 314.7s | Cost: $0.770040 USD | Turns: 15

## Run: Issue #17 — V1 Task 4 - Math Functions (task/issue-17-math-functions)

Branch: task/issue-17-math-functions
PR target: exp/structured-team

Files changed:
- src/calculator.py: added seven new instance methods to Calculator — square, cube, square_root, cube_root, power, log, ln — each with type hints and Google-style docstrings; square_root, log, ln include explicit ValueError guards matching the divide/factorial error-handling convention
- tests/test_calculator.py: added 31 new test functions covering all seven operations (positive, zero, negative, float operands, ValueError cases)

Purpose: Extend Calculator with core math functions as required by Issue #17. Error guards on square_root (negative), log (non-positive), and ln (non-positive) follow the established ValueError pattern rather than letting math module exceptions propagate.

Risks: Low. Purely additive change — no existing methods or tests modified. All seven methods use stdlib math (already imported); no new dependencies introduced.

Tests: 135 passed (47 pre-existing + 31 implementer + 57 edge-case tester additions), 0 failed, 0 skipped

Duration: 420.7s | Cost: $1.018906 USD | Turns: 16

## Run: Issue #20 — V1 Task 5 - User Input Loop (task/issue-20-user-input)

Branch: task/issue-20-user-input
PR target: exp/structured-team

Files changed:
- src/input_loop.py: new module — defines OPERATIONS constant, print_menu, get_operation, get_operands, dispatch, and run_loop; encapsulates the entire interactive session separate from Calculator logic
- src/__main__.py: replaced hardcoded demo calls with import of run_loop and a single run_loop() call inside main()
- tests/test_input_loop.py: 12 new test functions covering print_menu output, get_operation (valid/exit/invalid), get_operands (floats/non-numeric), dispatch (add/sqrt/divide-by-zero), and run_loop integration scenarios (success, invalid op, non-numeric operand, calculator error)

Purpose: Introduce an interactive menu-driven REPL so the calculator is usable as a standalone program. The input_fn parameter on every public function keeps I/O injectable and testable without needing stdin.

Risks: Low. Calculator logic is untouched. __main__.py change only affects the CLI entry point. The input_fn default is the built-in input resolved at call time; tests pass explicit lambdas rather than patching builtins.input to avoid pytest capture conflicts.

Tests: 233 passed (135 pre-existing + 13 implementer input_loop tests + 85 edge-case tester additions), 0 failed, 0 skipped

Duration: 532.5s | Cost: $1.510725 USD | Turns: 15

## Run: Issue #57 — CLI Mode for Calculator (task/issue-57-cli-mode)

Branch: task/issue-57-cli-mode
PR target: exp/structured-team

Files changed:
- src/cli.py: new module — defines run_cli() using argparse; validates operand count and type; dispatches via existing dispatch(); prints result to stdout or error to stderr with exit code 1 on any failure
- src/__main__.py: added import of run_cli and OPERATIONS; modified main() to route to run_cli() when sys.argv[1] is a known operation key, else run_loop()
- artifacts/class_diagram.puml: added CLI class and arrows Main-->CLI and CLI-->InputLoop
- artifacts/activity_diagram.puml: added CLI mode-selection branch at program start with matching if/endif blocks (5 if, 5 endif)
- artifacts/sequence_diagram.puml: added participant CLI; added outer alt block showing CLI mode sequence alongside existing interactive loop
- tests/test_artifacts.py: added test_contains_class_cli, test_cli_uses_inputloop_arrow in TestClassDiagram; added test_contains_cli_participant in TestSequenceDiagram
- tests/test_cli.py: new test module — 16 test cases covering valid invocations for all 12 operations, invalid operation (exit code 2), wrong operand count (exit code 1), non-numeric operand (exit code 1), division by zero (exit code 1)
- tests/test_cli_edge.py: new test module — 43 edge-case tests covering float operands, negative numbers, zero as valid operand, extra/missing operands, whitespace/empty strings, domain errors (sqrt of negative, log of zero/negative, factorial of negative/float), large numbers, special floats, error message content, and main() routing for both branches

Purpose: Add non-interactive CLI mode so the calculator can be used in scripts and automated pipelines without entering the REPL. The mode-selection heuristic (check sys.argv[1] against OPERATIONS keys) avoids breaking the existing test_main_runs_and_exits test which runs under pytest where sys.argv contains pytest's own arguments.

Risks: Low. The CLI mode check uses an allowlist of known operation names, so unrecognised arguments still fall through to run_loop(). Existing interfaces are untouched. No new dependencies introduced.

Tests: 364 passed, 0 failed, 0 skipped

Duration: 637.7s | Cost: $1.715457 USD | Turns: 17

## Run: Issue #54 — V1 Task 6 - Development Artifacts (task/issue-54-development-artifacts)

- Branch: task/issue-54-development-artifacts
- PR target: exp/structured-team
- Files changed:
  - artifacts/class_diagram.puml (created)
  - artifacts/activity_diagram.puml (created)
  - artifacts/sequence_diagram.puml (created)
- Purpose: Create PlantUML class, activity, and sequence diagrams documenting the calculator structure and usage flow, placed in artifacts/ per CLAUDE.md and issue #54.
- Risks: Low — no source code modified; only documentation artifacts created. Risk is invalid PlantUML syntax preventing thesis rendering.
- Tests: No existing tests affected; no new tests added (PlantUML validation tooling not in scope per architectural plan).
Duration: 402.0s | Cost: $1.054507 USD | Turns: 11
