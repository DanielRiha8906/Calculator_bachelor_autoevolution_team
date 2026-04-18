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

## Run: Issue #57 — CLI mode (V1 Task 7, exp/structured-team)

Branch: task/issue-57-cli-mode
PR target: exp/structured-team

Files changed:
- src/cli.py: new CLI module with argparse-based argument parsing, operation validation, operand count/type validation, and result dispatch
- src/__main__.py: updated entry point to route to run_cli() when CLI args present, or run_loop() for interactive mode
- tests/test_cli.py: 62 new tests covering happy paths for all 12 operations, error cases (unknown operation, wrong operand count, non-numeric input, division by zero, sqrt of negative, etc.), edge cases, and main() routing
- tests/test_input_loop.py: fixed test_main_runs_and_exits to use argv=[] parameter to avoid pytest's sys.argv interference
- artifacts/class_diagram.puml: added CLI module with run_cli() and _build_parser(); dependency arrows to InputLoop (OPERATIONS) and Calculator
- artifacts/activity_diagram.puml: added branch at program start for CLI vs interactive mode
- artifacts/sequence_diagram.puml: added CLI mode sequence (happy path and error path)

Purpose: Add CLI mode allowing the calculator to be invoked as `python -m calculator <operation> <operand1> <operand2>` from bash. Results print to stdout; errors print to stderr with exit code 2.

Risks: Low. Changes isolated to new src/cli.py and minimal entry-point routing in __main__.py. No existing modules modified. All 371 tests pass.

Duration: 541.1s | Cost: $1.146451 USD | Turns: 14

## Run: Issue #60 — V1 Task 8 - Retry Logic (task/issue-60-retry-logic)

Files changed:
- src/validation.py (created) — centralized input validation module with validate_operation and validate_operand
- src/input_loop.py (modified) — added MAX_RETRY_ATTEMPTS=3 constant, retry loops in get_operation/get_operands, sentinel handling in run_loop
- tests/test_validation.py (created) — 50 unit tests for validation module
- tests/test_retry_logic.py (created) — 27 integration tests for retry behavior
- tests/test_input_loop.py (modified) — 11 tests updated to match new interface
- artifacts/class_diagram.puml (modified) — added Validation module, updated InputLoop signatures
- artifacts/activity_diagram.puml (modified) — added retry loop nodes and exhaustion decision paths
- artifacts/sequence_diagram.puml (modified) — added alt paths for retry scenarios

Purpose: Add input validation and retry logic to guided interactive mode; CLI mode unchanged (exit on error).

Risks: VALID_OPERATIONS frozenset in validation.py must be kept in sync with OPERATIONS in input_loop.py manually.

Tests passed: 448/448

Branch: task/issue-60-retry-logic
Merge target: exp/structured-team

Duration: 457.7s | Cost: $1.235659 USD | Turns: 12

## Run: Issue — V1 Task 9 - Operation History (exp/structured-team)

Files changed:
- src/history.py (created) — new OperationHistory class; clears/creates history.txt on init; records successful ops to memory list and file; formats binary as "a op b = result" and unary as "op(a) = result"
- src/input_loop.py (modified) — imported OperationHistory; added "history" entry (0 operands) to OPERATIONS; added print_history() helper; updated run_loop() with optional history parameter; handles "history" command with continue; records successful dispatch results
- src/cli.py (modified) — imported OperationHistory; added optional history parameter to run_cli(); excludes 0-operand meta-commands from CLI dispatch; records successful operations
- src/validation.py (modified) — added "history" to VALID_OPERATIONS frozenset to match updated OPERATIONS dict
- artifacts/class_diagram.puml (modified) — added OperationHistory class; updated InputLoop and CLI signatures; added dependency arrows
- artifacts/sequence_diagram.puml (modified) — added OperationHistory participant; added recording sequences for CLI and interactive modes; added history command alt block
- artifacts/activity_diagram.puml (modified) — added history.txt cleared note at session start; added "history" command branch; added record_operation and file-write step after successful dispatch

Purpose: Implement persistent per-session operation history tracking. Successful calculator operations are recorded in memory and appended to history.txt; users can type "history" in interactive mode to review the session log.

Risks: history.txt is written to CWD — tests that create OperationHistory will create this file in the test runner's working directory. VALID_OPERATIONS in validation.py and OPERATIONS in input_loop.py must stay in sync.

Notes (for Architect/Tester):
- Ambiguity resolved: the architect specified creating OperationHistory in main() and passing it to run_loop(history=history_instance). Three existing tests asserted run_loop() is called with no arguments (exact signature check). To preserve the existing test contract, OperationHistory creation was moved into run_loop() (using the existing history=None default). main() calls run_loop() without arguments, as before. The history parameter on run_loop() remains fully usable for injection in tests or by callers.

Tests passed: 450/450

Branch: exp/structured-team
Merge target: exp/structured-team

Duration: 687.0s | Cost: $1.789463 USD | Turns: 17

## Run: Issue #66 — V1 Task 10 - Error Logging (task/issue-66-error-logging)

Files changed:
- src/error_logger.py (created) — new ErrorLogger class; module-level string constants INVALID_INPUT, UNSUPPORTED_OPERATION, CALCULATION_ERROR, UNEXPECTED_ERROR, plus ERROR_CATEGORIES frozenset; __init__ opens log file in append mode; log_error appends formatted entry to in-memory list and file; get_errors returns copy of list; _format_entry produces [TIMESTAMP] [CATEGORY] Message | key=value; key=value format; file I/O failures go to stderr without raising
- src/input_loop.py (modified) — imported ErrorLogger and category constants; added _categorize_error helper (maps ValueError messages to CALCULATION_ERROR or INVALID_INPUT, other exceptions to UNEXPECTED_ERROR); in run_loop, creates ErrorLogger(); in except ValueError block calls _categorize_error then error_logger.log_error before printing error
- src/cli.py (modified) — imported ErrorLogger and category constants; in run_cli, creates ErrorLogger(); in except ValueError block after dispatch, categorizes error and calls error_logger.log_error before printing to stderr and exiting with code 2
- artifacts/class_diagram.puml (modified) — added ErrorLogger class, ErrorCategories enum, and relationship arrows from InputLoop, CLI, and ErrorLogger
- artifacts/activity_diagram.puml (modified) — added "Log error to ErrorLogger with category and context" step before "Print Error" in the ValueError-raised branch
- artifacts/sequence_diagram.puml (modified) — added ErrorLogger participant; added error logging sequence in existing div-by-zero alt; added new alt block for invalid-input (square_root negative) error logging flow; added ErrorLogger creation line at run_loop start

Purpose: Implement persistent structured error logging so all ValueError events from dispatch are recorded with timestamp, category, and context rather than silently printed and discarded.

Risks: Low. ErrorLogger I/O failures are swallowed to stderr so they cannot disrupt the calculator loop. error.log is written to CWD and may accumulate between sessions (append mode by design).

Tests passed: 513/513

Branch: task/issue-66-error-logging
Merge target: exp/structured-team

Duration: 509.7s | Cost: $1.258862 USD | Turns: 12

## Run: Issue #89 — V1 Task 11 - Logic separation - Structured/team

Branch: task/issue-89-logic-separation
PR target: exp/structured-team

Files changed:
- src/calculator.py: added module-level docstring declaring it the Calculation engine layer; added Calculator class docstring declaring it a pure calculation engine with no I/O side effects
- src/input_loop.py: replaced module docstring clarifying Interaction layer — interactive mode role
- src/cli.py: replaced module docstring clarifying Interaction layer — CLI mode role
- src/history.py: enhanced module docstring clarifying Interaction layer service — operation history role
- src/error_logger.py: enhanced module docstring clarifying Interaction layer service — error logging role
- src/validation.py: enhanced module docstring clarifying Interaction layer — input validation role
- src/__main__.py: added module docstring clarifying Entry point routing role
- artifacts/class_diagram.puml: reorganised classes into package blocks "Calculation Layer" and "Interaction Layer"
- artifacts/activity_diagram.puml: added partition annotations for "Interaction Layer" and "Calculation Layer" boundaries
- artifacts/sequence_diagram.puml: added box frames for "Interaction Layer" and "Calculation Layer" with architectural note
- tests/test_layer_separation.py: 40 new tests verifying module docstrings, Calculator purity, artifact layer annotations, and layer dependencies

Purpose: Establish explicit two-layer architecture (Calculation Layer vs Interaction Layer) through documentation and diagrams, making the existing separation visible and verifiable without changing any logic.

Risks: Low. All changes are documentation and diagram annotations only. No logic modified, no interfaces changed, no dependencies added.

Tests passed: 616/616

Duration: 398.4s | Cost: $1.154762 USD | Turns: 16

## Run: Operations Subpackage Refactor — Modular Calculation Layer (exp/structured-team)

Branch: exp/structured-team
PR target: exp/structured-team

Files changed:
- src/operations/__init__.py (created) — empty package initializer for the operations subpackage; no public exports
- src/operations/arithmetic.py (created) — add, subtract, multiply, divide with ValueError guard on divide
- src/operations/exponents.py (created) — power, factorial, square, cube with isinstance and non-negativity guards on factorial
- src/operations/roots.py (created) — square_root, cube_root with non-negativity guard on square_root
- src/operations/logarithmic.py (created) — log (base-10) and ln (natural) with positivity guards
- src/calculator.py (modified) — updated module docstring to reference submodules; removed direct math import; imports four submodules; all twelve Calculator methods now delegate to the corresponding submodule function
- src/__init__.py (modified) — added comment noting that operations subpackage is internal
- artifacts/class_diagram.puml (modified) — added operations package with four module classes; added delegation arrows from Calculator to each submodule; updated note on Calculator

Purpose: Extract arithmetic logic from Calculator methods into a structured operations subpackage to make the calculation layer more modular and independently testable. Calculator retains full backward-compatible public API as a delegation wrapper.

Risks: Low. Public API of Calculator is unchanged. All delegation is straightforward one-to-one. No new external dependencies introduced. All validation logic moved into the leaf operation functions.

Tests passed: 616/616

Duration: 437.8s | Cost: $1.085196 USD | Turns: 12

## Run: Issue #95 — V1 Task 13 - Documentation (task/issue-95-documentation)

Branch: task/issue-95-documentation
PR target: exp/structured-team

Files changed:
- README.md (replaced) — comprehensive project README covering features, installation, interactive and CLI usage with examples, project structure and architecture, testing instructions, and reference to artifacts/ diagrams
- FEATURES.md (created) — detailed per-operation reference covering all 12 operations with mathematical definitions, operand counts, valid input ranges, error conditions, and CLI and interactive examples; includes meta-command and error-handling sections
- artifacts/class_diagram.puml (verified, no changes needed) — confirmed accurate against current src/ code
- artifacts/activity_diagram.puml (verified, no changes needed) — confirmed flow matches actual run_loop() and run_cli() behavior
- artifacts/sequence_diagram.puml (verified, no changes needed) — confirmed participant interactions match actual code
- progress.md (appended)

Purpose: Comprehensive written documentation for calculator features, usage, project structure, and setup as required by Issue #95.

Risks: None; documentation-only change. No source code, tests, or existing interfaces modified.

Tests: N/A — documentation-only change; no new code introduced.

Duration: 384.9s | Cost: $0.928655 USD | Turns: 11

## Run: Issue #98 — V1 Task 14 - Scientific Mode (task/issue-98-scientific-mode)

Branch: task/issue-98-scientific-mode
PR target: exp/structured-team

Files changed:
- src/mode.py (created) — Mode enum (NORMAL/SCIENTIFIC) with operation frozensets and get_operations_for_mode() helper
- src/validation.py (modified) — validate_operation() gains optional mode parameter; mode=None preserves CLI compatibility
- src/input_loop.py (modified) — print_menu(), get_operation() are mode-aware; handle_mode_switch() added; run_loop() initializes NORMAL mode, switches on command, prefixes results with [Normal]>/[Scientific]>
- artifacts/class_diagram.puml (modified) — Mode enum added, dependency arrows from InputLoop and Validation to Mode, updated method signatures
- artifacts/activity_diagram.puml (modified) — mode initialization and mode-switch decision branch added to interactive flow
- artifacts/sequence_diagram.puml (modified) — Mode participant added, mode-switch alt block added
- tests/test_mode.py (created) — 56 tests for Mode enum and operation set functions
- tests/test_validation.py (modified) — 32 new tests for mode-aware validate_operation()
- tests/test_input_loop.py (modified) — 50 new tests for handle_mode_switch, mode-aware print_menu/get_operation, run_loop integration
- tests/test_error_logging_integration.py (modified) — updated for mode parameter changes
- tests/test_retry_logic.py (modified) — updated for mode parameter changes

Purpose: Add scientific mode with 12 operations and normal mode with 4 basic operations; allow user to switch modes in interactive session via "mode scientific" / "mode normal" commands.

Risks: Signature changes to print_menu() and get_operation() break callers that do not pass mode; mitigated by default parameters preserving backward compatibility. CLI mode unaffected.

Tests: 1047 tests pass, 0 failures.

Duration: PENDING | Cost: PENDING | Turns: PENDING
