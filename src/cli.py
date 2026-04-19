"""CLI argument parsing and execution logic for the Calculator application.

This module provides functions to parse command-line arguments, convert
operand strings to numeric types, and dispatch calculator operations
from a non-interactive (CLI) context.
"""

import sys

from src.calculator import Calculator
from src.error_logger import ErrorLogger
from src.core.operations import get_operation_registry

_error_logger = ErrorLogger()


def parse_arguments(args: list[str]) -> tuple[str, list[str]]:
    """Parse CLI arguments into an operation name and operand strings.

    Args:
        args: A list of string arguments where the first element is the
            operation name and all remaining elements are operand strings.

    Returns:
        A 2-tuple of ``(operation_name, operand_strs)`` where
        *operation_name* is the first argument and *operand_strs* is the
        (possibly empty) list of remaining arguments.

    Examples:
        >>> parse_arguments(["add", "3", "4"])
        ('add', ['3', '4'])
        >>> parse_arguments(["factorial", "5"])
        ('factorial', ['5'])
    """
    operation_name = args[0]
    operand_strs = args[1:]
    return operation_name, operand_strs


def convert_operand(value: str) -> int | float:
    """Convert a string argument to a numeric type.

    Parses the string as a float first. If the resulting float is a whole
    number (i.e. ``float_val == int(float_val)``), returns an int;
    otherwise returns the float.

    Args:
        value: A string representation of a number.

    Returns:
        An ``int`` if *value* represents a whole number, or a ``float``
        otherwise.

    Raises:
        ValueError: If *value* cannot be parsed as a number.

    Examples:
        >>> convert_operand("3")
        3
        >>> convert_operand("3.0")
        3
        >>> convert_operand("3.5")
        3.5
    """
    try:
        float_val = float(value)
    except ValueError:
        raise ValueError(f"operand '{value}' is not a valid number.")
    if float_val == int(float_val):
        return int(float_val)
    return float_val


def execute_cli(
    operation_name: str,
    operand_strs: list[str],
    registry: dict,
    calculator: Calculator,
) -> int:
    """Execute a calculator operation from a CLI context.

    Looks up *operation_name* in *registry*, validates operand count,
    converts operand strings to numbers, calls the operation on
    *calculator*, and writes the result to stdout.

    Error messages are written to stderr prefixed with ``"Error: "``.
    This function never calls ``sys.exit()`` — callers are responsible
    for using the returned exit code.

    Args:
        operation_name: The name of the calculator operation to invoke.
        operand_strs: A list of string operand values to pass to the
            operation.
        registry: A dict mapping operation names to ``(method, arity)``
            2-tuples, as returned by
            :func:`src.input_handler.get_operation_registry`.
        calculator: A :class:`src.calculator.Calculator` instance.

    Returns:
        ``0`` on success, ``1`` on any error.
    """
    # --- operation look-up ---
    if operation_name not in registry:
        available = ", ".join(registry.keys())
        _error_logger.log_error(
            "UNSUPPORTED_OPERATION",
            {
                "operation": operation_name,
                "operands": ", ".join(operand_strs),
                "message": f"unknown operation '{operation_name}'",
            },
        )
        print(
            f"Error: unknown operation '{operation_name}'."
            f" Available operations: {available}",
            file=sys.stderr,
        )
        return 1

    method, arity = registry[operation_name]

    # --- arity validation ---
    actual = len(operand_strs)
    if actual != arity:
        _error_logger.log_error(
            "ARGUMENT_COUNT_MISMATCH",
            {
                "operation": operation_name,
                "operands": ", ".join(operand_strs),
                "message": (
                    f"operation '{operation_name}' expects {arity}"
                    f" operand(s), got {actual}"
                ),
            },
        )
        print(
            f"Error: operation '{operation_name}' expects {arity}"
            f" operand(s), got {actual}.",
            file=sys.stderr,
        )
        return 1

    # --- operand conversion ---
    operands: list[int | float] = []
    for raw in operand_strs:
        try:
            operands.append(convert_operand(raw))
        except ValueError:
            _error_logger.log_error(
                "INVALID_OPERAND",
                {
                    "operation": operation_name,
                    "operands": raw,
                    "message": f"operand '{raw}' is not a valid number",
                },
            )
            print(f"Error: operand '{raw}' is not a valid number.", file=sys.stderr)
            return 1

    # --- dispatch ---
    try:
        result = method(*operands)
    except ZeroDivisionError as exc:
        _error_logger.log_error(
            "DIVISION_BY_ZERO",
            {
                "operation": operation_name,
                "operands": ", ".join(str(o) for o in operands),
                "message": str(exc),
            },
        )
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except TypeError as exc:
        _error_logger.log_error(
            "INVALID_OPERAND",
            {
                "operation": operation_name,
                "operands": ", ".join(str(o) for o in operands),
                "message": str(exc),
            },
        )
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        _error_logger.log_error(
            "INVALID_OPERAND",
            {
                "operation": operation_name,
                "operands": ", ".join(str(o) for o in operands),
                "message": str(exc),
            },
        )
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0
