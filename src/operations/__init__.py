"""Operations subpackage for the calculator application.

Exports the public surface of the modular operation modules so that
consumers can import directly from ``src.operations``.
"""

from src.operations.arithmetic import ArithmeticOperations
from src.operations.advanced import AdvancedOperations
from src.operations.base import OperationModule
from src.operations.scientific import ScientificOperations

__all__ = [
    "OperationModule",
    "ArithmeticOperations",
    "AdvancedOperations",
    "ScientificOperations",
]
