"""Core package for the Calculator application.

Exports CalculationEngine and OperationRegistry from their respective
submodules.
"""

from .engine import CalculationEngine
from .operations import Operation, OperationRegistry, _CATALOG

__all__ = ["CalculationEngine", "Operation", "OperationRegistry", "_CATALOG"]
