"""Extensible operations framework for the Calculator application.

This module provides :class:`OperationRegistry`, which manages operation
categories and dispatch.  It contains no UI, printing, or interactive
concerns — it is part of the core calculation layer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .calculator import Calculator


class OperationRegistry:
    """Manages operation categories and dispatch.

    Normal mode operations are registered in _normal_operations.
    Future scientific mode operations will go in _scientific_operations.
    """

    def __init__(self, calculator: "Calculator") -> None:
        """Initialise the registry and load standard operations.

        Args:
            calculator: A :class:`~src.core.calculator.Calculator` instance
                whose bound methods are stored in the registry.
        """
        self._calculator = calculator
        self._normal_operations: dict[str, tuple] = {}
        self._scientific_operations: dict[str, tuple] = {}
        self._load_normal_operations()

    def _load_normal_operations(self) -> None:
        """Load all standard calculator operations."""
        # Binary operations (2 operands)
        self._register_op("add", self._calculator.add, 2)
        self._register_op("subtract", self._calculator.subtract, 2)
        self._register_op("multiply", self._calculator.multiply, 2)
        self._register_op("divide", self._calculator.divide, 2)
        self._register_op("power", self._calculator.power, 2)
        # Unary operations (1 operand)
        self._register_op("factorial", self._calculator.factorial, 1)
        self._register_op("square", self._calculator.square, 1)
        self._register_op("cube", self._calculator.cube, 1)
        self._register_op("square_root", self._calculator.square_root, 1)
        self._register_op("cube_root", self._calculator.cube_root, 1)
        self._register_op("log", self._calculator.log, 1)
        self._register_op("ln", self._calculator.ln, 1)

    def _register_op(self, name: str, method: object, arity: int) -> None:
        """Register an operation in the normal operations dict.

        Args:
            name: The operation name key.
            method: The bound calculator method to invoke.
            arity: The number of operands the operation expects.
        """
        self._normal_operations[name] = (method, arity)

    def get_all_operations(self) -> dict[str, tuple]:
        """Return all available operations (normal + scientific).

        Returns:
            A dict mapping operation name (str) to a 2-tuple of
            ``(method, arity)``.
        """
        return {**self._normal_operations, **self._scientific_operations}

    def get_normal_operations(self) -> dict[str, tuple]:
        """Return only normal mode operations.

        Returns:
            A dict mapping operation name (str) to a 2-tuple of
            ``(method, arity)``.
        """
        return dict(self._normal_operations)
