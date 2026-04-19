"""CLI argument parsing and operand conversion for the Calculator application.

This module contains the canonical implementations of CLI input parsing and
operand string conversion.  It has no dependency on UI output or session
concerns.
"""


def parse_cli_args(args: list[str]) -> tuple[str, list[str]]:
    """Parse CLI arguments into an operation name and operand strings.

    Args:
        args: A list of string arguments where the first element is the
            operation name and all remaining elements are operand strings.

    Returns:
        A 2-tuple of ``(operation_name, operand_strs)`` where
        *operation_name* is the first argument and *operand_strs* is the
        (possibly empty) list of remaining arguments.

    Examples:
        >>> parse_cli_args(["add", "3", "4"])
        ('add', ['3', '4'])
        >>> parse_cli_args(["factorial", "5"])
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
