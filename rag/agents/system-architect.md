# RAG: system-architect

## Purpose
Accumulated architectural context for this experiment branch. Each cycle entry records key design decisions, patterns observed in `src/`, and handoff notes for the next invocation.

## Cycle Log

### 2026-04-24 — Issue #376 V3 Task 2 — Comprehensive Calculator Test Suite Plan

**Task:** Create comprehensive unit test suite for all calculator operations without modifying `src/` logic.

**Key Decisions:**
- Test-only task: zero source code changes to `src/calculator.py` or `src/__main__.py`
- Preserve existing 3 division-by-zero tests; add ~50 new tests covering add, subtract, multiply, divide
- Invalid input tests document actual Python behavior (not prescriptive fixes)
- All floating-point tests use pytest.approx() for precision tolerance
- Organize tests by operation then by scenario type (normal inputs, edge cases, invalid inputs, consistency)

**Architecture Observations:**
- Calculator class is minimal (4 methods, no type checking, no input validation)
- Existing test file has only 3 tests focused on division by zero
- No __init__.py in tests/ directory (simple flat structure)
- Test organization by operation makes maintenance and coverage verification easier

**Patterns Found:**
- pytest fixture pattern already established with `calc` fixture
- All operations perform raw Python operations (a + b, a - b, etc.) with no defensive checks

**Test Specifications Provided:**
- Addition: 9 tests (positive, negative, zero cases, floats, large numbers)
- Subtraction: 9 tests (positive, negative, zero cases, floats, large numbers)
- Multiplication: 10 tests (positive, negative, zero cases, floats, identity element)
- Division: 10 tests (existing 3 + 7 new, floats, zero dividend, zero divisor, large numbers)
- Invalid inputs: 8 tests (strings, None, type mismatches)
- Consistency/cross-operation: 6 tests (inverse operations, commutativity, non-commutativity)

**Handoff to pytest-edge-tester (WRITE):**
Implement ~52 test scenarios in `tests/test_calculator.py`. Keep existing 3 division-by-zero tests. All new tests must initially fail (not yet implemented). Organize by operation for clarity. Use pytest.approx() for floating-point comparisons.

**Handoff to python-code-implementer:**
NO SOURCE CHANGES REQUIRED. This task is test-only. If pytest-edge-tester produces failing tests, the implementer should not modify `src/` to make them pass — only the test suite is being built. The calculator implementation remains as-is.

---

### 2026-04-24 — Issue #379 — Factorial Operation Feature — DETAILED PLAN EMITTED

**Task:** Add factorial operation to Calculator class. Must handle valid non-negative integers (0→1, 1→1, n≥2→n!), explicitly reject negative integers (ValueError), and reject non-integer types (bool, float, str, None with ValueError).

**Key Decisions:**
- Single new method `factorial(self, n: int) -> int` added to Calculator class.
- Iterative (not recursive) implementation to avoid stack overflow on large n.
- Type validation executed first (bool, float, str, None all rejected with ValueError before value check).
- Value validation executed second (negative integers rejected with ValueError).
- Optional single-line demo added to `src/__main__.py` showing `calc.factorial(5)`.
- Unary operation; does not change class API or require refactoring.

**Architecture Observations (confirmed in source exploration):**
- Calculator class at `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/calculator.py` contains 4 methods (add, subtract, multiply, divide), no __init__, pure functions.
- Existing methods perform raw Python operations with no defensive validation.
- Factorial introduces first unary operation but fits existing single-responsibility pattern.
- Type validation for factorial more strict than binary ops, justified by mathematical domain.
- Tests file at `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/tests/test_calculator.py` already contains 3 division tests and 52+ other tests from V3 Task 2.

**Test Specifications Provided to pytest-edge-tester (WRITE):**
- Category 1 (Valid non-negative): 4 tests (0, 1, parametrized 2-10, large 20).
- Category 2 (Negative): 1 parametrized test (-1, -5, -100).
- Category 3 (Non-integers): 4 tests (float, string, None, bool).
- Category 4 (Type/edge): 2 tests (return type is int, match math.factorial).
- Total: 11 test functions with ~15 individual assertions when parametrized.

**Source Changes Plan for python-code-implementer:**
- File 1: `src/calculator.py` — Add method `factorial(self, n: int) -> int` with full input validation (type + value) and iterative computation. Placement: after divide method, before blank line.
- File 2 (optional): `src/__main__.py` — Add single print line `print("Factorial:", calc.factorial(5))` after Division line.

**Handoff to pytest-edge-tester (WRITE):**
Implement 11 test functions (or ~8-10 if parametrized aggressively) organized in 4 categories. All must fail initially. Use parametrize for multi-case tests. Use pytest.raises for exception testing. Match existing test style in test_calculator.py.

**Handoff to python-code-implementer (upon tester's WRITE report):**
Implement `Calculator.factorial(self, n: int) -> int` in `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/calculator.py`. Must:
1. Reject bool (ValueError, "boolean values")
2. Reject float (ValueError, "got float")
3. Reject str (ValueError, "got str")
4. Reject None (ValueError, "got NoneType")
5. Reject negative int (ValueError, "negative numbers")
6. Return 1 for n=0, return 1 for n=1, compute iteratively for n≥2.
7. Return type always int.

Execution order: pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

---

### 2026-04-24 — Issue #385 — V3 Task 5 - Expert/team — Interactive User Input Session

**Task:** Add interactive user input to calculator enabling operation selection, variable-arity operand input, result display, and multi-calculation session support.

**Key Decisions:**
- Create two new modules: `operation_registry.py` (operation discovery and arity metadata) and `interactive.py` (session handler)
- Dynamic operation discovery via reflection on Calculator class using `inspect.signature()`
- Unary detection: 1 non-self parameter; binary: 2 non-self parameters
- Interactive session loop: operation prompt → operand prompts (based on arity) → calculation → result display → continue/exit prompt → loop or exit
- Error handling: catch ValueError, ZeroDivisionError, and other exceptions; display error message; ask "Continue? (yes/no):" and allow recovery
- Input parsing: attempt float() conversion; if fails, re-prompt with "Invalid input. Please enter a number."
- Operation selection: numeric (0, 1, 2...) or name-based (TBD by implementer); invalid selection re-prompts
- No modifications to Calculator methods; no changes to operation implementations
- Existing hardcoded demo in `__main__.py` preserved; interactive mode added as new optional path

**Architecture Observations (from source exploration):**
- Calculator class (`/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/calculator.py`): 12 methods total
  - Binary (5): add, subtract, multiply, divide, power
  - Unary (7): factorial, square, cube, sqrt, cbrt, ln, log10
- No existing operation registry; operations are bare methods on class
- `__main__.py` currently calls hardcoded demo; no interactive entry point
- Test file uses pytest fixture pattern with `calc` fixture; easily extensible
- Trigonometric functions (sin, cos, tan, cot, asin, acos) mentioned in brief are NOT implemented; task uses only what exists

**Patterns Found:**
- Single-responsibility methods on Calculator class
- Type hints already present on recent methods (factorial, square, cube, etc.)
- Test organization by operation type works well
- Input/output testing requires mocking of `builtins.input` and `builtins.print`

**Test Specifications Provided to pytest-edge-tester (WRITE):**
15 comprehensive interactive scenarios in `tests/test_interactive.py`:
1. Binary operation (add) with valid operands → result displayed
2. Unary operation (factorial) with valid operand → result displayed
3. Unary operation (square) with valid operand → result displayed
4. Invalid operation selection → re-prompt
5. Non-numeric operand → re-prompt
6. Domain error (sqrt of negative) → error message, ask continue, allow recovery
7. Binary operation (divide) with valid operands → result displayed
8. Zero division error → error message, ask continue
9. Multiple calculations in session → both results shown, loop works
10. Factorial with float operand → domain error
11. Operation list displayed at start
12. User chooses "Continue: yes" → loops correctly
13. User chooses "Continue: no" → session exits
14. Operand input with whitespace/type tolerance (if applicable)
15. Float operands for binary operations → calculated correctly

All tests mock `builtins.input` and `builtins.print` to control interaction flow.

**Source Changes Plan for python-code-implementer:**
1. Create `src/operation_registry.py`:
   - Class `OperationRegistry(calculator: Calculator)`
   - Methods: `get_operations() -> List[str]`, `get_arity(op_name: str) -> int`, `call(op_name: str, *args) -> Any`
   - Uses `inspect.signature()` to determine arity
   - Sorted operation list for consistent UI
   - Full type hints

2. Create `src/interactive.py`:
   - Function `run_interactive_session(calculator: Calculator = None) -> None`
   - Function `parse_operand(user_input: str) -> float | int` (attempts float conversion; raises ValueError on fail)
   - Main loop: operation prompt → operand prompts → execute → display result or error → continue/exit
   - All exception handling in loop; no unhandled exceptions leak
   - Uses `input()` and `print()` for user interaction
   - Full type hints

3. Optionally modify `src/__main__.py`:
   - Add import: `from src.interactive import run_interactive_session`
   - Keep hardcoded `main()` unchanged (regression safety)
   - Either: add conditional flag `--interactive` in `if __name__` block, OR add comment noting interactive mode availability
   - Simplest: NO CHANGE to `__main__.py` is acceptable; interactive mode available as importable function

**No Changes to `src/calculator.py`:**
- All 12 existing methods remain unchanged
- No type validation added to binary operations
- No new methods added (trigonometric ops NOT included in this task)

**Handoff to pytest-edge-tester (WRITE):**
Write 15 test scenarios in `tests/test_interactive.py`. All tests must mock `builtins.input` (with list of user inputs in sequence) and `builtins.print` (to capture output). Each test calls `run_interactive_session(calculator)` or similar. Scenarios cover: valid calculations (unary/binary), invalid operation selection, non-numeric operands, domain errors, zero division, session loops, operation list display, continue/exit handling. All tests must FAIL initially (functions don't exist yet).

**Handoff to python-code-implementer (upon tester's WRITE report):**
Implement two new modules and optionally modify `__main__.py` per source changes plan above. Key requirements:
- OperationRegistry must correctly identify arity (1 or 2) for all 12 operations
- Interactive session must support the full flow: list → select → prompt operands → calculate → result/error → continue/exit
- All exceptions caught and handled gracefully; user can recover from any error
- Input parsing robust (float conversion, re-prompt on failure)
- Operation selection validation (re-prompt on invalid)
- Session loop correctly implements "Continue? (yes/no):" logic

Execution order: pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

---

### 2026-04-24 — PR #434 — Interactive Mode Entry Point (Unresolved Blocker)

**Task:** Address blocker feedback from Owner (DanielRiha8906): "There is no way to launch the application to get into the interactive mode. Change __main__.py that when launched via python -m src, user input will be possible."

**Status:** The `src/interactive.py` and `src/operation_registry.py` modules are ALREADY FULLY IMPLEMENTED and FUNCTIONAL from the previous cycle (issue #385). The blocker is that `src/__main__.py` does not invoke them; it only runs a hardcoded demo.

**Current State:**
- `src/__main__.py`: imports Calculator, defines `main()` with hardcoded demo operations, calls `main()` in `if __name__` block
- `src/interactive.py`: fully implemented with `run_interactive_session()` function; accepts user input via `input()`, displays operation menu, prompts for operands, computes and displays results, handles errors gracefully, loops until user exits
- `src/operation_registry.py`: fully implemented; introspects Calculator class, discovers all public methods, filters to arity 1 or 2, provides get_operations(), get_arity(), call() methods

**Key Decisions:**
- Single-file change to `src/__main__.py`: replace the `main()` call with `run_interactive_session()`
- Keep existing `main()` function for backward compatibility (may be imported elsewhere)
- Add import: `from .interactive import run_interactive_session`
- Change `if __name__ == "__main__":` block from `main()` to `run_interactive_session()`
- This is a 2-line change with zero impact on existing Calculator class or test suite

**Architecture Impact:**
- MINIMAL: only the entry point changes
- `main()` is only called from `__main__` block; nothing else depends on it
- No changes to Calculator, operation_registry, or interactive modules
- Pre-existing tests continue to pass (unless they explicitly test entry point behavior)
- Backward compatible: any code doing `from src import main; main()` still works (just invokes interactive session instead of demo)

**Test Specifications for pytest-edge-tester (WRITE):**
10 scenarios in new `tests/test_interactive_entrypoint.py` or extended `tests/test_interactive.py`:
1. `__main__` block calls `run_interactive_session()` with no arguments
2. User selects 'add', provides operands 5 and 3, gets result 8
3. User selects 'factorial', provides operand 5, gets result 120
4. User completes operation, chooses 'yes' to continue, performs second operation, then exits
5. User completes operation, chooses 'no' to exit (session exits cleanly)
6. Operation list is displayed at session start
7. User enters invalid operation index (e.g., 999), sees "Invalid operation" message, re-prompted
8. User enters non-numeric operand (e.g., "abc"), sees "Invalid input" message, re-prompted
9. User selects divide with operands 5 and 0, sees "Error: Division by zero" message
10. User selects sqrt with operand -4, sees "Error:" message (domain error), session continues

All tests mock `builtins.input()` with sequence of user inputs and mock/capture `builtins.print()` to verify output.

**Source Changes Plan for python-code-implementer:**
- File: `src/__main__.py`
  - Action: Modify existing file
  - Change 1: Add import line at top: `from .interactive import run_interactive_session`
  - Change 2: Keep existing `main()` function unchanged
  - Change 3: In `if __name__ == "__main__":` block, replace `main()` with `run_interactive_session()`
  - Total: 2 lines changed (1 added, 1 modified)
  - No other files need modification

**Why This Fixes the Blocker:**
- Users can now run `python -m src` and immediately enter interactive mode
- No more hardcoded demo; interactive session accepts live user input
- All supporting infrastructure already exists and is tested
- Minimal risk: one entry point change with zero side effects

**Handoff to pytest-edge-tester (WRITE):**
Write 10 test scenarios in `tests/test_interactive_entrypoint.py` (or append to `tests/test_interactive.py`). Tests must mock `input()` and `print()` to simulate user interaction. All tests should FAIL initially because the new import and entry point do not yet exist. Tests verify:
- `run_interactive_session()` is invoked from `__main__` when module is executed
- Normal flow: operation selection → operand input → result display → continue/exit
- Error recovery: invalid operation, non-numeric operand, domain errors, zero division
- Session loop: multi-calculation sessions with proper exit handling

**Handoff to python-code-implementer:**
Implement single-file change to `src/__main__.py`:
1. Add import: `from .interactive import run_interactive_session`
2. Keep `main()` function as-is (backward compatibility)
3. Replace `main()` call in `if __name__ == "__main__":` block with `run_interactive_session()`

No other source files need modification. `src/interactive.py` and `src/operation_registry.py` are already complete and functional. All Calculator methods remain unchanged.

**Execution order:** pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

---

### 2026-04-24 — Issue #391 — V3 Task 7 - Expert/team — CLI for Bash Invocation

**Task:** Add a command-line interface (CLI) enabling bash-based calculator invocation with operation name and operand arguments, supporting both unary and binary operations.

**Requirements:**
- Accept operation name as first positional argument
- Accept operand(s) as subsequent positional arguments
- Support variable operand counts: unary operations (e.g., factorial) and binary operations (e.g., add)
- Example invocations: `python -m src add 5 7` (binary), `python -m src factorial 5` (unary)
- Invoke calculator's operation registry with parsed operands
- Print operation result to standard output
- Incorrect argument usage must produce predictable, consistent behavior with non-zero exit code

**Key Decisions:**
- Create new module `src/cli.py` with CLI argument parser and operation executor
- Reuse existing `OperationRegistry` for operation discovery and execution (no duplication)
- Auto-detect CLI vs interactive mode in `__main__.py`: if argv > 1, run CLI; else run interactive
- Error handling: argument errors and computation errors both exit with code 1
- Results printed to stdout; errors and usage messages to stderr
- Operand parsing: supports int and float (decimal point detection); non-numeric input raises ValueError
- No changes to Calculator, OperationRegistry, or interactive modules; they remain unchanged

**Architecture Observations (from source exploration):**
- OperationRegistry (`src/operation_registry.py`) already introspects Calculator and discovers 12 operations (5 binary, 7 unary)
- Interactive mode (`src/interactive.py`) already uses OperationRegistry; mirrors operand parsing pattern
- Current `__main__.py` only dispatches to interactive; no CLI support exists
- Calculator has 12 methods with proper type hints and domain validation (e.g., sqrt rejects negatives, factorial rejects non-ints)
- Test infrastructure uses pytest with fixture pattern; mocking for input/output is standard

**Patterns Observed:**
- Parse operand pattern: try int first (no decimal point), fall back to float (has decimal point)
- Error handling pattern: catch specific exceptions (ZeroDivisionError, ValueError), print to stderr, exit with non-zero code
- Operation execution pattern: OperationRegistry.call(operation_name, *operands) returns result or raises exception
- Input validation pattern: validate before execution (operand count, operand format, operation existence)

**Test Specifications Provided to pytest-edge-tester (WRITE):**
25 test scenarios in new `tests/test_cli.py`:

1. **test_cli_binary_add_valid_integers**: argv=['add', '5', '7'] → stdout='12\n', exit=0
2. **test_cli_binary_subtract_valid_integers**: argv=['subtract', '10', '3'] → stdout='7\n', exit=0
3. **test_cli_binary_multiply_valid_integers**: argv=['multiply', '4', '5'] → stdout='20\n', exit=0
4. **test_cli_binary_divide_valid_integers**: argv=['divide', '10', '2'] → stdout='5.0\n', exit=0
5. **test_cli_binary_power_valid**: argv=['power', '2', '3'] → stdout='8\n', exit=0
6. **test_cli_unary_factorial_valid**: argv=['factorial', '5'] → stdout='120\n', exit=0
7. **test_cli_unary_square_valid**: argv=['square', '4'] → stdout='16\n', exit=0
8. **test_cli_unary_cube_valid**: argv=['cube', '3'] → stdout='27\n', exit=0
9. **test_cli_unary_sqrt_valid**: argv=['sqrt', '9'] → stdout='3.0\n', exit=0
10. **test_cli_unary_cbrt_valid**: argv=['cbrt', '8'] → stdout='2.0\n', exit=0
11. **test_cli_unary_ln_valid**: argv=['ln', '2.718281828'] → stdout≈'1.0\n', exit=0
12. **test_cli_unary_log10_valid**: argv=['log10', '100'] → stdout='2.0\n', exit=0
13. **test_cli_float_operands_binary**: argv=['add', '1.5', '2.5'] → stdout='4.0\n', exit=0
14. **test_cli_negative_operands**: argv=['add', '-5', '-3'] → stdout='-8\n', exit=0
15. **test_cli_division_by_zero_error**: argv=['divide', '5', '0'] → stderr contains "Division by zero", exit=1
16. **test_cli_sqrt_negative_error**: argv=['sqrt', '-4'] → stderr contains error, exit=1
17. **test_cli_factorial_negative_error**: argv=['factorial', '-5'] → stderr contains error, exit=1
18. **test_cli_missing_operation_argument**: argv=[] → stderr contains usage message, exit=1
19. **test_cli_missing_operands_unary**: argv=['factorial'] → stderr contains "requires 1 operand", exit=1
20. **test_cli_missing_operands_binary**: argv=['add', '5'] → stderr contains "requires 2 operands", exit=1
21. **test_cli_too_many_operands_unary**: argv=['factorial', '5', '6'] → stderr contains error, exit=1
22. **test_cli_too_many_operands_binary**: argv=['add', '5', '7', '9'] → stderr contains error, exit=1
23. **test_cli_unknown_operation**: argv=['unknown_op', '5'] → stderr contains "Unknown operation", exit=1
24. **test_cli_non_numeric_operand**: argv=['add', 'abc', '5'] → stderr contains "Invalid operand", exit=1
25. **test_cli_large_number_computation**: argv=['multiply', '1000000', '1000000'] → stdout='1000000000000\n', exit=0

All tests capture stdout and stderr; verify exit code via return value or sys.exit() mock.

**Source Changes Plan for python-code-implementer:**

**File 1: Create `src/cli.py`**
- Action: Create new file
- Purpose: CLI argument parser and operation executor
- Key functions:
  - `parse_cli_operand(operand_str: str) -> Union[int, float]`: parse int or float from string
  - `run_cli(argv=None) -> int`: main CLI entry point; returns exit code (0 on success, 1 on error)
- Logic flow:
  1. Validate argv length (must have operation name)
  2. Extract operation name and operand arguments
  3. Create Calculator and OperationRegistry
  4. Validate operation exists in registry
  5. Validate operand count matches operation arity
  6. Parse operands (int/float conversion)
  7. Execute operation via registry.call()
  8. Print result to stdout on success
  9. Print error to stderr and return 1 on any failure
- Exception handling: ZeroDivisionError, ValueError, and generic Exception
- All error messages consistent and informative

**File 2: Modify `src/__main__.py`**
- Action: Modify existing file
- Changes:
  1. Add import: `from .cli import run_cli`
  2. Add `import sys` in the `if __name__ == "__main__":` block
  3. Replace hardcoded `if __name__ == "__main__": run_interactive_session()` with:
     ```
     if __name__ == "__main__":
         import sys
         # If arguments provided, run CLI mode; else run interactive mode
         if len(sys.argv) > 1:
             exit_code = run_cli()
             sys.exit(exit_code)
         else:
             run_interactive_session()
     ```
- Rationale: Auto-detects whether user wants CLI (arguments present) or interactive (no arguments)
- Backward compatibility: `python -m src` still launches interactive mode
- New capability: `python -m src add 5 7` launches CLI mode

**No Changes Required:**
- `src/calculator.py`: remains unchanged (all 12 methods functional as-is)
- `src/operation_registry.py`: remains unchanged (OperationRegistry fully supports CLI use case)
- `src/interactive.py`: remains unchanged (interactive mode independent)

**Architecture Impact:**
- New module `cli.py` follows existing patterns from `interactive.py` (operation discovery, error handling, input parsing)
- Entry point in `__main__.py` now supports both CLI and interactive modes (mutually exclusive based on argv)
- CLI mode leverages existing OperationRegistry; no duplication of operation logic
- Error handling consistent across CLI and interactive modes
- No changes to core calculator logic; all changes are presentation/input layer
- Test suite grows by ~25 CLI-specific tests; existing tests unaffected
- CLI output format: result to stdout (plain), errors to stderr (prefixed with "Error:")
- Exit codes: 0 on success, 1 on any error (argument validation, domain error, computation error)

**Handoff to pytest-edge-tester (WRITE):**
Write 25 test scenarios in `tests/test_cli.py`. Each test calls `run_cli(argv=...)` with mocked stdout/stderr (use capsys or StringIO). Scenarios cover:
- All 5 binary operations with valid inputs
- All 7 unary operations with valid inputs
- Float and negative operands
- Domain errors (sqrt negative, factorial negative, zero division)
- Argument validation (missing operation, missing operands, too many operands, unknown operation)
- Operand format validation (non-numeric input)
- Large number computation
All tests must FAIL initially (run_cli does not exist).

**Handoff to python-code-implementer (upon tester's WRITE report):**
Implement new file `src/cli.py` with `run_cli(argv=None) -> int` function and helper `parse_cli_operand(operand_str: str) -> Union[int, float]`. Modify `src/__main__.py` to dispatch based on argv length. Implementation must pass all 25 test scenarios and maintain backward compatibility with existing interactive mode.

**Execution order:** pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

---

### 2026-04-24 — PR #436 — CLI Entry Point Implementation Fix (BLOCKER RESOLUTION)

**Task:** Fix critical blocker in PR #436: `src/__main__.py` does not dispatch to `run_cli()` when command-line arguments are present, so `python -m src add 5 7` incorrectly launches interactive mode instead of executing CLI operation.

**Status:** PR describes adding `src/cli.py` with full functionality and 53 passing tests. However, the entry point (`src/__main__.py`) was not updated to conditionally dispatch to CLI mode when arguments are detected. The `src/cli.py` implementation exists and is fully functional; only the entry point wiring is missing.

**Current State (verified via source inspection):**
- `src/cli.py`: EXISTS and COMPLETE with `run_cli(argv=None) -> int` function; fully tested with 53 passing tests (verified via test_cli.py)
- `src/__main__.py`: MISSING the conditional dispatch; currently only calls `run_interactive_session()` unconditionally
- The PR claims to implement the feature but the entry point routing is unimplemented (blocker)

**Root Cause:**
- `src/__main__.py` line 15-16 invokes `run_interactive_session()` unconditionally
- No check for `len(sys.argv) > 1` to detect CLI arguments
- `run_cli()` function exists but is never called from the entry point
- As a result: `python -m src add 5 7` launches interactive mode instead of executing CLI command

**Required Fix:**
Modify `src/__main__.py` to implement argument-count conditional:
```python
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        exit_code = run_cli()
        sys.exit(exit_code)
    else:
        run_interactive_session()
```

**Architectural Impact:**
- MINIMAL: single-method entry point change
- No impact on Calculator, OperationRegistry, or other modules
- Backward compatible: `python -m src` (no args) still launches interactive
- New behavior enabled: `python -m src <op> <operands>` now correctly routes to CLI
- No changes to existing 141 tests; 53 new CLI tests are already passing (once entry point is fixed, all will pass)

**Test Specifications for pytest-edge-tester (WRITE):**
8 test scenarios to verify the entry point dispatch logic (can be added to `tests/test_cli.py` or separate):
1. **test_main_no_args_launches_interactive**: sys.argv=['src'] → run_interactive_session() called (mocked), not run_cli()
2. **test_main_with_cli_args_launches_cli**: sys.argv=['src', 'add', '5', '7'] → run_cli() called (mocked), not run_interactive_session()
3. **test_main_cli_success_exits_zero**: sys.argv=['src', 'add', '5', '7'] → exit code 0 (or no sys.exit call on success)
4. **test_main_cli_error_exits_one**: sys.argv=['src', 'unknown'] → exit code 1 (or sys.exit(1) called)
5. **test_main_interactive_no_exit**: sys.argv=['src'] → run_interactive_session() completes normally, no sys.exit() called
6. **test_cli_dispatch_correctly_invokes_run_cli_function**: Verify sys.argv is passed correctly to run_cli() (i.e., run_cli() receives argv[1:] or run_cli() uses sys.argv internally)
7. **test_cli_exit_code_zero_on_valid_operation**: sys.argv=['src', 'factorial', '5'] → produces exit code 0 and correct output
8. **test_cli_exit_code_one_on_invalid_operation**: sys.argv=['src', 'invalid_op', '5'] → produces exit code 1 (or non-zero) and error output

All tests must mock `sys.argv` and either mock/capture `sys.exit()` or verify exit behavior via subprocess invocation.

**Source Changes Plan for python-code-implementer:**

**File: `src/__main__.py`**
- Action: MODIFY existing file
- Current lines 15-16:
  ```python
  if __name__ == "__main__":
      run_interactive_session()
  ```
- Required changes:
  1. Add import at top of file: `import sys`
  2. Add import at top of file: `from .cli import run_cli` (already exists: `from .cli import run_cli` imported)
  3. Replace lines 15-16 with:
     ```python
     if __name__ == "__main__":
         if len(sys.argv) > 1:
             exit_code = run_cli()
             sys.exit(exit_code)
         else:
             run_interactive_session()
     ```
- Total: 1 import line added (`import sys`), 5 lines in entry point (replacing 2 lines)
- Verification: `import sys` is needed for `sys.argv` and `sys.exit()`; `from .cli import run_cli` already present in lines 1-2

**Why This Fixes the Blocker:**
- Restores intended behavior: CLI invocations now correctly dispatch to `run_cli()`
- Interactive invocations remain unchanged: `python -m src` still launches interactive
- All 53 CLI tests now pass (they test `run_cli()` directly; once entry point calls it, integration is complete)
- All 141 pre-existing tests remain passing (no changes to Calculator, interactive, or registry modules)
- PR can now be merged: blocker resolved with minimal, targeted change

**Handoff to pytest-edge-tester (WRITE):**
Write 8 test scenarios in `tests/test_cli.py` or new `tests/test_entrypoint.py`:
- 3 tests for CLI dispatch path: valid op, invalid op, correct exit code handling
- 2 tests for interactive dispatch path: no args invocation, no sys.exit() call
- 3 tests for integration: sys.argv mocking, run_cli() invocation verification, exit code propagation

All tests should mock `sys.argv`, mock or verify `sys.exit()` behavior, and mock `run_interactive_session()` to prevent actual interactive startup. All tests must FAIL initially because the conditional logic does not yet exist.

**Handoff to python-code-implementer:**
Modify `src/__main__.py`:
1. Verify `import sys` is present (or add it)
2. Verify `from .cli import run_cli` is present (already exists in current file)
3. Replace the unconditional `run_interactive_session()` call with the conditional dispatch logic above
4. Total modification: ~5 lines in the `if __name__ == "__main__":` block

No other files need modification. `src/cli.py` is already complete and functional. All tests will pass once the entry point correctly invokes `run_cli()` for CLI arguments and `run_interactive_session()` for no arguments.

**Execution order:** pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

---

### 2026-04-24 — Issue #394 — V3 Task 8 - Expert/team — Input Validation with Retry Mechanism

**Task:** Add retry counter mechanism to interactive mode for consecutive invalid inputs (operation selection or operand entry), with automatic session termination after 5 consecutive failures. Computation errors (domain validation, zero division) do NOT count toward the limit. CLI mode remains unchanged (fail-fast behavior).

**Current State (verified via source exploration):**
- `src/interactive.py`: fully implemented interactive session with operation menu, operand gathering loops, error handling (lines 45-113)
- `src/operation_registry.py`: complete operation discovery and execution
- `src/calculator.py`: 12 operations (5 binary, 7 unary) with domain validation on sqrt, ln, log10, factorial
- `src/cli.py`: complete CLI implementation with fail-fast behavior
- `src/__main__.py`: correctly dispatches to CLI or interactive based on argv length

**Requirements Analysis:**
1. Invalid operation index → error + re-prompt, counter increments
2. Invalid operand (non-numeric) → error + re-prompt, counter increments
3. Valid input (operation or operand) → counter resets to 0
4. Computation error (ZeroDivisionError, ValueError from domain check) → error displayed, counter NOT incremented, session continues
5. After 5 consecutive invalid inputs → session terminates with clear message
6. Counter shared across operation selection and all operand prompts
7. CLI mode unaffected (no retry loop, fail-fast exit with code 1)
8. MAX_ATTEMPTS constant = 5

**Key Decisions:**
- Add `MAX_ATTEMPTS = 5` constant at module level in `src/interactive.py`
- Initialize `retry_count = 0` before main session loop
- Increment counter on ValueError/IndexError during operation selection
- Increment counter on ValueError during operand parsing (unary and both binary operands)
- Distinguish between input validation errors (increment counter) and domain computation errors (do NOT increment)
- Display list of available operations when invalid operation is entered
- Display termination message "Too many consecutive invalid inputs. Session terminated." when limit exceeded
- Reset counter to 0 on successful operation selection or operand entry
- Reset counter to 0 on continuing session after computation error (user says "yes")

**Architecture Observations (from source code review):**
- Current `run_interactive_session()` has simple re-prompting logic (lines 56-64 for operation, lines 71-94 for operands)
- Operation selection uses try/except to catch ValueError (invalid int()) and IndexError (out of range)
- Operand gathering uses try/except to catch ValueError from `parse_operand()`
- Computation errors caught separately (lines 98-104): ZeroDivisionError, generic Exception
- No counter tracking exists; logic must be threaded through all validation points
- Continue/exit prompt (lines 107-112) re-prompts on unexpected input; should reset counter when session continues

**Test Specifications (18 scenarios for pytest-edge-tester):**
1. Valid operation → counter resets
2. Invalid operation (shows error + list) → counter increments
3. Invalid unary operand → counter increments
4. Invalid binary operand 1 → counter increments
5. Invalid binary operand 2 → counter increments
6. Counter resets after prior failures → valid operation succeeds
7. Session terminates after 5 consecutive invalid operations
8. Session terminates after 5 consecutive invalid operands
9. Mixed operation and operand failures count together → terminates at 5th attempt
10. Zero division error → counter NOT incremented, session continues
11. Sqrt negative error → counter NOT incremented, session continues
12. Factorial negative error → counter NOT incremented, session continues
13. Counter resets after computation error then valid input
14. Counter persists across multiple operations in session
15. MAX_ATTEMPTS constant = 5 (constant validation)
16. CLI mode unaffected (fail-fast with no retry)
17. Session continues after reset, doesn't exit
18. Available operations listed on invalid operation entry

**Source Changes Plan for python-code-implementer:**

**File: `src/interactive.py`**
- Action: MODIFY existing file
- Changes required:
  1. Add `MAX_ATTEMPTS = 5` constant after imports
  2. In `run_interactive_session()`, initialize `retry_count = 0` before the main `while True:` loop
  3. Modify operation selection loop (lines 55-64):
     - Wrap in try/except for ValueError and IndexError
     - On error: increment `retry_count`, print error, print available operations list, check if `retry_count >= MAX_ATTEMPTS`, if yes print termination message and `return`, else continue re-prompting
     - On success: set `op_name = operations[index]`, reset `retry_count = 0`, break loop
  4. Modify unary operand gathering loop (lines 69-77):
     - On ValueError: increment `retry_count`, print error, check limit, if exceeded print termination message and `return`, else continue re-prompting
     - On success: set `operand = parse_operand(raw)`, reset `retry_count = 0`, break loop
  5. Modify binary operand gathering loops (lines 78-95):
     - Same logic for both `operand1` and `operand2` gathering
     - Both share same `retry_count` variable (not reset between operand1 and operand2)
  6. Computation error handling (lines 98-104):
     - KEEP AS-IS: do NOT modify counter when ZeroDivisionError or domain ValueError occurs
     - Just display error and continue to continue/exit prompt
  7. Continue/exit prompt (lines 107-112):
     - On user says "yes": reset `retry_count = 0` before breaking to loop again
     - Simplest: no change needed (counter will be reset at start of next operation selection)
     - Alternative: explicitly reset to 0 before break for clarity

**No Changes to Other Files:**
- `src/calculator.py`: unchanged (all operations with domain validation as-is)
- `src/cli.py`: unchanged (fail-fast behavior preserved)
- `src/operation_registry.py`: unchanged (operation discovery unaffected)
- `src/__main__.py`: unchanged (entry point routing unaffected)

**Architectural Impact:**
- Interactive mode behavior changes: now includes retry limit and counter tracking
- Session UX improved: clear error messages and operation list on invalid operation
- Session safety: automatic termination after repeated input failures prevents infinite loops
- API unchanged: `run_interactive_session()` still takes optional calculator argument
- Backward compatibility: existing tests may need review for new counter behavior
- CLI mode unaffected: all changes scoped to interactive.py only
- Error distinction preserved: input validation errors ≠ computation domain errors

**Implementation Order:**
1. Add MAX_ATTEMPTS constant
2. Initialize retry_count in main session loop
3. Implement operation selection retry logic with counter and limit check
4. Implement unary operand retry logic with counter and limit check
5. Implement binary operand retry logic (both operands) with shared counter
6. Ensure computation errors do NOT increment counter
7. Ensure counter resets on valid input
8. Ensure session can continue after reset (or terminates when limit exceeded)
9. Test all 18 scenarios

**Execution order:** pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

---

### 2026-04-24 — Issue #397 — V3 Task 9 - Operation History Tracking

**Task:** Add operation history tracking to interactive mode. Record all successful operations in function-style format: `operation_name(arg1, ...) = result`. Allow users to display history on request. Write complete session history to `history.txt` when session ends. Each new session starts with empty history (no persistence across sessions).

**Requirements Clarification:**
- Scope: interactive mode only (no CLI history tracking)
- Format: `operation_name(arg1, arg2, ...) = result` using Python's default str() representation
- Persistence: write to `history.txt` in project root on session exit
- Error handling: only record successful operations (skip errors)
- Session isolation: fresh history for each new `run_interactive_session()` call
- File I/O: graceful error handling (no session crash on write failure)

**Key Decisions:**
- Create new `src/history.py` module with `OperationHistory` class to manage in-memory history list and file I/O
- `OperationHistory` tracks ordered list of successful operations with `record()` method
- `record(operation_name, operands, result)` formats entry as `operation_name(arg1, ...) = result`
- `display()` returns formatted string (one entry per line) for printing
- `write_to_file(filepath)` writes all entries to `history.txt` in project root; handles IOError gracefully
- Modify `src/interactive.py` to initialize `OperationHistory()` instance at session start
- After each successful operation (line 129-130), call `history.record(op_name, operands, result)` to append to history
- Before each session exit (return statement), call `history.write_to_file()` to persist to file
- No history display command in UI initially (can be added later; tests will access history.display() directly)

**Architecture Observations (from source exploration):**
- `src/interactive.py`: 144 lines, fully functional session handler with operation menu, operand gathering, error handling, continue/exit logic
- `src/calculator.py`: 12 methods (5 binary, 7 unary) all with proper type hints and domain validation
- `src/operation_registry.py`: complete introspection and operation discovery
- `src/__main__.py`: correctly dispatches CLI vs interactive based on argv
- Test infrastructure uses pytest with mocking of `builtins.input` and `builtins.print`

**Patterns Found:**
- Successful operation execution happens at line 129: `result = registry.call(op_name, *operands)`
- Session exits via 3 return paths: user selects "no", MAX_ATTEMPTS exceeded (operation), MAX_ATTEMPTS exceeded (operand)
- Error handling pattern: try/except for ValueError/ZeroDivisionError; computation errors do NOT prevent history reset
- Module responsibilities: Calculator (computation), OperationRegistry (discovery), interactive (UI loop), **history (tracking & persistence)**

**Test Specifications (30 scenarios for pytest-edge-tester in `tests/test_history.py`):**

1. **test_history_unary_square**: Verify `square(5) = 25` recorded
2. **test_history_unary_factorial**: Verify `factorial(4) = 24` recorded
3. **test_history_unary_sqrt**: Verify `sqrt(9) = 3.0` recorded
4. **test_history_binary_add**: Verify `add(10, 5) = 15` recorded
5. **test_history_binary_multiply**: Verify `multiply(3, 4) = 12` recorded
6. **test_history_binary_divide**: Verify `divide(10, 2) = 5.0` recorded
7. **test_history_float_operands**: Verify `add(1.5, 2.5) = 4.0` recorded
8. **test_history_negative_operands**: Verify `subtract(-5, -3) = -2` recorded
9. **test_history_large_numbers**: Verify `multiply(1000000, 1000000) = 1000000000000` recorded
10. **test_history_multiple_operations**: 3 operations recorded in chronological order
11. **test_history_same_operation_twice**: Same op executed twice; both results (e.g., `square(2)=4`, `square(3)=9`) recorded
12. **test_history_unary_then_binary**: Unary then binary recorded in correct order
13. **test_history_domain_error_not_recorded**: `sqrt(-4)` raises ValueError; history unchanged
14. **test_history_zero_division_not_recorded**: `divide(5, 0)` raises ZeroDivisionError; history unchanged
15. **test_history_factorial_negative_not_recorded**: `factorial(-5)` raises ValueError; history unchanged
16. **test_history_display_empty_session**: No operations; display shows "No operations recorded" or empty
17. **test_history_display_after_operation**: One operation; display shows formatted entry
18. **test_history_display_multiple**: 5 operations; display shows all 5 in order
19. **test_history_display_formatting**: Format is `operation_name(arg1, arg2) = result` with no extra spaces
20. **test_history_write_to_file_on_exit**: 3 operations → session exits → `history.txt` created with all 3 entries
21. **test_history_file_format**: File entries are one per line in format `operation_name(...) = result`
22. **test_history_file_empty_session**: 0 operations → session exits → `history.txt` empty or not created
23. **test_history_file_overwrite**: Session 1 (2 ops) → history.txt created. Session 2 (3 ops) → history.txt overwritten (only 3 ops from session 2)
24. **test_history_file_path_absolute**: `history.txt` written to project root (absolute path), not relative
25. **test_history_file_write_permission_error**: Write fails (permission denied); session logs error but exits cleanly
26. **test_history_file_io_error_graceful**: OSError/IOError during write; caught and logged; no unhandled exception
27. **test_history_display_command_in_loop**: (Optional) Display history during session; session continues
28. **test_history_tracking_across_loop_iterations**: 2 ops → display (shows 2) → continue → 1 more op → display (shows 3)
29. **test_history_fresh_session_empty**: New session instance; history is empty
30. **test_history_per_session_isolation**: Two session instances have independent history

**Source Changes Plan for python-code-implementer:**

**File 1: Create `src/history.py` (NEW)**
- Purpose: Operation history tracking and persistence
- Class `OperationHistory`:
  - `__init__()`: initialize empty list for history entries
  - `record(operation_name: str, operands: tuple, result: Any) -> None`: format and append entry
  - `display() -> str`: return formatted history string (one entry per line)
  - `get_entries() -> list[str]`: return list of history entries for testing
  - `write_to_file(filepath: str = "history.txt") -> None`: write all entries to file; handle IOError gracefully
- Helper function `format_history_entry(operation_name: str, operands: tuple, result: Any) -> str`: format single entry as `operation_name(arg1, arg2, ...) = result`
- Uses `pathlib.Path` or `os.path` to resolve project root (absolute path to `history.txt`)
- Full type hints on all public methods

**File 2: Modify `src/interactive.py` (EXISTING)**
- Add import: `from .history import OperationHistory`
- In `run_interactive_session()` function:
  - After `registry = OperationRegistry(calculator)` and `retry_count = 0`, add: `history = OperationHistory()`
  - After successful operation execution (`result = registry.call(...)`), add: `history.record(op_name, operands, result)`
  - Before each `return` statement (3 locations: user "no", operation MAX_ATTEMPTS, operand MAX_ATTEMPTS), add: `history.write_to_file()`
- No other changes to interactive.py logic

**Execution order:** pytest-edge-tester WRITE → python-code-implementer → pytest-edge-tester VERIFY → commit.

**Key Files Affected:**
- `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/interactive.py` (modify)
- `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/history.py` (create)
- `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/tests/test_history.py` (create)

**Risks & Mitigations:**
- Risk: Operands formatting (float/int representation): Mitigation: Use Python's default `str()` and `repr()` for consistency with test expectations
- Risk: File path resolution across systems: Mitigation: Use `pathlib.Path.cwd() / "history.txt"` or `os.path.abspath("history.txt")`
- Risk: IOError during file write breaks session: Mitigation: Wrap in try/except; log to stderr; allow session to exit cleanly
- Risk: History instance persists across multiple `run_interactive_session()` calls: Mitigation: Create new instance per session (line in function start, not module global)

