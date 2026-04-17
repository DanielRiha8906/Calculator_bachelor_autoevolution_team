"""CLI interface for the calculator.

Provides a non-interactive command-line mode that accepts an operation name
and its operands as positional arguments, dispatches the calculation, and
prints the result to stdout.  On any error (wrong operand count, non-numeric
input, or a domain error such as division by zero), a message is printed to
stderr and the process exits with code 1.
"""

from __future__ import annotations

import argparse
import sys

from .calculator import Calculator
from .input_loop import OPERATIONS, dispatch


def run_cli(argv: list[str] | None = None) -> None:
    """Parse command-line arguments and run a single calculator operation.

    Args:
        argv: Argument list to parse.  Defaults to ``None``, which causes
            :mod:`argparse` to read from ``sys.argv[1:]``.  Pass an explicit
            list in tests to avoid touching the real ``sys.argv``.

    Raises:
        SystemExit: With code 1 on operand-count mismatch, non-numeric
            operand, or a domain error raised by the Calculator.  With
            code 2 if argparse rejects the arguments (e.g. unknown operation).
    """
    parser = argparse.ArgumentParser(
        description="Run a single calculator operation from the command line.",
    )
    parser.add_argument(
        "operation",
        choices=list(OPERATIONS.keys()),
        help="The operation to perform.",
    )
    parser.add_argument(
        "operands",
        nargs="*",
        help="Numeric operand(s) required by the chosen operation.",
    )

    args = parser.parse_args(argv)

    _, operand_count = OPERATIONS[args.operation]

    if len(args.operands) != operand_count:
        print(
            f"Error: '{args.operation}' requires exactly {operand_count} operand(s), "
            f"but {len(args.operands)} were provided.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        operands_as_floats: list[float] = [float(o) for o in args.operands]
    except ValueError:
        print(
            "Error: all operands must be numeric values.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        result = dispatch(args.operation, operands_as_floats, Calculator())
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(result)
