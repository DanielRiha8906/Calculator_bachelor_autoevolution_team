"""Command-line interface helpers for the interactive calculator.

Provides functions to prompt the user for operands and operator,
display results, and orchestrate a full calculation workflow.
"""

from .calculator import Calculator

SUPPORTED_OPERATORS = {"+", "-", "*", "/"}


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
    """Prompt the user for an arithmetic operator, re-prompting on invalid input.

    Valid operators are: +, -, *, /

    Returns:
        The operator as a string.
    """
    while True:
        raw = input("Enter an operator (+, -, *, /): ")
        if raw in SUPPORTED_OPERATORS:
            return raw
        print(f"Invalid operator '{raw}'. Please enter one of: +, -, *, /")


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


def display_error(error_message: str) -> None:
    """Print an error message in a user-friendly format.

    Args:
        error_message: The error description to display.
    """
    print(f"Error: {error_message}")


def run_calculator() -> float:
    """Run a single interactive calculation and return the result.

    Prompts the user for two operands and an operator, performs the
    calculation using Calculator, displays the result, and returns it.

    Returns:
        The numeric result of the calculation.

    Raises:
        ZeroDivisionError: If division by zero is attempted and not caught
            internally.
    """
    calc = Calculator()

    first = prompt_for_first_number()
    operator = prompt_for_operator()
    second = prompt_for_second_number()

    if operator == "+":
        result = calc.add(first, second)
    elif operator == "-":
        result = calc.subtract(first, second)
    elif operator == "*":
        result = calc.multiply(first, second)
    else:
        result = calc.divide(first, second)

    display_result(first, operator, second, result)
    return result
