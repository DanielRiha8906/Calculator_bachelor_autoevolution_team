"""Command-line interface for the Calculator.

Provides a thin CLI wrapper that maps a single operation name and its operands
(supplied as command-line arguments) to the corresponding Calculator method via
the OperationRegistry.
"""

import sys
from typing import Union

from .calculator import Calculator
from .operation_registry import OperationRegistry


def parse_cli_operand(operand_str: str) -> Union[int, float]:
    """Parse a string operand into an int or float.

    Tries int conversion first.  If the string contains a decimal point or
    cannot be parsed as an integer, float conversion is attempted instead.

    Args:
        operand_str: The raw string to parse.

    Returns:
        An ``int`` when the string represents a whole number without a decimal
        point, or a ``float`` otherwise.

    Raises:
        ValueError: If the string cannot be parsed as either int or float,
            with message "Invalid operand: <operand_str>".
    """
    if "." in operand_str:
        try:
            return float(operand_str)
        except ValueError:
            raise ValueError(f"Invalid operand: {operand_str}")
    try:
        return int(operand_str)
    except ValueError:
        try:
            return float(operand_str)
        except ValueError:
            raise ValueError(f"Invalid operand: {operand_str}")


def run_cli(argv: list[str] | None = None) -> int:
    """Run the calculator CLI with the provided argument vector.

    Dispatches a single operation to the Calculator via the OperationRegistry.
    Prints the result to stdout on success, or an error message to stderr on
    failure.

    Args:
        argv: List of string arguments (operation name followed by operands).
            Defaults to ``sys.argv[1:]`` when ``None``.

    Returns:
        0 on success, 1 on any error (unknown operation, wrong operand count,
        invalid operand format, or a domain error raised by the operation).
    """
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: calculator <operation> [operands...]", file=sys.stderr)
        return 1

    operation_name = argv[0]
    operand_args = argv[1:]

    calculator = Calculator()
    registry = OperationRegistry(calculator)

    if operation_name not in registry.get_operations():
        print(f"Error: Unknown operation: {operation_name}", file=sys.stderr)
        return 1

    arity = registry.get_arity(operation_name)

    if len(operand_args) != arity:
        print(
            f"Error: {operation_name} requires {arity} operand(s),"
            f" got {len(operand_args)}",
            file=sys.stderr,
        )
        return 1

    operands: list[Union[int, float]] = []
    for raw in operand_args:
        try:
            operands.append(parse_cli_operand(raw))
        except ValueError:
            print(f"Error: Invalid operand: {raw}", file=sys.stderr)
            return 1

    try:
        result = registry.call(operation_name, *operands)
    except ZeroDivisionError:
        print("Error: Division by zero", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0
