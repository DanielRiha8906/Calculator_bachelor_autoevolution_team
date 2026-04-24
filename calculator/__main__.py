"""Entry point for `python -m calculator`.

Delegates to the src package main() to avoid duplicating logic.
"""

import sys
import os

# Ensure the project root is on the path so `src` is importable.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cli import main_cli_noninteractive, run_calculator, display_error


def main() -> None:
    """Entry point for the calculator CLI.

    If command-line arguments are provided, run in non-interactive mode.
    Otherwise, run the interactive prompt-based mode.
    """
    if len(sys.argv) > 1:
        sys.exit(main_cli_noninteractive(sys.argv[1:]))

    try:
        run_calculator()
    except ZeroDivisionError:
        display_error("Division by zero is not allowed.")
    except Exception as e:
        display_error(str(e))


if __name__ == "__main__":
    main()
