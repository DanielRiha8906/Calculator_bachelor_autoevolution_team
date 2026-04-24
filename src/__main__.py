"""Interactive calculator entry point.

Provides a REPL-style loop that reads an operation name and its operands
from stdin, calls the corresponding Calculator method, and prints the result.
"""

from .calculator import Calculator


def _parse_number(raw: str) -> int | float:
    """Parse a string as a number, preferring int over float.

    Args:
        raw: The raw string read from user input.

    Returns:
        An int if the string represents a whole number without a decimal point,
        otherwise a float.

    Raises:
        ValueError: If the string cannot be interpreted as a number.
    """
    try:
        return int(raw)
    except ValueError:
        return float(raw)


def main() -> None:
    """Run the interactive calculator loop.

    Continuously prompts the user to select an operation, then collects the
    required operands and prints the result.  Typing 'quit', 'exit', or 'q'
    terminates the loop.
    """
    calculator = Calculator()

    # Registry maps operation name -> (method, arity)
    registry: dict[str, tuple] = {
        "add": (calculator.add, 2),
        "subtract": (calculator.subtract, 2),
        "multiply": (calculator.multiply, 2),
        "divide": (calculator.divide, 2),
        "factorial": (calculator.factorial, 1),
        "square": (calculator.square, 1),
        "cube": (calculator.cube, 1),
        "square_root": (calculator.square_root, 1),
        "cube_root": (calculator.cube_root, 1),
        "power": (calculator.power, 2),
        "log10": (calculator.log10, 1),
        "ln": (calculator.ln, 1),
    }

    while True:
        print("Enter operation (add, subtract, multiply, divide, factorial, square, cube,")
        print("square_root, cube_root, power, log10, ln) or 'quit' to exit:")
        operation = input("Select operation: ").strip().lower()

        if operation in ("quit", "exit", "q"):
            break

        if operation not in registry:
            print(f"Error: Unknown operation '{operation}'. Please try again.")
            continue

        method, arity = registry[operation]

        # Collect operands
        operands: list[int | float] = []
        error_occurred = False
        for i in range(arity):
            if arity == 1:
                label = "Enter value: "
            else:
                label = f"Enter operand {i + 1}: "
            raw = input(label).strip()
            try:
                operands.append(_parse_number(raw))
            except ValueError:
                print(f"Error: Invalid number '{raw}'. Please enter a numeric value.")
                error_occurred = True
                break

        if error_occurred:
            continue

        # Execute the operation
        try:
            result = method(*operands)
            print(f"Result: {result}")
        except (ValueError, ZeroDivisionError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
