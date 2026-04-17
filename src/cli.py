"""CLI dispatch layer for the Calculator application.

This module provides ``run_cli``, a function that accepts a list of string
arguments (typically ``sys.argv[1:]``), validates them against the OPERATIONS
registry, coerces operands, dispatches to a Calculator instance, and writes
the result to stdout.  All error messages go to stderr; the process exits with
code 1 on any failure and code 0 on success.
"""

from __future__ import annotations

import sys
from typing import Callable

from .calculator import Calculator
from .input_handler import OPERATIONS


def run_cli(args: list[str]) -> None:
    """Parse *args* and dispatch a single calculator operation.

    Args:
        args: Positional CLI arguments, normally ``sys.argv[1:]``.
            Expected layout: ``[op_name, operand1 [, operand2]]``.

    Raises:
        SystemExit: Always — exit code 0 on success, 1 on any error.
    """
    if len(args) == 0:
        _die(
            "Usage: python main.py <operation> [operand ...]\n"
            f"Available operations: {', '.join(OPERATIONS)}"
        )

    op_name: str = args[0]

    if op_name not in OPERATIONS:
        _die(
            f"Error: Unknown operation '{op_name}'. "
            f"Available operations: {', '.join(OPERATIONS)}"
        )

    op_info: dict = OPERATIONS[op_name]
    expected_arity: int = op_info["arity"]
    provided: int = len(args) - 1

    if provided != expected_arity:
        _die(
            f"Error: Operation '{op_name}' expects {expected_arity} operand(s), "
            f"but {provided} were provided."
        )

    coerce: Callable = op_info.get("coerce", float)  # type: ignore[assignment]

    operands: list = []
    for raw in args[1:]:
        try:
            operands.append(coerce(raw))
        except (ValueError, TypeError):
            _die(
                f"Error: Invalid operand '{raw}' for operation '{op_name}': "
                f"expected a numeric value."
            )

    calc = Calculator()
    method_name: str = op_info["method"]

    try:
        result = getattr(calc, method_name)(*operands)
    except ZeroDivisionError:
        _die("Error: Division by zero is not allowed.")
    except ValueError as exc:
        _die(f"Error: {exc}")
    except TypeError as exc:
        _die(f"Error: {exc}")

    print(result)
    sys.exit(0)


def _die(message: str) -> None:
    """Write *message* to stderr and exit with code 1.

    Args:
        message: Human-readable error description.

    Raises:
        SystemExit: Always, with exit code 1.
    """
    print(message, file=sys.stderr)
    sys.exit(1)
