"""Interactive input handling for the Calculator application.

This module centralises all user-facing I/O: building the operation registry,
displaying the menu, reading and validating user input, and running the main
interactive session loop.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .history import HistoryTracker

if TYPE_CHECKING:
    from .calculator import Calculator

MAX_VALIDATION_ATTEMPTS = 5


def get_operation_registry(calculator: "Calculator") -> dict[str, tuple]:
    """Build a registry of available calculator operations.

    Args:
        calculator: A ``Calculator`` instance whose bound methods are
            stored in the registry.

    Returns:
        A dict mapping operation name (str) to a 2-tuple of
        ``(method, arity)`` where *arity* is the number of operands
        the operation expects (1 for unary, 2 for binary).

    Examples:
        >>> from src.calculator import Calculator
        >>> registry = get_operation_registry(Calculator())
        >>> "add" in registry
        True
        >>> registry["add"][1]
        2
    """
    return {
        "add": (calculator.add, 2),
        "subtract": (calculator.subtract, 2),
        "multiply": (calculator.multiply, 2),
        "divide": (calculator.divide, 2),
        "power": (calculator.power, 2),
        "factorial": (calculator.factorial, 1),
        "square": (calculator.square, 1),
        "cube": (calculator.cube, 1),
        "square_root": (calculator.square_root, 1),
        "cube_root": (calculator.cube_root, 1),
        "log": (calculator.log, 1),
        "ln": (calculator.ln, 1),
    }


def display_menu(registry: dict[str, tuple]) -> None:
    """Print the list of available operations to stdout.

    Args:
        registry: The operation registry returned by
            :func:`get_operation_registry`.

    Returns:
        None
    """
    print("\nAvailable operations:")
    for index, name in enumerate(registry, start=1):
        _method, arity = registry[name]
        operand_hint = f"({arity} operand{'s' if arity != 1 else ''})"
        print(f"  {index:2}. {name} {operand_hint}")
    print("   h. View history")
    print("   q. quit")


_HISTORY_TOKEN = "h"


def get_operation_choice(registry: dict[str, tuple]) -> tuple | None:
    """Prompt the user to select an operation.

    Keeps reprompting until a valid selection, a quit command, a history
    request, or the maximum number of invalid attempts is reached.

    Args:
        registry: The operation registry returned by
            :func:`get_operation_registry`.

    Returns:
        A ``(name, method, arity)`` tuple for the chosen operation,
        ``None`` if the user entered a quit command (``"q"``, ``"quit"``,
        or ``"exit"``), ``(_HISTORY_TOKEN, None, None)`` when the user
        requests history (``"h"``), or ``(None, None, None)`` when
        :data:`MAX_VALIDATION_ATTEMPTS` consecutive invalid inputs have
        been entered.
    """
    names = list(registry.keys())
    quit_tokens = {"q", "quit", "exit"}
    available = ", ".join(names)
    attempt_count = 0

    while True:
        raw = input("\nEnter operation name or number (h for history, q to quit): ").strip().lower()

        if raw in quit_tokens:
            return None

        if raw == _HISTORY_TOKEN:
            return (_HISTORY_TOKEN, None, None)

        # Allow numeric selection
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(names):
                name = names[index]
                method, arity = registry[name]
                return (name, method, arity)
            attempt_count += 1
            print(
                f"  Invalid number. Choose between 1 and {len(names)}."
                f" Available operations: {available}."
            )
        elif raw in registry:
            method, arity = registry[raw]
            return (raw, method, arity)
        else:
            attempt_count += 1
            print(
                f"  Unknown operation '{raw}'."
                f" Available operations: {available}."
            )

        if attempt_count >= MAX_VALIDATION_ATTEMPTS:
            print("Maximum invalid input attempts reached. Ending session.")
            return (None, None, None)


def get_operands(arity: int) -> list[float] | None:
    """Prompt the user for the required number of operand values.

    Parses each entry as a float and reprompts on invalid input.  When
    the cumulative number of invalid entries across all operand slots
    reaches :data:`MAX_VALIDATION_ATTEMPTS`, the prompt is abandoned.

    Args:
        arity: The number of operand values to collect.

    Returns:
        A list of *arity* floats entered by the user, or ``None`` when
        :data:`MAX_VALIDATION_ATTEMPTS` invalid entries have been made.
    """
    operands: list[float] = []
    attempt_count = 0
    for i in range(1, arity + 1):
        while True:
            raw = input(f"  Enter operand {i}: ").strip()
            try:
                operands.append(float(raw))
                break
            except ValueError:
                attempt_count += 1
                print(f"  '{raw}' is not a valid number. Please enter a numeric value.")
                if attempt_count >= MAX_VALIDATION_ATTEMPTS:
                    print("Maximum invalid input attempts reached. Ending session.")
                    return None
    return operands


def run_interactive_session(
    calculator: "Calculator",
    history_tracker: HistoryTracker | None = None,
) -> None:
    """Run the main interactive calculator session.

    Displays the menu, collects input, executes operations, and prints
    results until the user quits. Exceptions raised by the calculator
    (``TypeError``, ``ValueError``, ``ZeroDivisionError``) are caught and
    displayed without terminating the session.

    Each successful operation is recorded in *history_tracker*.  When the
    session ends the history is saved to ``history.txt`` via
    :meth:`~history.HistoryTracker.save_to_file`.

    Args:
        calculator: A ``Calculator`` instance to perform operations with.
        history_tracker: An optional :class:`~history.HistoryTracker`
            instance.  If ``None``, a new one is created internally.

    Returns:
        None
    """
    if history_tracker is None:
        history_tracker = HistoryTracker()

    registry = get_operation_registry(calculator)
    print("Welcome to the interactive calculator.")
    failed_attempts = 0

    while True:
        display_menu(registry)
        choice = get_operation_choice(registry)

        # Explicit quit by the user
        if choice is None:
            print("Goodbye.")
            break

        # History display request
        if choice == (_HISTORY_TOKEN, None, None):
            history_tracker.display()
            continue

        # Max-attempts sentinel: get_operation_choice already printed the
        # termination message, so just exit the loop.
        if choice == (None, None, None):
            break

        operation_name, method, arity = choice

        # For factorial the operand must be an int; collect as float then
        # convert to int so that e.g. "5.0" is accepted gracefully.
        operands = get_operands(arity)

        # Max-attempts sentinel: get_operands already printed the
        # termination message, so just exit the loop.
        if operands is None:
            break

        # factorial requires an int — convert if the float is whole-valued.
        if method == calculator.factorial:
            converted: list = []
            for value in operands:
                if value == int(value):
                    converted.append(int(value))
                else:
                    converted.append(value)  # let the calculator raise TypeError
            operands = converted

        try:
            result = method(*operands)
            print(f"  Result: {result}")
            history_tracker.record(operation_name, operands, result)
            failed_attempts = 0
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            print(f"  Error: {exc}")

    history_tracker.save_to_file()
