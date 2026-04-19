"""Interactive user input handler for the calculator.

Provides prompt-based input parsing, operation dispatch, and a top-level
interactive loop that drives the Calculator through user-supplied commands.
"""

from src.calculator import Calculator


class InvalidInputError(Exception):
    """Raised when user-supplied input cannot be parsed as a valid number."""


# Maps operation names to (Calculator method name, number of operands).
OPERATIONS: dict[str, tuple[str, int]] = {
    "add": ("add", 2),
    "subtract": ("subtract", 2),
    "multiply": ("multiply", 2),
    "divide": ("divide", 2),
    "factorial": ("factorial", 1),
    "square": ("square", 1),
    "cube": ("cube", 1),
    "square_root": ("square_root", 1),
    "cube_root": ("cube_root", 1),
    "power": ("power", 2),
    "log10": ("log10", 1),
    "natural_log": ("natural_log", 1),
}


def parse_number(input_str: str) -> int | float:
    """Convert a string to an int or float.

    Attempts int conversion first; falls back to float. Raises
    ``InvalidInputError`` if neither conversion succeeds.

    Args:
        input_str: The raw string supplied by the user.

    Returns:
        The parsed numeric value as an ``int`` or ``float``.

    Raises:
        InvalidInputError: If ``input_str`` cannot be parsed as a number.
    """
    stripped = input_str.strip()
    try:
        return int(stripped)
    except ValueError:
        pass
    try:
        return float(stripped)
    except ValueError:
        raise InvalidInputError(
            f"Invalid number: '{input_str}'. Please enter an integer or decimal value."
        )


def get_operands(operation: str) -> list[int | float]:
    """Prompt the user for the operands required by *operation*.

    The number of operands is determined by ``OPERATIONS``. Each prompt
    re-tries until a valid number is entered.

    Args:
        operation: A key present in ``OPERATIONS``.

    Returns:
        A list of parsed numeric operands in input order.
    """
    _, operand_count = OPERATIONS[operation]
    operands: list[int | float] = []
    for i in range(operand_count):
        label = f"operand {i + 1}" if operand_count > 1 else "operand"
        while True:
            raw = input(f"  Enter {label}: ")
            try:
                operands.append(parse_number(raw))
                break
            except InvalidInputError as exc:
                print(f"  Error: {exc}")
    return operands


def execute_operation(calc: Calculator, operation: str, operands: list) -> object:
    """Invoke the appropriate Calculator method and return the result.

    Catches ``TypeError``, ``ValueError``, and ``ZeroDivisionError`` raised by
    the Calculator and converts them into user-friendly error strings so that
    callers receive a plain message rather than a traceback.

    Args:
        calc: A ``Calculator`` instance to dispatch on.
        operation: A key present in ``OPERATIONS``.
        operands: The list of numeric operands to pass to the method.

    Returns:
        The numeric result of the operation, or a human-readable error string
        if the Calculator raises a handled exception.
    """
    method_name, _ = OPERATIONS[operation]
    method = getattr(calc, method_name)
    try:
        return method(*operands)
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except ValueError as exc:
        return f"Error: {exc}"
    except TypeError as exc:
        return f"Error: {exc}"


def format_result(result: object) -> str:
    """Format a calculation result as a human-readable string.

    Args:
        result: The value returned by ``execute_operation``.

    Returns:
        A string representation of *result*.
    """
    return str(result)


def run_interactive() -> None:
    """Run the interactive calculator loop.

    Displays the list of available operations, prompts the user for a
    selection, collects operands, executes the operation, and prints the
    result. The loop continues until the user enters ``quit`` or ``exit``,
    at which point "Bye!" is printed and the function returns.
    """
    calc = Calculator()
    operation_list = list(OPERATIONS.keys())

    print("Calculator — available operations:")
    for idx, name in enumerate(operation_list, start=1):
        print(f"  {idx:2}. {name}")
    print("  Type 'quit' or 'exit' to leave.\n")

    while True:
        raw = input("Select operation: ").strip().lower()

        if raw in ("quit", "exit"):
            print("Bye!")
            return

        if raw not in OPERATIONS:
            print(
                f"  Unknown operation '{raw}'. "
                "Please choose from the list above or type 'quit'.\n"
            )
            continue

        operands = get_operands(raw)
        result = execute_operation(calc, raw, operands)
        print(f"  Result: {format_result(result)}\n")
