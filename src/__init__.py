from .calculator import Calculator
from .support.error_logger import ErrorLogger
from .interface.repl import REPLInterface

__all__ = ["Calculator", "ErrorLogger", "REPLInterface", "GUICalculator"]

# GUICalculator is conditionally importable; tkinter may not be present in
# headless environments (e.g. CI runners).  Expose it at package level only
# when tkinter is available so that non-GUI modes are unaffected.
try:
    from .interface.gui import GUICalculator
except ImportError:
    pass
