# RAG: python-code-implementer

## Purpose
Accumulated implementation context for this experiment branch. Each cycle entry records files changed, implementation decisions made to satisfy failing tests, and patterns or pitfalls found in `src/`.

## Cycle Log

### 2026-04-24 — issue-372 div-by-zero verification
- Task: Confirm `src/calculator.py` divide method satisfies 5 new tests for division by zero, normal division, float division, negative divisor, and zero dividend.
- Files changed: none (no src/ changes required).
- Decision: Python's native `/` operator already raises `ZeroDivisionError` automatically when divisor is 0. All 5 tests passed without modification.
- Pattern: Python's built-in arithmetic already handles zero-division; no explicit guard is needed in `divide()`.
- Handoff notes: No implementation work was required. Tests were already green on read.

### 2026-04-24 — issue-378 factorial method
- Task: Add `factorial(self, n: int) -> int` to `Calculator` in `src/calculator.py` to satisfy 10 failing tests in `TestCalculatorFactorial`.
- Files changed: `src/calculator.py` — added `import math` at top; added `factorial` method with type validation and delegation to `math.factorial`.
- Decision: Used `math.factorial` from stdlib rather than a hand-rolled iterative loop — it is correct, optimized, and already raises `ValueError` for negatives (though we guard before reaching it for a descriptive message). Added an explicit `isinstance(n, bool)` guard because `bool` is a subclass of `int` in Python and `True`/`False` would otherwise pass the `int` check.
- Pattern: Always check `isinstance(n, bool)` before `isinstance(n, int)` when you want to exclude booleans from an int-typed parameter.
- Handoff notes: All 33 tests pass (10 new + 23 pre-existing). No interface changes; the new method is additive only.
