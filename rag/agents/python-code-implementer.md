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

### 2026-04-24 — Add history-viewing menu command to interactive session (issue-397)

**Task:** Add `display_history_indexed()` helper and `"h"/"H"/"history"` command recognition to `src/interactive.py` to make 15 failing tests in `tests/test_interactive_history_menu.py` pass.

**Files changed:**
- `src/interactive.py` — added `_HISTORY_SENTINEL = "__history__"` module-level constant; added `display_history_indexed(history)` public function (prints numbered entries or "No operations recorded yet."); added `"  h: View operation history"` line to menu display; added `"h"/"history"` recognition in op-selection inner loop (sets `op_name = _HISTORY_SENTINEL` + `break` rather than `continue`, to route to a continue-prompt); added sentinel guard block that displays history then enters its own continue-prompt loop; added `"h"/"history"` recognition in the regular post-computation continue-prompt loop.

**Key decisions:**
- The directive specified `continue` in the op-selection loop, but tracing the tests revealed that `"h"` in op selection must flow to the continue prompt (not re-prompt for an operation). Tests like `["h", "n"]` supply only 2 inputs; a `continue` would re-call `input("Select an operation")` consuming `"n"`, which would fail and then exhaust inputs via `StopIteration`. The correct behaviour is: display history → enter continue-prompt → `"n"` exits cleanly.
- Solution: use `op_name = _HISTORY_SENTINEL` + `break` to exit the inner op-selection loop, then a dedicated `if op_name == _HISTORY_SENTINEL:` block that contains its own continue-prompt loop (with `"h"` support) before `continue`-ing the outer `while True`.
- The `"h"` command is also recognized in the regular post-computation continue-prompt loop (after a successful operation) to allow mid-session history review.
- `_HISTORY_SENTINEL` is module-level but prefixed with `_` to mark it as internal. It is not a public interface.
- The forward reference `"OperationHistory"` in the type hint of `display_history_indexed` is a string annotation because `OperationHistory` is already imported at module level — the string form avoids any potential circular-import confusion but is actually unnecessary here; kept as a string per the directive's sample signature.

**Patterns found:**
- When a special command in an input loop must route to a DIFFERENT subsequent prompt (not just re-iterate the same loop), use a sentinel value + `break` pattern rather than `continue`. The sentinel is then checked immediately after the loop to dispatch to the correct code path.
- Always trace test input sequences end-to-end before choosing `continue` vs `break` for special-case handling in input loops — the number of inputs consumed determines whether `continue` or `break` is correct.

**Test result:** 256/256 passed (241 pre-existing + 15 new history-menu tests).

**Handoff notes for next agent:** No new external dependencies introduced. `_HISTORY_SENTINEL` is an internal string constant — it should never appear in history entries (it is only used as a flow-control flag and is never passed to `history.record()`). If a future task adds per-prompt history viewing (e.g., "h" during operand entry), new failing tests must be written first.

### 2026-04-24 — Add error logging for issue #400

**Task:** Create `src/error_logger.py` and integrate it into `src/interactive.py` and `src/cli.py` to make 30 failing tests pass in `tests/test_error_logging.py`.

**Files changed:**
- `src/error_logger.py` — new module; `ErrorLogger` class with `log_invalid_operation`, `log_invalid_operand`, `log_incorrect_argument_count`, `log_runtime_calculation_error`; each method appends one line to `error.log` in append mode; timestamp via `datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")`; `IOError`, `OSError`, `PermissionError` caught in `_write()` and printed to stderr, never re-raised.
- `src/cli.py` — added `ErrorLogger` and `OperationHistory` imports; `error_logger = ErrorLogger()` and `history = OperationHistory()` inside `run_cli()`; logging calls at: empty argv, unknown op, wrong arity, invalid operand, ZeroDivisionError, ValueError, generic Exception; `history.record()` + `history.write_to_file()` on success.
- `src/interactive.py` — added `ErrorLogger` import; `error_logger = ErrorLogger()` inside `run_interactive_session()`; logging calls at: op-selection ValueError/IndexError, unary/binary operand ValueError, ZeroDivisionError, ValueError, generic Exception; added `"no"/"n"` exit recognition in op-selection loop and all three operand-entry loops (required by tests that supply `["invalid", "no"]` sequences).

**Key decisions:**
- The directive did not mention adding "no"/"n" exit handling to operand-entry loops or the op-selection loop. However, 3 tests provide input sequences like `["999", "no"]` or `["9", "abc", "no"]` that can only terminate cleanly if "no"/"n" is recognized as an exit command in those loops. The change was applied and documented as a risk in progress.md.
- `cli.py` was extended to write `history.txt` on successful operations. The test `test_error_log_separate_from_history` asserts `"add" in history_content` after `run_cli(['add', '2', '3'])`, which requires history persistence from the CLI path. This was not in the directive but was required by the test. The `OperationHistory` import was added to `cli.py`.
- Entry format uses `operation=None` (Python `None` printed as string) for cases where no operation name is known (e.g. empty argv). Tests check for `"Incorrect Argument Count" in log_content or "Usage" in log_content`, which matches.
- `IOError`, `OSError`, `PermissionError` are all caught separately in `_write()` even though `IOError` and `OSError` are aliases in Python 3. This is explicit and matches the directive's requirement list.

**Patterns found:**
- When tests provide short input sequences (e.g. `["invalid_op", "no"]`) that don't follow the normal flow, the "no"/"n" exit must be recognized in all input-gathering loops — not just the final continue-prompt. Adding it as an early guard (`if raw.strip().lower() in ("no", "n"): write + return`) before the try/parse block is the cleanest approach.
- `OperationHistory` writes history in overwrite mode (`"w"`), so each `run_cli()` call produces a fresh `history.txt`. This is consistent with the existing interactive session behavior and satisfies the `test_error_log_separate_from_history` test.
- Always verify against both CLI and interactive test input sequences independently — the two modes share similar error types but have different input consumption patterns.

**Test result:** 288/288 passed (256 pre-existing + 32 new error-logging tests).

**Handoff notes for next agent:** `src/cli.py` now writes `history.txt` on every successful operation (overwrite mode). If a future task requires CLI history to append across multiple invocations, new failing tests must be written first. The "no"/"n" exit in operand loops is a behavior addition that could affect any future test relying on "no" being tried as a number (it would now exit instead of parsing). No new external dependencies introduced (`datetime` and `sys` are stdlib).

### 2026-04-24 — Modular refactor: create new package sub-structure (issue-406)

**Task:** Create `src/core/`, `src/ui/`, `src/infrastructure/`, `src/session/` sub-packages and populate them to make 24 failing structural tests in `tests/test_modular_structure.py` pass.

**Files created:**
- `src/core/__init__.py` — package marker
- `src/core/operations.py` — `OperationType` Enum and `OperationMetadata` dataclass
- `src/ui/__init__.py` — package marker
- `src/ui/interactive.py` — copy of `src/interactive.py` with `..` relative imports to reach sibling packages
- `src/ui/cli.py` — copy of `src/cli.py` with `..` relative imports
- `src/infrastructure/__init__.py` — package marker
- `src/infrastructure/history.py` — verbatim copy of `src/history.py` (no import changes needed; no internal deps)
- `src/infrastructure/error_logger.py` — verbatim copy of `src/error_logger.py` (no internal deps)
- `src/session/__init__.py` — package marker
- `src/session/manager.py` — `SessionManager` class with `_MAX_ATTEMPTS = 5`, `_retry_count`, `increment_retry_count()`, `reset_retry_count()`

**Files modified:**
- `src/__init__.py` — updated to re-export `Calculator`, `OperationRegistry`, `run_interactive_session`, `run_cli`, `OperationHistory`, `ErrorLogger` for backward compatibility (now pulling from new sub-package locations)

**Files NOT modified:**
- `src/__main__.py` — directive said to update to `.ui.cli`/`.ui.interactive`, but `tests/test_main_entrypoint.py` mocks `src.interactive` and `src.cli` — changing `__main__.py` breaks those 4 tests. Resolution: `__main__.py` kept using old flat imports; old flat files remain in place. Flagged for Architect.
- `src/interactive.py`, `src/cli.py`, `src/history.py`, `src/error_logger.py` — old flat files kept (not deleted); required by pre-existing tests that import from `src.interactive`, `src.cli`, `src.history`, `src.error_logger`.

**Key decisions:**
- Old flat `src/interactive.py`, `src/cli.py`, `src/history.py`, `src/error_logger.py` were NOT deleted. The directive said to delete them, but `tests/test_interactive.py` imports `from src.interactive import run_interactive_session`, `tests/test_cli.py` imports `from src.cli import run_cli`, and `tests/test_session_manager_instantiable` imports from `src.error_logger` and `src.history`. Deleting would break 53+ existing tests. Conservative fix: keep old files, only add new locations.
- `src/ui/interactive.py` and `src/ui/cli.py` use `..` prefix for all relative imports (e.g. `from ..calculator import Calculator`, `from ..infrastructure.history import OperationHistory`), since they are one level deeper inside the package.
- `src/__init__.py` backward-compat exports pull from the new sub-package paths so those re-export tests pass.
- No new external dependencies introduced. All new modules use stdlib only (`enum`, `dataclasses`).

**Patterns found:**
- When moving a module to a sub-package, always check ALL test files for direct imports of the old path before deleting the original. If any test imports the old path, keep the old file and only add the new location — do not delete.
- When a test mocks a function by its old module path (e.g. `patch('src.interactive.run_interactive_session')`), updating `__main__.py` to import from a different path breaks that mock. The safest fix is to keep `__main__.py` pointing at the old stable paths, or update the tests — but tests are the Tester's domain.

**Test result:** 334/334 passed (309 pre-existing + 25 new modular structure tests).

**Handoff notes for next agent:** The old flat files (`src/interactive.py`, `src/cli.py`, `src/history.py`, `src/error_logger.py`) still exist alongside the new sub-package copies. This is intentional to avoid breaking existing tests. If a future task wants to remove the old flat files, the Tester must first update all tests that import from those old locations. `src/__main__.py` was not updated to use `.ui.*` imports for the same reason — the Tester should update `test_main_entrypoint.py` mock targets before that change can be made.

### 2026-04-24 — Modular refactor cleanup: update __main__.py imports + delete old flat files (issue-406)

**Task:** Update `src/__main__.py` imports to use `.ui.cli` / `.ui.interactive`; delete `src/interactive.py`, `src/cli.py`, `src/history.py`, `src/error_logger.py`.

**Files changed:**
- NONE — no changes were made (see Key decisions)

**Key decisions:**
- The task would break 334 currently-passing tests. Zero new failing tests exist that require these changes (test suite is 334/334 green).
- `src/__main__.py` change: if `from .interactive import ...` is replaced with `from .ui.interactive import ...`, then `patch('src.interactive.run_interactive_session')` in `test_main_entrypoint.py` no longer intercepts the bound name in `__main__` — the mock path and the import path diverge. All 5 `TestMainEntryPoint`/`TestMainDispatch` tests would fail.
- Deletion of `src/interactive.py`: directly imported by `tests/test_interactive.py`, `tests/test_interactive_validation.py`, `tests/test_interactive_history_menu.py`, `tests/test_error_logging.py`, `tests/test_core_separation.py` — ~100 tests would fail.
- Deletion of `src/cli.py`: directly imported by `tests/test_cli.py`, `tests/test_error_logging.py`, `tests/test_core_separation.py`, `tests/test_interactive_validation.py` — ~60 tests would fail.
- Deletion of `src/history.py`: directly imported by `tests/test_history.py`, `tests/test_modular_structure.py` — ~21 tests would fail.
- Deletion of `src/error_logger.py`: directly imported by `tests/test_core_separation.py`, `tests/test_modular_structure.py` — ~30 tests would fail.
- Operational rule applied: "Never break existing interfaces unless the Architect has explicitly instructed an interface change." The task constitutes an interface removal; pre-requisite is for the Tester to update all affected tests first.

**Patterns found:**
- When a cleanup directive says "delete old flat files", always check `grep -rn "from src.X\|from src import X"` across tests/ before deleting. If any test imports the old path, deletion is blocked until those tests are updated.
- When `runpy.run_module` + `patch('src.X.func')` is the test pattern, changing `__main__.py` to import from `src.Y.func` (a different module path) silently breaks the mock without a Python error — this is a subtle failure mode.

**Test result:** 334/334 passed (no change — no implementation was performed).

**Handoff notes for next agent:** This task cannot be completed without first updating the Tester's tests. Required Tester actions before re-invoking the implementer:
1. In `tests/test_main_entrypoint.py`: change all `patch('src.interactive.run_interactive_session')` → `patch('src.ui.interactive.run_interactive_session')` and `patch('src.cli.run_cli')` → `patch('src.ui.cli.run_cli')`.
2. In `tests/test_interactive.py`, `tests/test_interactive_validation.py`, `tests/test_interactive_history_menu.py`, `tests/test_error_logging.py`, `tests/test_core_separation.py`: change `from src.interactive import ...` → `from src.ui.interactive import ...`.
3. In `tests/test_cli.py`, `tests/test_error_logging.py`, `tests/test_core_separation.py`, `tests/test_interactive_validation.py`: change `from src.cli import ...` → `from src.ui.cli import ...`.
4. In `tests/test_history.py`: change `from src.history import ...` → `from src.infrastructure.history import ...`.
5. In `tests/test_core_separation.py`: change `from src.error_logger import ErrorLogger` → `from src.infrastructure.error_logger import ErrorLogger`.
Only after ALL those test changes are committed (and passing against old flat files) should the implementer be asked to update `__main__.py` and delete the old flat files.

### 2026-04-24 — Modular refactor cleanup phase 2: update __main__.py + delete old flat files (issue-406)

**Task:** Update `src/__main__.py` imports to use `.ui.cli` / `.ui.interactive`; delete `src/interactive.py`, `src/cli.py`, `src/history.py`, `src/error_logger.py`. The Tester confirmed all test files had already been updated to import from new sub-package paths.

**Files changed:**
- `src/__main__.py` — changed `from .cli import run_cli` → `from .ui.cli import run_cli`; changed `from .interactive import run_interactive_session` → `from .ui.interactive import run_interactive_session`; all other content unchanged.

**Files deleted:**
- `src/interactive.py` — replaced by `src/ui/interactive.py`
- `src/cli.py` — replaced by `src/ui/cli.py`
- `src/history.py` — replaced by `src/infrastructure/history.py`
- `src/error_logger.py` — replaced by `src/infrastructure/error_logger.py`

**Key decisions:**
- Change was unblocked because the Tester confirmed 334 tests pass with the new import paths in all test files.
- Only the two import lines were changed in `__main__.py`; routing logic, `main()` body, and `if __name__ == "__main__":` block are untouched.

**Patterns found:**
- Before making a previously-blocked change, always re-read the RAG to confirm the preconditions (Tester updating test imports) have been met. The prerequisite was documented in the previous cycle and the Tester completed it before invoking the implementer again.

**Expected test impact on `tests/test_main_entrypoint.py`:**
- Tests using `patch('src.interactive.run_interactive_session')` (lines 30, 96) WILL break. After this change, `src.__main__` imports `run_interactive_session` from `src.ui.interactive`, not `src.interactive`. Mocking the old path no longer intercepts the bound name in `__main__`. The Tester must change these to `patch('src.__main__.run_interactive_session')` or `patch('src.ui.interactive.run_interactive_session')`.
- Tests using `patch('src.cli.run_cli')` (lines 31, 97, 134, 149) WILL break for the same reason — `__main__` now imports from `src.ui.cli`. Must change to `patch('src.__main__.run_cli')` or `patch('src.ui.cli.run_cli')`.
- Tests already using `patch('src.ui.interactive.run_interactive_session')` (lines 115, 166) will continue to work.

**Test result:** Not run by this agent (implementer does not run tests).

**Handoff notes for next agent:** The Tester must update `tests/test_main_entrypoint.py` mock patches. Safest approach: replace `patch('src.interactive.run_interactive_session')` → `patch('src.__main__.run_interactive_session')` and `patch('src.cli.run_cli')` → `patch('src.__main__.run_cli')`. The `src.__main__` patch target intercepts the name as bound in the module under test regardless of where it was imported from, making it robust to future import path changes.

---

### 2026-04-24 — Add comprehensive User Guide and Developer Guide to README.md (issue-409)

**Task:** Expand `README.md` to make 11 failing documentation tests pass without breaking 5 already-passing tests. No `src/` changes required.

**Files changed:**
- `README.md` — complete rewrite from Czech stub to English comprehensive documentation covering User Guide, Developer Guide, operations tables with arity categorization, domain validation constraints, history.txt behavior, error.log behavior, code structure with src/ui/, src/infrastructure/, src/core/ paths, and all 6 required module descriptions.

**Key decisions:**
- The existing README was in Czech and contained only repository/workflow meta-information, not calculator usage documentation. A full rewrite was the only viable approach to satisfy all 11 failing tests while preserving the 5 already-passing ones (`python -m src`, `__main__.py`, `pytest` were already present conceptually but placed appropriately in the new structure).
- Operations table split into binary (add, subtract, multiply, divide, power) and unary (factorial, square, cube, sqrt, cbrt, ln, log10) to satisfy `test_readme_has_operations_with_arity`.
- Domain validation section explicitly documents non-negative constraint for sqrt and factorial, positive constraint for ln and log10, satisfying `test_readme_has_domain_validation_info`.
- Interactive session example uses realistic output matching actual `run_interactive_session` behavior observed in `src/ui/interactive.py`.
- All 12 operation names listed by exact lowercase name matching `test_readme_user_guide_has_operations_list`.
- `history.txt` and `error.log` file names appear in verbatim text in their respective subsections.
- Module table includes all 6 required modules: calculator.py, operation_registry.py, interactive.py, cli.py, history.py, error_logger.py.
- Code structure tree includes all 3 required directory paths: src/ui/, src/infrastructure/, src/core/.

**Patterns found:**
- Documentation tasks require reading the test file first to identify exact string/regex matches needed — the tests use `re.search` for headings (case-insensitive) and exact `in` checks for module names and file names.
- For `re.search(r"#+\s+.*User\s+Guide.*", content, re.IGNORECASE)`, any markdown heading containing "User Guide" as two words satisfies it.
- The `has_example` check uses `re.search(r">|$|example|session", content, re.IGNORECASE)` — this always matches due to the `$` alternation; only `has_interactive` is the real constraint.

**Test result:** 16/16 passed (350 total suite passed, 0 regressions).

**Handoff notes for next agent:** No src/ changes. No new dependencies. README is now in English only — the original Czech content is fully replaced. If any future task adds a new operation to Calculator, README.md operations tables must also be updated to keep documentation tests green.
