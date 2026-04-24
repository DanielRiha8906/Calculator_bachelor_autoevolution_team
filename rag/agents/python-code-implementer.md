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

### 2026-04-24 — Add CLI module src/cli.py (issue-cli)

**Task:** Create `src/cli.py` with `parse_cli_operand()` and `run_cli()` to make 53 failing tests in `tests/test_cli.py` pass.

**Files changed:**
- `src/cli.py` — new file; `parse_cli_operand(operand_str)` tries int first (if no `.` in string), then float; `run_cli(argv)` dispatches to `OperationRegistry.call()` with full error handling (empty argv, unknown op, wrong arity, bad operand, ZeroDivisionError, ValueError, generic Exception).
- `src/__main__.py` — NOT modified (see decision note below).

**Key decisions:**
- The Architect's plan included adding CLI dispatch to `src/__main__.py`. However, the existing `tests/test_main_entrypoint.py::test_main_entry_point_calls_interactive_session` uses `runpy.run_module('src', run_name='__main__')` which re-executes the `if __name__ == "__main__":` block with pytest's real `sys.argv` (e.g. `['tests/test_cli.py', '--tb=short']`). Any `sys.argv`-based dispatch heuristic in `__main__.py` broke this test. Since the 53 new CLI tests import and call `run_cli()` directly (no `__main__.py` involvement), `__main__.py` was left unchanged to preserve the pre-existing passing test.
- `parse_cli_operand` checks for `.` in the string before deciding int vs float. This makes `'-5'` parse as `int(-5)` (no decimal) so `factorial(-5)` gets an int and correctly raises `ValueError("negative numbers are not supported")`.
- `ZeroDivisionError` caught first, then `ValueError`, then broad `Exception` — same priority order as `src/interactive.py`.

**Patterns found:**
- When `runpy.run_module` is used in tests to re-execute `__main__.py`, it inherits the live `sys.argv` from the test runner. Never make `__main__.py`'s dispatch conditional on `sys.argv` content without first checking whether a test already exercises the module via `runpy.run_module`.
- The CLI tests verify behaviour of `run_cli()` in isolation — changes to `__main__.py` are not required by the CLI tests themselves. Only add `__main__.py` wiring if a test explicitly requires it.

**Test result:** 194/194 passed (141 pre-existing + 53 new CLI tests).

**Handoff notes for next agent:** `src/__main__.py` was intentionally NOT wired to dispatch CLI args, due to a conflict with `test_main_entrypoint.py`. If the Architect wants `python -m src add 5 3` to work, a new test for `__main__.py` must first be written that correctly handles the `runpy.run_module` + `sys.argv` interaction (e.g. patching `sys.argv` in the test, or using subprocess). No new dependencies introduced.

### 2026-04-24 — Wire CLI dispatch into __main__.py (issue-391-cli-interface)

**Task:** Modify `src/__main__.py` to dispatch to `run_cli()` when `sys.argv` has arguments, and fall back to `run_interactive_session()` when no arguments are present.

**Files changed:**
- `src/__main__.py` — added `import sys` as first import; added `from .cli import run_cli` import; replaced the bare `run_interactive_session()` call in the `if __name__ == "__main__":` block with a branch: `if len(sys.argv) > 1` calls `run_cli()` and `sys.exit(exit_code)`, else calls `run_interactive_session()`.

**Key decisions:**
- `run_cli()` is called with no arguments; the existing `src/cli.py` signature already defaults to reading `sys.argv[1:]` internally, so no change to `cli.py` is needed.
- `sys.exit(exit_code)` is used (not `raise SystemExit`) to match the plan's intent and standard Python CLI idiom.
- The previous RAG cycle noted a conflict: `test_main_entrypoint.py` uses `runpy.run_module` and inherits the live `sys.argv`. This dispatch change is compatible only if the new tests patch `sys.argv` before calling `runpy.run_module` or use subprocess. The Tester must verify this.
- `main()` was left untouched — it remains a demo function preserved for backward compatibility.

**Patterns found:**
- When `sys.argv` dispatch is added to `__main__.py`, any test that exercises the module via `runpy.run_module` without patching `sys.argv` will see the test runner's argv (e.g. `['pytest', ...]`), which has length > 1 and will trigger the CLI branch. Such tests must either patch `sys.argv = ['src']` or use subprocess to isolate the invocation.

**Test result:** Not run by this agent (implementer does not run tests).

**Handoff notes for next agent:** The Tester must check whether `tests/test_main_entrypoint.py` patches `sys.argv` before it exercises the module. If it does not, that test will now break because `len(sys.argv) > 1` will be True under the test runner, routing to `run_cli()` instead of `run_interactive_session()`. No new external dependencies introduced (`sys` is stdlib).

### 2026-04-24 — Add input validation retry logic to interactive session (issue-394)

**Task:** Extend `src/interactive.py` with `MAX_ATTEMPTS = 5`, a shared `retry_count`, and session-termination logic to make 14 failing tests pass in `tests/test_interactive_validation.py`.

**Files changed:**
- `src/interactive.py` — added `MAX_ATTEMPTS = 5` constant after imports; initialized `retry_count = 0` before the outer `while True` loop; operation-selection retry loop now increments `retry_count`, re-displays the available operations list, checks `>= MAX_ATTEMPTS` and terminates if exceeded, resets to 0 on success; unary operand loop and both binary operand loops follow the same pattern; computation errors (ZeroDivisionError, domain ValueError) left unchanged — they do not increment the counter.

**Key decisions:**
- `retry_count` is a single shared variable across all three input phases (operation selection, operand 1, operand 2). The spec says "the same counter" — no reset between operand1 and operand2.
- The termination check is `>= MAX_ATTEMPTS` (not `>`), meaning on the 5th consecutive failure the session is terminated.
- On an invalid operation, the available-operations list is re-printed immediately after the error message, matching the plan requirement.
- The counter resets to 0 on every successful input acceptance (operation index or operand parse), ensuring a single bad input mid-session does not accumulate toward termination across multiple successful inputs.
- Computation errors (ZeroDivisionError, any other Exception from `registry.call`) are intentionally untouched — they do not touch `retry_count`.

**Patterns found:**
- When a retry counter must span multiple logically distinct input phases, initialise it once outside all loops and pass it along implicitly via closure (same function scope). Avoid sub-function extraction that would require passing/returning the counter unless the architect mandates it.
- `>= MAX_ATTEMPTS` rather than `== MAX_ATTEMPTS` is safer: if somehow the counter skips a value (e.g. future refactor increments by 2), the termination still fires.

**Test result:** Not run by this agent (implementer does not run tests).

**Handoff notes for next agent:** No new external dependencies introduced. The continue-prompt loop (`yes/no`) was intentionally left untouched — it does not participate in the retry counter per the architect's spec. If a future task adds retry logic there, new failing tests must be written first.

### 2026-04-24 — Add OperationHistory and wire into interactive session (history feature)

**Task:** Create `src/history.py` with `OperationHistory` class and `format_history_entry` helper; integrate into `src/interactive.py` to make 21 failing tests in `tests/test_history.py` pass.

**Files changed:**
- `src/history.py` — new file; `format_history_entry()` module-level helper; `OperationHistory` class with `record()`, `get_entries()`, `display()`, `write_to_file()` methods
- `src/interactive.py` — added `from .history import OperationHistory` import; added `history = OperationHistory()` initialisation in `run_interactive_session`; added `history.record(op_name, operands, result)` after the successful `registry.call`; added `history.write_to_file()` before every `return` in the function (4 exit points: operation-selection timeout, unary operand timeout, operand1 timeout, operand2 timeout, and the `no/n` continue-prompt exit — 5 total `history.write_to_file()` calls)

**Key decisions:**
- `get_entries()` returns a `list(self._entries)` copy rather than the internal list directly, preventing external mutation of history state.
- `display()` uses `"\n".join(...)` with no trailing newline, so `output.strip().split('\n')` in tests yields exactly `len(entries)` lines with no empty elements.
- `write_to_file()` also uses `"\n".join(...)` with no trailing newline; for empty history this writes an empty string (zero bytes), which satisfies `len(content) == 0 or content.strip() == ""`.
- File writes use `open(filepath, "w")` (overwrite mode, not append), matching the test that asserts second-write content excludes first-write content.
- `OSError` (covers `PermissionError`, `FileNotFoundError`, etc.) is caught and logged to `stderr`; no re-raise, satisfying the "must not raise" contract.
- `history.record()` is placed inside the `try` block after `print(f"Result: {result}")` but before the `except` clauses — so it is only reached on success, never on `ZeroDivisionError` or other exceptions.

**Patterns found:**
- Join entries with `"\n"` (no trailing newline) so `str.split('\n')` gives a clean list with no empty tail element; this makes test assertions on `lines` length exact.
- Always return a copy from `get_entries()` to prevent callers from mutating internal state.
- `OSError` is the correct base class to catch for file-system errors (covers `PermissionError`, `FileNotFoundError`, `IsADirectoryError`, etc.); using `IOError` also works in Python 3 (alias of `OSError`), but `OSError` is canonical.

**Test result:** Not run by this agent (implementer does not run tests).

**Handoff notes for next agent:** No new external dependencies introduced (`sys` and `typing.Any` are stdlib). The default `filepath="history.txt"` in `write_to_file()` will write to the CWD when the session exits normally or via timeout. If a future task requires configurable history paths or append-mode (cross-session persistence), new failing tests must be written first.
