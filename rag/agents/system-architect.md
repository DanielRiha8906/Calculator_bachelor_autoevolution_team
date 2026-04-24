# RAG: system-architect

## Purpose
Accumulated architectural context for this experiment branch. Each cycle entry records key design decisions, patterns observed in `src/`, and handoff notes for the next invocation.

## Cycle Log

### Cycle 1: 2026-04-24 — Issue #372 V3 Task 1 — Division by Zero Handling

**Task:** Add unit test for division by zero and ensure implementation handles the edge case correctly.

**Key Decisions:**
1. No source code changes required to `src/calculator.py` — the `divide` method already correctly raises `ZeroDivisionError` natively via Python's `/` operator when divisor is zero.
2. Test specifications created for 5 test cases covering: division by zero (exception), normal division, float operands, negative divisor, and zero dividend.
3. All tests target `Calculator.divide()` method; no changes to other operations.

**Patterns Observed:**
- Minimal calculator implementation with raw operators — no defensive programming or custom error handling needed.
- Python's native exception behavior is sufficient and expected per requirements.

**Handoff Notes for pytest-edge-tester (WRITE phase):**
- Write 5 failing test functions in `tests/test_calculator.py` covering division edge cases
- Test `test_division_by_zero` MUST assert `ZeroDivisionError` is raised when divisor is 0
- Use pytest's `pytest.raises(ZeroDivisionError)` context manager
- All other tests verify normal behavior with various input types and signs
- File: `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/tests/test_calculator.py`

**Handoff Notes for python-code-implementer:**
- No `src/` changes required — existing `divide` implementation is correct
- Simply receive pytest-edge-tester's WRITE report; implementation is already complete

### Cycle 2: 2026-04-24 — Issue #381 V3 Task 4 — Seven Advanced Operations

**Task:** Add seven advanced mathematical operations (square, cube, square_root, cube_root, power, log10, ln) to Calculator class with comprehensive test coverage.

**Key Decisions:**

1. **Method signatures:** All methods accept flexible numeric types (int/float mix), following existing Calculator pattern (no strict type validation).

2. **Error handling strategy:** 
   - Domain validation methods (`square_root`, `cube_root`, `power`, `log10`, `ln`) raise explicit `ValueError` with descriptive messages, mirroring the `factorial()` pattern.
   - Non-domain methods (`square`, `cube`) accept all real numbers without error handling.
   - Cube root supports negative inputs (real cube root semantics).

3. **Computation approach:**
   - Leverage existing `math` module imports (`math.sqrt()`, `math.log10()`, `math.log()`).
   - For `power()`: use native `**` operator with validation for negative base + non-integer exponent.
   - For `cube_root()`: compute as `x**(1/3)` for x≥0, or `-((-x)**(1/3))` for x<0 to preserve sign.

4. **Test suite organization:**
   - Create 7 new test classes in `tests/test_calculator.py` (one per operation).
   - Each class follows existing naming pattern (`TestCalculator<Operation>`).
   - Each covers: happy path, edge cases (zero, negatives), floats, and error conditions.
   - Use `pytest.raises(ValueError)` for domain violations; use `pytest.approx()` for floating-point comparisons.
   - Total: ~50 new test functions across all classes, no modifications to existing 23 tests.

**Patterns Observed:**
- Test suite uses class-based organization with consistent fixtures and assertion patterns.
- Error handling in `factorial()` demonstrates the expected pattern for domain validation.
- Calculator methods accept flexible numeric types without strict type enforcement.

**Architectural Impact:**
- Additive changes only — no breaking changes to existing API.
- Error handling pattern (explicit `ValueError`) extends established `factorial()` precedent.
- All computation delegated to `math` module; no new external dependencies required.

**Handoff Notes for pytest-edge-tester (WRITE phase):**
- Create 7 test classes in `tests/test_calculator.py`:
  - `TestCalculatorSquare` (5 tests: positive/negative integers, zero, float, small float)
  - `TestCalculatorCube` (5 tests: positive/negative integers, zero, float, negative float)
  - `TestCalculatorSquareRoot` (6 tests: perfect square, non-perfect, zero, float, negative raises ValueError × 2)
  - `TestCalculatorCubeRoot` (6 tests: positive/negative cube, non-perfect, zero, negative float, float)
  - `TestCalculatorPower` (10 tests: basic power, zero exponent, exponent 1, negative exponent, float base/exponent, negative base cases, zero base cases)
  - `TestCalculatorLog10` (8 tests: log10(10), log10(1), log10(100), float, small positive, zero/negative each raise ValueError × 3)
  - `TestCalculatorLn` (8 tests: ln(e), ln(1), small/large positive, float, zero/negative each raise ValueError × 3)
- All tests must be initially failing.
- Use `pytest.approx()` for floating-point assertions.
- Use `pytest.raises(ValueError)` context manager for error cases.

**Handoff Notes for python-code-implementer:**
- Modify `/home/runner/work/Calculator_bachelor_autoevolution_team/Calculator_bachelor_autoevolution_team/src/calculator.py`:
  - Add 7 methods to Calculator class: `square()`, `cube()`, `square_root()`, `cube_root()`, `power()`, `log10()`, `ln()`.
  - Follow docstring style from `factorial()` (Args, Returns, Raises sections).
  - `square_root()`: raise `ValueError` if x < 0.
  - `cube_root()`: handle negatives via sign-aware computation; no errors.
  - `power()`: raise `ValueError` for negative base + non-integer/non-rational exponent; use `**` operator.
  - `log10()`, `ln()`: raise `ValueError` if x ≤ 0.
  - No changes to existing methods.
