"""Entry point for the interactive calculator session."""

import sys

from .calculator import Calculator
from .cli_handler import CLIHandler
from .io_handler import InputHandler
from .operations import OperationRegistry


def main() -> None:
    """Run the calculator in CLI or interactive mode.

    When command-line arguments are present (``sys.argv[1:]`` is non-empty),
    the calculator runs in CLI mode: parse the operation and operands from the
    arguments, execute the operation, print the result, and exit.

    Otherwise the original interactive loop is started: prompts the user for
    an operation and operands in an infinite loop until the user exits or sends
    a keyboard interrupt.
    """
    calc = Calculator()
    handler = InputHandler()
    registry = OperationRegistry(calc)
    cli = CLIHandler()

    if cli.is_cli_mode(sys.argv[1:]):
        try:
            operation_key, operand_strings = cli.parse_arguments(sys.argv[1:])
            method, arity, description = registry.get_operation(operation_key)
            operands = cli.validate_operands(operand_strings, arity)
            if operation_key == "factorial":
                operands = [int(operands[0])]
            result = method(*operands)
            cli.print_result(description, operands, result)
            sys.exit(0)
        except (ValueError, ZeroDivisionError, KeyError) as exc:
            cli.print_error(str(exc))
            sys.exit(1)

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
