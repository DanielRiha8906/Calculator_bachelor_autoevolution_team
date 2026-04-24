# RAG: python-code-implementer

## Purpose
Accumulated implementation context for this experiment branch. Each cycle entry records files changed, implementation decisions made to satisfy failing tests, and patterns or pitfalls found in `src/`.

## Cycle Log

### 2026-04-24 — Add factorial method to Calculator

**Task:** Implement `Calculator.factorial(n: int) -> int` to make 21 failing tests pass.

**Files changed:**
- `src/calculator.py` — added `factorial` method after `divide`; iterative implementation with ordered type guards (bool before float/int due to Python's `bool` subclassing `int`)
- `src/__main__.py` — added `print("Factorial:", calc.factorial(5))` demonstration line

**Key decisions:**
- Bool guard (`isinstance(n, bool)`) placed first because `bool` is a subclass of `int`; without this, `True`/`False` would pass the int check silently.
- None guard uses identity check (`n is None`) rather than `isinstance` to be explicit.
- Catch-all `not isinstance(n, int)` placed last to handle any other unexpected types.
- Iterative loop preferred over `math.factorial` to avoid a hidden dependency and keep the implementation self-contained.

**Patterns found:**
- In Python, always check `bool` before `int` when type-dispatching, since `bool` is a subclass of `int`.
- The existing Calculator class has no type validation on other methods (add, subtract, multiply, divide). The architect specified validation only for factorial; other methods were left untouched.

**Test result:** 73/73 passed (52 pre-existing + 21 new factorial tests).

**Handoff notes for next agent:** No new dependencies introduced. The other Calculator methods still lack input validation — a future task could add it, but that would require new failing tests first (TDD pipeline).

### 2026-04-24 — Add advanced math operations to Calculator (issue-382)

**Task:** Implement 7 new methods on `Calculator` to make 50 failing tests pass: `square`, `cube`, `sqrt`, `cbrt`, `log10`, `ln`, `power`.

**Files changed:**
- `src/calculator.py` — added `import math` at the top; added 7 methods after `factorial`

**Key decisions:**
- The architect's plan named the methods `square_root` and `cube_root`, but the actual tests call `sqrt` and `cbrt`. Authoritative source is the test file (tester's WRITE report), so the shorter names were used. This is a discrepancy in the architect's plan — noted here for future reference.
- `cbrt` handles negative inputs via `-math.pow(-x, 1/3)` to avoid complex-number results from Python's `**` operator on negative fractional exponents.
- `sqrt` and both log methods raise `ValueError` with a descriptive message matching the test expectations.
- No aliases for `square_root`/`cube_root` were created; only the test-required names were added to keep the change minimal (YAGNI).

**Patterns found:**
- Always treat the actual test method calls as the canonical method name specification, not the architect's plan prose. The architect wrote `square_root`/`cube_root` in the plan but the tests used `sqrt`/`cbrt`. Defer to the tests.
- `math.pow(-x, 1/3)` for cube root of negatives is safer than `(-x) ** (1/3)` in Python, which returns a complex number.

**Test result:** 123/123 passed (73 pre-existing + 50 new advanced math tests).

**Handoff notes for next agent:** No new dependencies introduced (`math` is stdlib). The existing simple methods (add, subtract, multiply, divide) still lack input validation — a future task could add it, but only after failing tests are written first.
