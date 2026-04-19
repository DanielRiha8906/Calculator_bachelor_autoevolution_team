"""Interactive input handling for the Calculator application.

This module centralises all user-facing I/O: building the operation registry,
displaying the menu, reading and validating user input, and running the main
interactive session loop.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .calculator import Calculator


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
    print("   q. quit")


def get_operation_choice(registry: dict[str, tuple]) -> tuple | None:
    """Prompt the user to select an operation.

    Keeps reprompting until a valid selection or a quit command is given.

    Args:
        registry: The operation registry returned by
            :func:`get_operation_registry`.

    Returns:
        A ``(method, arity)`` tuple for the chosen operation, or ``None``
        if the user entered a quit command (``"q"``, ``"quit"``, or
        ``"exit"``).
    """
    names = list(registry.keys())
    quit_tokens = {"q", "quit", "exit"}

    while True:
        raw = input("\nEnter operation name or number (q to quit): ").strip().lower()

        if raw in quit_tokens:
            return None

        # Allow numeric selection
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(names):
                name = names[index]
                return registry[name]
            print(f"  Invalid number. Choose between 1 and {len(names)}.")
            continue

        if raw in registry:
            return registry[raw]

        print(f"  Unknown operation '{raw}'. Type a name or number from the menu.")


def get_operands(arity: int) -> list[float]:
    """Prompt the user for the required number of operand values.

    Parses each entry as a float and reprompts on invalid input.

    Args:
        arity: The number of operand values to collect.

    Returns:
        A list of *arity* floats entered by the user.
    """
    operands: list[float] = []
    for i in range(1, arity + 1):
        while True:
            raw = input(f"  Enter operand {i}: ").strip()
            try:
                operands.append(float(raw))
                break
            except ValueError:
                print(f"  '{raw}' is not a valid number. Please enter a numeric value.")
    return operands


def run_interactive_session(calculator: "Calculator") -> None:
    """Run the main interactive calculator session.

    Displays the menu, collects input, executes operations, and prints
    results until the user quits. Exceptions raised by the calculator
    (``TypeError``, ``ValueError``, ``ZeroDivisionError``) are caught and
    displayed without terminating the session.

    Args:
        calculator: A ``Calculator`` instance to perform operations with.

    Returns:
        None
    """
    registry = get_operation_registry(calculator)
    print("Welcome to the interactive calculator.")

    while True:
        display_menu(registry)
        choice = get_operation_choice(registry)

        if choice is None:
            print("Goodbye.")
            break

        method, arity = choice

        # For factorial the operand must be an int; collect as float then
        # convert to int so that e.g. "5.0" is accepted gracefully.
        operands = get_operands(arity)

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
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            print(f"  Error: {exc}")
