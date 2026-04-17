## Run: Issue #9 - ZeroDivisionError test coverage

Branch: task/issue-9-zero-division-error
PR target: exp/expert-team

Files changed:
- tests/test_calculator.py — added test_divide_by_zero

Purpose: Add test asserting Calculator.divide(1, 0) raises ZeroDivisionError. No implementation change needed; Python's native / operator already raises ZeroDivisionError.

Risks: None. Implementation untouched; test-only change.

Tests passed: yes (1/1, no regressions)

Duration: PENDING | Cost: PENDING | Turns: PENDING
