"""Entry point for the Calculator application.

Supports two launch modes selected via command-line arguments:

- **CLI mode** (default): launches the interactive text-based session by
  calling ``run_session(calc)``.  This is the existing behaviour and is
  preserved when the ``--gui`` flag is absent.

- **GUI mode** (``--gui``): imports ``GuiCalculator`` from
  ``src/interface/gui.py``, creates a Tk root window, and enters the
  Tkinter main-event loop via ``GuiCalculator.run()``.

Usage::

    python -m src              # CLI mode
    python -m src --gui        # GUI mode
"""

import sys

from .core import Calculator
from .session import run_session


def main() -> None:
    """Parse arguments and launch the appropriate calculator interface."""
    calc = Calculator()

    if "--gui" in sys.argv:
        import tkinter as tk
        from .interface.gui import GuiCalculator

        root = tk.Tk()
        gui = GuiCalculator(root, calc)
        gui.run()
    else:
        run_session(calc)


if __name__ == "__main__":
    main()
