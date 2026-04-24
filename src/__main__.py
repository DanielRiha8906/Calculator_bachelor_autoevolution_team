"""Interactive and CLI calculator entry point.

Provides two modes of operation:
- CLI mode: pass operation and operands as command-line arguments
  (e.g. ``python -m calculator add 5 3``).
- Interactive mode: a REPL-style loop that reads an operation name and its
  operands from stdin, calls the corresponding Calculator method, and prints
  the result.
"""

import sys

from .calculator import Calculator


# ---------------------------------------------------------------------------
# Shared operation registry (built lazily from a fresh Calculator instance)
# ---------------------------------------------------------------------------

def _build_registry(calculator: Calculator) -> dict[str, tuple]:
    """Build the operation registry from a Calculator instance.

    Args:
        calculator: An instantiated Calculator whose methods are registered.

    Returns:
        A dict mapping operation name (str) to a (callable, arity) tuple.
    """
    return {
        "add": (calculator.add, 2),
        "subtract": (calculator.subtract, 2),
        "multiply": (calculator.multiply, 2),
        "divide": (calculator.divide, 2),
        "factorial": (calculator.factorial, 1),
        "square": (calculator.square, 1),
        "cube": (calculator.cube, 1),
        "square_root": (calculator.square_root, 1),
        "cube_root": (calculator.cube_root, 1),
        "power": (calculator.power, 2),
        "log10": (calculator.log10, 1),
        "ln": (calculator.ln, 1),
    }


def _parse_number(raw: str) -> int | float:
    """Parse a string as a number, preferring int over float.

    Args:
        raw: The raw string read from user input or a CLI argument.

    Returns:
        An int if the string represents a whole number without a decimal point,
        otherwise a float.

    Raises:
        ValueError: If the string cannot be interpreted as a number.
    """
    try:
        return int(raw)
    except ValueError:
        return float(raw)


# ---------------------------------------------------------------------------
# CLI helpers
# ---------------------------------------------------------------------------

def _parse_cli_arguments(
    registry: dict[str, tuple],
) -> tuple[str, list[int | float]] | None:
    """Parse and validate command-line arguments for CLI mode.

    Args:
        registry: The operation registry mapping name to (callable, arity).

    Returns:
        A (operation_name, operands) tuple on success, or ``None`` when no
        CLI arguments are present (caller should fall through to interactive
        mode).

    Side-effects:
        Prints an error message to *stderr* and calls ``sys.exit(1)`` on any
        validation failure.
    """
    # No CLI arguments beyond the program name → signal interactive mode.
    if len(sys.argv) <= 1:
        return None

    operation = sys.argv[1].lower()

    if operation not in registry:
        print(
            f"Error: Unknown operation '{operation}'. "
            f"Available operations: {list(registry.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    _, arity = registry[operation]
    raw_operands = sys.argv[2:]

    if len(raw_operands) != arity:
        print(
            f"Error: operation '{operation}' requires {arity} operand(s), "
            f"got {len(raw_operands)}",
            file=sys.stderr,
        )
        sys.exit(1)

    operands: list[int | float] = []
    for raw in raw_operands:
        try:
            operands.append(_parse_number(raw))
        except ValueError:
            print(
                f"Error: Invalid number '{raw}'. Please enter a numeric value.",
                file=sys.stderr,
            )
            sys.exit(1)

    return operation, operands


def _execute_cli_mode(
    operation: str,
    operands: list[int | float],
    registry: dict[str, tuple],
) -> None:
    """Execute a single CLI operation and print the result.

    Args:
        operation: The validated operation name (lowercase).
        operands: The parsed operand list.
        registry: The operation registry mapping name to (callable, arity).

    Side-effects:
        Prints the result to *stdout*.  On ``ValueError`` or
        ``ZeroDivisionError`` prints the error to *stderr* and calls
        ``sys.exit(1)``.
    """
    method, _ = registry[operation]
    try:
        result = method(*operands)
        print(result)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------

def cli_mode() -> None:
    """Handle calculator invocation in both CLI and interactive modes.

    When command-line arguments are present (beyond the program name) this
    function parses them, executes the requested operation, and returns.

    When no command-line arguments are present this function falls back to
    the full interactive REPL loop (identical to what ``main()`` used to do
    stand-alone).  An ``EOFError`` from the interactive loop (e.g. stdin is
    closed, no terminal attached) is treated as a missing-operation condition:
    an error is printed to *stderr* and the process exits with code 1.
    """
    calculator = Calculator()
    registry = _build_registry(calculator)

    parsed = _parse_cli_arguments(registry)
    if parsed is not None:
        operation, operands = parsed
        _execute_cli_mode(operation, operands, registry)
        return

    # --- Interactive (REPL) fallback ---
    try:
        _run_interactive_loop(registry)
    except (EOFError, OSError):
        # EOFError: stdin is closed (e.g. piped input exhausted).
        # OSError: stdin is blocked (e.g. pytest capture with no monkeypatched input).
        # Both conditions mean no interactive input is available; treat as
        # a missing-operation invocation and exit with an error.
        print(
            "Error: operation required. "
            "Usage: calculator <operation> <operand1> [<operand2> ...]",
            file=sys.stderr,
        )
        sys.exit(1)


def _run_interactive_loop(registry: dict[str, tuple]) -> None:
    """Run the interactive REPL loop.

    Args:
        registry: The operation registry mapping name to (callable, arity).

    The loop continues until the user types ``quit``, ``exit``, or ``q``,
    or until 3 consecutive failures occur (unknown operation, invalid operand,
    or domain error).  On reaching 3 consecutive failures the loop prints
    "Too many invalid attempts. Exiting." and terminates.
    ``EOFError`` is intentionally *not* caught here so that callers can
    decide how to handle a closed stdin.
    """
    consecutive_failures: int = 0

    while True:
        print("Enter operation (add, subtract, multiply, divide, factorial, square, cube,")
        print("square_root, cube_root, power, log10, ln) or 'quit' to exit:")
        operation = input("Select operation: ").strip().lower()

        if operation in ("quit", "exit", "q"):
            break

        if operation not in registry:
            print(f"Error: Unknown operation '{operation}'. Please try again.")
            consecutive_failures += 1
            if consecutive_failures >= 3:
                print("Too many invalid attempts. Exiting.")
                break
            continue

        method, arity = registry[operation]

        # Collect operands
        operands: list[int | float] = []
        error_occurred = False
        for i in range(arity):
            if arity == 1:
                label = "Enter value: "
            else:
                label = f"Enter operand {i + 1}: "
            raw = input(label).strip()
            try:
                operands.append(_parse_number(raw))
            except ValueError:
                print(f"Error: Invalid number '{raw}'. Please enter a numeric value.")
                consecutive_failures += 1
                error_occurred = True
                if consecutive_failures >= 3:
                    print("Too many invalid attempts. Exiting.")
                break

        if error_occurred:
            if consecutive_failures >= 3:
                break
            continue

        # Execute the operation
        try:
            result = method(*operands)
            print(f"Result: {result}")
            consecutive_failures = 0
        except (ValueError, ZeroDivisionError) as exc:
            print(f"Error: {exc}")
            consecutive_failures += 1
            if consecutive_failures >= 3:
                print("Too many invalid attempts. Exiting.")
                break


def main() -> None:
    """Run the interactive calculator loop.

    Continuously prompts the user to select an operation, then collects the
    required operands and prints the result.  Typing 'quit', 'exit', or 'q'
    terminates the loop.

    This function goes directly to the interactive REPL and does **not**
    inspect ``sys.argv``.  Use :func:`cli_mode` when you want argv-aware
    dispatch (CLI mode falling back to interactive when no args are given).
    """
    calculator = Calculator()
    registry = _build_registry(calculator)
    _run_interactive_loop(registry)


if __name__ == "__main__":
    cli_mode()
