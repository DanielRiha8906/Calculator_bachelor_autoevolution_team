import sys

from .calculator import Calculator
from .cli import run_calculator, display_error, MaxRetriesExceeded, persist_history_to_file


def main() -> None:
    """Entry point for the calculator.

    Routes to batch mode when command-line arguments are present, handles
    the 'history' sub-command, or falls back to the interactive CLI loop
    when invoked with no arguments.

    The interactive loop keeps a single Calculator instance alive for the
    full session so that history accumulates across operations. When the
    session ends (user quits, Ctrl-C, or max retries exceeded), history
    is persisted to disk via persist_history_to_file().
    """
    if len(sys.argv) > 1:
        if sys.argv[1:] == ["history"]:
            try:
                with open("history.txt") as f:
                    print(f.read(), end="")
            except FileNotFoundError:
                print("No history found.")
            sys.exit(0)
            return

        from .batch_cli import batch_main
        batch_main(sys.argv[1:])
    else:
        calc = Calculator()
        try:
            while True:
                try:
                    result = run_calculator(calc=calc, max_retries=3)
                    if result == "QUIT":
                        break
                except MaxRetriesExceeded as e:
                    display_error(str(e))
                    break
                except (ZeroDivisionError, ValueError):
                    # Error already displayed by run_calculator; continue loop
                    pass
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            persist_history_to_file(calc)

        sys.exit(0)


if __name__ == "__main__":
    main()
