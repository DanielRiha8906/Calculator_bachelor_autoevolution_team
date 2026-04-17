## Run: Issue #12 — V1 Task 2 - Test Suite Expansion (add, subtract, multiply)

Branch: task/issue-12-test-suite-expert-team
PR target: exp/expert-team

Files changed:
- tests/test_calculator.py — appended three new sections: test_add_cases (7 rows), test_add_does_not_mutate_inputs, test_subtract_cases (6 rows), test_subtract_does_not_mutate_inputs, test_multiply_cases (7 rows), test_multiply_does_not_mutate_inputs

Purpose: Expand test coverage to Calculator.add, Calculator.subtract, and Calculator.multiply with parametrized happy-path cases and side-effect-freedom checks. No production code was modified.

Risks: None. Change is purely additive (test-only). No existing tests removed or altered.

Test results: 46 passed, 0 failed, 0 skipped (python -m pytest)

Duration: 355.4s | Cost: $0.810131 USD | Turns: 13

---

## Run: Issue #9 — V1 Task 1 - ZeroDivisionError - Expert/team

Branch: task/issue-9-zero-division-error
PR target: exp/expert-team

Files changed:
- tests/test_calculator.py — added test_divide_by_zero and 22 edge-case tests covering integer/float zero divisors, negative numerators, large numerators, 0/0, and IEEE 754 negative zero

Purpose: Add focused test coverage asserting Calculator.divide raises ZeroDivisionError on zero divisors. No implementation change was needed — the native Python / operator already raises ZeroDivisionError.

Risks: None. Change is purely additive (test-only). No production code was modified.

Test results: 23 passed, 0 failed, 0 skipped (python -m pytest)

Duration: 293.9s | Cost: $0.799775 USD | Turns: 13
