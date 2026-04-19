"""Operation registry for the Calculator application.

This module provides :func:`get_operation_registry`, which maps operation
names to their bound calculator methods and arity.  It contains no UI,
printing, or interactive concerns — it is part of the core calculation layer.

Internally the registry is built by :class:`~src.core.operations_manager.OperationRegistry`;
the return value format is identical to the previous implementation so all
existing callers remain unaffected.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .operations_manager import OperationRegistry

if TYPE_CHECKING:
    from .calculator import Calculator


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
    registry = OperationRegistry(calculator)
    return registry.get_all_operations()
