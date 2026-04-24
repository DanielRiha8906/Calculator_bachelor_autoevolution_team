# RAG: python-code-implementer

## Purpose
Accumulated implementation context for this experiment branch. Each cycle entry records files changed, implementation decisions made to satisfy failing tests, and patterns or pitfalls found in `src/`.

## Cycle Log

### 2026-04-24 — issue-374: add advanced calculator methods

- **Task:** Add 8 new methods to `Calculator` class to satisfy 45 failing tests.
- **Files changed:** `src/calculator.py`
- **Changes made:**
  - Added `import math` at the top of the module.
  - Added `square(a)`: returns `a ** 2`.
  - Added `cube(a)`: returns `a ** 3`.
  - Added `square_root(a)`: returns `math.sqrt(a)`; raises `ValueError` if `a < 0`.
  - Added `cube_root(a)`: returns cube root handling negatives via `-(abs(a) ** (1/3))`; returns `0.0` for zero.
  - Added `factorial(n)`: guards against booleans and non-integers before delegating to `math.factorial`; raises `ValueError` for negative or non-integer inputs.
  - Added `power(base, exp)`: returns `base ** exp`.
  - Added `log(a)`: returns `math.log10(a)`; raises `ValueError` if `a <= 0`.
  - Added `ln(a)`: returns `math.log(a)`; raises `ValueError` if `a <= 0`.
- **Patterns found:**
  - `math.factorial` raises `TypeError` for non-integers, not `ValueError` — explicit isinstance guard needed to produce consistent `ValueError`.
  - Boolean is a subclass of `int` in Python; must check `isinstance(n, bool)` before `isinstance(n, int)` to reject booleans.
  - Negative cube root via `-(abs(a) ** (1/3))` avoids complex-number issues from Python's `(-x) ** (1/3)`.
- **Test result:** 68/68 passed.

### 2026-04-24 — add CLI module for interactive calculator

- **Task:** Create `src/cli.py` to satisfy 27 failing tests in `tests/test_cli.py`; update `src/__main__.py` entry point.
- **Files changed:** `src/cli.py` (created), `src/__main__.py` (modified)
- **Changes made:**
  - Created `src/cli.py` exporting: `prompt_for_first_number`, `prompt_for_operator`, `prompt_for_second_number`, `display_result`, `display_error`, `run_calculator`.
  - `prompt_for_first_number` / `prompt_for_second_number`: loop calling `input()`, parse with `float()`, catch `ValueError` and re-prompt.
  - `prompt_for_operator`: loop calling `input()`, check membership in `SUPPORTED_OPERATORS = {"+", "-", "*", "/"}`, re-prompt on invalid.
  - `display_result(first, operator, second, result)`: 4-argument signature matching test call `display_result(5, '+', 3, 8)`; prints `"{first} {operator} {second} = {result}"`.
  - `run_calculator()`: orchestrates the three prompt functions, delegates to `Calculator`, calls `display_result`, returns the numeric result as float.
  - Updated `src/__main__.py` to call `run_calculator()` from the new CLI module, wrapping in try-except for `ZeroDivisionError` and generic `Exception`.
- **Patterns found:**
  - Architect plan used different function names (`get_first_number`, `get_operator`, etc.) than the test file (`prompt_for_first_number`, `prompt_for_operator`, etc.) — always read the actual test file to determine the true required interface; the test file is authoritative.
  - `display_result` in the plan was described as 1-argument, but the test called it with 4 args — test file is the ground truth.
  - `run_calculator()` must return the numeric result (not None) so that workflow tests can assert on the value.
- **Test result:** 95/95 passed (68 existing + 27 new).

### 2026-04-24 — issue-383: add user input (CLI refactor for unary + extended operations)

- **Task:** Refactor `src/cli.py` to replace `SUPPORTED_OPERATORS` with `OPERATIONS` dict supporting 12 operations (4 binary, 8 unary), update `run_calculator` to handle both arities, add `display_result_unary` and `display_result_binary`, add private helper functions.
- **Files changed:** `src/cli.py`
- **Changes made:**
  - Replaced `SUPPORTED_OPERATORS = {"+", "-", "*", "/"}` with `OPERATIONS` dict mapping 12 keys to `(arity, method_name, display_symbol, description)` tuples.
  - Added three private helpers: `_get_operation_arity`, `_get_calculator_method`, `_get_display_symbol`.
  - Replaced `prompt_for_operator` body to validate against `OPERATIONS.keys()` and show the extended list in the prompt.
  - Added `display_result_unary(operation_key, operand, result)` — prints `symbol(operand) = result`.
  - Added `display_result_binary(operation_key, first, second, result)` — prints `first symbol second = result`.
  - Refactored `run_calculator()`: uses `getattr(calc, method_name)` for dispatch; branches on arity to call either unary or binary path; wraps in try-except for `ValueError` and `ZeroDivisionError`, calls `display_error` and re-raises.
  - Preserved `display_result(first, operator, second, result)` (4-argument legacy form) unchanged for backward compatibility.
- **Patterns found:**
  - `getattr(calc, method_name)` is a clean dispatch pattern; avoids long if/elif chains and automatically stays in sync with new Calculator methods.
  - Preserving the legacy `display_result` is essential: existing tests call it with 4 positional args; removing or renaming it would break the prior test suite.
  - The OPERATIONS dict acts as a self-documenting registry — arity, method name, display symbol, and description in one place makes future extension trivial.
- **Test result:** pending VERIFY phase.

### 2026-04-24 — issue-389: add non-interactive CLI mode

- **Task:** Implement `main_cli_noninteractive(args: list[str]) -> int` in `src/cli.py` and add mode detection in `src/__main__.py`; create `calculator/` top-level package so `python -m calculator` works from the project root. Satisfy 34 failing tests in `tests/test_cli_noninteractive.py`.
- **Files changed:** `src/cli.py`, `src/__main__.py`, `calculator/__init__.py` (new), `calculator/__main__.py` (new)
- **Changes made:**
  - Added `import sys` to `src/cli.py`.
  - Extended `OPERATIONS` dict with four new word-based keys (`"add"`, `"subtract"`, `"multiply"`, `"divide"`) pointing to the same Calculator methods as the symbol-based keys (`"+"`, `"-"`, `"*"`, `"/"`). Existing keys preserved for backward compatibility.
  - Added `_USAGE` module-level constant (multi-line usage string) and implemented `main_cli_noninteractive(args: list[str]) -> int`:
    - Returns 1 (stderr error) when `args` is empty.
    - Returns 0 (stdout usage) for `--help` / `-h`.
    - Returns 1 for unknown operation name, wrong operand count, non-numeric operand, or any Calculator exception (ZeroDivisionError, ValueError, TypeError, Exception).
    - Returns 0 and prints result on success.
  - Updated `src/__main__.py`: added `import sys`, imported `main_cli_noninteractive`, added `if len(sys.argv) > 1: sys.exit(main_cli_noninteractive(sys.argv[1:]))` before the interactive branch.
  - Created `calculator/__init__.py` (empty alias package) and `calculator/__main__.py` that delegates to `src.cli` so `python -m calculator` works from the project root without an installed package.
- **Patterns found:**
  - Subprocess integration tests used `python -m calculator` (not `python -m src`). The `src/` package is not exposed as `calculator` by name on the system Python path, so creating a thin `calculator/` top-level package is the minimal fix — no `setup.py`/`pyproject.toml` changes needed.
  - The OPERATIONS dict needed word aliases (`"add"` etc.) alongside symbol aliases (`"+"`); the tests drove operation names derived from Calculator method names, not the symbols used in interactive mode.
  - All error output goes to `sys.stderr` so pytest's `capsys.readouterr().err` can assert on it; printing to stdout would cause `err == ""` assertion failures in the error test cases.
- **Test result:** 155/155 passed (34 new + 121 existing).
