"""Entry point for launching the calculator GUI.

Run directly with::

    python -m src --gui

or by calling :func:`main` programmatically.
"""

import tkinter as tk

from .calculator import Calculator
from .gui import CalculatorGUI
from .mode_manager import ModeManager
from .operations import OperationRegistry
from .session_history import SessionHistory


def main() -> None:
    """Launch the tkinter-based calculator GUI.

    Creates all required engine and history objects, builds the root window,
    attaches a :class:`~gui.CalculatorGUI`, and enters the main event loop.
    The function returns only after the window is closed.
    """
    root = tk.Tk()
    history = SessionHistory()
    gui = CalculatorGUI(root, history)
    gui.run()
