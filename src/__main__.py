from .calculator import Calculator
from .repl import REPLInterface


def main() -> None:
    """Entry point for the calculator REPL application."""
    calc = Calculator()
    repl = REPLInterface(calc)
    try:
        repl.run()
    except (EOFError, KeyboardInterrupt):
        print("\nCalculator closed.")


if __name__ == "__main__":
    main()
