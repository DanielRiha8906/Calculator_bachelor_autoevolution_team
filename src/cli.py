"""Command-line interface for the calculator.

Parses infix arithmetic expressions supplied as CLI arguments, evaluates them
using the ``Calculator`` class, and writes results to stdout.  User input is
never passed to ``eval()``; a safe ``ast``-based traversal is used instead.

Supported operators: ``+``, ``-``, ``*``, ``/``, ``**`` (power).
Numbers may be integers or decimals (e.g. ``3``, ``3.14``).
Unary minus is supported (e.g. ``-5 + 2``).
"""

import ast
import sys

from src.calculator import Calculator


def _eval_node(node: ast.expr, calc: Calculator) -> int | float:
    """Recursively evaluate a single AST node using ``Calculator`` methods.

    Args:
        node: An ``ast.expr`` node produced by ``ast.parse``.
        calc: The ``Calculator`` instance used for arithmetic operations.

    Returns:
        The numeric result of the (sub-)expression.

    Raises:
        ValueError: If the expression contains unsupported syntax or operators.
        ZeroDivisionError: If a division by zero is attempted.
        TypeError: If operand types are incompatible with the requested operation.
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}.")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand, calc)
        if isinstance(node.op, ast.USub):
            return calc.multiply(operand, -1)
        if isinstance(node.op, ast.UAdd):
            return operand
        raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}.")

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, calc)
        right = _eval_node(node.right, calc)
        if isinstance(node.op, ast.Add):
            return calc.add(left, right)
        if isinstance(node.op, ast.Sub):
            return calc.subtract(left, right)
        if isinstance(node.op, ast.Mult):
            return calc.multiply(left, right)
        if isinstance(node.op, ast.Div):
            return calc.divide(left, right)
        if isinstance(node.op, ast.Pow):
            return calc.power(left, right)
        raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}.")

    raise ValueError(f"Unsupported expression node: {type(node).__name__}.")


def parse_and_evaluate(expression: str, calc: Calculator) -> int | float:
    """Parse and evaluate an infix arithmetic expression string.

    The expression is parsed with ``ast.parse`` in ``eval`` mode and then
    walked with ``_eval_node``.  No ``eval()`` call is used on the raw string.

    Supported operators: ``+``, ``-`` (binary and unary), ``*``, ``/``,
    ``**`` (exponentiation).

    Args:
        expression: A string containing an infix arithmetic expression,
            e.g. ``"5 + 3"``, ``"10 - 2 * 3"``, ``"2 ** 8"``.
        calc: A ``Calculator`` instance used to perform each arithmetic step.

    Returns:
        The numeric result of the expression as an ``int`` or ``float``.

    Raises:
        ValueError: If the expression is syntactically invalid or contains
            unsupported operations.
        ZeroDivisionError: If any division by zero occurs during evaluation.
        TypeError: If operand types are incompatible with the Calculator method.
    """
    expression = expression.strip()
    if not expression:
        raise ValueError("Expression must not be empty.")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression syntax: {exc}") from exc

    return _eval_node(tree.body, calc)


def run_cli(args: list[str]) -> int:
    """Main entry point for CLI mode.

    Joins *args* with spaces to form an expression, evaluates it, and prints
    the result to stdout.  All errors are printed to stderr.

    Args:
        args: The command-line arguments after the script name (i.e.
            ``sys.argv[1:]``).

    Returns:
        ``0`` on success, ``1`` on any error (missing args, parse failure,
        arithmetic error, etc.).
    """
    if not args:
        print("Error: No expression provided. Usage: calculator <expression>", file=sys.stderr)
        return 1

    expression = " ".join(args)
    calc = Calculator()

    try:
        result = parse_and_evaluate(expression, calc)
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except TypeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0
