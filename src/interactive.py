"""Interactive command-line session for the Calculator."""

from typing import Union

from .calculator import Calculator
from .history import OperationHistory
from .operation_registry import OperationRegistry

MAX_ATTEMPTS = 5


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
    retry_count = 0

    while True:
        # --- Display operation menu ---
        operations = registry.get_operations()
        print("Available operations:")
        for idx, name in enumerate(operations):
            arity = registry.get_arity(name)
            label = "unary" if arity == 1 else "binary"
            print(f"  {idx}: {name} ({label})")

        # --- Select operation ---
        op_name: str | None = None
        while op_name is None:
            raw_index = input("Select an operation (index): ")
            try:
                index = int(raw_index)
                if index < 0 or index >= len(operations):
                    raise IndexError
                op_name = operations[index]
                retry_count = 0
            except (ValueError, IndexError):
                retry_count += 1
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

        arity = registry.get_arity(op_name)

        # --- Gather operands ---
        if arity == 1:
            operand: Union[int, float] | None = None
            while operand is None:
                raw = input("Enter operand: ")
                try:
                    operand = parse_operand(raw)
                    retry_count = 0
                except ValueError:
                    retry_count += 1
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
                try:
                    operand1 = parse_operand(raw)
                    retry_count = 0
                except ValueError:
                    retry_count += 1
                    print("Invalid input. Please enter a number.")
                    if retry_count >= MAX_ATTEMPTS:
                        print("Too many consecutive invalid inputs. Session terminated.")
                        history.write_to_file()
                        return

            operand2: Union[int, float] | None = None
            while operand2 is None:
                raw = input("Enter operand 2: ")
                try:
                    operand2 = parse_operand(raw)
                    retry_count = 0
                except ValueError:
                    retry_count += 1
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
            print("Error: Division by zero")
        except Exception as exc:
            print(f"Error: {exc}")

        # --- Continue prompt ---
        while True:
            answer = input("Continue? (yes/no): ").strip().lower()
            if answer in ("yes", "y"):
                break
            if answer in ("no", "n"):
                history.write_to_file()
                return
            # Unexpected input: re-prompt
