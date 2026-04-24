# Evolution Log

Per-cycle entries appended by the orchestrator after each completed run.

<!-- Format:
### Cycle: <YYYY-MM-DD> — Issue #N: <title>
- **Branch:** <branch>
- **Files changed:** <list>
- **Tests:** <X passed, Y failed>
- **Notes:** <anything significant>
-->

### Cycle: 2026-04-24 — Issue #399: V3 Task 10 - Structured/team (error logging)
- **Branch:** task/issue-399-error-logging
- **Files changed:** `src/error_logging.py` (new: ErrorLog class), `src/__main__.py` (added ErrorLog import + injection into cli_mode and _run_interactive_loop), `tests/test_error_logging.py` (23 new tests)
- **Tests:** 189 passed, 0 failed
- **Notes:** Added `ErrorLog` class with lazy file initialization, pipe-delimited format, ISO 8601 UTC timestamps, silent exception handling. Error logging is orthogonal to computation — no changes to Calculator class or OperationHistory. Three error categories: `invalid_input`, `unsupported_operation`, `calculation_error`. Error log (`error_log.txt`) completely separate from operation history (`history.txt`).

### Cycle: 2026-04-24 — Issue #396: V3 Task 9 - Structured/team (operation history)
- **Branch:** task/issue-396-operation-history
- **Files changed:** `src/history.py` (new: OperationHistory class), `src/__main__.py` (added history integration + "history" command), `tests/test_history.py` (23 new tests)
- **Tests:** 166 passed, 0 failed
- **Notes:** Added `OperationHistory` class with in-memory tracking + file persistence. Session isolation via file clear on construction. "history" pseudo-command in interactive loop shows current session entries. Failed/invalid operations never recorded. history_file_path injectable for test isolation.

### Cycle: 2026-04-24 — Issue #393: V3 Task 8 - Structured/team (input validation)
- **Branch:** task/issue-393-input-validation
- **Files changed:** `src/__main__.py` (consecutive-failure counter in `_run_interactive_loop`), `tests/test_interactive_validation.py` (14 new tests)
- **Tests:** 143 passed, 0 failed
- **Notes:** Added `consecutive_failures` counter to interactive loop; increments on unknown op, invalid operand, domain/math error; resets on success; exits gracefully after 3 consecutive failures. CLI mode unchanged.

### Cycle: 2026-04-24 — Issue #390: V3 Task 7 - Structured/team (CLI mode)
- **Branch:** task/issue-390-cli-mode
- **Files changed:** `src/__main__.py` (CLI + interactive refactor), `tests/test_cli_mode.py` (22 new tests)
- **Tests:** 129 passed, 0 failed
- **Notes:** Added `cli_mode()` public entry point with `_parse_cli_arguments()`, `_execute_cli_mode()`, `_run_interactive_loop()`. `main()` preserved for existing tests. `if __name__ == "__main__"` now calls `cli_mode()`.

### Cycle: 2026-04-24 — Issue #375: V3 Task 2 - Structured/team
- **Branch:** task/issue-375-unit-test-suite
- **Files changed:** `tests/test_calculator.py` (added 18 tests for add/subtract/multiply)
- **Tests:** 23 passed, 0 failed
- **Notes:** No source changes required; all Calculator operations were already implemented. Added TestCalculatorAdd (6), TestCalculatorSubtract (6), TestCalculatorMultiply (6) to existing test file alongside TestCalculatorDivide (5).
