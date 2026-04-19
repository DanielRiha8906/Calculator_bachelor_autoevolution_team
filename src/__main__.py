from .calculator import Calculator
from .input_handler import run_interactive_session


def main() -> None:
    """Entry point for the interactive calculator session."""
    run_interactive_session(Calculator())


if __name__ == "__main__":
    main()
