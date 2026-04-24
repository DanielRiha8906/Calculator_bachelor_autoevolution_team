# Evolution Log

Per-cycle entries appended by the orchestrator after each completed run.

<!-- Format:
### Cycle: <YYYY-MM-DD> — Issue #N: <title>
- **Branch:** <branch>
- **Files changed:** <list>
- **Tests:** <X passed, Y failed>
- **Notes:** <anything significant>
-->

### Cycle: 2026-04-24 — Issue #395: V3 Task 9 - Add History of Operations
- **Branch:** task/issue-395-history-of-operations
- **Files changed:** `src/calculator.py`, `src/cli.py`, `tests/test_history.py`
- **Tests:** 215 passed, 0 failed, 1 skipped
- **Notes:** Calculator made stateful with `__init__`; `_record_operation` appended after each of 12 methods on success path only; `get_history()` returns defensive copy; `display_history()` added to cli.py. 30 new history tests added.
