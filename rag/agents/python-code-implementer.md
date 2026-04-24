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

### 2026-04-24 — Add interactive session and operation registry (src/interactive.py, src/operation_registry.py)

**Task:** Implement `src/operation_registry.py` and `src/interactive.py` to make 15 failing tests pass in `tests/test_interactive.py`.

**Files changed:**
- `src/operation_registry.py` — new file; `OperationRegistry` class uses `inspect.signature` to discover public Calculator methods with arity 1 or 2, exposes `get_operations()`, `get_arity()`, `call()`
- `src/interactive.py` — new file; `parse_operand()` helper (int-first, then float); `run_interactive_session()` main loop with operation menu, operand gathering, result printing, and continue-prompt

**Key decisions:**
- `parse_operand` checks for "." in the raw string before deciding int vs float; this lets "3.5" resolve to float so `Calculator.factorial(3.5)` raises `ValueError` (caught as "Error: ...") matching the test expectation.
- `OperationRegistry` uses `inspect.getmembers(..., predicate=inspect.ismethod)` which already excludes `self` from the parameter list, so `arity = len(params)` gives the correct user-facing arity (1 or 2).
- Operation list is sorted once in `__init__` and stored; ordering is deterministic, matching the alphabetical index mapping in the tester's report.
- Exception handling catches `ZeroDivisionError` first (to emit "Error: Division by zero"), then broad `Exception` for all others (ValueError, math domain errors, etc.).
- The continue-prompt loop re-prompts silently on unexpected input, matching the spec.
- `run_interactive_session` accepts an optional `Calculator` arg (default `None`) to support both test injection and standalone use.

**Patterns found:**
- `inspect.getmembers(instance, predicate=inspect.ismethod)` returns bound methods, so their signature already excludes `self` — no need to subtract 1 from parameter count.
- Always handle `ZeroDivisionError` before broad `Exception` when both are in the same try/except chain, to give a more informative message.

**Test result:** 138/138 passed (123 pre-existing + 15 new interactive tests).

**Handoff notes for next agent:** No new dependencies introduced. `src/__main__.py` was not modified. The interactive module currently has no way to reach it from `__main__.py` — a future task could wire it in, but that requires a new failing test first.

### 2026-04-24 — Wire interactive session into __main__.py (issue-385)

**Task:** Modify `src/__main__.py` so that `python -m src` launches `run_interactive_session()` instead of the demo `main()`.

**Files changed:**
- `src/__main__.py` — added `from .interactive import run_interactive_session` import; added docstring to `main()` labelling it as demo/backward-compat; replaced `main()` with `run_interactive_session()` in the `if __name__ == "__main__":` block.

**Key decisions:**
- `main()` was preserved unchanged (aside from adding a docstring) to honour backward compatibility and not break any callers that import and call `main` directly.
- `run_interactive_session()` is called with no arguments so it defaults to constructing its own `Calculator` instance, matching the standalone-use path already supported by the function signature.

**Patterns found:**
- No new patterns. The change is purely a wiring step.

**Test result:** Not run by this agent (implementer does not run tests).

**Handoff notes for next agent:** No new dependencies introduced. `src/__main__.py` is now the entry point for the interactive session. The Tester should verify that `python -m src` launches the interactive loop and that all 138 pre-existing tests continue to pass.
