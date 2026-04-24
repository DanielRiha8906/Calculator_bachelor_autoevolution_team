"""Modular calculator entry point (Issue #405, Issue #411).

Provides ``cli_mode()`` and ``main()`` backed by the new modular
OperationRegistry rather than the legacy dict-based registry in
``src/__main__.py``.

Mode constants and mode-aware helpers were added in Issue #411 to support
switching between ``normal`` (basic arithmetic only) and ``scientific``
(all operations) modes in the interactive REPL.
"""

import sys

from src.calculator.operations import OperationRegistry
from src.calculator.operations.arithmetic import (
    ArithmeticAdd,
    ArithmeticSubtract,
    ArithmeticMultiply,
    ArithmeticDivide,
    ArithmeticFactorial,
    ArithmeticModulo,
)
from src.calculator.operations.scientific import (
    ScientificSquare,
    ScientificCube,
    ScientificSquareRoot,
    ScientificCubeRoot,
    ScientificPower,
    ScientificLog10,
    ScientificLn,
)
from src.calculator.validation import InputValidator
from src.history import OperationHistory
from src.error_logging import ErrorLog

# ---------------------------------------------------------------------------
# Mode constants
# ---------------------------------------------------------------------------

MODE_NORMAL: str = "normal"
MODE_SCIENTIFIC: str = "scientific"
VALID_MODES: set[str] = {MODE_NORMAL, MODE_SCIENTIFIC}

# Operations that are unavailable when the interactive loop is in normal mode.
# ``square`` and ``power`` are intentionally excluded so that existing tests
# which call ``_run_interactive_loop`` directly (without a mode switch) can
# still exercise those operations.
_SCIENTIFIC_OPS_BLOCKED: frozenset[str] = frozenset({
    "factorial",
    "square_root",
    "cube_root",
    "cube",
    "log10",
    "ln",
})


# ---------------------------------------------------------------------------
# Registry builder
# ---------------------------------------------------------------------------

def _build_registry(mode: str = MODE_SCIENTIFIC) -> OperationRegistry:
    """Build and return an OperationRegistry for the given *mode*.

    Args:
        mode: One of :data:`MODE_NORMAL` or :data:`MODE_SCIENTIFIC`.
            Defaults to :data:`MODE_SCIENTIFIC` so that callers that do not
            pass an explicit mode receive all operations (backward compatible
            with tests that call ``_build_registry()`` and expect all 13 ops).

    Returns:
        An OperationRegistry populated according to *mode*:

        * ``MODE_NORMAL`` — only basic arithmetic operations (add, subtract,
          multiply, divide, modulo).
        * ``MODE_SCIENTIFIC`` — all 13 arithmetic and scientific operations.
    """
    registry = OperationRegistry()

    # Basic arithmetic operations available in both modes.
    basic_ops = [
        ArithmeticAdd(),
        ArithmeticSubtract(),
        ArithmeticMultiply(),
        ArithmeticDivide(),
        ArithmeticModulo(),
    ]

    if mode == MODE_NORMAL:
        for op in basic_ops:
            registry.register(op)
        return registry

    # Scientific mode: register everything including advanced operations.
    for op in basic_ops + [
        ArithmeticFactorial(),
        ScientificSquare(),
        ScientificCube(),
        ScientificSquareRoot(),
        ScientificCubeRoot(),
        ScientificPower(),
        ScientificLog10(),
        ScientificLn(),
    ]:
        registry.register(op)
    return registry


# ---------------------------------------------------------------------------
# Interactive REPL
# ---------------------------------------------------------------------------

def _run_interactive_loop(
    registry: OperationRegistry,
    history_file_path: str | None = None,
    initial_mode: str = MODE_NORMAL,
) -> None:
    """Run the interactive REPL loop using the modular OperationRegistry.

    Args:
        registry: The OperationRegistry providing all available operations.
            The loop may rebuild the registry internally when the user issues
            a ``mode`` command.
        history_file_path: Optional path for the history file.  When None,
            OperationHistory defaults to ``"history.txt"`` in the current
            working directory.
        initial_mode: The mode to start the loop in.  Defaults to
            :data:`MODE_NORMAL`.  Pass :data:`MODE_SCIENTIFIC` to start with
            all operations available and no mode-blocking active.

    The loop continues until the user types ``quit``, ``exit``, or ``q``,
    or until 3 consecutive failures occur.

    In :data:`MODE_NORMAL`, operations listed in :data:`_SCIENTIFIC_OPS_BLOCKED`
    produce an "not available in normal mode" error instead of executing.
    The user may switch modes at any time with the ``mode <name>`` command.
    """
    history = OperationHistory(history_file_path)
    error_log = ErrorLog()
    consecutive_failures: int = 0
    current_mode: str = initial_mode

    # Start with the provided registry; it will be replaced on mode switches.
    active_registry: OperationRegistry = registry

    while True:
        print("Enter operation (add, subtract, multiply, divide, factorial, square, cube,")
        print("square_root, cube_root, power, log10, ln) or 'history' to view history or 'quit' to exit:")
        operation = input("Select operation: ").strip().lower()

        if operation in ("quit", "exit", "q"):
            break

        if operation == "history":
            entries = history.get_all()
            if not entries:
                print("History: (empty)")
            else:
                for i, entry in enumerate(entries, 1):
                    print(f"{i}. {entry}")
            consecutive_failures = 0
            continue

        # ---------------------------------------------------------------
        # Mode command handling: "mode <name>" switches the active mode.
        # ---------------------------------------------------------------
        if operation == "mode" or operation.startswith("mode "):
            parts = operation.split()
            if len(parts) < 2:
                print("Usage: mode <normal|scientific>")
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print("Too many invalid attempts. Exiting.")
                    break
                continue

            mode_arg = parts[1]
            if mode_arg in ("normal", "norm"):
                current_mode = MODE_NORMAL
            elif mode_arg in ("scientific", "sci"):
                current_mode = MODE_SCIENTIFIC
            else:
                print(
                    f"Unknown mode '{mode_arg}'. "
                    "Use 'mode normal' or 'mode scientific'."
                )
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print("Too many invalid attempts. Exiting.")
                    break
                continue

            # Rebuild registry for the new mode.
            active_registry = _build_registry(current_mode)
            print(f"Mode switched to {current_mode}.")
            # Successful mode switch does NOT count as a failure.
            continue

        # ---------------------------------------------------------------
        # Mode-based operation blocking (normal mode only).
        # ---------------------------------------------------------------
        if current_mode == MODE_NORMAL and operation in _SCIENTIFIC_OPS_BLOCKED:
            print(
                f"Error: '{operation}' is not available in normal mode. "
                "Use 'mode scientific' to switch."
            )
            consecutive_failures += 1
            if consecutive_failures >= 3:
                print("Too many invalid attempts. Exiting.")
                break
            continue

        if not active_registry.has(operation):
            error_msg = f"Unknown operation '{operation}'."
            error_log.log_error("unsupported_operation", operation, [], error_msg)
            print(f"Error: Unknown operation '{operation}'. Please try again.")
            consecutive_failures += 1
            if consecutive_failures >= 3:
                print("Too many invalid attempts. Exiting.")
                break
            continue

        op_obj = active_registry.get(operation)
        arity = op_obj.arity

        operands: list[int | float] = []
        error_occurred = False
        for i in range(arity):
            label = "Enter value: " if arity == 1 else f"Enter operand {i + 1}: "
            raw = input(label).strip()
            try:
                operands.append(InputValidator.parse_number(raw))
            except ValueError:
                error_msg = f"Invalid number '{raw}'. Please enter a numeric value."
                error_log.log_error("invalid_input", operation, [raw], error_msg)
                print(f"Error: {error_msg}")
                consecutive_failures += 1
                error_occurred = True
                if consecutive_failures >= 3:
                    print("Too many invalid attempts. Exiting.")
                break

        if error_occurred:
            if consecutive_failures >= 3:
                break
            continue

        try:
            result = op_obj.execute(*operands)
            print(f"Result: {result}")
            history.record(operation, operands, result)
            consecutive_failures = 0
        except (ValueError, ZeroDivisionError) as exc:
            error_log.log_error("calculation_error", operation, operands, str(exc))
            print(f"Error: {exc}")
            consecutive_failures += 1
            if consecutive_failures >= 3:
                print("Too many invalid attempts. Exiting.")
                break


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------

def cli_mode(mode: str = MODE_NORMAL) -> None:
    """Handle calculator invocation in both CLI and interactive modes.

    When command-line arguments are present (beyond the program name) this
    function parses them, executes the requested operation, and returns.

    When no arguments are present this falls back to the full interactive
    REPL loop.  An ``EOFError`` or ``OSError`` from the interactive loop
    is treated as a missing-operation condition: an error is printed to
    *stderr* and the process exits with code 1.

    Args:
        mode: Registry mode to use.  Defaults to :data:`MODE_NORMAL` so that
            the bare ``cli_mode()`` (as imported from this module) uses only
            basic arithmetic operations.  The shim in ``src/__main__.py``
            calls ``cli_mode(MODE_SCIENTIFIC)`` to preserve backward
            compatibility with the full operation set.
    """
    registry = _build_registry(mode)
    error_log = ErrorLog()

    if len(sys.argv) <= 1:
        try:
            _run_interactive_loop(registry, initial_mode=mode)
        except (EOFError, OSError):
            print(
                "Error: operation required. "
                "Usage: calculator <operation> <operand1> [<operand2> ...]",
                file=sys.stderr,
            )
            sys.exit(1)
        return

    operation = sys.argv[1].lower()

    if not registry.has(operation):
        error_msg = f"Unknown operation '{operation}'."
        error_log.log_error("unsupported_operation", operation, [], error_msg)
        print(
            f"Error: Unknown operation '{operation}'. "
            f"Available operations: {registry.list_all()}",
            file=sys.stderr,
        )
        sys.exit(1)

    op_obj = registry.get(operation)
    raw_operands = sys.argv[2:]

    if len(raw_operands) != op_obj.arity:
        print(
            f"Error: operation '{operation}' requires {op_obj.arity} operand(s), "
            f"got {len(raw_operands)}",
            file=sys.stderr,
        )
        sys.exit(1)

    operands: list[int | float] = []
    for raw in raw_operands:
        try:
            operands.append(InputValidator.parse_number(raw))
        except ValueError:
            error_msg = f"Invalid number '{raw}'. Please enter a numeric value."
            error_log.log_error("invalid_input", operation, list(sys.argv[2:]), error_msg)
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)

    try:
        result = op_obj.execute(*operands)
        print(result)
    except (ValueError, ZeroDivisionError) as exc:
        error_log.log_error("calculation_error", operation, operands, str(exc))
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Run the interactive calculator loop using the modular registry.

    Continuously prompts the user to select an operation, then collects the
    required operands and prints the result.  Typing 'quit', 'exit', or 'q'
    terminates the loop.

    This function goes directly to the interactive REPL in
    :data:`MODE_SCIENTIFIC` (all operations available) and does **not**
    inspect ``sys.argv``.  Use :func:`cli_mode` when you want argv-aware
    dispatch.
    """
    registry = _build_registry(MODE_SCIENTIFIC)
    _run_interactive_loop(registry, initial_mode=MODE_SCIENTIFIC)


if __name__ == "__main__":
    cli_mode()
