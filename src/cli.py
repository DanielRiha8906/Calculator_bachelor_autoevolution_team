"""Interactive command-line interface for the Calculator.

Provides a menu-driven REPL that allows a user to select and invoke any
public operation exposed by a Calculator instance without knowing its
internal structure in advance.
"""

import inspect

from .calculator import Calculator
from .error_logger import ErrorLogger
from .history import OperationHistory
from .validation import (
    OperandValidationSession,
    OperationValidationSession,
    detect_mode,
    format_operation_error,
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
    operations = get_operation_menu(calculator)
    op_session = OperationValidationSession(mode=mode, available_ops=operations)
    history = OperationHistory()
    error_logger = ErrorLogger()

    while True:
        # Refresh the operation list each iteration in case Calculator grows.
        operations = get_operation_menu(calculator)
        op_session._available_ops = operations

        print("\nAvailable operations:")
        for idx, op_name in enumerate(operations, start=1):
            print(f"  {idx}. {op_name}")
        print("  (type 'quit', 'exit', or 'q' to exit)")
        print("  (type 'history' or 'h' to view operation history)")

        raw_choice = input("\nSelect operation (name or number): ").strip()

        # Handle quit aliases before passing to the validation session.
        if raw_choice.lower() in {"quit", "exit", "q"}:
            history.save_to_file("history.txt")
            print("Goodbye!")
            break

        # Handle history display command.
        if raw_choice.lower() in {"history", "h"}:
            entries = history.get_history()
            if entries:
                print("\nOperation history:")
                for entry in entries:
                    print(f"  {entry}")
            else:
                print("  No history yet.")
            continue

        # Resolve a numeric shortcut to an operation name.
        resolved_choice = raw_choice
        try:
            idx = int(raw_choice)
            if 1 <= idx <= len(operations):
                resolved_choice = operations[idx - 1]
            else:
                print(
                    f"  Selection out of range. Choose between 1 and {len(operations)}."
                )
                op_session._attempt_count += 1
                if op_session.attempt_count >= op_session._max_retries:
                    print(
                        f"Maximum retry attempts ({op_session._max_retries}) "
                        "exceeded. Session terminated."
                    )
                    history.save_to_file("history.txt")
                    break
                continue
        except ValueError:
            pass  # not a number — treat as an operation name and validate below

        # Validate the (possibly resolved) operation name.
        ops_lower: dict[str, str] = {op.lower(): op for op in operations}
        matched = ops_lower.get(resolved_choice.lower())

        if matched is None:
            error_logger.log_unsupported_operation(resolved_choice)
            print(
                f"  Invalid selection '{resolved_choice}'. "
                + format_operation_error(operations)
            )
            op_session._attempt_count += 1
            if op_session.attempt_count >= op_session._max_retries:
                print(
                    f"Maximum retry attempts ({op_session._max_retries}) "
                    "exceeded. Session terminated."
                )
                history.save_to_file("history.txt")
                break
            continue

        op_name = matched
        op_session.reset_counter()

        arity = get_arity(calculator, op_name)

        # In CLI mode OperandValidationSession raises SystemExit on invalid
        # operand input.  Intercept it here so we can log the event before
        # the process terminates; then re-raise to preserve original behaviour.
        try:
            operands = get_operands(arity, mode=mode)
        except SystemExit as exc:
            # The SystemExit message contains the offending value; log with
            # a generic reason since the raw string is embedded in the message.
            error_logger.log_invalid_operand(
                str(exc).split("'")[1] if "'" in str(exc) else "unknown",
                str(exc),
            )
            raise

        if operands is None:
            # Operand retry limit reached in interactive mode — end the
            # session gracefully.  Individual invalid entries were already
            # reported by the validation session; log the overall session
            # failure here.
            error_logger.log_invalid_operand(
                "interactive-session",
                "Maximum retry attempts exceeded for operand input.",
            )
            history.save_to_file("history.txt")
            break

        try:
            result = getattr(calculator, op_name)(*operands)
            history.record_operation(op_name, operands, result)
            print(f"  Result: {result}")
        except ZeroDivisionError as exc:
            numerator = operands[0] if operands else float("nan")
            error_logger.log_division_by_zero(numerator)
            print(f"  Error: {exc}")
        except ValueError as exc:
            operand_ctx = operands[0] if operands else float("nan")
            error_logger.log_invalid_domain(op_name, operand_ctx, str(exc))
            print(f"  Error: {exc}")
        except Exception as exc:  # noqa: BLE001
            print(f"  Error: {exc}")
