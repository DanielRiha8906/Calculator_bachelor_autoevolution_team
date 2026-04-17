"""CLI mode for the calculator.

This module provides argument parsing and expression evaluation for
non-interactive (command-line) invocations of the calculator.

Supports expressions supplied either as a single quoted string
(e.g. "3 + 4") or as separate arguments (e.g. 3 + 4).
"""

import sys

from src.input_handler import parse_input, run_calculation


def parse_cli_expression(expr: str) -> tuple[float, float, str]:
    """Parse a mathematical expression string into operands and operator.

    The expression must contain exactly three whitespace-separated tokens:
    a numeric operand, a binary operator symbol, and a second numeric operand
    (e.g. "3 + 4" or "10 / 2").  Parsing and validation are delegated to
    input_handler.parse_input so that operator support and error messages
    remain consistent with interactive mode.

    Args:
        expr: A string containing the full expression (e.g. "3 + 4").

    Returns:
        A tuple of (a, b, method_name) where a and b are floats and
        method_name is the corresponding Calculator method name.

    Raises:
        ValueError: If the expression does not have exactly three tokens,
            if either operand is non-numeric, or if the operator is
            not supported.
    """
    tokens = expr.split()
    if len(tokens) != 3:
        raise ValueError(
            f"Expression must contain exactly three tokens "
            f"(<operand> <operator> <operand>), got: {expr!r}"
        )
    operand_a, operator, operand_b = tokens
    return parse_input(operand_a, operand_b, operator)


def run_cli() -> None:
    """Main CLI entry point.

    Reads sys.argv to construct an expression string, delegates parsing to
    parse_cli_expression, evaluates the result via run_calculation, and
    prints it in the standard "Result: {result}" format.

    Accepts two calling conventions:
      - Single quoted argument: python -m src "3 + 4"
      - Separate arguments:     python -m src 3 + 4

    Exits with status 1 and a message on stderr on any input or arithmetic
    error.
    """
    # sys.argv[0] is the module/script name; arguments start at index 1.
    args = sys.argv[1:]

    # Normalise both calling conventions into a single expression string.
    expr = " ".join(args)

    try:
        a, b, method_name = parse_cli_expression(expr)
        result = run_calculation(a, b, method_name)
    except (ValueError, ZeroDivisionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Result: {result}")
