"""Calculator package — public API for backward compatibility."""
from .calculator import Calculator
from .core.operations import OperationMode
from .operation_registry import OperationRegistry
from .ui.interactive import run_interactive_session
from .ui.cli import run_cli
from .infrastructure.history import OperationHistory
from .infrastructure.error_logger import ErrorLogger

__all__ = [
    "Calculator",
    "OperationMode",
    "OperationRegistry",
    "run_interactive_session",
    "run_cli",
    "OperationHistory",
    "ErrorLogger",
]
