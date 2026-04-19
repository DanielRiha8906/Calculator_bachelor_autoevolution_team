import sys

from src.cli import run_cli
from src.logging_config import setup_logging
from src.user_input import run_interactive


def main() -> None:
    """Entry point for the calculator.

    Dispatches to CLI mode when arguments are provided on the command line,
    otherwise falls back to the interactive prompt.
    """
    setup_logging()
    if len(sys.argv) > 1:
        exit_code = run_cli(sys.argv[1:])
        sys.exit(exit_code)
    else:
        run_interactive()


if __name__ == "__main__":
    main()
