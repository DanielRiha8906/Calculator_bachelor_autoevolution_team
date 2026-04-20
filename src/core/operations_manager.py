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

    Normal mode operations (6: add, subtract, multiply, divide, square,
    square_root) are registered in _normal_operations.  Scientific mode
    operations (12: power, cube, cube_root, factorial, log, ln, sin, cos,
    tan, cot, asin, acos) are registered in _scientific_operations.
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
        self._load_scientific_operations()

    def _load_normal_operations(self) -> None:
        """Load the 6 standard normal-mode calculator operations.

        Normal mode contains only the basic arithmetic and root operations:
        add, subtract, multiply, divide, square, square_root.
        """
        # Binary operations (2 operands)
        self._register_normal_op("add", self._calculator.add, 2)
        self._register_normal_op("subtract", self._calculator.subtract, 2)
        self._register_normal_op("multiply", self._calculator.multiply, 2)
        self._register_normal_op("divide", self._calculator.divide, 2)
        # Unary operations (1 operand)
        self._register_normal_op("square", self._calculator.square, 1)
        self._register_normal_op("square_root", self._calculator.square_root, 1)

    def _load_scientific_operations(self) -> None:
        """Load all scientific-mode calculator operations.

        Scientific operations extend normal mode with: power, cube, cube_root,
        factorial, log, ln, sin, cos, tan, cot, asin, acos.
        """
        # Binary operations (2 operands)
        self._register_scientific_op("power", self._calculator.power, 2)
        # Unary operations (1 operand)
        self._register_scientific_op("cube", self._calculator.cube, 1)
        self._register_scientific_op("cube_root", self._calculator.cube_root, 1)
        self._register_scientific_op("factorial", self._calculator.factorial, 1)
        self._register_scientific_op("log", self._calculator.log, 1)
        self._register_scientific_op("ln", self._calculator.ln, 1)
        self._register_scientific_op("sin", self._calculator.sin, 1)
        self._register_scientific_op("cos", self._calculator.cos, 1)
        self._register_scientific_op("tan", self._calculator.tan, 1)
        self._register_scientific_op("cot", self._calculator.cot, 1)
        self._register_scientific_op("asin", self._calculator.asin, 1)
        self._register_scientific_op("acos", self._calculator.acos, 1)

    def _register_normal_op(self, name: str, method: object, arity: int) -> None:
        """Register an operation in the normal operations dict.

        Args:
            name: The operation name key.
            method: The bound calculator method to invoke.
            arity: The number of operands the operation expects.
        """
        self._normal_operations[name] = (method, arity)

    def _register_scientific_op(self, name: str, method: object, arity: int) -> None:
        """Register an operation in the scientific operations dict.

        Args:
            name: The operation name key.
            method: The bound calculator method to invoke.
            arity: The number of operands the operation expects.
        """
        self._scientific_operations[name] = (method, arity)

    def get_normal_operations(self) -> dict[str, tuple]:
        """Return only the 6 normal-mode operations.

        Returns:
            A dict mapping operation name (str) to a 2-tuple of
            ``(method, arity)`` for the 6 normal-mode operations:
            add, subtract, multiply, divide, square, square_root.
        """
        return dict(self._normal_operations)

    def get_scientific_operations(self) -> dict[str, tuple]:
        """Return the full scientific-mode operation set.

        The scientific set combines all 6 normal operations with the 12
        additional scientific operations (power, cube, cube_root, factorial,
        log, ln, sin, cos, tan, cot, asin, acos), giving 18 total.

        Returns:
            A dict mapping operation name (str) to a 2-tuple of
            ``(method, arity)``.
        """
        return {**self._normal_operations, **self._scientific_operations}

    def get_all_operations(self) -> dict[str, tuple]:
        """Return all available operations (normal + scientific).

        This method exists for backward compatibility with callers that do
        not yet distinguish between modes.

        Returns:
            A dict mapping operation name (str) to a 2-tuple of
            ``(method, arity)``.
        """
        return {**self._normal_operations, **self._scientific_operations}
