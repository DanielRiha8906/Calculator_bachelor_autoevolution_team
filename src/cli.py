"""Command-line interface helpers for the interactive calculator.

Provides functions to prompt the user for operands and operator,
display results, and orchestrate a full calculation workflow.
"""

import sys
from .calculator import Calculator

OPERATIONS = {
    "+": (2, "add", "+", "Addition"),
    "-": (2, "subtract", "-", "Subtraction"),
    "*": (2, "multiply", "*", "Multiplication"),
    "/": (2, "divide", "/", "Division"),
    "add": (2, "add", "+", "Addition"),
    "subtract": (2, "subtract", "-", "Subtraction"),
    "multiply": (2, "multiply", "*", "Multiplication"),
    "divide": (2, "divide", "/", "Division"),
    "square": (1, "square", "square", "Square (x^2)"),
    "cube": (1, "cube", "cube", "Cube (x^3)"),
    "sqrt": (1, "square_root", "sqrt", "Square root"),
    "cbrt": (1, "cube_root", "cbrt", "Cube root"),
    "factorial": (1, "factorial", "factorial", "Factorial"),
    "power": (2, "power", "^", "Power (x^y)"),
    "log": (1, "log", "log", "Base-10 logarithm"),
    "ln": (1, "ln", "ln", "Natural logarithm"),
}


def _get_operation_arity(operation_key: str) -> int:
    return OPERATIONS[operation_key][0]


def _get_calculator_method(operation_key: str) -> str:
    return OPERATIONS[operation_key][1]


def _get_display_symbol(operation_key: str) -> str:
    return OPERATIONS[operation_key][2]


def prompt_for_first_number() -> float:
    """Prompt the user for the first operand, re-prompting on invalid input.

    Returns:
        The first operand as a float.
    """
    while True:
        raw = input("Enter the first number: ")
        try:
            return float(raw)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def prompt_for_operator() -> str:
    """Prompt the user for an operation, re-prompting on invalid input.

    Valid operations include: +, -, *, /, square, cube, sqrt, cbrt,
    factorial, power, log, ln

    Returns:
        The operation key as a string.
    """
    valid_ops = list(OPERATIONS.keys())
    while True:
        raw = input(
            "Enter an operator or operation (+, -, *, /, square, cube, sqrt, cbrt, "
            "factorial, power, log, ln): "
        )
        if raw in OPERATIONS:
            return raw
        print(f"Invalid operator '{raw}'. Please enter one of: {', '.join(valid_ops)}")


def prompt_for_second_number() -> float:
    """Prompt the user for the second operand, re-prompting on invalid input.

    Returns:
        The second operand as a float.
    """
    while True:
        raw = input("Enter the second number: ")
        try:
            return float(raw)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def display_result(first: float, operator: str, second: float, result: float) -> None:
    """Print the calculation result in a user-friendly format.

    Args:
        first: The first operand.
        operator: The arithmetic operator used.
        second: The second operand.
        result: The computed result.
    """
    print(f"{first} {operator} {second} = {result}")


def display_result_unary(operation_key: str, operand: float, result: float) -> None:
    """Print the result of a unary operation in user-friendly format."""
    symbol = _get_display_symbol(operation_key)
    print(f"{symbol}({operand}) = {result}")


def display_result_binary(operation_key: str, first: float, second: float, result: float) -> None:
    """Print the result of a binary operation in user-friendly format."""
    symbol = _get_display_symbol(operation_key)
    print(f"{first} {symbol} {second} = {result}")


def display_error(error_message: str) -> None:
    """Print an error message in a user-friendly format.

    Args:
        error_message: The error description to display.
    """
    print(f"Error: {error_message}")


def run_calculator() -> float:
    """Run a single interactive calculation and return the result.

    Prompts the user for an operation and required operand(s), performs the
    calculation using Calculator, displays the result, and returns it.

    Supports both unary operations (e.g., square, sqrt) and binary operations
    (e.g., +, power).

    Returns:
        The numeric result of the calculation.

    Raises:
        ValueError: If a domain error occurs (e.g., sqrt of negative).
        ZeroDivisionError: If division by zero is attempted.
    """
    calc = Calculator()

    operation_key = prompt_for_operator()
    arity = _get_operation_arity(operation_key)
    method_name = _get_calculator_method(operation_key)
    method = getattr(calc, method_name)

    try:
        if arity == 1:
            operand = prompt_for_first_number()
            result = method(operand)
            display_result_unary(operation_key, operand, result)
        else:
            first = prompt_for_first_number()
            second = prompt_for_second_number()
            result = method(first, second)
            display_result_binary(operation_key, first, second, result)

        return result
    except (ValueError, ZeroDivisionError) as e:
        display_error(str(e))
        raise


_USAGE = (
    "Usage: calculator <operation> [operand1] [operand2]\n"
    "\n"
    "Binary operations (require two operands):\n"
    "  add, +           Addition\n"
    "  subtract, -      Subtraction\n"
    "  multiply, *      Multiplication\n"
    "  divide, /        Division\n"
    "  power            Power (x^y)\n"
    "\n"
    "Unary operations (require one operand):\n"
    "  square           Square (x^2)\n"
    "  cube             Cube (x^3)\n"
    "  sqrt             Square root\n"
    "  cbrt             Cube root\n"
    "  factorial        Factorial\n"
    "  log              Base-10 logarithm\n"
    "  ln               Natural logarithm\n"
)


def main_cli_noninteractive(args: list[str]) -> int:
    """Non-interactive CLI mode: parse arguments and perform calculation.

    Takes a list of command-line arguments (operation and operands) and
    performs the calculation without prompting the user.

    Args:
        args: List of command-line arguments [operation, operand(s)]
              For unary ops: [operation, operand]
              For binary ops: [operation, operand1, operand2]
              Special: [--help] or [-h] for help

    Returns:
        Exit code (0 for success, 1 for error)
    """
    if not args:
        print("Error: No operation specified.", file=sys.stderr)
        print(_USAGE, file=sys.stderr)
        return 1

    operation_name = args[0]

    if operation_name in ("--help", "-h"):
        print(_USAGE)
        return 0

    if operation_name not in OPERATIONS:
        print(
            f"Error: Unknown operation '{operation_name}'. "
            f"Valid operations: {', '.join(OPERATIONS.keys())}",
            file=sys.stderr,
        )
        return 1

    arity, method_name, _symbol, _description = OPERATIONS[operation_name]
    operand_args = args[1:]

    if arity == 1 and len(operand_args) != 1:
        print(
            f"Error: Operation '{operation_name}' requires exactly 1 operand, "
            f"got {len(operand_args)}.",
            file=sys.stderr,
        )
        return 1

    if arity == 2 and len(operand_args) != 2:
        print(
            f"Error: Operation '{operation_name}' requires exactly 2 operands, "
            f"got {len(operand_args)}.",
            file=sys.stderr,
        )
        return 1

    try:
        operands = [float(o) for o in operand_args]
    except ValueError as exc:
        print(f"Error: Invalid operand — {exc}", file=sys.stderr)
        return 1

    calc = Calculator()
    method = getattr(calc, method_name)

    try:
        result = method(*operands)
    except ZeroDivisionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except TypeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0
