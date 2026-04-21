## Run: Issue #233 — Add tests for incorrect inputs in division

- **Branch:** task/issue-233-division-input-tests
- **PR target:** exp2/naive-team
- **PR:** https://github.com/DanielRiha8906/Calculator_bachelor_autoevolution_team/pull/282
- **Files changed:** tests/test_calculator.py (163 lines added)
- **Purpose:** Add comprehensive pytest tests for `Calculator.divide()` covering incorrect inputs (ZeroDivisionError for zero divisors, TypeError for non-numeric operands) plus happy-path and edge cases
- **Risks:** None — test-only change; no source modifications
- **Tests passed:** 30/30
- **Worktree/branch:** task/issue-233-division-input-tests → exp2/naive-team
