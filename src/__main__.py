"""Entry point for the interactive calculator session."""

from .calculator import Calculator
from .history import OperationHistory
from .io_handler import InputHandler, InputRetryExhaustedError
from .mode_manager import ModeManager
from .operations import OperationRegistry


def main() -> None:
    """Run the interactive calculator loop.

    Initialises Calculator, InputHandler, OperationHistory, OperationRegistry,
    and ModeManager, then enters an infinite loop that prompts the user for an
    operation and operands, invokes the operation, displays the result, and
    records it in the history log.

    The loop exits cleanly on KeyboardInterrupt, when the user types
    "exit" / "quit", or when the user exhausts all retry attempts for any
    input prompt.

    The user may type "mode", "switch", or "m" to toggle between Normal and
    Scientific mode.  Scientific mode exposes additional trigonometric
    operations (sin, cos, tan).
    """
    history = OperationHistory()
    history.clear()

    calc = Calculator()
    handler = InputHandler(history=history)
    registry = OperationRegistry(calc)
    mode_manager = ModeManager()

    print("Welcome to the Calculator. Press Ctrl+C or type 'exit' to quit.")

    while True:
        try:
            try:
                available = registry.get_available_operations(mode_manager)
                choice = handler.get_operation_choice(
                    available,
                    current_mode=mode_manager.get_mode_display_name(),
                )
            except InputRetryExhaustedError:
                break

            if choice in ("exit", "quit"):
                print("Goodbye!")
                break

            if choice == "mode":
                mode_manager.switch_mode()
                print(f"Switched to {mode_manager.get_mode_display_name()} mode.")
                continue

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

    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        from .gui_main import main as gui_main
        gui_main()
    elif len(sys.argv) > 1:
        from .cli import cli_main
        cli_main(sys.argv[1:])
    else:
        main()
