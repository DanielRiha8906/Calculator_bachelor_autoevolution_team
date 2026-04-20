"""Top-level CLI entry point for the Calculator application.

Usage:
    python main.py <operation> [operand ...]

Examples:
    python main.py add 3 4
    python main.py factorial 5
    python main.py square_root 9
"""

import sys

from src.calculator import Calculator
from src.cli import execute_cli
from src.input_handler import get_operation_registry


def main() -> None:
    """Parse CLI arguments and run the requested calculator operation.

    Reads ``sys.argv[1:]``, validates that at least one argument (the
    operation name) is present, builds the operation registry, and
    delegates to :func:`src.cli.execute_cli`. Exits with the code
    returned by that function.
    """
    args = sys.argv[1:]

    if not args:
        print(
            "Usage: python main.py <operation> [operand ...]\n"
            "Example: python main.py add 3 4",
            file=sys.stderr,
        )
        sys.exit(1)

    calculator = Calculator()
    registry = get_operation_registry(calculator)
    operation_name, operand_strs = args[0], args[1:]
    exit_code = execute_cli(operation_name, operand_strs, registry, calculator)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
