"""CLI mode for the calculator.

Parses command-line arguments using argparse and dispatches the requested
operation to the Calculator.  Intended to be invoked when ``sys.argv``
contains arguments beyond the module name.

Typical usage::

    python -m src add 3 5
    python -m src divide 10 2
    python -m src square_root 9
"""

from __future__ import annotations

import argparse
import sys

from .calculator import Calculator
from .input_loop import OPERATIONS, dispatch


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for CLI mode.

    Returns:
        A configured :class:`argparse.ArgumentParser` instance with a
        positional ``operation`` argument and one-or-more positional
        ``operands``.
    """
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Command-line calculator. Pass an operation and its operands as arguments.",
    )
    parser.add_argument(
        "operation",
        type=str,
        help=(
            "Operation to perform. Valid operations: "
            + ", ".join(OPERATIONS.keys())
        ),
    )
    parser.add_argument(
        "operands",
        nargs="+",
        metavar="OPERAND",
        help="One or more numeric operands required by the operation.",
    )
    return parser


def run_cli() -> None:
    """Parse CLI arguments, validate them, run the operation, and print the result.

    Validates that:
    - The operation is a recognised key in :data:`~src.input_loop.OPERATIONS`.
    - The number of operands supplied matches the expected operand count.
    - Every operand can be parsed as a :class:`float`.

    On any validation failure the error message is written to *stderr* and
    the process exits with code ``2``.  On success the numeric result is
    printed to *stdout* and the process exits normally (code ``0``).
    """
    # CLI mode validation is one-pass: invalid input exits immediately with code 2.
    # Retry logic (see src/retry_logic.py) is used only in guided interactive mode.
    parser = _build_parser()
    args = parser.parse_args()

    operation: str = args.operation

    if operation not in OPERATIONS:
        valid = ", ".join(OPERATIONS.keys())
        print(
            f"error: unknown operation '{operation}'. Valid operations are: {valid}",
            file=sys.stderr,
        )
        sys.exit(2)

    _, expected_count = OPERATIONS[operation]
    supplied_count = len(args.operands)

    if supplied_count != expected_count:
        print(
            f"error: operation '{operation}' requires {expected_count} operand(s), "
            f"but {supplied_count} were supplied.",
            file=sys.stderr,
        )
        sys.exit(2)

    operands: list[float] = []
    for raw in args.operands:
        try:
            operands.append(float(raw))
        except ValueError:
            print(
                f"error: '{raw}' is not a valid number.",
                file=sys.stderr,
            )
            sys.exit(2)

    calc = Calculator()
    try:
        result = dispatch(operation, operands, calc)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)

    print(result)
