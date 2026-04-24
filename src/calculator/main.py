"""Modular calculator entry point (Issue #405).

Provides ``cli_mode()`` and ``main()`` backed by the new modular
OperationRegistry rather than the legacy dict-based registry in
``src/__main__.py``.
"""

import sys

from src.calculator.core import Calculator
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


def _build_registry() -> OperationRegistry:
    """Build and return an OperationRegistry populated with all operations.

    Returns:
        An OperationRegistry containing all 13 arithmetic and scientific
        operations.
    """
    registry = OperationRegistry()
    for op in [
        ArithmeticAdd(),
        ArithmeticSubtract(),
        ArithmeticMultiply(),
        ArithmeticDivide(),
        ArithmeticFactorial(),
        ArithmeticModulo(),
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


def cli_mode() -> None:
    """Handle calculator invocation in both CLI and interactive modes.

    When command-line arguments are present (beyond the program name) this
    function parses them, executes the requested operation, and returns.

    When no arguments are present this falls back to the full interactive
    REPL loop.  An ``EOFError`` or ``OSError`` from the interactive loop
    is treated as a missing-operation condition: an error is printed to
    *stderr* and the process exits with code 1.
    """
    registry = _build_registry()
    error_log = ErrorLog()

    if len(sys.argv) <= 1:
        try:
            _run_interactive_loop(registry)
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


def _run_interactive_loop(
    registry: OperationRegistry,
    history_file_path: str | None = None,
) -> None:
    """Run the interactive REPL loop using the modular OperationRegistry.

    Args:
        registry: The OperationRegistry providing all available operations.
        history_file_path: Optional path for the history file.  When None,
            OperationHistory defaults to ``"history.txt"`` in the current
            working directory.

    The loop continues until the user types ``quit``, ``exit``, or ``q``,
    or until 3 consecutive failures occur.
    """
    history = OperationHistory(history_file_path)
    error_log = ErrorLog()
    consecutive_failures: int = 0

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

        if not registry.has(operation):
            error_msg = f"Unknown operation '{operation}'."
            error_log.log_error("unsupported_operation", operation, [], error_msg)
            print(f"Error: Unknown operation '{operation}'. Please try again.")
            consecutive_failures += 1
            if consecutive_failures >= 3:
                print("Too many invalid attempts. Exiting.")
                break
            continue

        op_obj = registry.get(operation)
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


def main() -> None:
    """Run the interactive calculator loop using the modular registry.

    Continuously prompts the user to select an operation, then collects the
    required operands and prints the result.  Typing 'quit', 'exit', or 'q'
    terminates the loop.

    This function goes directly to the interactive REPL and does **not**
    inspect ``sys.argv``.  Use :func:`cli_mode` when you want argv-aware
    dispatch.
    """
    registry = _build_registry()
    _run_interactive_loop(registry)


if __name__ == "__main__":
    cli_mode()
