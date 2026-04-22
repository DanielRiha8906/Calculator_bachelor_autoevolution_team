"""scientific.py — scientific mathematical operations for the calculator modes package.

Provides :class:`ScientificOperations`, which implements trigonometric,
hyperbolic, exponential, and related functions.  All computation is pure;
history recording is handled via an injected callback so this module has no
dependency on the engine layer.
"""

from __future__ import annotations

import math
from typing import Callable, Optional, Union

from .operations import BaseOperationSet

from ..logger import get_logger

logger = get_logger(__name__)

Numeric = Union[int, float]


class ScientificOperations(BaseOperationSet):
    """Implements scientific mathematical operations.

    Each method performs a pure computation and, if a ``record_callback``
    was supplied at construction time, invokes it with the result before
    returning.  Error handling and logging mirror the behaviour found in
    :class:`~src.modes.advanced.AdvancedOperations`.

    Covered function families:

    - Trigonometric: sin, cos, tan, asin, acos, atan (all in radians)
    - Hyperbolic: sinh, cosh, tanh
    - Angle conversion: degrees, radians
    - Exponential / logarithmic: exp, ln

    Args:
        record_callback: An optional callable that accepts a single positional
            argument (the numeric result).  Used for history recording.
    """

    def __init__(self, record_callback: Optional[Callable] = None) -> None:
        """Initialise ScientificOperations with an optional history callback."""
        super().__init__(record_callback)

    # ------------------------------------------------------------------
    # BaseOperationSet interface
    # ------------------------------------------------------------------

    def get_operations(self) -> dict[str, Callable]:
        """Return a mapping of operation name to bound method.

        Returns:
            A dict whose keys are scientific operation name strings and whose
            values are the corresponding bound methods.
        """
        return {
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,
            "asin": self.asin,
            "acos": self.acos,
            "atan": self.atan,
            "sinh": self.sinh,
            "cosh": self.cosh,
            "tanh": self.tanh,
            "degrees": self.degrees,
            "radians": self.radians,
            "exp": self.exp,
            "ln": self.ln,
        }

    # ------------------------------------------------------------------
    # Trigonometric methods
    # ------------------------------------------------------------------

    def sin(self, x: Numeric) -> float:
        """Return the sine of *x* (given in radians).

        Args:
            x: The angle in radians.

        Returns:
            The sine of *x*.
        """
        result = math.sin(x)
        self._record(result)
        return result

    def cos(self, x: Numeric) -> float:
        """Return the cosine of *x* (given in radians).

        Args:
            x: The angle in radians.

        Returns:
            The cosine of *x*.
        """
        result = math.cos(x)
        self._record(result)
        return result

    def tan(self, x: Numeric) -> float:
        """Return the tangent of *x* (given in radians).

        Args:
            x: The angle in radians.

        Returns:
            The tangent of *x*.
        """
        result = math.tan(x)
        self._record(result)
        return result

    def asin(self, x: Numeric) -> float:
        """Return the arc sine of *x*, in radians.

        Args:
            x: A value in the interval [-1, 1].

        Returns:
            The arc sine of *x* in radians, in the range [-π/2, π/2].

        Raises:
            ValueError: If *x* is outside the interval [-1, 1].
        """
        try:
            result = math.asin(x)
        except ValueError as exc:
            logger.error(
                "asin() failed: operand=%r %s: %s",
                x,
                type(exc).__name__,
                exc,
            )
            raise
        self._record(result)
        return result

    def acos(self, x: Numeric) -> float:
        """Return the arc cosine of *x*, in radians.

        Args:
            x: A value in the interval [-1, 1].

        Returns:
            The arc cosine of *x* in radians, in the range [0, π].

        Raises:
            ValueError: If *x* is outside the interval [-1, 1].
        """
        try:
            result = math.acos(x)
        except ValueError as exc:
            logger.error(
                "acos() failed: operand=%r %s: %s",
                x,
                type(exc).__name__,
                exc,
            )
            raise
        self._record(result)
        return result

    def atan(self, x: Numeric) -> float:
        """Return the arc tangent of *x*, in radians.

        Args:
            x: Any real number.

        Returns:
            The arc tangent of *x* in radians, in the range [-π/2, π/2].
        """
        result = math.atan(x)
        self._record(result)
        return result

    # ------------------------------------------------------------------
    # Hyperbolic methods
    # ------------------------------------------------------------------

    def sinh(self, x: Numeric) -> float:
        """Return the hyperbolic sine of *x*.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic sine of *x*.
        """
        result = math.sinh(x)
        self._record(result)
        return result

    def cosh(self, x: Numeric) -> float:
        """Return the hyperbolic cosine of *x*.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic cosine of *x*.
        """
        result = math.cosh(x)
        self._record(result)
        return result

    def tanh(self, x: Numeric) -> float:
        """Return the hyperbolic tangent of *x*.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic tangent of *x*.
        """
        result = math.tanh(x)
        self._record(result)
        return result

    # ------------------------------------------------------------------
    # Angle conversion methods
    # ------------------------------------------------------------------

    def degrees(self, x: Numeric) -> float:
        """Convert angle *x* from radians to degrees.

        Args:
            x: The angle in radians.

        Returns:
            The equivalent angle in degrees.
        """
        result = math.degrees(x)
        self._record(result)
        return result

    def radians(self, x: Numeric) -> float:
        """Convert angle *x* from degrees to radians.

        Args:
            x: The angle in degrees.

        Returns:
            The equivalent angle in radians.
        """
        result = math.radians(x)
        self._record(result)
        return result

    # ------------------------------------------------------------------
    # Exponential / logarithmic methods
    # ------------------------------------------------------------------

    def exp(self, x: Numeric) -> float:
        """Return *e* raised to the power *x* (eˣ).

        Args:
            x: The exponent.

        Returns:
            e raised to the power *x*.
        """
        result = math.exp(x)
        self._record(result)
        return result

    def ln(self, x: Numeric) -> float:
        """Return the natural logarithm of *x* (ln(x)).

        This is an alias for the natural-log function, complementing the
        ``natural_log`` method already present in
        :class:`~src.modes.advanced.AdvancedOperations`.

        Args:
            x: A strictly positive real number.

        Returns:
            The natural logarithm of *x*.

        Raises:
            ValueError: If *x* is less than or equal to 0.
        """
        try:
            result = math.log(x)
        except ValueError as exc:
            logger.error(
                "ln() failed: operand=%r %s: %s",
                x,
                type(exc).__name__,
                exc,
            )
            raise
        self._record(result)
        return result
