import sys

from .calculator import Calculator
from .cli import CLIHandler
from .history import OperationHistory
from .repl import REPLInterface


def main(argv: list[str] | None = None) -> None:
    """Entry point for the calculator application.

    Operates in two modes depending on the command-line arguments:

    - REPL mode: launched when no extra arguments are provided (argv is empty).
    - CLI mode: launched when an operation and at least one operand are provided.

    Args:
        argv: Argument list to parse.  Defaults to ``sys.argv[1:]`` when
              ``None``.  Pass an explicit list to override (useful in tests).

    Exit codes:
        0: success
        1: usage error (wrong number of arguments)
        2: unknown operation name
        3: invalid operands (missing, non-numeric, wrong count)
        4: operation error (division by zero, math domain error)
    """
    if argv is None:
        argv = sys.argv[1:]

    history = OperationHistory()
    history.clear_history()

    calc = Calculator()

    if len(argv) == 0 or (len(argv) == 1 and argv[0] == "--repl"):
        # REPL mode — existing behaviour unchanged.
        repl = REPLInterface(calc, history=history)
        try:
            repl.run()
        except (EOFError, KeyboardInterrupt):
            print("\nCalculator closed.")
        return

    if len(argv) == 1 and argv[0] != "--repl":
        print(
            "Usage: python -m src <operation> <operand> [operand2]",
            file=sys.stderr,
        )
        sys.exit(1)

    # CLI mode: len(argv) >= 2, first arg is the operation.
    handler = CLIHandler(calc, history=history)
    try:
        result = handler.execute(argv)
        print(result)
        sys.exit(0)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if str(exc).startswith("Unknown operation"):
            sys.exit(2)
        sys.exit(3)
    except ZeroDivisionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(4)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    main()
