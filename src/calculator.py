"""Calculation engine layer.

Contains the Calculator class which handles all mathematical operations
with no I/O side effects.
"""

import math


class Calculator:
    """Pure calculation engine.

    All methods perform arithmetic operations and return results.
    No input/output or user interaction occurs in this class.
    """
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        """Divide a by b.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            The result of a divided by b.

        Raises:
            ValueError: If b is zero.
        """
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b

    def factorial(self, n: int) -> int:
        """Compute the factorial of a non-negative integer.

        Args:
            n: The non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n (n!).

        Raises:
            ValueError: If n is not an integer.
            ValueError: If n is negative.
        """
        if not isinstance(n, int):
            raise ValueError(f"n must be an integer, got {type(n).__name__}")
        if n < 0:
            raise ValueError(f"n must be a non-negative integer, got {n}")
        return math.factorial(n)

    def square(self, x: float) -> float:
        """Compute the square of a number.

        Args:
            x: The operand.

        Returns:
            x squared (x ** 2).
        """
        return x ** 2

    def cube(self, x: float) -> float:
        """Compute the cube of a number.

        Args:
            x: The operand.

        Returns:
            x cubed (x ** 3).
        """
        return x ** 3

    def square_root(self, x: float) -> float:
        """Compute the square root of a non-negative number.

        Args:
            x: The operand. Must be non-negative.

        Returns:
            The square root of x.

        Raises:
            ValueError: If x is negative.
        """
        if x < 0:
            raise ValueError(f"square_root requires a non-negative number, got {x}")
        return math.sqrt(x)

    def cube_root(self, x: float) -> float:
        """Compute the cube root of a number.

        Negative inputs are supported via Python 3.12 math.cbrt.

        Args:
            x: The operand.

        Returns:
            The cube root of x.
        """
        return math.cbrt(x)

    def power(self, base: float, exponent: float) -> float:
        """Raise base to the given exponent.

        Args:
            base: The base value.
            exponent: The exponent to raise the base to.

        Returns:
            base raised to the power of exponent (base ** exponent).
        """
        return base ** exponent

    def log(self, x: float) -> float:
        """Compute the base-10 logarithm of a positive number.

        Args:
            x: The operand. Must be positive.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        if x <= 0:
            raise ValueError(f"log requires a positive number, got {x}")
        return math.log10(x)

    def ln(self, x: float) -> float:
        """Compute the natural logarithm (base e) of a positive number.

        Args:
            x: The operand. Must be positive.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        if x <= 0:
            raise ValueError(f"ln requires a positive number, got {x}")
        return math.log(x)

