"""Pure calculation core — independent of all UI and infrastructure layers.

This module is the PURE CALCULATION CORE of the calculator system.  It has
NO dependency on interactive.py, cli.py, history.py, or error_logger.py and
can be imported and reused in any context without pulling in any UI-layer
module.

The ``Calculator`` class raises only standard Python exceptions:
- ``ValueError`` for invalid inputs (e.g. negative factorial, log of zero).
- ``ZeroDivisionError`` for division by zero.

Supported operation categories
--------------------------------
Binary (two operands):
    add, subtract, multiply, divide, power

Unary (one operand):
    factorial, square, cube, sqrt, cbrt, ln, log10
"""

import math


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b

    def factorial(self, n: int) -> int:
        """Compute the factorial of a non-negative integer.

        Args:
            n: A non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n as an integer.

        Raises:
            ValueError: If n is a bool, float, str, None, a non-int type,
                or a negative integer.
        """
        if isinstance(n, bool):
            raise ValueError("boolean values are not supported")
        if isinstance(n, float):
            raise ValueError("got float, expected int")
        if isinstance(n, str):
            raise ValueError("got str, expected int")
        if n is None:
            raise ValueError("got NoneType, expected int")
        if not isinstance(n, int):
            raise ValueError("expected int")
        if n < 0:
            raise ValueError("negative numbers are not supported")
        if n in (0, 1):
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def square(self, x: int | float) -> int | float:
        """Return the square of x.

        Args:
            x: A real number.

        Returns:
            x raised to the power of 2.
        """
        return x ** 2

    def cube(self, x: int | float) -> int | float:
        """Return the cube of x.

        Args:
            x: A real number.

        Returns:
            x raised to the power of 3.
        """
        return x ** 3

    def sqrt(self, x: int | float) -> float:
        """Return the square root of x.

        Args:
            x: A non-negative real number.

        Returns:
            The square root of x as a float.

        Raises:
            ValueError: If x is negative.
        """
        if x < 0:
            raise ValueError("square root of negative numbers is not supported")
        return math.sqrt(x)

    def cbrt(self, x: int | float) -> float:
        """Return the cube root of x.

        Args:
            x: A real number.

        Returns:
            The cube root of x as a float.
        """
        if x < 0:
            return -math.pow(-x, 1 / 3)
        return math.pow(x, 1 / 3)

    def log10(self, x: int | float) -> float:
        """Return the base-10 logarithm of x.

        Args:
            x: A positive real number.

        Returns:
            The base-10 logarithm of x as a float.

        Raises:
            ValueError: If x is zero or negative.
        """
        if x <= 0:
            raise ValueError("logarithm of non-positive numbers is not supported")
        return math.log10(x)

    def ln(self, x: int | float) -> float:
        """Return the natural logarithm of x.

        Args:
            x: A positive real number.

        Returns:
            The natural logarithm of x as a float.

        Raises:
            ValueError: If x is zero or negative.
        """
        if x <= 0:
            raise ValueError("logarithm of non-positive numbers is not supported")
        return math.log(x)

    def power(self, base: int | float, exponent: int | float) -> int | float:
        """Return base raised to the power of exponent.

        Args:
            base: The base value.
            exponent: The exponent value.

        Returns:
            base raised to the power of exponent.
        """
        return base ** exponent

