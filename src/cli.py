"""CLI argument parsing and execution for the calculator."""

import sys

from .calculator import Calculator
from .operations import OperationRegistry
from .validation import OperandValidationError, validate_operand

# Operations whose underlying Calculator method expects an int, not a float.
_INT_OPERAND_OPERATIONS: frozenset[str] = frozenset({"factorial"})

_USAGE = (
    "Usage: python -m src <operation> <operand> [<operand> ...]\n"
    "Example: python -m src add 3 5\n"
    "         python -m src factorial 7\n"
    "Run without arguments to start the interactive session."
)


def parse_args(argv: list[str]) -> tuple[str, list[float]]:
    """Parse CLI arguments into operation name and operand list.

    Args:
        argv: Argument list, where the first element is the operation name
            and remaining elements are operands expressed as strings.

    Returns:
        A 2-tuple of (operation_name, operands).

    Raises:
        SystemExit: If ``argv`` is empty (prints usage to stderr first).
        OperandValidationError: If any operand string cannot be converted to float.
    """
    if not argv:
        print(_USAGE, file=sys.stderr)
        sys.exit(1)

    operation = argv[0]
    raw_operands = argv[1:]

    operands: list[float] = []
    for token in raw_operands:
        try:
            operands.append(validate_operand(token))
        except OperandValidationError as exc:
            raise OperandValidationError(
                f"Invalid numeric operand: {exc}"
            ) from exc

    return operation, operands


def execute_cli(operation: str, operands: list[float]) -> float | int:
    """Execute a named operation and return the result.

    Retrieves the operation from the registry, validates the operand count
    against the registered arity, converts operands to int for operations
    that require integer input (e.g. factorial), then calls the bound
    Calculator method.

    Args:
        operation: The operation key as registered in ``OperationRegistry``.
        operands: The operand values to pass to the operation.

    Returns:
        The computed result as returned by the Calculator method.

    Raises:
        KeyError: If ``operation`` is not registered.
        ValueError: If the operand count does not match the operation's arity,
            or if the Calculator method raises ValueError.
        ZeroDivisionError: If the operation produces a division by zero.
    """
    calc = Calculator()
    registry = OperationRegistry(calc)

    method, arity, _description = registry.get_operation(operation)

    if len(operands) != arity:
        raise ValueError(
            f"Operation '{operation}' expects {arity} operand(s), "
            f"but {len(operands)} were provided."
        )

    # Some Calculator methods (factorial) only accept int; convert accordingly.
    if operation in _INT_OPERAND_OPERATIONS:
        call_operands: list[float | int] = [int(o) for o in operands]
    else:
        call_operands = list(operands)

    return method(*call_operands)


def cli_main(argv: list[str]) -> None:
    """Main CLI entry point.

    Parses arguments, executes the requested operation, and prints the result
    to stdout.  On any error, prints an ``Error: <message>`` line to stderr
    and exits with code 1.  On success, prints the plain result and exits with
    code 0.

    Args:
        argv: Argument list (typically ``sys.argv[1:]``), where the first
            element is the operation name and the rest are operands.
    """
    try:
        operation, operands = parse_args(argv)
    except OperandValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        result = execute_cli(operation, operands)
    except KeyError:
        print(
            f"Error: Invalid operation — '{operation}' is not a supported operation.",
            file=sys.stderr,
        )
        sys.exit(1)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    # Format: omit the ".0" suffix for whole-number floats so the output is
    # readable (e.g. "5" instead of "5.0"), but preserve genuine fractional
    # values (e.g. "3.5").
    if isinstance(result, float) and result.is_integer():
        print(int(result))
    else:
        print(result)

    sys.exit(0)
