# Architecture

## Module Organization

The source tree under `src/` is divided into four functional sub-packages and a set
of root-level backwards-compatibility shims.

```
src/
├── __init__.py          # Re-exports Calculator, CliDispatcher, OperationDispatcher,
│                        # Logger, OPERATIONS at the package root
├── __main__.py          # Entry point for `python -m src` (interactive mode)
│
├── core/
│   ├── __init__.py      # Re-exports Calculator
│   └── calculator.py    # Calculator — pure math, no I/O
│
├── session/
│   ├── __init__.py      # Re-exports InputHandler, run_session
│   ├── input_handler.py # InputHandler class + run_session convenience function
│   └── history.py       # History — session-scoped operation recorder
│
├── interface/
│   ├── __init__.py      # Re-exports CliDispatcher
│   └── cli.py           # CliDispatcher — single-shot CLI mode
│
├── shared/
│   ├── __init__.py      # Re-exports OperationDispatcher, Logger
│   ├── dispatcher.py    # OperationDispatcher — operand coercion + method dispatch
│   └── logger.py        # Logger — file-based error logging
│
├── operations/
│   ├── __init__.py      # Merges NORMAL_OPERATIONS + SCIENTIFIC_OPERATIONS → OPERATIONS
│   ├── normal.py        # NORMAL_OPERATIONS registry (12 entries)
│   └── scientific.py    # SCIENTIFIC_OPERATIONS registry (currently empty)
│
├── calculator.py        # Shim → src.core.calculator
├── cli.py               # Shim → src.interface.cli
├── dispatcher.py        # Shim → src.shared.dispatcher
├── history.py           # Shim → src.session.history
├── input_handler.py     # Shim → src.session.input_handler
├── logger.py            # Shim → src.shared.logger
└── operations.py        # Shim → src.operations
```

### Sub-package responsibilities

| Sub-package | Responsibility |
|-------------|---------------|
| `src/core` | Pure computation. `Calculator` methods perform math and raise domain exceptions. No I/O. |
| `src/session` | Interactive REPL. Owns the prompt loop, retry logic, history tracking, and session teardown. |
| `src/interface` | CLI mode. Parses `sys.argv`, validates argument count, prints result to stdout or error to stderr. |
| `src/shared` | Cross-cutting utilities used by both session and interface: operand coercion/dispatch (`OperationDispatcher`) and error logging (`Logger`). |
| `src/operations` | Operation metadata registry. Defines the `OPERATIONS` dict that both session and interface consume. |

---

## Data Flow

### Interactive mode (`python -m src`)

```
src/__main__.py
  └─ run_session(calc)
       └─ InputHandler.run()
            ├─ _show_menu()           reads OPERATIONS registry → prints to stdout
            ├─ _prompt_operands()
            │    └─ OperationDispatcher.coerce_operands()
            ├─ _dispatch()
            │    └─ OperationDispatcher.dispatch()
            │         └─ Calculator.<method>()
            ├─ History.add_operation()
            └─ (on exit) History.save_to_file("history.txt")
```

### CLI mode (`python main.py <op> <operands>`)

```
main.py main()
  └─ CliDispatcher.dispatch_from_args(sys.argv[1:])
        ├─ validates op_key in OPERATIONS
        ├─ validates operand count vs. arity
        ├─ _coerce_operands()
        │    └─ OperationDispatcher.coerce_operands()
        ├─ _dispatch()
        │    └─ OperationDispatcher.dispatch()
        │         └─ Calculator.<method>()
        └─ print(result) → stdout   |   print(error) → stderr
```

---

## Operation Registry Design

Operations are described by a metadata-driven dispatch pattern. The unified
`OPERATIONS` dict (assembled in `src/operations/__init__.py`) maps string keys to
dispatch records:

```python
OPERATIONS: dict[str, dict] = {
    "add": {
        "method": "add",    # name of a Calculator method
        "arity": 2,         # number of operands required
        "label": "Add two numbers",
    },
    "factorial": {
        "method": "factorial",
        "arity": 1,
        "label": "Factorial of a non-negative integer",
        "coerce": int,      # optional; defaults to float when absent
    },
    ...
}
```

`OperationDispatcher.dispatch()` resolves the `method` field via `getattr` on the
`Calculator` instance, keeping all routing logic out of both `InputHandler` and
`CliDispatcher`. Adding a new operation requires only a new entry in the registry and
a corresponding method on `Calculator`.

---

## Session vs. CLI Interaction Modes

| Aspect | Session (`InputHandler`) | CLI (`CliDispatcher`) |
|--------|--------------------------|----------------------|
| Entry point | `python -m src` | `python main.py` |
| Lifecycle | Continuous REPL loop | Single invocation |
| Input source | `input()` (interactive) | `sys.argv[1:]` |
| Output channel | `stdout` | `stdout` (result) / `stderr` (errors) |
| History | `history.txt` written on exit | Not produced |
| Retry logic | Up to `MAX_RETRIES=5` per prompt | No retries; exit immediately |
| Exit code | N/A (process exits normally) | `0` success / `1` error |

---

## Error Handling Strategy

Errors are handled at the boundary closest to user-facing output:

1. **Domain errors** (`ValueError`, `ZeroDivisionError`, `TypeError`) propagate up
   from `Calculator` methods through `OperationDispatcher.dispatch()` without being
   caught there. `InputHandler.run()` and `CliDispatcher.dispatch_from_args()` catch
   them, log them via `Logger`, and print a user-friendly message.

2. **Coercion errors** (`ValueError` from invalid operand strings) are caught by
   `InputHandler._prompt_operands()` or `CliDispatcher._coerce_operands()`. The
   session retries up to `MAX_RETRIES` times; the CLI fails immediately.

3. **All error events** are written to `error.log` via `Logger`. Successful operations
   are recorded only in `History` (session mode only).

---

## Backward Compatibility

Prior to the modular refactor, source files lived directly in `src/`. Flat shim files
(`src/calculator.py`, `src/cli.py`, etc.) re-export every public symbol from the new
sub-package locations. Code that imports from the old paths continues to work without
modification.

---

## PlantUML Diagrams

Structural diagrams are maintained in [`artifacts/`](../artifacts/):

- `artifacts/class_diagram.puml` — class relationships and public interfaces
- `artifacts/activity_diagram.puml` — interactive and CLI operation flows
- `artifacts/sequence_diagram.puml` — message sequence for a typical session
