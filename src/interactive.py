"""Interactive command-line session for the Calculator."""

from typing import Union

from .calculator import Calculator
from .operation_registry import OperationRegistry


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

    Args:
        calculator: An optional ``Calculator`` instance to use.  A new
            ``Calculator()`` is created when ``None`` is supplied.
    """
    if calculator is None:
        calculator = Calculator()

    registry = OperationRegistry(calculator)

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
            except (ValueError, IndexError):
                print("Invalid operation. Please try again.")

        arity = registry.get_arity(op_name)

        # --- Gather operands ---
        if arity == 1:
            operand: Union[int, float] | None = None
            while operand is None:
                raw = input("Enter operand: ")
                try:
                    operand = parse_operand(raw)
                except ValueError:
                    print("Invalid input. Please enter a number.")
            operands = (operand,)
        else:
            operand1: Union[int, float] | None = None
            while operand1 is None:
                raw = input("Enter operand 1: ")
                try:
                    operand1 = parse_operand(raw)
                except ValueError:
                    print("Invalid input. Please enter a number.")

            operand2: Union[int, float] | None = None
            while operand2 is None:
                raw = input("Enter operand 2: ")
                try:
                    operand2 = parse_operand(raw)
                except ValueError:
                    print("Invalid input. Please enter a number.")

            operands = (operand1, operand2)

        # --- Compute and display result ---
        try:
            result = registry.call(op_name, *operands)
            print(f"Result: {result}")
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
                return
            # Unexpected input: re-prompt
