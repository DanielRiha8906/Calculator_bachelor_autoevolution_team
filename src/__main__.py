"""Entry point for the interactive calculator session."""

from .calculator import Calculator
from .history import OperationHistory
from .io_handler import InputHandler, InputRetryExhaustedError
from .operations import OperationRegistry


def main() -> None:
    """Run the interactive calculator loop.

    Initialises Calculator, InputHandler, OperationHistory, and OperationRegistry,
    then enters an infinite loop that prompts the user for an operation and
    operands, invokes the operation, displays the result, and records it in the
    history log.  The loop exits cleanly on KeyboardInterrupt, when the user
    types "exit" / "quit", or when the user exhausts all retry attempts for any
    input prompt.
    """
    history = OperationHistory()
    history.clear()

    calc = Calculator()
    handler = InputHandler(history=history)
    registry = OperationRegistry(calc)

    print("Welcome to the Calculator. Press Ctrl+C or type 'exit' to quit.")

    while True:
        try:
            try:
                choice = handler.get_operation_choice(registry.list_operations())
            except InputRetryExhaustedError:
                break

            if choice in ("exit", "quit"):
                print("Goodbye!")
                break

            method, arity, description = registry.get_operation(choice)

            operands: list[float] = []
            try:
                if arity == 1:
                    value = handler.get_operand("Enter value: ")
                    if choice == "factorial":
                        value = int(value)
                    operands.append(value)
                else:
                    operands.append(handler.get_operand("Enter first operand: "))
                    operands.append(handler.get_operand("Enter second operand: "))
            except InputRetryExhaustedError:
                break

            result = method(*operands)
            handler.display_result(description, operands, result)
            history.record_operation(choice, operands, result)

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
    import sys

    if len(sys.argv) > 1:
        from .cli import cli_main
        cli_main(sys.argv[1:])
    else:
        main()
