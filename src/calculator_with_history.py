"""Stateful wrapper around Calculator that records a history of operations.

Intercepts every arithmetic operation delegated to the underlying Calculator,
records each successful operation as a formatted string, and provides
``get_history()`` for retrieving the accumulated log.
"""

import logging

from src.calculator import Calculator
from src.logger import get_logger

# Symbol used in formatted history entries, keyed by Calculator method name.
_METHOD_TO_SYMBOL: dict[str, str] = {
    "add": "+",
    "subtract": "-",
    "multiply": "*",
    "divide": "/",
}


class CalculatorWithHistory:
    """A stateful wrapper around Calculator that captures operation history.

    Each successful arithmetic call is appended to an internal list as a
    formatted string of the form ``"a OP b = result"``.  Failed operations
    (those that raise an exception) are not recorded.

    Attributes:
        _calculator: The underlying Calculator instance.
        _history: Accumulated list of formatted operation strings.
    """

    def __init__(self) -> None:
        """Initialise the wrapper with a fresh Calculator and empty history."""
        self._calculator: Calculator = Calculator()
        self._history: list[str] = []

    # ------------------------------------------------------------------
    # Binary arithmetic operations
    # ------------------------------------------------------------------

    def add(self, a: float, b: float) -> float:
        """Add two numbers, recording the operation in history.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The sum of a and b.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.add(a, b)
            self._history.append(f"{a} + {b} = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"add({a}, {b}) failed: {type(exc).__name__}: {exc}")
            raise

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a, recording the operation in history.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The difference a - b.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.subtract(a, b)
            self._history.append(f"{a} - {b} = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"subtract({a}, {b}) failed: {type(exc).__name__}: {exc}")
            raise

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers, recording the operation in history.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The product of a and b.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.multiply(a, b)
            self._history.append(f"{a} * {b} = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"multiply({a}, {b}) failed: {type(exc).__name__}: {exc}")
            raise

    def divide(self, a: float, b: float) -> float:
        """Divide a by b, recording the operation in history.

        Failed divisions (e.g. division by zero) are not recorded.

        Args:
            a: The numerator.
            b: The denominator.

        Returns:
            The quotient a / b.

        Raises:
            ZeroDivisionError: Propagated when b is zero.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.divide(a, b)
            self._history.append(f"{a} / {b} = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"divide({a}, {b}) failed: {type(exc).__name__}: {exc}")
            raise

    # ------------------------------------------------------------------
    # Unary operations (not recorded with infix notation; logged verbatim)
    # ------------------------------------------------------------------

    def factorial(self, n: int) -> int:
        """Return the factorial of n.

        Args:
            n: A non-negative integer.

        Returns:
            The factorial of n.

        Raises:
            ValueError: Propagated for non-integer or negative n.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.factorial(n)
            self._history.append(f"factorial({n}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"factorial({n}) failed: {type(exc).__name__}: {exc}")
            raise

    def square(self, x: float) -> float:
        """Return the square of x.

        Args:
            x: The number to square.

        Returns:
            x squared.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.square(x)
            self._history.append(f"square({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"square({x}) failed: {type(exc).__name__}: {exc}")
            raise

    def cube(self, x: float) -> float:
        """Return the cube of x.

        Args:
            x: The number to cube.

        Returns:
            x cubed.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.cube(x)
            self._history.append(f"cube({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"cube({x}) failed: {type(exc).__name__}: {exc}")
            raise

    def square_root(self, x: float) -> float:
        """Return the square root of x.

        Args:
            x: A non-negative number.

        Returns:
            The square root of x.

        Raises:
            ValueError: Propagated for negative x.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.square_root(x)
            self._history.append(f"square_root({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"square_root({x}) failed: {type(exc).__name__}: {exc}")
            raise

    def cube_root(self, x: float) -> float:
        """Return the real cube root of x.

        Args:
            x: The number whose cube root is to be computed.

        Returns:
            The real cube root of x.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.cube_root(x)
            self._history.append(f"cube_root({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"cube_root({x}) failed: {type(exc).__name__}: {exc}")
            raise

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the given exponent.

        Args:
            base: The base number.
            exponent: The exponent.

        Returns:
            base ** exponent.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.power(base, exponent)
            self._history.append(f"power({base}, {exponent}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"power({base}, {exponent}) failed: {type(exc).__name__}: {exc}")
            raise

    def log(self, x: float) -> float:
        """Return the base-10 logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            log10(x).

        Raises:
            ValueError: Propagated for non-positive x.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.log(x)
            self._history.append(f"log({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"log({x}) failed: {type(exc).__name__}: {exc}")
            raise

    def ln(self, x: float) -> float:
        """Return the natural logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            ln(x).

        Raises:
            ValueError: Propagated for non-positive x.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.ln(x)
            self._history.append(f"ln({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"ln({x}) failed: {type(exc).__name__}: {exc}")
            raise

    # ------------------------------------------------------------------
    # Scientific unary operations
    # ------------------------------------------------------------------

    def sin(self, x: float) -> float:
        """Return the sine of x (in radians), recording the operation in history.

        Args:
            x: The angle in radians.

        Returns:
            The sine of x.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.sin(x)
            self._history.append(f"sin({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"sin({x}) failed: {type(exc).__name__}: {exc}")
            raise

    def cos(self, x: float) -> float:
        """Return the cosine of x (in radians), recording the operation in history.

        Args:
            x: The angle in radians.

        Returns:
            The cosine of x.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.cos(x)
            self._history.append(f"cos({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"cos({x}) failed: {type(exc).__name__}: {exc}")
            raise

    def tan(self, x: float) -> float:
        """Return the tangent of x (in radians), recording the operation in history.

        Args:
            x: The angle in radians.

        Returns:
            The tangent of x.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.tan(x)
            self._history.append(f"tan({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"tan({x}) failed: {type(exc).__name__}: {exc}")
            raise

    def exp(self, x: float) -> float:
        """Return e raised to the power of x, recording the operation in history.

        Args:
            x: The exponent.

        Returns:
            e ** x.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.exp(x)
            self._history.append(f"exp({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"exp({x}) failed: {type(exc).__name__}: {exc}")
            raise

    def sqrt(self, x: float) -> float:
        """Return the square root of x, recording the operation in history.

        Args:
            x: A non-negative number.

        Returns:
            The square root of x.

        Raises:
            ValueError: Propagated for negative x.
        """
        logger = get_logger(__name__)
        try:
            result = self._calculator.sqrt(x)
            self._history.append(f"sqrt({x}) = {result}")
            return result
        except (ValueError, ZeroDivisionError, TypeError, OverflowError) as exc:
            logger.error(f"sqrt({x}) failed: {type(exc).__name__}: {exc}")
            raise

    # ------------------------------------------------------------------
    # History access
    # ------------------------------------------------------------------

    def get_history(self) -> list[str]:
        """Return a copy of the accumulated operation history.

        Each entry is a formatted string such as ``"2.0 + 3.0 = 5.0"``.
        Only successfully completed operations are included; calls that
        raised an exception are omitted.

        Returns:
            A list of formatted operation strings in chronological order.
        """
        return list(self._history)
