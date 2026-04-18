"""Interaction layer — interactive mode.

Handles user prompts, menu display, input parsing, retry logic, history
recording, and error logging. Delegates all arithmetic to the Calculator
class via dispatch().
"""

from __future__ import annotations

from typing import Callable

from .calculator import Calculator
from .error_logger import (
    CALCULATION_ERROR,
    INVALID_INPUT,
    UNEXPECTED_ERROR,
    ErrorLogger,
)
from .history import OperationHistory
from .validation import validate_operation, validate_operand

# Maximum number of re-prompt attempts before the loop is terminated.
MAX_RETRY_ATTEMPTS: int = 3

# Maps string keys to (display_label, operand_count).
# operand_count == 1 for unary operations, 2 for binary operations,
# 0 for meta-commands such as "history".
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
    "history":     ("View operation history",         0),
}


def print_menu() -> None:
    """Print the operation menu to stdout."""
    print("\nAvailable operations:")
    for key, (label, _) in OPERATIONS.items():
        print(f"  {key:12s} - {label}")
    print("  exit         - Quit the calculator")


def print_history(history: OperationHistory) -> None:
    """Print all recorded history entries to stdout.

    If no operations have been recorded yet, prints an informational message
    instead.

    Args:
        history: The :class:`~src.history.OperationHistory` instance to read
            from.
    """
    entries = history.get_history()
    if not entries:
        print("No operations recorded in this session.")
    else:
        for entry in entries:
            print(entry)


def get_operation(
    input_fn: Callable[[str], str] = input,
    retry_limit: int = MAX_RETRY_ATTEMPTS,
) -> str | None:
    """Prompt the user to choose an operation, with bounded retry attempts.

    Args:
        input_fn: Callable used to read user input.  Defaults to the
            built-in ``input``.
        retry_limit: Maximum number of attempts before giving up.  Defaults
            to :data:`MAX_RETRY_ATTEMPTS`.

    Returns:
        The operation key string on success, ``None`` if the user typed
        "exit", or the sentinel string ``"__max_retries_exceeded__"`` when
        the user exhausts all allowed attempts without supplying a valid
        operation.
    """
    for attempt in range(1, retry_limit + 1):
        choice = input_fn("Enter operation: ").strip().lower()
        if choice == "exit":
            return None
        valid, error_msg = validate_operation(choice)
        if valid:
            return choice
        print(f"{error_msg}")
        print(f"Please try again. (Attempt {attempt} of {retry_limit})")

    print("Maximum retry attempts reached. Terminating session.")
    return "__max_retries_exceeded__"


def get_operands(
    count: int,
    input_fn: Callable[[str], str] = input,
    retry_limit: int = MAX_RETRY_ATTEMPTS,
) -> list[float] | None:
    """Prompt the user to enter ``count`` numeric operands, with bounded retries.

    Args:
        count: Number of operands to collect.
        input_fn: Callable used to read user input.  Defaults to the
            built-in ``input``.
        retry_limit: Maximum number of attempts per operand before giving up.
            Defaults to :data:`MAX_RETRY_ATTEMPTS`.

    Returns:
        A list of ``float`` values entered by the user on success, or ``None``
        if the retry limit was exceeded for any individual operand.
    """
    operands: list[float] = []
    for i in range(count):
        label = f"operand {i + 1}" if count > 1 else "operand"
        value: float | None = None
        for attempt in range(1, retry_limit + 1):
            raw = input_fn(f"Enter {label}: ").strip()
            valid, parsed, error_msg = validate_operand(raw)
            if valid:
                value = parsed
                break
            print(f"{error_msg}")
            print(f"Please enter a number. (Attempt {attempt} of {retry_limit})")
        if value is None:
            print(f"Maximum retry attempts reached for {label}. Returning to menu.")
            return None
        operands.append(value)
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


def _categorize_error(
    exc: Exception,
    operation: str,
    operands: list[float],
) -> tuple[str, dict]:  # type: ignore[type-arg]
    """Map an exception raised by dispatch to an error category and context.

    ``ValueError`` messages are inspected to choose the most specific
    category:

    * "division by zero" / "zero" in the message → :data:`CALCULATION_ERROR`
    * "invalid" in the message → :data:`INVALID_INPUT`
    * Any other ``ValueError`` → :data:`CALCULATION_ERROR`
    * Any other exception type → :data:`UNEXPECTED_ERROR`

    Args:
        exc: The caught exception.
        operation: The operation key that was being dispatched.
        operands: The list of operands passed to dispatch.

    Returns:
        A ``(category_string, context_dict)`` tuple where *context_dict*
        contains ``operation``, ``operands``, and ``error`` keys.
    """
    context: dict = {  # type: ignore[type-arg]
        "operation": operation,
        "operands": operands,
        "error": str(exc),
    }

    if isinstance(exc, ValueError):
        lower_msg = str(exc).lower()
        if "division by zero" in lower_msg or "zero" in lower_msg:
            return CALCULATION_ERROR, context
        if "invalid" in lower_msg:
            return INVALID_INPUT, context
        # Any other ValueError is still a calculation-level problem.
        return CALCULATION_ERROR, context

    return UNEXPECTED_ERROR, context


def run_loop(
    input_fn: Callable[[str], str] = input,
    history: OperationHistory | None = None,
) -> None:
    """Run the interactive calculator loop.

    Creates a single :class:`~src.calculator.Calculator` instance and
    repeatedly:

    1. Prints the operation menu.
    2. Reads and validates the user's operation choice.
    3. If the user typed "history", prints the session history and continues.
    4. Collects the required operands.
    5. Dispatches the calculation and prints the result.
    6. Records the successful result in *history*.

    The loop exits when the user types "exit".  :exc:`ValueError` raised by
    either operand parsing or the Calculator is caught at the loop level so
    the user is shown an error message and the loop continues.

    Args:
        input_fn: Callable used to read user input throughout the session.
            Defaults to the built-in ``input``.  Pass a custom callable in
            tests to avoid interactive I/O.
        history: :class:`~src.history.OperationHistory` instance used to
            record successful operations.  When ``None`` (the default) a new
            instance is created at the start of the loop.
    """
    calc = Calculator()
    if history is None:
        history = OperationHistory()
    error_logger = ErrorLogger()

    while True:
        print_menu()
        operation = get_operation(input_fn)

        if operation is None:
            print("Goodbye!")
            break

        if operation == "__max_retries_exceeded__":
            print("Session terminated due to too many invalid operation entries.")
            break

        if operation == "history":
            print_history(history)
            continue

        _, operand_count = OPERATIONS[operation]

        operands = get_operands(operand_count, input_fn)
        if operands is None:
            print("Returning to the main menu.")
            continue

        try:
            result = dispatch(operation, operands, calc)
            print(f"Result: {result}")
            history.record_operation(operation, operands, result)
        except ValueError as exc:
            category, context = _categorize_error(exc, operation, operands)
            error_logger.log_error(category, str(exc), context)
            print(f"Error: {exc}")
