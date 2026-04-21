import sys

from src.presentation.cli import run_cli
from src.logging_config import setup_logging
from src.presentation.interactive import run_interactive


def main() -> None:
    """Entry point for the calculator.

    Dispatches based on the provided arguments:

    - ``--gui``: Launch the Tkinter graphical interface.
    - Any other arguments: Evaluate the expression in CLI mode.
    - No arguments: Start the interactive prompt.
    """
    setup_logging()
    args = sys.argv[1:]

    if args and args[0] == "--gui":
        import tkinter as tk
        from src.presentation.gui import CalculatorGUI

        root = tk.Tk()
        app = CalculatorGUI(root)
        app.run()
    elif args:
        exit_code = run_cli(args)
        sys.exit(exit_code)
    else:
        run_interactive()


if __name__ == "__main__":
    main()
