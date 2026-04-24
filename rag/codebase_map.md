# Codebase Map

Per-file summaries of `src/`. Update after any cycle that modifies a listed file.

## src/calculator.py
- **Last updated:** 2026-04-24 (Issue #395)
- **Purpose:** Stateful Calculator class implementing 12 arithmetic/math operations with in-memory operation history
- **Public interface:** `Calculator()`, `add`, `subtract`, `multiply`, `divide`, `square`, `cube`, `square_root`, `cube_root`, `factorial`, `power`, `log`, `ln`, `get_history() -> list[dict]`, `clear_history()`
- **Known constraints:** Each instance maintains its own history; callers must reuse the same instance across operations to accumulate history. History entries: `{"operation": str, "operands": list, "result": numeric}`. Only successful operations are recorded.

## src/cli.py
- **Last updated:** 2026-04-24 (Issue #395)
- **Purpose:** Interactive and batch CLI wrappers for Calculator; exposes `run_calculator()` for interactive mode, `display_history(calc)` for history display
- **Public interface:** `run_calculator()`, `display_history(calc)`, `MaxRetriesExceeded`, OPERATIONS dict, prompt helpers
- **Known constraints:** `display_history` prints to stdout; uses `_format_history_entry` for formatting. Binary ops shown as `N. op(x, y) = r`; unary as `N. op(x) = r`.

## src/__main__.py
- **Last updated:** — (not yet populated)
- **Purpose:** Entry point; dispatches to interactive or batch CLI based on sys.argv
- **Notes:** Handles MaxRetriesExceeded, ValueError, ZeroDivisionError
