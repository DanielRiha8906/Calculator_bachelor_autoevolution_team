"""advanced.py — advanced mathematical operations for the calculator modes package.

Provides :class:`AdvancedOperations`, which implements mathematical functions
beyond basic arithmetic.  Math logic is replicated from
:class:`~src.logic.CalculatorEngine` with history recording delegated to an
injected callback.
"""

from __future__ import annotations

import math
from typing import Callable, Optional, Union

from .operations import BaseOperationSet

from ..logger import get_logger

logger = get_logger(__name__)

Numeric = Union[int, float]


class AdvancedOperations(BaseOperationSet):
    """Implements advanced mathematical operations.

    Each method performs a pure computation and, if a ``record_callback``
    was supplied at construction time, invokes it with the result before
    returning.  Error handling and logging mirror the behaviour found in
    :class:`~src.logic.CalculatorEngine`.

    Args:
        record_callback: An optional callable that accepts a single positional
            argument (the numeric result).  Used for history recording.
    """

    def __init__(self, record_callback: Optional[Callable] = None) -> None:
        """Initialise AdvancedOperations with an optional history callback."""
        super().__init__(record_callback)

    # ------------------------------------------------------------------
    # BaseOperationSet interface
    # ------------------------------------------------------------------

    def get_operations(self) -> dict[str, Callable]:
        """Return a mapping of operation name to bound method.

        Returns:
            A dict with keys for each advanced operation mapped to the
            corresponding method.
        """
        return {
            "factorial": self.factorial,
            "square": self.square,
            "cube": self.cube,
            "square_root": self.square_root,
            "cube_root": self.cube_root,
            "power": self.power,
            "natural_log": self.natural_log,
            "log_base_10": self.log_base_10,
        }

    # ------------------------------------------------------------------
    # Advanced operation methods
    # ------------------------------------------------------------------

    def factorial(self, n: int) -> int:
        """Compute the factorial of a non-negative integer *n*.

        Args:
            n: The non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of *n* (n!).

        Raises:
            TypeError: If *n* is not an integer (e.g. float, str, list, None).
            ValueError: If *n* is a negative integer.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            exc = TypeError(
                f"factorial() requires a non-negative integer, got {type(n).__name__}"
            )
            logger.error(
                "factorial() failed: operand=%r %s: %s",
                n,
                type(exc).__name__,
                exc,
            )
            raise exc
        if n < 0:
            exc = ValueError(
                f"factorial() is not defined for negative integers, got {n}"
            )
            logger.error(
                "factorial() failed: operand=%r %s: %s",
                n,
                type(exc).__name__,
                exc,
            )
            raise exc
        result = 1
        for i in range(2, n + 1):
            result *= i
        self._record(result)
        return result

    def square(self, x: float) -> float:
        """Return the square of *x* (x²).

        Args:
            x: The number to square.

        Returns:
            *x* multiplied by itself.
        """
        result = x * x
        self._record(result)
        return result

    def cube(self, x: float) -> float:
        """Return the cube of *x* (x³).

        Args:
            x: The number to cube.

        Returns:
            *x* multiplied by itself twice.
        """
        result = x * x * x
        self._record(result)
        return result

    def square_root(self, x: float) -> float:
        """Return the square root of *x* (√x).

        Args:
            x: The number to take the square root of.

        Returns:
            The non-negative square root of *x*.

        Raises:
            ValueError: If *x* is negative.
        """
        try:
            result = math.sqrt(x)
        except ValueError as exc:
            logger.error(
                "square_root() failed: operand=%r %s: %s",
                x,
                type(exc).__name__,
                exc,
            )
            raise
        self._record(result)
        return result

    def cube_root(self, x: float) -> float:
        """Return the real cube root of *x* (∛x).

        Supports negative inputs by preserving the sign.

        Args:
            x: The number to take the cube root of.

        Returns:
            The real cube root of *x*.
        """
        result = math.copysign(abs(x) ** (1 / 3), x)
        self._record(result)
        return result

    def power(self, base: float, exponent: float) -> float:
        """Return *base* raised to the given *exponent* (base^exponent).

        Args:
            base: The base number.
            exponent: The exponent to raise *base* to.

        Returns:
            *base* raised to the power of *exponent*.
        """
        result = base ** exponent
        self._record(result)
        return result

    def natural_log(self, x: float) -> float:
        """Return the natural logarithm of *x* (ln(x)).

        Args:
            x: The number to compute the natural log of.

        Returns:
            The natural logarithm of *x*.

        Raises:
            ValueError: If *x* is less than or equal to 0.
        """
        try:
            result = math.log(x)
        except ValueError as exc:
            logger.error(
                "natural_log() failed: operand=%r %s: %s",
                x,
                type(exc).__name__,
                exc,
            )
            raise
        self._record(result)
        return result

    def log_base_10(self, x: float) -> float:
        """Return the base-10 logarithm of *x* (log₁₀(x)).

        Args:
            x: The number to compute the base-10 log of.

        Returns:
            The base-10 logarithm of *x*.

        Raises:
            ValueError: If *x* is less than or equal to 0.
        """
        try:
            result = math.log10(x)
        except ValueError as exc:
            logger.error(
                "log_base_10() failed: operand=%r %s: %s",
                x,
                type(exc).__name__,
                exc,
            )
            raise
        self._record(result)
        return result
