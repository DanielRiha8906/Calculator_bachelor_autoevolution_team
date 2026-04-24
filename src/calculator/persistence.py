"""Persistence facade for the modular calculator (Issue #405).

Re-exports OperationHistory and ErrorLog from their canonical locations so
they are accessible under the src.calculator.persistence namespace.
"""

from src.history import OperationHistory
from src.error_logging import ErrorLog

__all__ = ["OperationHistory", "ErrorLog"]
