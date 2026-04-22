"""CLI entry point for the Calculator.

Accepts an operation name and its operands as positional command-line
arguments and prints the result to stdout.

Usage:
    python main.py <operation> [operand ...]

Examples:
    python main.py add 3 5
    python main.py square_root 16
    python main.py factorial 7
"""

import inspect
import sys

from src.calculator import Calculator
from src.error_logger import ErrorLogger


def get_operation_arity(operation_name: str) -> int:
    """Return the number of operands required by a Calculator operation.

    Inspects the Calculator method signature dynamically so that new
    operations added to Calculator are automatically supported without
    any changes here.

    Args:
        operation_name: Name of the Calculator method to inspect.

    Returns:
        The count of non-``self`` parameters for the method, or ``-1``
        if the operation does not exist on Calculator.
    """
    method = getattr(Calculator, operation_name, None)
    if method is None:
        return -1
    sig = inspect.signature(method)
    # Count every parameter except 'self'
    non_self_params = [
        name
        for name, param in sig.parameters.items()
        if name != "self"
    ]
    return len(non_self_params)


def parse_arguments(args: list) -> tuple[str, list]:
    """Extract operation name and operand strings from argument list.

    Args:
        args: Equivalent to ``sys.argv[1:]`` — the raw CLI arguments.

    Returns:
        A tuple of ``(operation_name, operands_list)`` where
        ``operands_list`` is a (possibly empty) list of raw strings.

    Raises:
        SystemExit: With exit code 1 if no arguments are provided.
    """
    if not args:
        print(
            "Usage: python main.py <operation> [operand ...]",
            file=sys.stderr,
        )
        sys.exit(1)
    operation_name = args[0]
    operands = args[1:]
    return operation_name, operands


def _to_number(value: str) -> int | float:
    """Convert a string to int or float.

    Tries int first; falls back to float.

    Args:
        value: String representation of a number.

    Returns:
        An ``int`` if the string represents a whole number, otherwise a
        ``float``.

    Raises:
        ValueError: If the string cannot be parsed as a number.
    """
    try:
        return int(value)
    except ValueError:
        return float(value)


def execute_operation(calc: Calculator, operation_name: str, operands: list):
    """Call a Calculator method with the given operand strings.

    Converts each operand string to a numeric type (int preferred, then
    float), looks up the method by name, and calls it.

    Args:
        calc: A Calculator instance.
        operation_name: Name of the method to call on ``calc``.
        operands: List of raw string operands (already sliced to the
            correct arity).

    Returns:
        The result returned by the Calculator method.

    Raises:
        ValueError: If an operand string cannot be parsed as a number.
        Any exception raised by the underlying Calculator method.
    """
    numeric_operands = [_to_number(op) for op in operands]
    method = getattr(calc, operation_name)
    return method(*numeric_operands)


def main() -> None:
    """Orchestrate CLI argument parsing and Calculator execution.

    Flow:
    1. Parse ``sys.argv[1:]`` for operation name and operands.
    2. Determine required arity via ``get_operation_arity``.
    3. Validate that enough operands were supplied.
    4. Execute the operation and print the result.

    Exits with code 0 on success, 1 on any error.
    """
    error_logger = ErrorLogger()

    operation_name, operands = parse_arguments(sys.argv[1:])

    calc = Calculator()

    arity = get_operation_arity(operation_name)
    if arity == -1:
        error_logger.log_unsupported_operation(operation_name)
        print(
            f"Error: unknown operation '{operation_name}'",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(operands) < arity:
        error_logger.log_incorrect_arity(operation_name, arity, len(operands))
        print(
            f"Error: operation '{operation_name}' requires {arity} "
            f"operand(s), got {len(operands)}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Use exactly the number of operands the operation expects
    operands = operands[:arity]

    # Convert operands first so that parse failures can be logged separately
    # from Calculator-level domain errors, without altering control flow.
    numeric_operands: list[int | float] = []
    for op_str in operands:
        try:
            numeric_operands.append(_to_number(op_str))
        except ValueError as exc:
            error_logger.log_invalid_operand(op_str, str(exc))
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    try:
        method = getattr(calc, operation_name)
        result = method(*numeric_operands)
    except ZeroDivisionError as exc:
        # numerator is the first operand when divide is called; use the
        # first numeric operand as context, falling back to "unknown".
        numerator = numeric_operands[0] if numeric_operands else float("nan")
        error_logger.log_division_by_zero(numerator)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        operand_ctx = numeric_operands[0] if numeric_operands else float("nan")
        error_logger.log_invalid_domain(operation_name, operand_ctx, str(exc))
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(result)
    sys.exit(0)


if __name__ == "__main__":
    main()
