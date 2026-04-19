## Run: issue-139 — ZeroDivisionError test coverage

- **Branch:** task/issue-139-zero-division-error
- **PR target:** exp2/expert-team
- **Files changed:** tests/test_calculator.py (modified — added 4 test functions)
- **Purpose:** Add explicit test coverage for ZeroDivisionError in Calculator.divide(); verify the existing implementation raises naturally via Python's / operator with no suppression.
- **Risks:** None — purely additive test changes; no source code modified.
- **Tests passed:** 4/4 (test_divide_integer_by_zero_raises_error, test_divide_float_by_zero_raises_error, test_divide_negative_by_zero_raises_error, test_divide_normal_division_works)

Duration: PENDING | Cost: PENDING | Turns: PENDING
