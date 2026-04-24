# RAG: python-code-implementer

## Purpose
Accumulated implementation context for this experiment branch. Each cycle entry records files changed, implementation decisions made to satisfy failing tests, and patterns or pitfalls found in `src/`.

## Cycle Log

### 2026-04-24 | issue-377: add factorial method to Calculator

**Task:** Add `factorial` method to `Calculator` class to satisfy 11 failing tests.

**Files changed:**
- `src/calculator.py` — added `import math` at module top; added `factorial(self, n: int) -> int` method with TypeError guard for booleans/non-integers and ValueError guard for negatives; delegates to `math.factorial`.

**Decisions:**
- Boolean check (`isinstance(n, bool)`) placed before the general int check because `bool` is a subclass of `int`; this matches the architect spec exactly.
- No other files touched; all 19 tests (8 pre-existing + 11 new factorial) pass.

**Patterns:**
- `bool` is a subclass of `int` in Python — always check for bool explicitly before int when rejecting non-integers.
- `math.factorial` raises `ValueError` for negatives itself, but explicit pre-check keeps error messages user-controlled.
