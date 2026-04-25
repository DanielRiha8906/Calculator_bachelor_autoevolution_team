# Codebase Map

Per-file summaries of `src/`. Update after any cycle that modifies a listed file.

## src/calculator.py
- **Last updated:** — (not yet populated)
- **Purpose:** —
- **Public interface:** —
- **Known constraints:** —

## src/__main__.py
- **Last updated:** 2026-04-25 (Issue #415)
- **Purpose:** Entry point dispatcher — routes to GUI, CLI, or interactive mode
- **Public interface:** Routes `--gui` flag to CalculatorApp, argv>1 to run_cli(), no-args to run_interactive_session()
- **Notes:** --gui flag added in Issue #415; previous dispatch logic preserved unchanged

## src/ui/modes.py
- **Last updated:** 2026-04-25 (Issue #415)
- **Purpose:** OO mode abstraction for calculator UI modes
- **Public interface:** CalculatorMode (ABC), SimpleMode (6 ops: add, subtract, multiply, divide, square, sqrt), ScientificMode (12 ops: all legacy ops)
- **Known constraints:** ScientificMode uses registry.get_operations() (legacy 12), not get_operations_by_mode(SCIENTIFIC) which returns 18 including trig

## src/ui/gui.py
- **Last updated:** 2026-04-25 (Issue #415)
- **Purpose:** Tkinter-based GUI for calculator; reuses Calculator, OperationRegistry, OperationHistory
- **Public interface:** CalculatorApp(root=None, calculator=None, registry=None); methods: calculate(), switch_mode(), get_current_mode_operations(), get_history(), is_unary_operation(), run()
- **Known constraints:** tkinter unavailable in CI; uses try/except ImportError stub assigned to `tk` so tests can patch `src.ui.gui.tk.Tk` in headless environments; _parse_operand returns int for whole numbers (required for factorial)

## src/__init__.py
- **Last updated:** 2026-04-24 (Issue #406)
- **Purpose:** Backward-compatibility re-exports for public API; allows `from src import Calculator` etc.
- **Public interface:** Re-exports Calculator, OperationRegistry, run_interactive_session, run_cli, OperationHistory, ErrorLogger
- **Known constraints:** Must remain in sync when modules are moved

## src/core/operations.py
- **Last updated:** 2026-04-24 (Issue #406)
- **Purpose:** Operation type definitions and metadata (OperationType enum, OperationMetadata dataclass)
- **Public interface:** OperationType (UNARY, BINARY), OperationMetadata(name, arity, op_type, description)
- **Known constraints:** No UI or infrastructure dependencies; pure data layer

## src/ui/interactive.py
- **Last updated:** 2026-04-24 (Issue #406)
- **Purpose:** Interactive terminal session entry point (moved from src/interactive.py)
- **Public interface:** run_interactive_session(calculator=None)
- **Known constraints:** Imports from ..calculator, ..operation_registry, ..infrastructure.history, ..infrastructure.error_logger

## src/ui/cli.py
- **Last updated:** 2026-04-24 (Issue #406)
- **Purpose:** CLI entry point (moved from src/cli.py)
- **Public interface:** run_cli(argv=None) -> int
- **Known constraints:** Imports from ..calculator, ..operation_registry, ..infrastructure.history, ..infrastructure.error_logger

## src/infrastructure/history.py
- **Last updated:** 2026-04-24 (Issue #406)
- **Purpose:** Operation history tracking and persistence (moved from src/history.py)
- **Public interface:** OperationHistory
- **Known constraints:** No internal package dependencies

## src/infrastructure/error_logger.py
- **Last updated:** 2026-04-24 (Issue #406)
- **Purpose:** Error logging (moved from src/error_logger.py)
- **Public interface:** ErrorLogger
- **Known constraints:** No internal package dependencies

## src/session/manager.py
- **Last updated:** 2026-04-24 (Issue #406)
- **Purpose:** Session state management for interactive mode
- **Public interface:** SessionManager(calculator, error_logger, history)
- **Known constraints:** Internal refactoring class; not directly exposed in public API
