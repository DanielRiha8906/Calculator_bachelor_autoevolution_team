import sys

from .core.calculator import Calculator
from .cli import interactive_session


def main() -> None:
    """Entry point for the calculator application.

    Launches the Tkinter GUI when ``--gui`` is present in the command-line
    arguments; otherwise starts the default interactive CLI session.
    """
    if "--gui" in sys.argv:
        from .gui.app import run_gui
        run_gui()
    else:
        calc = Calculator()
        interactive_session(calc)


if __name__ == "__main__":
    main()
