# Evolution Log

Per-cycle entries appended by the orchestrator after each completed run.

<!-- Format:
### Cycle: <YYYY-MM-DD> — Issue #N: <title>
- **Branch:** <branch>
- **Files changed:** <list>
- **Tests:** <X passed, Y failed>
- **Notes:** <anything significant>
-->

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
