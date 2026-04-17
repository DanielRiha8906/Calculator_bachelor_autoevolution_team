"""Interactive input loop for the calculator.

Provides a menu-driven REPL that reads operations and operands from the user,
dispatches them to a Calculator instance, and prints the result.  The loop
runs until the user types "exit".
"""

from __future__ import annotations

from typing import Callable

from .calculator import Calculator
from .retry_logic import retry_get_operands, retry_get_operation

# Maps string keys to (display_label, operand_count).
# operand_count == 1 for unary operations, 2 for binary operations.
OPERATIONS: dict[str, tuple[str, int]] = {
    "add":         ("Add (a + b)",                    2),
    "subtract":    ("Subtract (a - b)",               2),
    "multiply":    ("Multiply (a * b)",               2),
    "divide":      ("Divide (a / b)",                 2),
    "power":       ("Power (base ^ exponent)",        2),
    "factorial":   ("Factorial (n!)",                 1),
    "square":      ("Square (x^2)",                   1),
    "cube":        ("Cube (x^3)",                     1),
    "square_root": ("Square root (√x)",               1),
    "cube_root":   ("Cube root (∛x)",                 1),
    "log":         ("Log base-10 (log₁₀ x)",          1),
    "ln":          ("Natural logarithm (ln x)",       1),
}


def print_menu() -> None:
    """Print the operation menu to stdout."""
    print("\nAvailable operations:")
    for key, (label, _) in OPERATIONS.items():
        print(f"  {key:12s} - {label}")
    print("  exit         - Quit the calculator")


def get_operation(input_fn: Callable[[str], str] = input) -> str | None:
    """Prompt the user to choose an operation.

    Args:
        input_fn: Callable used to read user input.  Defaults to the
            built-in ``input``.

    Returns:
        The operation key string if valid, or ``None`` if the user typed
        "exit".  If the input is unrecognised the function prints an error
        message and returns the sentinel string ``"__invalid__"``.
    """
    choice = input_fn("Enter operation: ").strip().lower()
    if choice == "exit":
        return None
    if choice in OPERATIONS:
        return choice
    print(f"Unknown operation: '{choice}'. Type a valid operation key or 'exit'.")
    return "__invalid__"


def get_operands(count: int, input_fn: Callable[[str], str] = input) -> list[float]:
    """Prompt the user to enter ``count`` numeric operands.

    Args:
        count: Number of operands to collect.
        input_fn: Callable used to read user input.  Defaults to the
            built-in ``input``.

    Returns:
        A list of ``float`` values entered by the user.

    Raises:
        ValueError: If any entered value cannot be converted to float.
    """
    operands: list[float] = []
    for i in range(count):
        label = f"operand {i + 1}" if count > 1 else "operand"
        raw = input_fn(f"Enter {label}: ").strip()
        operands.append(float(raw))
    return operands


def dispatch(operation: str, operands: list[float], calc: Calculator) -> float:
    """Call the appropriate Calculator method for the given operation.

    Args:
        operation: A key from :data:`OPERATIONS`.
        operands: List of float operands (length must match operand_count
            recorded in :data:`OPERATIONS`).
        calc: The :class:`~src.calculator.Calculator` instance to use.

    Returns:
        The numeric result of the operation.

    Raises:
        ValueError: Propagated from the Calculator method on invalid input
            (e.g. division by zero, square root of negative number).
        KeyError: If *operation* is not in :data:`OPERATIONS`.
    """
    if operation == "add":
        return calc.add(operands[0], operands[1])
    if operation == "subtract":
        return calc.subtract(operands[0], operands[1])
    if operation == "multiply":
        return calc.multiply(operands[0], operands[1])
    if operation == "divide":
        return calc.divide(operands[0], operands[1])
    if operation == "power":
        return calc.power(operands[0], operands[1])
    if operation == "factorial":
        return float(calc.factorial(int(operands[0])))
    if operation == "square":
        return calc.square(operands[0])
    if operation == "cube":
        return calc.cube(operands[0])
    if operation == "square_root":
        return calc.square_root(operands[0])
    if operation == "cube_root":
        return calc.cube_root(operands[0])
    if operation == "log":
        return calc.log(operands[0])
    if operation == "ln":
        return calc.ln(operands[0])
    raise KeyError(f"Unknown operation: '{operation}'")


def run_loop(input_fn: Callable[[str], str] = input) -> None:
    """Run the interactive calculator loop with retry logic.

    Creates a single :class:`~src.calculator.Calculator` instance and
    repeatedly:

    1. Prints the operation menu.
    2. Reads and validates the user's operation choice via
       :func:`~src.retry_logic.retry_get_operation` (up to
       :data:`~src.retry_logic.MAX_RETRIES` attempts).
    3. Collects the required operands via
       :func:`~src.retry_logic.retry_get_operands` (up to
       :data:`~src.retry_logic.MAX_RETRIES` attempts).
    4. Dispatches the calculation and prints the result.

    The loop exits when the user types ``"exit"``.  If the operation prompt
    exhausts its retry count within a single menu cycle the warning
    ``"Too many failed attempts. Please try again."`` is printed and the loop
    returns to the top of the menu without terminating the session.
    :exc:`ValueError` raised during operand parsing or by the Calculator (e.g.
    division by zero) is caught at the loop level so the user is shown an error
    message and the loop continues from the top.

    Args:
        input_fn: Callable used to read user input throughout the session.
            Defaults to the built-in ``input``.  Pass a custom callable in
            tests to avoid interactive I/O.
    """
    calc = Calculator()

    while True:
        print_menu()
        operation = retry_get_operation(input_fn, _get_operation_fn=get_operation)

        if operation is None:
            # User typed "exit".
            print("Goodbye!")
            break

        if operation == "__exhausted__":
            # Max retries exceeded for the operation prompt; warn and loop back
            # to the menu so the user can try again in the next cycle.
            print("Too many failed attempts. Please try again.")
            continue

        _, operand_count = OPERATIONS[operation]

        try:
            operands = retry_get_operands(operand_count, input_fn, _get_operands_fn=get_operands)
            result = dispatch(operation, operands, calc)
            print(f"Result: {result}")
        except ValueError as exc:
            print(f"Error: {exc}")
