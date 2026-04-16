## Run: Issue #12 — Comprehensive test suite expansion

- **Date**: 2026-04-16
- **Branch**: task/issue-12-test-suite
- **PR target**: exp/expert-team

### Files changed
- `tests/test_calculator.py` — appended four test sections (sections 1–4) covering: integer happy path (16 parametrized cases), float inputs with `pytest.approx` (12 cases), invalid inputs raising `TypeError` (13 cases), and large/edge case numerics (12 cases)

### Purpose
Expand test coverage for all four `Calculator` methods (`add`, `subtract`, `multiply`, `divide`) with parametrized tests for normal operation, floating-point precision, invalid type inputs, and large-number edge cases.

### Risks
None. Change is purely additive to the test file; no production code (`src/calculator.py`) was modified. The existing two tests were preserved unchanged.

### Test results
57 passed, 0 failed. Full test suite green.

### Tokens used
Duration: N/A | Cost: N/A | Turns: N/A

---

## Run: Issue #9 — ZeroDivisionError test coverage

- **Date**: 2026-04-16
- **Branch**: task/issue-9-zero-division-error
- **PR target**: exp/expert-team

### Files changed
- `tests/test_calculator.py` — added `test_divide_by_zero` and `test_divide_by_zero_alternate_zero_types`

### Purpose
Add focused test coverage asserting that `Calculator.divide()` raises `ZeroDivisionError` for integer zero, float zero, and complex zero denominators. No implementation change was required — `return a / b` natively raises `ZeroDivisionError` in all cases.

### Risks
None. Change is purely additive; no production code was modified.

### Test results
4 passed, 0 failed. All tests in `tests/test_calculator.py` pass.

### Tokens used
Duration: 238.6s | Cost: $0.752894 USD | Turns: 20
