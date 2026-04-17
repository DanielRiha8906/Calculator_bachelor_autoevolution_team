"""Root-level entry point for the Calculator CLI mode.

Usage::

    python main.py <operation> <operand1> [<operand2>]

Examples::

    python main.py add 5 7
    python main.py factorial 5
    python main.py divide 10 3
"""

import sys

from src.calculator import Calculator
from src.cli import CliDispatcher


def main() -> None:
    """Parse sys.argv and dispatch the requested calculation.

    Creates a Calculator and CliDispatcher, then calls
    dispatch_from_args with the command-line arguments.  Exits with
    the return code produced by the dispatcher (0 for success, 1 for
    any error).
    """
    calculator = Calculator()
    dispatcher = CliDispatcher(calculator)
    exit_code = dispatcher.dispatch_from_args(sys.argv[1:])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
