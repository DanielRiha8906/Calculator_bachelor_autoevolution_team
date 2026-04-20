"""Interactive user input handler for the calculator.

Provides prompt-based input parsing, operation dispatch, and a top-level
interactive loop that drives the Calculator through user-supplied commands.
"""

import logging

from src.logic import Calculator
from src.input_retry import DEFAULT_MAX_RETRIES

logger = logging.getLogger("calculator")

MAX_RETRIES: int = DEFAULT_MAX_RETRIES


class InvalidInputError(Exception):
    """Raised when user-supplied input cannot be parsed as a valid number."""


class OperandRetryExceeded(Exception):
    """Raised when the user fails to supply a valid operand within MAX_RETRIES attempts."""


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
    "sin": ("sin", 1),
    "cos": ("cos", 1),
    "tan": ("tan", 1),
    "exp": ("exp", 1),
}

# Names of operations that are only available in scientific mode.
SCIENTIFIC_OPERATIONS: frozenset[str] = frozenset({"sin", "cos", "tan", "exp"})


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
        logger.error(
            f"parse_number: could not parse '{input_str}' as a number; InvalidInputError"
        )
        raise InvalidInputError(
            f"Invalid number: '{input_str}'. Please enter an integer or decimal value."
        )


def get_operands(operation: str) -> list[int | float]:
    """Prompt the user for the operands required by *operation*.

    The number of operands is determined by ``OPERATIONS``.  Each operand is
    retried up to ``MAX_RETRIES`` times.  If the user fails to supply a valid
    number within the allowed attempts for any single operand,
    ``OperandRetryExceeded`` is raised so the caller can return to operation
    selection.

    Args:
        operation: A key present in ``OPERATIONS``.

    Returns:
        A list of parsed numeric operands in input order.

    Raises:
        OperandRetryExceeded: If the user exhausts all retry attempts for any
            single operand.
    """
    _, operand_count = OPERATIONS[operation]
    operands: list[int | float] = []
    for i in range(operand_count):
        label = f"operand {i + 1}" if operand_count > 1 else "operand"
        attempt = 0
        while True:
            attempt += 1
            raw = input(f"  Enter {label}: ")
            try:
                operands.append(parse_number(raw))
                break
            except InvalidInputError as exc:
                print(f"  Error: {exc}")
                if attempt >= MAX_RETRIES:
                    print(
                        "  Too many invalid inputs. Returning to operation selection."
                    )
                    raise OperandRetryExceeded(
                        f"Exceeded {MAX_RETRIES} attempts for {label}."
                    )
                print(f"  Invalid input. Attempt {attempt} of {MAX_RETRIES}.")
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
        logger.error(
            f"execute_operation: {operation} with operands {operands} failed; ZeroDivisionError"
        )
        return "Error: Division by zero is not allowed."
    except ValueError as exc:
        logger.error(
            f"execute_operation: {operation} with operands {operands} failed; {exc}"
        )
        return f"Error: {exc}"
    except TypeError as exc:
        logger.error(
            f"execute_operation: {operation} with operands {operands} failed; {exc}"
        )
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

    Mode switching is supported via ``mode scientific`` and ``mode normal``
    commands entered at the operation selection prompt.  Scientific operations
    (sin, cos, tan, exp) are only executable when the calculator is in
    scientific mode.
    """
    calc = Calculator()
    operation_list = list(OPERATIONS.keys())

    print("Calculator — available operations:")
    for idx, name in enumerate(operation_list, start=1):
        print(f"  {idx:2}. {name}")
    print("  Type 'mode scientific' or 'mode normal' to switch mode.")
    print("  Type 'quit' or 'exit' to leave.\n")

    op_attempt = 0
    while True:
        mode_label = "[Scientific Mode]" if calc.is_scientific_mode() else "[Normal Mode]"
        raw = input(f"Select operation {mode_label}: ").strip().lower()

        if raw in ("quit", "exit"):
            print("Bye!")
            return

        # Handle mode switching commands.
        if raw in ("mode scientific", "mode normal"):
            new_mode = raw.split()[1]
            calc.set_mode(new_mode)
            print(f"Mode set to {new_mode}.")
            op_attempt = 0
            continue

        if raw not in OPERATIONS:
            op_attempt += 1
            print(
                f"  Unknown operation '{raw}'. "
                "Please choose from the list above or type 'quit'.\n"
                f"  Invalid input. Attempt {op_attempt} of {MAX_RETRIES}.\n"
            )
            if op_attempt >= MAX_RETRIES:
                print(
                    "  Too many invalid operation selections. Exiting."
                )
                return
            continue

        # Guard scientific operations when not in scientific mode.
        if raw in SCIENTIFIC_OPERATIONS and not calc.is_scientific_mode():
            print(
                f"Error: {raw} is not available in normal mode. "
                "Use 'mode scientific' to enable scientific functions."
            )
            continue

        # Valid operation entered — reset the operation-selection retry counter.
        op_attempt = 0

        try:
            operands = get_operands(raw)
        except OperandRetryExceeded:
            continue

        result = execute_operation(calc, raw, operands)
        print(f"  Result: {format_result(result)}\n")
