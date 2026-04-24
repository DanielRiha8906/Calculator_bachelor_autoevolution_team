# RAG: system-architect

## Purpose
Accumulated architectural context for this experiment branch. Each cycle entry records key design decisions, patterns observed in `src/`, and handoff notes for the next invocation.

## Cycle Log

### Cycle 1: 2026-04-24 — Issue #371 V3 Task 1 (test division incorrect inputs)
**Task:** Write test cases for division with invalid/incorrect inputs, particularly division by zero.

**Analysis:**
- `src/calculator.py` contains a `Calculator` class with a `divide(a, b)` method that performs simple division
- Division naturally raises `ZeroDivisionError` when b=0 (no special handling needed)
- `tests/test_calculator.py` exists but is minimal (only imports)
- Task is test-only; no source code changes needed

**Key Decisions:**
- Write 8 test cases covering: division by zero (error case), zero as numerator, negative operands (all combinations), normal division, and fractional results
- All tests go in `tests/test_calculator.py` and will initially fail (Red phase)
- No modifications to `src/calculator.py` required—existing division behavior already satisfies requirements

**Patterns Found:**
- Test file was pre-created but empty of test functions (common pattern in this repo for task initialization)

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** 8 test functions to write in `tests/test_calculator.py`. All tests must initially fail because the test file currently has no test functions.
- **python-code-implementer:** No source changes needed. Division already exists and behaves correctly. Pass only if pytest-edge-tester confirms all new tests are written and fail.

### Cycle 2: 2026-04-24 — Issue #374 V3 Task 2 (comprehensive calculator test suite)
**Task:** Create comprehensive test suite covering all existing calculator functionality plus advanced mathematical functions.

**Analysis:**
- Current Calculator has only 4 basic operations: add, subtract, multiply, divide
- Issue #371 task already added 8 division tests; total existing test count = 8
- Requirements call for tests on: basic arithmetic (partially done), advanced functions (square, cube, sqrt, cbrt, factorial, power, log, ln), error handling
- Advanced mathematical functions do NOT exist yet in `src/calculator.py`
- This is a test-creation task, but tests cannot pass without implementation
- Solution: Define comprehensive test specs in architect output; implementation comes after tests are written

**Key Decisions:**
- Write 68 total test cases: 15 new for basic arithmetic (add/subtract/multiply not yet tested), 45 for advanced functions, 8 for error handling and edge cases
- Tests require 8 new Calculator methods: square, cube, square_root, cube_root, factorial, power, log, ln
- Import math module in Calculator for sqrt, factorial, log functions
- Use pytest.approx() for floating-point comparisons; pytest.raises() for error cases
- All error conditions raise ValueError (domain errors) or TypeError (type errors)

**Patterns Found:**
- Test-first workflow: specs define the contract; implementation follows failing tests
- Calculator class design: pure functions, no state, consistent error handling

**Handoff Notes for Next Agent:**
- **pytest-edge-tester (WRITE phase):** Write all 68 test cases (including existing 8 division tests, which should not be re-created). Organize into test classes by functionality. Expected initial failure count: 60 (division tests already pass; new tests fail).
- **python-code-implementer:** After tester confirms tests are written and correct count fail, implement the 8 missing methods in Calculator. All methods must follow error specifications in test specs. Target: all 68 tests passing.
