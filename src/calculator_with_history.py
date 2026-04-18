"""Stateful wrapper around Calculator that records a history of operations.

Intercepts every arithmetic operation delegated to the underlying Calculator,
records each successful operation as a formatted string, and provides
``get_history()`` for retrieving the accumulated log.
"""

from src.calculator import Calculator

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
        result = self._calculator.add(a, b)
        self._history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a, recording the operation in history.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The difference a - b.
        """
        result = self._calculator.subtract(a, b)
        self._history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers, recording the operation in history.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The product of a and b.
        """
        result = self._calculator.multiply(a, b)
        self._history.append(f"{a} * {b} = {result}")
        return result

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
        result = self._calculator.divide(a, b)
        self._history.append(f"{a} / {b} = {result}")
        return result

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
        result = self._calculator.factorial(n)
        self._history.append(f"factorial({n}) = {result}")
        return result

    def square(self, x: float) -> float:
        """Return the square of x.

        Args:
            x: The number to square.

        Returns:
            x squared.
        """
        result = self._calculator.square(x)
        self._history.append(f"square({x}) = {result}")
        return result

    def cube(self, x: float) -> float:
        """Return the cube of x.

        Args:
            x: The number to cube.

        Returns:
            x cubed.
        """
        result = self._calculator.cube(x)
        self._history.append(f"cube({x}) = {result}")
        return result

    def square_root(self, x: float) -> float:
        """Return the square root of x.

        Args:
            x: A non-negative number.

        Returns:
            The square root of x.

        Raises:
            ValueError: Propagated for negative x.
        """
        result = self._calculator.square_root(x)
        self._history.append(f"square_root({x}) = {result}")
        return result

    def cube_root(self, x: float) -> float:
        """Return the real cube root of x.

        Args:
            x: The number whose cube root is to be computed.

        Returns:
            The real cube root of x.
        """
        result = self._calculator.cube_root(x)
        self._history.append(f"cube_root({x}) = {result}")
        return result

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the given exponent.

        Args:
            base: The base number.
            exponent: The exponent.

        Returns:
            base ** exponent.
        """
        result = self._calculator.power(base, exponent)
        self._history.append(f"power({base}, {exponent}) = {result}")
        return result

    def log(self, x: float) -> float:
        """Return the base-10 logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            log10(x).

        Raises:
            ValueError: Propagated for non-positive x.
        """
        result = self._calculator.log(x)
        self._history.append(f"log({x}) = {result}")
        return result

    def ln(self, x: float) -> float:
        """Return the natural logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            ln(x).

        Raises:
            ValueError: Propagated for non-positive x.
        """
        result = self._calculator.ln(x)
        self._history.append(f"ln({x}) = {result}")
        return result

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
