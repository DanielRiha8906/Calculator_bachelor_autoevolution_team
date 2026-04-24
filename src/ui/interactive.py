"""PRESENTATION LAYER — interactive terminal session for the Calculator.

This module is the interactive terminal presentation layer.  It depends on:
- ``Calculator`` (core) for computation.
- ``OperationRegistry`` (discovery) to enumerate and invoke operations.
- ``OperationHistory`` (history) to record and persist session operations.
- ``ErrorLogger`` (infrastructure) to log invalid inputs and runtime errors.

It does NOT depend on cli.py and must never import from it.

Responsibilities:
- Display the operation menu and prompt the user for input.
- Gather operands from the user with validation and retry logic.
- Execute operations via the OperationRegistry.
- Display results and error messages.
- Track the session operation history and persist it on exit.
- Log invalid inputs and runtime errors via ErrorLogger.
- Enforce session retry logic: terminate after MAX_ATTEMPTS consecutive
  invalid inputs across all input phases.
"""

from typing import Union

from ..calculator import Calculator
from ..core.operations import OperationMode
from ..infrastructure.error_logger import ErrorLogger
from ..infrastructure.history import OperationHistory
from ..operation_registry import OperationRegistry

MAX_ATTEMPTS = 5

_HISTORY_SENTINEL = "__history__"


def display_history_indexed(history: "OperationHistory") -> None:
    """Display the session history with 1-based numbered entries.

    Prints each recorded operation as ``"N. entry"`` where N is the 1-based
    position.  Prints ``"No operations recorded yet."`` when the history is
    empty.

    Args:
        history: The ``OperationHistory`` instance for the current session.
    """
    entries = history.get_entries()
    if not entries:
        print("No operations recorded yet.")
        return
    for idx, entry in enumerate(entries, start=1):
        print(f"{idx}. {entry}")


def parse_operand(user_input: str) -> Union[int, float]:
    """Parse a user-supplied string into a numeric operand.

    Tries ``int`` first when the string contains no decimal point; falls back
    to ``float`` otherwise.

    Args:
        user_input: The raw string typed by the user.

    Returns:
        An ``int`` if the input represents a whole number, a ``float`` if it
        contains a decimal point.

    Raises:
        ValueError: If the string cannot be converted to a number.
    """
    if "." in user_input:
        return float(user_input)
    return int(user_input)


def _select_mode() -> OperationMode:
    """Prompt the user to select a calculator mode and return the chosen OperationMode.

    Accepts "0" or "normal" for NORMAL mode, "1" or "scientific" for SCIENTIFIC mode.
    Re-prompts on invalid input until a valid choice is made.

    Returns:
        The selected ``OperationMode``.
    """
    print("Select mode: 0=Normal, 1=Scientific")
    while True:
        raw = input("Mode (0/normal or 1/scientific): ").strip().lower()
        if raw in ("0", "normal"):
            return OperationMode.NORMAL
        if raw in ("1", "scientific"):
            return OperationMode.SCIENTIFIC
        print("Invalid mode. Please enter 0 (normal) or 1 (scientific).")


def run_interactive_session(calculator: Calculator = None) -> None:
    """Run an interactive calculator session in the terminal.

    Presents a menu of available operations discovered from ``calculator``,
    accepts operand input, computes results, and loops until the user exits.
    Terminates the session automatically after MAX_ATTEMPTS consecutive invalid
    inputs (across operation selection and operand entry).

    Args:
        calculator: An optional ``Calculator`` instance to use.  A new
            ``Calculator()`` is created when ``None`` is supplied.
    """
    if calculator is None:
        calculator = Calculator()

    registry = OperationRegistry(calculator)
    history = OperationHistory()
    error_logger = ErrorLogger()
    retry_count = 0
    mode: OperationMode | None = None

    while True:
        # --- Display operation menu ---
        if mode is None:
            operations = registry.get_operations()
        else:
            operations = registry.get_operations_by_mode(mode)
        print("Available operations:")
        for idx, name in enumerate(operations):
            arity = registry.get_arity(name)
            label = "unary" if arity == 1 else "binary"
            print(f"  {idx}: {name} ({label})")
        print("  h: View operation history")
        print("  m: Switch mode")

        # --- Select operation ---
        op_name: str | None = None
        while op_name is None:
            raw_index = input("Select an operation (index): ")
            if raw_index.strip().lower() in ("h", "history"):
                display_history_indexed(history)
                op_name = _HISTORY_SENTINEL
                break
            if raw_index.strip().lower() in ("no", "n"):
                history.write_to_file()
                return
            if raw_index.strip().lower() == "m":
                mode = _select_mode()
                # Refresh the operation list for new mode and re-display menu
                operations = registry.get_operations_by_mode(mode)
                print("Available operations:")
                for idx, name in enumerate(operations):
                    arity = registry.get_arity(name)
                    label = "unary" if arity == 1 else "binary"
                    print(f"  {idx}: {name} ({label})")
                print("  h: View operation history")
                print("  m: Switch mode")
                continue
            try:
                index = int(raw_index)
                if index < 0 or index >= len(operations):
                    raise IndexError
                op_name = operations[index]
                retry_count = 0
            except (ValueError, IndexError):
                retry_count += 1
                error_logger.log_invalid_operation(None, "Invalid operation. Please try again.")
                print("Invalid operation. Please try again.")
                print("Available operations:")
                for idx, name in enumerate(operations):
                    arity = registry.get_arity(name)
                    label = "unary" if arity == 1 else "binary"
                    print(f"  {idx}: {name} ({label})")
                if retry_count >= MAX_ATTEMPTS:
                    print("Too many consecutive invalid inputs. Session terminated.")
                    history.write_to_file()
                    return

        # --- History command: skip computation, go to continue prompt ---
        if op_name == _HISTORY_SENTINEL:
            while True:
                answer = input("Continue? (yes/no): ").strip().lower()
                if answer in ("yes", "y"):
                    break
                if answer in ("no", "n"):
                    history.write_to_file()
                    return
                if answer in ("h", "history"):
                    display_history_indexed(history)
                    continue
                # Unexpected input: re-prompt
            continue

        arity = registry.get_arity(op_name)

        # --- Gather operands ---
        if arity == 1:
            operand: Union[int, float] | None = None
            while operand is None:
                raw = input("Enter operand: ")
                if raw.strip().lower() in ("no", "n"):
                    history.write_to_file()
                    return
                try:
                    operand = parse_operand(raw)
                    retry_count = 0
                except ValueError:
                    retry_count += 1
                    error_logger.log_invalid_operand(op_name, raw, "Invalid input. Please enter a number.")
                    print("Invalid input. Please enter a number.")
                    if retry_count >= MAX_ATTEMPTS:
                        print("Too many consecutive invalid inputs. Session terminated.")
                        history.write_to_file()
                        return
            operands = (operand,)
        else:
            operand1: Union[int, float] | None = None
            while operand1 is None:
                raw = input("Enter operand 1: ")
                if raw.strip().lower() in ("no", "n"):
                    history.write_to_file()
                    return
                try:
                    operand1 = parse_operand(raw)
                    retry_count = 0
                except ValueError:
                    retry_count += 1
                    error_logger.log_invalid_operand(op_name, raw, "Invalid input. Please enter a number.")
                    print("Invalid input. Please enter a number.")
                    if retry_count >= MAX_ATTEMPTS:
                        print("Too many consecutive invalid inputs. Session terminated.")
                        history.write_to_file()
                        return

            operand2: Union[int, float] | None = None
            while operand2 is None:
                raw = input("Enter operand 2: ")
                if raw.strip().lower() in ("no", "n"):
                    history.write_to_file()
                    return
                try:
                    operand2 = parse_operand(raw)
                    retry_count = 0
                except ValueError:
                    retry_count += 1
                    error_logger.log_invalid_operand(op_name, raw, "Invalid input. Please enter a number.")
                    print("Invalid input. Please enter a number.")
                    if retry_count >= MAX_ATTEMPTS:
                        print("Too many consecutive invalid inputs. Session terminated.")
                        history.write_to_file()
                        return

            operands = (operand1, operand2)

        # --- Compute and display result ---
        try:
            result = registry.call(op_name, *operands)
            print(f"Result: {result}")
            history.record(op_name, operands, result)
        except ZeroDivisionError:
            error_logger.log_runtime_calculation_error(op_name, operands, "ZeroDivisionError", "Division by zero")
            print("Error: Division by zero")
        except ValueError as exc:
            error_logger.log_runtime_calculation_error(op_name, operands, "ValueError", str(exc))
            print(f"Error: {exc}")
        except Exception as exc:
            error_logger.log_runtime_calculation_error(op_name, operands, type(exc).__name__, str(exc))
            print(f"Error: {exc}")

        # --- Continue prompt ---
        while True:
            answer = input("Continue? (yes/no): ").strip().lower()
            if answer in ("yes", "y"):
                break
            if answer in ("no", "n"):
                history.write_to_file()
                return
            if answer in ("h", "history"):
                display_history_indexed(history)
                continue
            # Unexpected input: re-prompt
