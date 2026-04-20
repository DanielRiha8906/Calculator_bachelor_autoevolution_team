"""Interactive session logic for the Calculator application.

This module contains all user-facing I/O for the interactive calculator:
displaying the operation menu, reading and validating user choices and
operands, and running the main session loop.  It delegates operation
registration to :mod:`src.core.operations` and history persistence to
:class:`~src.history.HistoryTracker`.

Input collection functions are also accessible via
:mod:`src.interactive.input_handler`, which re-exports them from here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..error_logger import ErrorLogger
from ..history import HistoryTracker
from ..core.operations import get_operation_registry
from ..core.operations_manager import OperationRegistry
from ..interface.menu_renderer import display_menu

if TYPE_CHECKING:
    from ..core.calculator import Calculator

_error_logger = ErrorLogger()

MAX_VALIDATION_ATTEMPTS = 5

_HISTORY_TOKEN = "h"
_MODE_SWITCH_TOKEN = "m"


def get_mode_selection() -> str:
    """Prompt the user to select a calculator mode.

    Displays a two-option prompt and accepts ``"1"`` for Normal mode or
    ``"2"`` for Scientific mode.  Reprompts on invalid input up to
    :data:`MAX_VALIDATION_ATTEMPTS` consecutive times; if that limit is
    reached ``"normal"`` is returned as a safe default.

    Returns:
        ``"normal"`` or ``"scientific"`` as a lowercase string.
    """
    attempt_count = 0
    while True:
        raw = input(
            "\nSelect calculator mode: 1. Normal  2. Scientific\n"
            "Enter 1 or 2: "
        ).strip()

        if raw == "1":
            return "normal"
        if raw == "2":
            return "scientific"

        attempt_count += 1
        print("  Invalid selection. Please enter 1 for Normal or 2 for Scientific.")
        if attempt_count >= MAX_VALIDATION_ATTEMPTS:
            print("Maximum invalid input attempts reached. Defaulting to Normal mode.")
            return "normal"


def get_operation_choice(registry: dict[str, tuple]) -> tuple | None:
    """Prompt the user to select an operation.

    Keeps reprompting until a valid selection, a quit command, a history
    request, or the maximum number of invalid attempts is reached.

    Args:
        registry: The operation registry returned by
            :func:`~src.core.operations.get_operation_registry`.

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
            _error_logger.log_error(
                "UNSUPPORTED_OPERATION",
                {
                    "operation": raw,
                    "operands": "N/A",
                    "message": (
                        f"numeric selection '{raw}' out of range"
                        f" (1–{len(names)})"
                    ),
                },
            )
            print(
                f"  Invalid number. Choose between 1 and {len(names)}."
                f" Available operations: {available}."
            )
        elif raw in registry:
            method, arity = registry[raw]
            return (raw, method, arity)
        else:
            attempt_count += 1
            _error_logger.log_error(
                "UNSUPPORTED_OPERATION",
                {
                    "operation": raw,
                    "operands": "N/A",
                    "message": f"unknown operation '{raw}'",
                },
            )
            print(
                f"  Unknown operation '{raw}'."
                f" Available operations: {available}."
            )

        if attempt_count >= MAX_VALIDATION_ATTEMPTS:
            print("Maximum invalid input attempts reached. Ending session.")
            return (None, None, None)


def get_operation_choice_with_mode_option(
    registry: dict[str, tuple],
) -> tuple | str | None:
    """Prompt the user to select an operation, with an additional mode-switch option.

    Extends :func:`get_operation_choice` with support for the ``"m"`` token,
    which signals the caller to switch the active calculator mode.

    Args:
        registry: The operation registry for the currently active mode.

    Returns:
        ``(_MODE_SWITCH_TOKEN, None, None)`` when the user enters ``"m"``,
        otherwise the same return values as :func:`get_operation_choice`:
        a ``(name, method, arity)`` tuple, ``None`` on quit, or
        ``(None, None, None)`` on max-attempts exhaustion.
    """
    names = list(registry.keys())
    quit_tokens = {"q", "quit", "exit"}
    available = ", ".join(names)
    attempt_count = 0

    while True:
        raw = input(
            "\nEnter operation name or number"
            " (h for history, m to switch mode, q to quit): "
        ).strip().lower()

        if raw in quit_tokens:
            return None

        if raw == _HISTORY_TOKEN:
            return (_HISTORY_TOKEN, None, None)

        if raw == _MODE_SWITCH_TOKEN:
            return (_MODE_SWITCH_TOKEN, None, None)

        # Allow numeric selection
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(names):
                name = names[index]
                method, arity = registry[name]
                return (name, method, arity)
            attempt_count += 1
            _error_logger.log_error(
                "UNSUPPORTED_OPERATION",
                {
                    "operation": raw,
                    "operands": "N/A",
                    "message": (
                        f"numeric selection '{raw}' out of range"
                        f" (1–{len(names)})"
                    ),
                },
            )
            print(
                f"  Invalid number. Choose between 1 and {len(names)}."
                f" Available operations: {available}."
            )
        elif raw in registry:
            method, arity = registry[raw]
            return (raw, method, arity)
        else:
            attempt_count += 1
            _error_logger.log_error(
                "UNSUPPORTED_OPERATION",
                {
                    "operation": raw,
                    "operands": "N/A",
                    "message": f"unknown operation '{raw}'",
                },
            )
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
                _error_logger.log_error(
                    "INVALID_OPERAND",
                    {
                        "operation": "N/A",
                        "operands": f"slot {i}: '{raw}'",
                        "message": f"'{raw}' is not a valid number",
                    },
                )
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
    results until the user quits.  The user first selects a mode (Normal or
    Scientific) and may switch modes at any point during the session via the
    ``m`` menu option.  Exceptions raised by the calculator
    (``TypeError``, ``ValueError``, ``ZeroDivisionError``) are caught and
    displayed without terminating the session.

    Each successful operation is recorded in *history_tracker*.  When the
    session ends the history is saved to ``history.txt`` via
    :meth:`~src.history.HistoryTracker.save_to_file`.

    Args:
        calculator: A ``Calculator`` instance to perform operations with.
        history_tracker: An optional :class:`~src.history.HistoryTracker`
            instance.  If ``None``, a new one is created internally.

    Returns:
        None
    """
    if history_tracker is None:
        history_tracker = HistoryTracker()

    op_registry = OperationRegistry(calculator)

    print("Welcome to the interactive calculator.")

    current_mode = get_mode_selection()

    while True:
        if current_mode == "scientific":
            active_registry = op_registry.get_scientific_operations()
        else:
            active_registry = op_registry.get_normal_operations()

        display_menu(active_registry, current_mode)
        choice = get_operation_choice_with_mode_option(active_registry)

        # Explicit quit by the user
        if choice is None:
            print("Goodbye.")
            break

        # Mode switch request
        if choice == (_MODE_SWITCH_TOKEN, None, None):
            current_mode = get_mode_selection()
            continue

        # History display request
        if choice == (_HISTORY_TOKEN, None, None):
            history_tracker.display()
            continue

        # Max-attempts sentinel: get_operation_choice_with_mode_option already
        # printed the termination message, so just exit the loop.
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
        except ZeroDivisionError as exc:
            _error_logger.log_error(
                "DIVISION_BY_ZERO",
                {
                    "operation": operation_name,
                    "operands": ", ".join(str(o) for o in operands),
                    "message": str(exc),
                },
            )
            print(f"  Error: {exc}")
        except TypeError as exc:
            _error_logger.log_error(
                "INVALID_OPERAND",
                {
                    "operation": operation_name,
                    "operands": ", ".join(str(o) for o in operands),
                    "message": str(exc),
                },
            )
            print(f"  Error: {exc}")
        except ValueError as exc:
            _error_logger.log_error(
                "INVALID_OPERAND",
                {
                    "operation": operation_name,
                    "operands": ", ".join(str(o) for o in operands),
                    "message": str(exc),
                },
            )
            print(f"  Error: {exc}")

    history_tracker.save_to_file()
