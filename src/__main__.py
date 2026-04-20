from .calculator import Calculator
from .history import HistoryTracker
from .input_handler import run_interactive_session


def main() -> None:
    """Entry point for the interactive calculator session."""
    run_interactive_session(Calculator(), HistoryTracker())


if __name__ == "__main__":
    main()
