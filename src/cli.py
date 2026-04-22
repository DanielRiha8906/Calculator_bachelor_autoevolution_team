"""Interactive command-line interface for the Calculator.

Provides a menu-driven REPL that allows a user to select and invoke any
public operation exposed by a Calculator instance without knowing its
internal structure in advance.
"""

import inspect

from .core.calculator import Calculator
from .formatter import (
    format_error,
    format_history_header,
    format_menu_header,
    format_quit_instruction,
    format_result,
)
from .session import CalculatorSession
from .validation import (
    OperandValidationSession,
    OperationValidationSession,
    detect_mode,
    format_operation_error as validation_format_operation_error,
)


def get_arity(calculator: Calculator, op_name: str) -> int:
    """Return the number of operands required by a Calculator operation.

    Uses :func:`inspect.signature` to count the parameters of the named
    method, excluding ``self``.

    Args:
        calculator: The Calculator instance whose method is inspected.
        op_name: The name of the public method to examine.

    Returns:
        The number of parameters the method accepts, not counting ``self``.

    Example:
        >>> calc = Calculator()
        >>> get_arity(calc, "add")
        2
        >>> get_arity(calc, "square")
        1
    """
    method = getattr(calculator, op_name)
    sig = inspect.signature(method)
    # ``method`` is already a bound method, so ``self`` is not present in
    # the signature — every parameter counted here is a real operand.
    return len(sig.parameters)


def get_operation_menu(calculator: Calculator) -> list[str]:
    """Return all public (non-dunder) method names on a Calculator instance.

    Args:
        calculator: The Calculator instance to introspect.

    Returns:
        A list of method name strings sorted in the order they are
        returned by :func:`dir`, with dunder names excluded.
    """
    return [
        name
        for name in dir(calculator)
        if not name.startswith("_") and callable(getattr(calculator, name))
    ]


def parse_float(value: str) -> float:
    """Parse a string as a float, raising ValueError if it is not numeric.

    Args:
        value: The raw string entered by the user.

    Returns:
        The parsed float value.

    Raises:
        ValueError: If *value* cannot be converted to a float.
    """
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"'{value}' is not a valid number.")


def get_operands(arity: int, mode: str | None = None) -> list[float] | None:
    """Prompt the user for the required number of numeric operands.

    Uses an :class:`~src.validation.OperandValidationSession` to manage retry
    logic.  In interactive mode each operand allows up to 5 consecutive failed
    attempts before the entire collection is aborted.  In CLI mode the first
    invalid entry causes an immediate :class:`SystemExit`.

    Args:
        arity: The number of operands to collect (typically 1 or 2).
        mode: ``'interactive'`` or ``'cli'``.  When ``None`` the function
            defaults to ``'interactive'`` to preserve backward-compatible
            reprompt behaviour for callers that do not supply an explicit mode.
            Pass ``detect_mode()`` explicitly when CLI fast-fail is desired.

    Returns:
        A list of *arity* floats in entry order, or ``None`` if the retry
        limit was exceeded in interactive mode.
    """
    if mode is None:
        mode = "interactive"

    session = OperandValidationSession(mode=mode)
    operands: list[float] = []

    for i in range(1, arity + 1):
        value = session.validate_input(
            prompt_fn=lambda idx=i: input(f"  Enter operand {idx}: "),
            error_msg="Invalid input:",
        )
        if value is None:
            # Retry limit reached in interactive mode.
            return None
        operands.append(value)

    return operands


def interactive_session(calculator: Calculator) -> None:
    """Run a menu-driven interactive session for the given calculator.

    Displays a numbered list of all public operations, prompts the user to
    select one by name or number, collects the required operands, executes
    the operation, and prints the result.  The loop continues until the user
    types ``quit``, ``exit``, or ``q`` at the selection prompt.

    Operation selection is managed by an
    :class:`~src.validation.OperationValidationSession`.  In interactive mode
    up to 5 consecutive invalid operation entries are allowed before the
    session terminates.  In CLI mode the first invalid entry causes an
    immediate :class:`SystemExit`.

    Args:
        calculator: The Calculator instance to use for all computations.
    """
    mode = detect_mode()
    session = CalculatorSession(calculator)
    operations = session.get_operation_list()
    op_session = OperationValidationSession(mode=mode, available_ops=operations)

    while True:
        # Refresh the operation list each iteration in case Calculator grows.
        operations = session.get_operation_list()
        op_session._available_ops = operations

        print(format_menu_header(operations))
        print(format_quit_instruction())

        raw_choice = input("\nSelect operation (name or number): ").strip()

        # Handle quit aliases before passing to the validation session.
        if raw_choice.lower() in {"quit", "exit", "q"}:
            session.save_history("history.txt")
            print("Goodbye!")
            break

        # Handle history display command.
        if raw_choice.lower() in {"history", "h"}:
            entries = session.get_history()
            if entries:
                print(format_history_header())
                for entry in entries:
                    print(f"  {entry}")
            else:
                print("  No history yet.")
            continue

        # Resolve the raw choice to a canonical operation name.
        op_name, exit_code = session.select_operation(raw_choice, mode)

        if exit_code == 2:
            # Numeric index was out of range.
            print(
                f"  Selection out of range. Choose between 1 and {len(operations)}."
            )
            op_session._attempt_count += 1
            if op_session.attempt_count >= op_session._max_retries:
                print(
                    f"Maximum retry attempts ({op_session._max_retries}) "
                    "exceeded. Session terminated."
                )
                session.save_history("history.txt")
                break
            continue

        if op_name is None:
            # Unrecognised operation name — reconstruct the same error string
            # that the original code produced.
            print(
                f"  Invalid selection '{raw_choice}'. "
                + validation_format_operation_error(operations)
            )
            op_session._attempt_count += 1
            if op_session.attempt_count >= op_session._max_retries:
                print(
                    f"Maximum retry attempts ({op_session._max_retries}) "
                    "exceeded. Session terminated."
                )
                session.save_history("history.txt")
                break
            continue

        op_session.reset_counter()

        arity = session.get_arity(op_name)

        # collect_operands handles logging; re-raise SystemExit for CLI mode.
        try:
            operands, op_exit_code = session.collect_operands(arity, mode=mode)
        except SystemExit:
            raise

        if operands is None:
            # Operand retry limit reached in interactive mode.
            session.save_history("history.txt")
            break

        result, error_msg = session.execute_operation(op_name, operands)

        if error_msg is not None:
            print(format_error(error_msg))
        else:
            session.record_history(op_name, operands, result)
            print(format_result(op_name, operands, result))
