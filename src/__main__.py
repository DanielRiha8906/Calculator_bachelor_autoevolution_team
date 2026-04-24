import sys

from .cli import run_calculator, display_error


def main() -> None:
    """Entry point for the calculator.

    Routes to batch mode when command-line arguments are present, or falls
    back to the interactive CLI when invoked with no arguments.
    """
    if len(sys.argv) > 1:
        from .batch_cli import batch_main
        batch_main(sys.argv[1:])
    else:
        try:
            run_calculator()
        except ZeroDivisionError:
            display_error("Division by zero is not allowed.")
        except Exception as e:
            display_error(str(e))


if __name__ == "__main__":
    main()
