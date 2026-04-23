"""High-level GUI launch entry point.

Provides :func:`run_gui`, which wires together the :class:`~src.core.calculator.Calculator`,
:class:`~src.session.CalculatorSession`, :class:`~src.gui.session_adapter.GUISessionAdapter`,
and :class:`~src.gui.window.CalculatorWindow` and starts the Tkinter event loop.
"""

from ..core.calculator import Calculator
from ..session import CalculatorSession
from .session_adapter import GUISessionAdapter
from .window import CalculatorWindow


def run_gui() -> None:
    """Create and run the Calculator GUI application.

    Constructs a :class:`~src.core.calculator.Calculator` instance, wraps it in
    a :class:`~src.session.CalculatorSession`, adapts it for GUI consumption via
    :class:`~src.gui.session_adapter.GUISessionAdapter`, and opens the
    :class:`~src.gui.window.CalculatorWindow`.

    This function blocks until the user closes the window.
    """
    calc = Calculator()
    session = CalculatorSession(calc)
    adapter = GUISessionAdapter(session)
    window = CalculatorWindow(adapter)
    window.mainloop()
