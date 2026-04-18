"""Pure parsing logic for the calculator interface.

This module provides utilities to validate and parse user-supplied strings,
and maps operator symbols / function names to Calculator method names. It
contains no I/O, no class instantiation, and no side effects beyond error
logging.
"""

from src.logger import get_logger

BINARY_OPERATORS: dict[str, str] = {
    "+": "add",
    "-": "subtract",
    "*": "multiply",
    "/": "divide",
}

UNARY_FUNCTIONS: dict[str, str] = {
    "sin": "sin",
    "cos": "cos",
    "tan": "tan",
    "log": "log",
    "ln": "ln",
    "exp": "exp",
    "sqrt": "sqrt",
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
    logger = get_logger(__name__)
    try:
        return float(raw.strip())
    except ValueError:
        logger.error(f"parse_operand({raw!r}) failed: cannot convert to float")
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

    logger = get_logger(__name__)
    stripped_op = operator.strip()
    if stripped_op not in BINARY_OPERATORS:
        supported = ", ".join(repr(op) for op in BINARY_OPERATORS)
        logger.error(f"parse_input: unsupported operator {operator!r}")
        raise ValueError(
            f"Unsupported operator {operator!r}. Supported operators are: {supported}."
        )

    method_name = BINARY_OPERATORS[stripped_op]
    return a, b, method_name
