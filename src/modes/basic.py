"""basic.py — basic arithmetic operations for the calculator modes package.

Provides :class:`BasicOperations`, which implements the four fundamental
arithmetic operations.  All computation is pure; history recording is
handled via an injected callback so this module has no dependency on the
engine layer.
"""

from __future__ import annotations

from typing import Callable, Optional, Union

from .operations import BaseOperationSet

from ..logger import get_logger

logger = get_logger(__name__)

Numeric = Union[int, float]


class BasicOperations(BaseOperationSet):
    """Implements the four basic arithmetic operations.

    Each method performs a pure computation and, if a ``record_callback``
    was supplied at construction time, invokes it with the result before
    returning.

    Args:
        record_callback: An optional callable that accepts a single positional
            argument (the numeric result).  Used for history recording.
    """

    def __init__(self, record_callback: Optional[Callable] = None) -> None:
        """Initialise BasicOperations with an optional history callback."""
        super().__init__(record_callback)

    # ------------------------------------------------------------------
    # BaseOperationSet interface
    # ------------------------------------------------------------------

    def get_operations(self) -> dict[str, Callable]:
        """Return a mapping of operation name to bound method.

        Returns:
            A dict with keys ``"add"``, ``"subtract"``, ``"multiply"``,
            and ``"divide"``, each mapped to the corresponding method.
        """
        return {
            "add": self.add,
            "subtract": self.subtract,
            "multiply": self.multiply,
            "divide": self.divide,
        }

    # ------------------------------------------------------------------
    # Arithmetic methods
    # ------------------------------------------------------------------

    def add(self, a: Numeric, b: Numeric) -> Numeric:
        """Return the sum of *a* and *b*.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            ``a + b``.
        """
        result = a + b
        self._record(result)
        return result

    def subtract(self, a: Numeric, b: Numeric) -> Numeric:
        """Return the difference of *a* and *b*.

        Args:
            a: The minuend.
            b: The subtrahend.

        Returns:
            ``a - b``.
        """
        result = a - b
        self._record(result)
        return result

    def multiply(self, a: Numeric, b: Numeric) -> Numeric:
        """Return the product of *a* and *b*.

        Args:
            a: The first factor.
            b: The second factor.

        Returns:
            ``a * b``.
        """
        result = a * b
        self._record(result)
        return result

    def divide(self, a: Numeric, b: Numeric) -> float:
        """Return the quotient of *a* divided by *b*.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            ``a / b``.

        Raises:
            ZeroDivisionError: If *b* is zero.
        """
        try:
            result = a / b
        except ZeroDivisionError as exc:
            logger.error(
                "divide() failed: operands=(%r, %r) %s: %s",
                a,
                b,
                type(exc).__name__,
                exc,
            )
            raise
        self._record(result)
        return result
