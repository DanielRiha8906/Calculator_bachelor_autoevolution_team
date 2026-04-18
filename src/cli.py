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
from .error_logger import (
    CALCULATION_ERROR,
    INVALID_INPUT,
    UNEXPECTED_ERROR,
    ErrorLogger,
)
from .history import OperationHistory
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


def run_cli(history: OperationHistory | None = None) -> None:
    """Parse CLI arguments, validate them, run the operation, and print the result.

    Validates that:
    - The operation is a recognised key in :data:`~src.input_loop.OPERATIONS`
      and is not a meta-command (e.g. ``"history"``).
    - The number of operands supplied matches the expected operand count.
    - Every operand can be parsed as a :class:`float`.

    On any validation failure the error message is written to *stderr* and
    the process exits with code ``2``.  On success the numeric result is
    printed to *stdout*, the operation is recorded in *history*, and the
    process exits normally (code ``0``).

    Args:
        history: :class:`~src.history.OperationHistory` instance used to
            record the successful operation.  When ``None`` (the default) a
            new instance is created internally.
    """
    if history is None:
        history = OperationHistory()
    error_logger = ErrorLogger()

    parser = _build_parser()
    args = parser.parse_args()

    operation: str = args.operation

    # Exclude meta-commands (0 operands) from CLI dispatch.
    if operation not in OPERATIONS or OPERATIONS[operation][1] == 0:
        valid = ", ".join(k for k, (_, c) in OPERATIONS.items() if c > 0)
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
        lower_msg = str(exc).lower()
        if "division by zero" in lower_msg or "zero" in lower_msg:
            category = CALCULATION_ERROR
        elif "invalid" in lower_msg:
            category = INVALID_INPUT
        else:
            category = CALCULATION_ERROR
        context: dict = {  # type: ignore[type-arg]
            "operation": operation,
            "operands": operands,
            "error": str(exc),
        }
        error_logger.log_error(category, str(exc), context)
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)

    history.record_operation(operation, operands, result)
    print(result)
