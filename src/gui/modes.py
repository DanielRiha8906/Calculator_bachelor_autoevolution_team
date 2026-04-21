"""Calculator GUI mode abstractions.

This module defines the mode abstraction used by the GUI to determine which
set of operations to expose.  Two concrete modes are provided:

- :class:`SimpleMode` — the 6 standard arithmetic/root operations.
- :class:`ScientificMode` — all 18 operations including trigonometric,
  logarithmic, and exponential functions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.core.calculator import Calculator
from src.core.operations_manager import OperationRegistry


class CalcMode(ABC):
    """Base abstraction for calculator GUI modes.

    Concrete subclasses must supply a human-readable :attr:`name` and
    implement :meth:`get_operations` to return the set of operations that
    should be available in that mode.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name for this mode (e.g. ``"Simple"``)."""
        ...

    @abstractmethod
    def get_operations(self) -> dict[str, tuple]:
        """Return the operations available in this mode.

        Returns:
            A dict mapping operation name (str) to a 2-tuple of
            ``(callable, arity)`` where *arity* is 1 or 2.
        """
        ...


class SimpleMode(CalcMode):
    """Simple mode: only the 6 normal operations.

    Exposes: add, subtract, multiply, divide, square, square_root.

    Args:
        calculator: A :class:`~src.core.calculator.Calculator` instance whose
            bound methods will be used for dispatch.
    """

    def __init__(self, calculator: Calculator) -> None:
        self._registry = OperationRegistry(calculator)

    @property
    def name(self) -> str:
        """Return the mode name."""
        return "Simple"

    def get_operations(self) -> dict[str, tuple]:
        """Return the 6 normal-mode operations.

        Returns:
            Dict mapping op name to ``(callable, arity)``.
        """
        return self._registry.get_normal_operations()


class ScientificMode(CalcMode):
    """Scientific mode: all 18 operations.

    Exposes all normal operations plus: power, cube, cube_root, factorial,
    log, ln, sin, cos, tan, cot, asin, acos.

    Args:
        calculator: A :class:`~src.core.calculator.Calculator` instance whose
            bound methods will be used for dispatch.
    """

    def __init__(self, calculator: Calculator) -> None:
        self._registry = OperationRegistry(calculator)

    @property
    def name(self) -> str:
        """Return the mode name."""
        return "Scientific"

    def get_operations(self) -> dict[str, tuple]:
        """Return all 18 scientific-mode operations.

        Returns:
            Dict mapping op name to ``(callable, arity)``.
        """
        return self._registry.get_scientific_operations()
