"""Entry point for the interactive calculator session."""

from .calculator import Calculator
from .io_handler import InputHandler
from .operations import OperationRegistry


def main() -> None:
    """Run the interactive calculator loop.

    Initialises Calculator, InputHandler, and OperationRegistry, then enters
    an infinite loop that prompts the user for an operation and operands,
    invokes the operation, and displays the result.  The loop exits cleanly
    on KeyboardInterrupt or when the user types "exit" / "quit".
    """
    calc = Calculator()
    handler = InputHandler()
    registry = OperationRegistry(calc)

    print("Welcome to the Calculator. Press Ctrl+C or type 'exit' to quit.")

    while True:
        try:
            choice = handler.get_operation_choice(registry.list_operations())

            if choice in ("exit", "quit"):
                print("Goodbye!")
                break

            method, arity, description = registry.get_operation(choice)

            operands: list[float] = []
            if arity == 1:
                value = handler.get_operand("Enter value: ")
                if choice == "factorial":
                    value = int(value)
                operands.append(value)
            else:
                operands.append(handler.get_operand("Enter first operand: "))
                operands.append(handler.get_operand("Enter second operand: "))

            result = method(*operands)
            handler.display_result(description, operands, result)

        except ValueError as exc:
            handler.display_error(str(exc))
        except ZeroDivisionError:
            handler.display_error("Division by zero is not allowed.")
        except KeyError as exc:
            handler.display_error(str(exc))
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
