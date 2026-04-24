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

### 2026-04-24 — issue-381 advanced operations
- Task: Add 7 new methods to `Calculator` in `src/calculator.py` to satisfy 49 failing tests: `square`, `cube`, `square_root`, `cube_root`, `power`, `log10`, `ln`.
- Files changed: `src/calculator.py` — added all 7 methods after `factorial`; no imports added (`math` was already present).
- Decision: Used `x ** (1/3)` / `-((-x) ** (1/3))` idiom for `cube_root` to handle real cube roots of negative numbers correctly (Python's `**` with fractional exponent raises for negative bases). Used `isinstance(exponent, int)` guard in `power()` to detect non-integer exponents — note: a float that is a whole number (e.g. `2.0`) will still fail this check, which matches the architect's specification of "integer exponent".
- Pattern: For real nth-root of negative numbers, split on sign and use `-((-x)**(1/n))` rather than relying on complex-number semantics from `**`.
- Handoff notes: All 82 tests pass (49 new + 33 pre-existing). All 7 methods are additive; no existing interfaces were modified.

### 2026-04-24 — issue-384 interactive-input
- Task: Replace `src/__main__.py` with a REPL-style interactive loop (`main()`) to satisfy 18 failing tests in `TestInteractiveLoop`.
- Files changed: `src/__main__.py` — complete replacement; kept `.calculator` relative import; introduced an operation registry `dict[str, tuple[callable, int]]`; helper `_parse_number()` that prefers `int` over `float` (so "5" → 5, enabling `factorial()` which requires `isinstance(n, int)`).
- Decision: Operation selection prompt is printed via `print()` (not the `input()` prompt arg) because tests use `monkeypatch.setattr("builtins.input", lambda _: next(inputs))` which discards the prompt string, so only `print()` output is captured by `capsys`. Used `print()` for the operation menu before each `input()` call so "operation" appears in `captured.out`.
- Decision: Number parsing tries `int()` first and falls back to `float()`. This ensures factorial receives an actual `int` and "5" → 5 passes the `isinstance(n, int)` guard inside `Calculator.factorial()`.
- Decision: On `ValueError` or `ZeroDivisionError` from Calculator methods, catch the exception and print `"Error: {exc}"` then `continue` — loop remains alive for the next iteration.
- Pattern: When tests monkeypatch `builtins.input` with a lambda that ignores its argument, all prompt text intended to be visible in test output must be emitted via `print()` before the `input()` call.
- Handoff notes: All 107 tests pass (18 new + 89 pre-existing). `main()` is importable as `from src.__main__ import main` (tests rely on this).
