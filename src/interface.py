"""User interface layer for the interactive calculator.

Consolidates all CLI interaction logic: prompting, displaying results,
formatting history, persisting history, and orchestrating a full
calculation workflow.  Mathematical operations are never performed here —
they are always delegated to :class:`~src.calculator.Calculator` methods.
"""

from .calculator_core import Calculator


class MaxRetriesExceeded(Exception):
    """Raised when user exhausts maximum retry attempts for a single input field."""
    pass


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

SCIENTIFIC_OPERATIONS = {
    "sin": (1, "sin", "sin", "Sine (radians)"),
    "cos": (1, "cos", "cos", "Cosine (radians)"),
    "tan": (1, "tan", "tan", "Tangent (radians)"),
    "asin": (1, "asin", "asin", "Arc sine"),
    "acos": (1, "acos", "acos", "Arc cosine"),
    "atan": (1, "atan", "atan", "Arc tangent"),
    "sinh": (1, "sinh", "sinh", "Hyperbolic sine"),
    "cosh": (1, "cosh", "cosh", "Hyperbolic cosine"),
    "tanh": (1, "tanh", "tanh", "Hyperbolic tangent"),
    "exp": (1, "exp", "exp", "Exponential (e^x)"),
    "pi": (0, "get_pi", "pi", "Pi constant"),
    "e": (0, "get_e", "e", "Euler's number"),
}


def _get_operation_arity(operation_key: str) -> int:
    """Return the arity (1 or 2) for the given operation key.

    Args:
        operation_key: A key from the OPERATIONS dict.

    Returns:
        The number of operands the operation requires.
    """
    return OPERATIONS[operation_key][0]


def _get_calculator_method(operation_key: str) -> str:
    """Return the Calculator method name for the given operation key.

    Args:
        operation_key: A key from the OPERATIONS dict.

    Returns:
        The Calculator method name as a string.
    """
    return OPERATIONS[operation_key][1]


def _get_display_symbol(operation_key: str) -> str:
    """Return the display symbol for the given operation key.

    Args:
        operation_key: A key from the OPERATIONS or SCIENTIFIC_OPERATIONS dict.

    Returns:
        The symbol string used when displaying results.
    """
    if operation_key in OPERATIONS:
        return OPERATIONS[operation_key][2]
    return SCIENTIFIC_OPERATIONS[operation_key][2]


def prompt_for_first_number(max_retries: int = 3) -> float:
    """Prompt the user for the first operand, re-prompting on invalid input.

    Args:
        max_retries: Maximum number of invalid attempts before raising
            MaxRetriesExceeded. Defaults to 3.

    Returns:
        The first operand as a float.

    Raises:
        MaxRetriesExceeded: If the user exhausts all retry attempts.
    """
    attempts = 0
    while True:
        raw = input("Enter the first number: ")
        try:
            return float(raw)
        except ValueError:
            attempts += 1
            print(
                f"Invalid input. Please enter a numeric value. "
                f"(Attempt {attempts}/{max_retries})"
            )
            if attempts > max_retries:
                raise MaxRetriesExceeded(
                    "Maximum retry attempts exceeded for first number input."
                )


def prompt_for_operator(max_retries: int = 3, mode: str = "normal") -> str:
    """Prompt the user for an operation, re-prompting on invalid input.

    Valid operations include: +, -, *, /, square, cube, sqrt, cbrt,
    factorial, power, log, ln.  When mode is 'scientific', additional
    scientific operations (sin, cos, tan, etc.) are also accepted.

    The user may also enter 'quit' or 'exit' (case-insensitive) to signal
    they want to stop; in that case the sentinel string "QUIT" is returned.
    The user may enter 'mode' or 'sci' (case-insensitive) to request a mode
    toggle; in that case the sentinel string "MODE_TOGGLE" is returned.

    Args:
        max_retries: Maximum number of invalid attempts before raising
            MaxRetriesExceeded. Defaults to 3.
        mode: Current calculator mode, either "normal" or "scientific".
            Defaults to "normal".

    Returns:
        The operation key as a string, "QUIT" if the user requested exit,
        or "MODE_TOGGLE" if the user requested a mode change.

    Raises:
        MaxRetriesExceeded: If the user exhausts all retry attempts.
    """
    if mode == "scientific":
        valid_ops_dict = {**OPERATIONS, **SCIENTIFIC_OPERATIONS}
    else:
        valid_ops_dict = OPERATIONS

    valid_ops = list(valid_ops_dict.keys())
    attempts = 0
    while True:
        raw = input(
            "Enter an operator or operation (+, -, *, /, square, cube, sqrt, cbrt, "
            "factorial, power, log, ln): "
        )
        if raw.lower() in ("quit", "exit"):
            return "QUIT"
        if raw.lower() in ("mode", "sci"):
            return "MODE_TOGGLE"
        if raw in valid_ops_dict:
            return raw
        attempts += 1
        print(
            f"Invalid operator '{raw}'. Please enter one of: {', '.join(valid_ops)}. "
            f"(Attempt {attempts}/{max_retries})"
        )
        if attempts > max_retries:
            raise MaxRetriesExceeded(
                "Maximum retry attempts exceeded for operator input."
            )


def prompt_for_second_number(max_retries: int = 3) -> float:
    """Prompt the user for the second operand, re-prompting on invalid input.

    Args:
        max_retries: Maximum number of invalid attempts before raising
            MaxRetriesExceeded. Defaults to 3.

    Returns:
        The second operand as a float.

    Raises:
        MaxRetriesExceeded: If the user exhausts all retry attempts.
    """
    attempts = 0
    while True:
        raw = input("Enter the second number: ")
        try:
            return float(raw)
        except ValueError:
            attempts += 1
            print(
                f"Invalid input. Please enter a numeric value. "
                f"(Attempt {attempts}/{max_retries})"
            )
            if attempts > max_retries:
                raise MaxRetriesExceeded(
                    "Maximum retry attempts exceeded for second number input."
                )


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
    """Print the result of a unary operation in user-friendly format.

    Args:
        operation_key: A key from the OPERATIONS dict.
        operand: The single operand value.
        result: The computed result.
    """
    symbol = _get_display_symbol(operation_key)
    print(f"{symbol}({operand}) = {result}")


def display_result_binary(operation_key: str, first: float, second: float, result: float) -> None:
    """Print the result of a binary operation in user-friendly format.

    Args:
        operation_key: A key from the OPERATIONS dict.
        first: The first operand.
        second: The second operand.
        result: The computed result.
    """
    symbol = _get_display_symbol(operation_key)
    print(f"{first} {symbol} {second} = {result}")


def _format_history_entry(index: int, entry: dict) -> str:
    """Format a single history entry for display.

    Args:
        index: 1-based position of the entry in the history list.
        entry: A dict with keys 'operation', 'operands', and 'result'.

    Returns:
        A formatted string representation of the history entry.
    """
    operation = entry["operation"]
    operands = entry["operands"]
    result = entry["result"]
    if len(operands) == 1:
        return f"{index}. {operation}({operands[0]}) = {result}"
    else:
        return f"{index}. {operation}({operands[0]}, {operands[1]}) = {result}"


def display_history(calc: "Calculator") -> None:
    """Print the full operation history of a Calculator instance.

    If no operations have been recorded, prints 'No operations recorded.'
    Otherwise prints one numbered line per recorded operation.

    Args:
        calc: A Calculator instance with a get_history() method.
    """
    history = calc.get_history()
    if not history:
        print("No operations recorded.")
        return
    for index, entry in enumerate(history, start=1):
        formatted = _format_history_entry(index, entry)
        print(formatted)


def display_error(error_message: str) -> None:
    """Print an error message in a user-friendly format.

    Args:
        error_message: The error description to display.
    """
    print(f"Error: {error_message}")


def display_mode_change(new_mode: str) -> None:
    """Print a user-friendly message indicating a mode change.

    Args:
        new_mode: The name of the new mode (e.g. "scientific" or "normal").
    """
    print(f"Switched to {new_mode} mode.")


def persist_history_to_file(calc: Calculator, filepath: str = "history.txt") -> None:
    """Write accumulated history from a Calculator instance to a disk file.

    Opens the file in append mode (creating it if it does not exist) and writes
    one formatted line per history entry using _format_history_entry().

    Args:
        calc: A Calculator instance whose history should be persisted.
        filepath: Path to the file to append history to. Defaults to "history.txt".
    """
    try:
        history = calc.get_history()
        with open(filepath, "a") as f:
            for index, entry in enumerate(history, start=1):
                line = _format_history_entry(index, entry)
                f.write(line + "\n")
    except (ValueError, IOError, OSError) as e:
        print(f"Warning: Could not save history to '{filepath}': {e}")


def display_history_notification(filepath: str = "history.txt") -> None:
    """Print a user-friendly message about the history feature.

    Args:
        filepath: The path where history is saved. Defaults to "history.txt".
    """
    print(
        f"History saved to {filepath}. "
        f"View your history with: python -m calculator history"
    )


def run_calculator(
    calc: "Calculator | None" = None,
    max_retries: int = 3,
    mode: str = "normal",
) -> "float | str":
    """Run a single interactive calculation and return the result.

    Prompts the user for an operation and required operand(s), performs the
    calculation using Calculator, displays the result, and returns it.

    Supports arity-0 (constants: pi, e), arity-1 (unary: square, sqrt, sin,
    etc.), and arity-2 (binary: +, power, etc.) operations.

    If the user enters 'quit' or 'exit' at the operator prompt, returns the
    sentinel string "QUIT" so the caller can break an interactive loop.

    If the user enters 'mode' or 'sci' at the operator prompt, returns the
    sentinel string "MODE_TOGGLE" so the caller can switch modes.

    Args:
        calc: An optional Calculator instance to reuse. If None, a new instance
            is created. Passing an existing instance allows history to accumulate
            across multiple calls. Defaults to None.
        max_retries: Maximum number of invalid attempts for each prompt before
            raising MaxRetriesExceeded. Defaults to 3.
        mode: Current calculator mode, either "normal" or "scientific".
            Controls which operations are offered to the user. Defaults to "normal".

    Returns:
        The numeric result of the calculation as a float, the string "QUIT"
        if the user requested to exit, or the string "MODE_TOGGLE" if the user
        requested a mode change.

    Raises:
        MaxRetriesExceeded: If the user exhausts retry attempts on any prompt.
        ValueError: If a domain error occurs (e.g., sqrt of negative).
        ZeroDivisionError: If division by zero is attempted.
    """
    if calc is None:
        calc = Calculator()

    operation_key = prompt_for_operator(max_retries=max_retries, mode=mode)
    if operation_key == "QUIT":
        return "QUIT"
    if operation_key == "MODE_TOGGLE":
        return "MODE_TOGGLE"

    # Determine arity and method from whichever registry the key belongs to.
    if mode == "scientific" and operation_key in SCIENTIFIC_OPERATIONS:
        op_tuple = SCIENTIFIC_OPERATIONS[operation_key]
    else:
        op_tuple = OPERATIONS[operation_key]

    arity = op_tuple[0]
    method_name = op_tuple[1]
    method = getattr(calc, method_name)

    try:
        if arity == 0:
            result = method()
            print(f"{operation_key} = {result}")
        elif arity == 1:
            operand = prompt_for_first_number(max_retries=max_retries)
            result = method(operand)
            display_result_unary(operation_key, operand, result)
        else:
            first = prompt_for_first_number(max_retries=max_retries)
            second = prompt_for_second_number(max_retries=max_retries)
            result = method(first, second)
            display_result_binary(operation_key, first, second, result)

        display_history_notification()
        return result
    except (ValueError, ZeroDivisionError) as e:
        display_error(str(e))
        raise
