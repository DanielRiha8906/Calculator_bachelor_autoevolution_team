"""Operation registry for the Calculator application.

This module provides :func:`get_operation_registry`, which maps operation
names to their bound calculator methods and arity.  It contains no UI,
printing, or interactive concerns — it is part of the core calculation layer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..calculator import Calculator


def get_operation_registry(calculator: "Calculator") -> dict[str, tuple]:
    """Build a registry of available calculator operations.

    Args:
        calculator: A ``Calculator`` instance whose bound methods are
            stored in the registry.

    Returns:
        A dict mapping operation name (str) to a 2-tuple of
        ``(method, arity)`` where *arity* is the number of operands
        the operation expects (1 for unary, 2 for binary).

    Examples:
        >>> from src.calculator import Calculator
        >>> registry = get_operation_registry(Calculator())
        >>> "add" in registry
        True
        >>> registry["add"][1]
        2
    """
    return {
        "add": (calculator.add, 2),
        "subtract": (calculator.subtract, 2),
        "multiply": (calculator.multiply, 2),
        "divide": (calculator.divide, 2),
        "power": (calculator.power, 2),
        "factorial": (calculator.factorial, 1),
        "square": (calculator.square, 1),
        "cube": (calculator.cube, 1),
        "square_root": (calculator.square_root, 1),
        "cube_root": (calculator.cube_root, 1),
        "log": (calculator.log, 1),
        "ln": (calculator.ln, 1),
    }
