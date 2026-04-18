import os
import sys

from .core import Calculator
from .session import run_session


def main() -> None:
    """Entry point for the calculator application.

    Selects the interface mode based on command-line arguments or environment
    variables:

    - Pass ``--gui`` as a command-line argument, or set the environment
      variable ``CALCULATOR_GUI=1`` to launch the tkinter GUI.
    - Otherwise, the interactive REPL session is started.

    Usage::

        python -m src           # interactive REPL
        python -m src --gui     # tkinter GUI
        CALCULATOR_GUI=1 python -m src  # tkinter GUI via env var
    """
    gui_requested = (
        "--gui" in sys.argv
        or os.environ.get("CALCULATOR_GUI", "").strip() == "1"
    )

    calc = Calculator()

    if gui_requested:
        try:
            from .interface.gui import run_gui
        except ImportError as exc:
            print(f"Cannot start GUI: {exc}", file=sys.stderr)
            sys.exit(1)
        run_gui(calc)
    else:
        run_session(calc)


if __name__ == "__main__":
    main()

