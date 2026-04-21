## Run: Issue #233 — V2 Task 1 - Naive/team

- **Branch:** task/issue-233-division-input-tests
- **PR target:** exp2/naive-team
- **Date:** 2026-04-21

### Files changed

- `tests/test_calculator.py` — extended with 56 tests covering incorrect inputs in division

### Purpose

Add tests for incorrect inputs in division (issue #233). Tests cover: division by zero (int and float zero), non-numeric dividend/divisor (strings, None, lists, dicts, tuples), and edge cases (infinity, NaN, very large/small numbers). Uses `pytest.raises()` for exception assertions and parametrize for data-driven coverage.

### Risks

Low — purely additive test changes. No source code modified.

### Test results

All 56 tests passed (pytest 9.0.3, Python 3.12.3).

### Tokens / Cost / Turns

Duration: 162.5s | Cost: $0.401912 USD | Turns: 14
