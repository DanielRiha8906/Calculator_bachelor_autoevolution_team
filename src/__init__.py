from .calculator import Calculator
from .engine import CalculationEngine
from .io_handler import InputHandler, UserInterface
from .operations import OperationRegistry
from .session_history import SessionHistory
from .workflow import CalculatorWorkflow

# CalculatorGUI requires tkinter, which is not available in all environments
# (e.g. headless CI).  Import it only when tkinter is present so that the rest
# of the package remains importable without a display server.
try:
    from .gui import CalculatorGUI
    _GUI_AVAILABLE = True
except ModuleNotFoundError:
    _GUI_AVAILABLE = False

__all__ = [
    "Calculator",
    "CalculationEngine",
    "CalculatorGUI",
    "CalculatorWorkflow",
    "InputHandler",
    "OperationRegistry",
    "SessionHistory",
    "UserInterface",
]
