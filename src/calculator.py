import math

from .logger import get_logger

logger = get_logger(__name__)


class Calculator:
    """Basic calculator with operation history tracking."""

    def __init__(self) -> None:
        """Initialise the Calculator with an empty history."""
        self._history: list[dict] = []

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _record_history(
        self,
        operand1,
        operator: str,
        operand2,
        result,
    ) -> None:
        """Append one operation record to the internal history list.

        Args:
            operand1: The primary (or only) operand.
            operator: The operation name (e.g. ``"add"``, ``"square"``).
            operand2: The second operand, or ``None`` for unary operations.
            result: The value returned by the operation.
        """
        self._history.append(
            {
                "operand1": operand1,
                "operator": operator,
                "operand2": operand2,
                "result": result,
            }
        )

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get_history(self) -> list[dict]:
        """Return the full list of recorded operations.

        Returns:
            A list of dicts, each with keys ``operand1``, ``operator``,
            ``operand2``, and ``result``.  The list is in chronological
            order.  One-operand operations store ``None`` for ``operand2``.
        """
        return self._history

    def add(self, a, b):
        result = a + b
        self._record_history(a, "add", b, result)
        return result

    def subtract(self, a, b):
        result = a - b
        self._record_history(a, "subtract", b, result)
        return result

    def multiply(self, a, b):
        result = a * b
        self._record_history(a, "multiply", b, result)
        return result

    def divide(self, a, b):
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
        self._record_history(a, "divide", b, result)
        return result

    def factorial(self, n: int) -> int:
        """Compute the factorial of a non-negative integer n.

        Args:
            n: The non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n (n!).

        Raises:
            TypeError: If n is not an integer (e.g. float, str, list, None).
            ValueError: If n is a negative integer.
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
        self._record_history(n, "factorial", None, result)
        return result

    def square(self, x: float) -> float:
        """Return the square of x (x²).

        Args:
            x: The number to square.

        Returns:
            x multiplied by itself.
        """
        result = x * x
        self._record_history(x, "square", None, result)
        return result

    def cube(self, x: float) -> float:
        """Return the cube of x (x³).

        Args:
            x: The number to cube.

        Returns:
            x multiplied by itself twice.
        """
        result = x * x * x
        self._record_history(x, "cube", None, result)
        return result

    def square_root(self, x: float) -> float:
        """Return the square root of x (√x).

        Args:
            x: The number to take the square root of.

        Returns:
            The non-negative square root of x.

        Raises:
            ValueError: If x is negative.
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
        self._record_history(x, "square_root", None, result)
        return result

    def cube_root(self, x: float) -> float:
        """Return the real cube root of x (∛x).

        Supports negative inputs by preserving the sign.

        Args:
            x: The number to take the cube root of.

        Returns:
            The real cube root of x.
        """
        result = math.copysign(abs(x) ** (1 / 3), x)
        self._record_history(x, "cube_root", None, result)
        return result

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the given exponent (base^exponent).

        Args:
            base: The base number.
            exponent: The exponent to raise the base to.

        Returns:
            base raised to the power of exponent.
        """
        result = base ** exponent
        self._record_history(base, "power", exponent, result)
        return result

    def natural_log(self, x: float) -> float:
        """Return the natural logarithm of x (ln(x)).

        Args:
            x: The number to compute the natural log of.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
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
        self._record_history(x, "natural_log", None, result)
        return result

    def log_base_10(self, x: float) -> float:
        """Return the base-10 logarithm of x (log₁₀(x)).

        Args:
            x: The number to compute the base-10 log of.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
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
        self._record_history(x, "log_base_10", None, result)
        return result
