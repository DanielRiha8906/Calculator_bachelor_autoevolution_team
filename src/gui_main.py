"""Entry point for the tkinter calculator GUI.

Run this module directly to launch the graphical calculator::

    python -m src.gui_main

or::

    python src/gui_main.py
"""

import tkinter as tk

from src.core.calculator import Calculator
from src.support.history import HistoryTracker
from src.gui.modes import SimpleMode
from src.gui.application import CalculatorGUI


def main() -> None:
    """Launch the tkinter calculator GUI."""
    root = tk.Tk()
    root.title("Calculator")
    calculator = Calculator()
    history_tracker = HistoryTracker()
    mode = SimpleMode(calculator)
    app = CalculatorGUI(root, calculator, mode, history_tracker)
    root.mainloop()


if __name__ == "__main__":
    main()
