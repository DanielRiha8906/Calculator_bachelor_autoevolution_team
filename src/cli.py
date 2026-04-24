"""Command-line interface helpers for the interactive calculator.

Provides functions to prompt the user for operands and operator,
display results, and orchestrate a full calculation workflow.
"""

from .calculator import Calculator

OPERATIONS = {
    "+": (2, "add", "+", "Addition"),
    "-": (2, "subtract", "-", "Subtraction"),
    "*": (2, "multiply", "*", "Multiplication"),
    "/": (2, "divide", "/", "Division"),
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
