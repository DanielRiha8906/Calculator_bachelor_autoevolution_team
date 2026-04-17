"""Input parsing and dispatch for the interactive calculator interface.

This module provides utilities to validate and parse user-supplied strings,
map operator symbols to Calculator method names, and execute calculations
through the Calculator class without using eval() or exec().
"""

from src.calculator import Calculator

BINARY_OPERATORS: dict[str, str] = {
    "+": "add",
    "-": "subtract",
    "*": "multiply",
    "/": "divide",
}


def parse_operand(raw: str) -> float:
    """Convert a raw string to a float operand.

    Args:
        raw: The user-supplied string to convert.

    Returns:
        The numeric value as a float.

    Raises:
        ValueError: If the string cannot be parsed as a float.
    """
    try:
        return float(raw.strip())
    except ValueError:
        raise ValueError(
            f"Invalid operand {raw!r}: expected a numeric value, e.g. '3' or '2.5'."
        )


def parse_input(
    operand_a: str, operand_b: str, operator: str
) -> tuple[float, float, str]:
    """Validate and parse both operands and the operator.

    Args:
        operand_a: Raw string for the first operand.
        operand_b: Raw string for the second operand.
        operator: Raw string for the operator symbol (e.g. '+', '-', '*', '/').

    Returns:
        A tuple of (a, b, method_name) where a and b are floats and
        method_name is the corresponding Calculator method name.

    Raises:
        ValueError: If either operand is non-numeric or the operator is
            not in BINARY_OPERATORS.
    """
    a = parse_operand(operand_a)
    b = parse_operand(operand_b)

    stripped_op = operator.strip()
    if stripped_op not in BINARY_OPERATORS:
        supported = ", ".join(repr(op) for op in BINARY_OPERATORS)
        raise ValueError(
            f"Unsupported operator {operator!r}. Supported operators are: {supported}."
        )

    method_name = BINARY_OPERATORS[stripped_op]
    return a, b, method_name


def run_calculation(a: float, b: float, method_name: str) -> float:
    """Instantiate a Calculator and dispatch the named method.

    Args:
        a: The first operand.
        b: The second operand.
        method_name: The Calculator method to call (e.g. 'add', 'divide').

    Returns:
        The result of the calculation as a float.

    Raises:
        ZeroDivisionError: Propagated from Calculator.divide when b is zero.
        ValueError: Propagated from Calculator when inputs are invalid.
    """
    calc = Calculator()
    return getattr(calc, method_name)(a, b)
