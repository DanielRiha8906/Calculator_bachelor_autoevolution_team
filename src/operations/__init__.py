"""Operations package for the Calculator application.

Aggregates all operation implementations: arithmetic, scientific, and roots.
Also re-exports Operation, OperationRegistry, and _CATALOG from the core
registry for backward compatibility with existing imports.
"""

from src.core.operations import Operation, OperationRegistry, _CATALOG
from .arithmetic import add, divide, multiply, subtract
from .roots import cube, cube_root, factorial, square, square_root
from .scientific import logarithm, natural_logarithm, power

__all__ = [
    # Registry (re-exported from core)
    "Operation",
    "OperationRegistry",
    "_CATALOG",
    # Arithmetic
    "add",
    "subtract",
    "multiply",
    "divide",
    # Scientific
    "power",
    "logarithm",
    "natural_logarithm",
    # Roots
    "factorial",
    "square",
    "cube",
    "square_root",
    "cube_root",
]
