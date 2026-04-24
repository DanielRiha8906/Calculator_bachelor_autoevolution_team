# RAG: python-code-implementer

## Purpose
Accumulated implementation context for this experiment branch. Each cycle entry records files changed, implementation decisions made to satisfy failing tests, and patterns or pitfalls found in `src/`.

## Cycle Log

### 2026-04-24 — issue-374: add advanced calculator methods

- **Task:** Add 8 new methods to `Calculator` class to satisfy 45 failing tests.
- **Files changed:** `src/calculator.py`
- **Changes made:**
  - Added `import math` at the top of the module.
  - Added `square(a)`: returns `a ** 2`.
  - Added `cube(a)`: returns `a ** 3`.
  - Added `square_root(a)`: returns `math.sqrt(a)`; raises `ValueError` if `a < 0`.
  - Added `cube_root(a)`: returns cube root handling negatives via `-(abs(a) ** (1/3))`; returns `0.0` for zero.
  - Added `factorial(n)`: guards against booleans and non-integers before delegating to `math.factorial`; raises `ValueError` for negative or non-integer inputs.
  - Added `power(base, exp)`: returns `base ** exp`.
  - Added `log(a)`: returns `math.log10(a)`; raises `ValueError` if `a <= 0`.
  - Added `ln(a)`: returns `math.log(a)`; raises `ValueError` if `a <= 0`.
- **Patterns found:**
  - `math.factorial` raises `TypeError` for non-integers, not `ValueError` — explicit isinstance guard needed to produce consistent `ValueError`.
  - Boolean is a subclass of `int` in Python; must check `isinstance(n, bool)` before `isinstance(n, int)` to reject booleans.
  - Negative cube root via `-(abs(a) ** (1/3))` avoids complex-number issues from Python's `(-x) ** (1/3)`.
- **Test result:** 68/68 passed.
