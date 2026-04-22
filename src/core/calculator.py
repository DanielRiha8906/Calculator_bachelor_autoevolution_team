"""Refactored Calculator class that delegates to operation classes."""

from .operations.normal import NormalOperations
from .operations.scientific import ScientificOperations


class Calculator:
    """Calculator that delegates arithmetic to NormalOperations and ScientificOperations."""

    def add(self, a, b):
        return NormalOperations.add(a, b)

    def subtract(self, a, b):
        return NormalOperations.subtract(a, b)

    def multiply(self, a, b):
        return NormalOperations.multiply(a, b)

    def divide(self, a, b):
        return NormalOperations.divide(a, b)

    def factorial(self, n: int) -> int:
        return ScientificOperations.factorial(n)

    def square(self, x: float) -> float:
        """Return x squared.

        Args:
            x: A real number (int or float).

        Returns:
            x raised to the power of 2, as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
        """
        return ScientificOperations.square(x)

    def cube(self, x: float) -> float:
        """Return x cubed.

        Args:
            x: A real number (int or float).

        Returns:
            x raised to the power of 3, as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
        """
        return ScientificOperations.cube(x)

    def square_root(self, x: float) -> float:
        """Return the square root of x.

        Args:
            x: A non-negative real number (int or float).

        Returns:
            The square root of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
            ValueError: If x is negative.
        """
        return ScientificOperations.square_root(x)

    def cube_root(self, x: float) -> float:
        """Return the real-valued cube root of x.

        Handles negative inputs correctly by preserving the sign.

        Args:
            x: A real number (int or float).

        Returns:
            The real cube root of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
        """
        return ScientificOperations.cube_root(x)

    def logarithm(self, x: float) -> float:
        """Return the base-10 logarithm of x.

        Args:
            x: A positive real number (int or float).

        Returns:
            The base-10 logarithm of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
            ValueError: If x is zero or negative.
        """
        return ScientificOperations.logarithm(x)

    def natural_logarithm(self, x: float) -> float:
        """Return the natural logarithm of x.

        Args:
            x: A positive real number (int or float).

        Returns:
            The natural logarithm of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
            ValueError: If x is zero or negative.
        """
        return ScientificOperations.natural_logarithm(x)

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the power of exponent.

        Args:
            base: A real number (int or float).
            exponent: A real number (int or float).

        Returns:
            base ** exponent as a float. 0 ** 0 returns 1.0.

        Raises:
            TypeError: If base or exponent is not an int or float (bool excluded).
        """
        return ScientificOperations.power(base, exponent)

    def sin(self, x: float) -> float:
        """Return the sine of x (in radians).

        Args:
            x: A real number (int or float) representing an angle in radians.

        Returns:
            The sine of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
        """
        return ScientificOperations.sin(x)

    def cos(self, x: float) -> float:
        """Return the cosine of x (in radians).

        Args:
            x: A real number (int or float) representing an angle in radians.

        Returns:
            The cosine of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
        """
        return ScientificOperations.cos(x)

    def tan(self, x: float) -> float:
        """Return the tangent of x (in radians).

        Args:
            x: A real number (int or float) representing an angle in radians.

        Returns:
            The tangent of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
        """
        return ScientificOperations.tan(x)

    def cot(self, x: float) -> float:
        """Return the cotangent of x (in radians).

        Cotangent is defined as 1/tan(x), which is undefined when sin(x)==0.

        Args:
            x: A real number (int or float) representing an angle in radians.

        Returns:
            The cotangent of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
            ValueError: If sin(x) == 0 (cotangent is undefined).
        """
        return ScientificOperations.cot(x)

    def asin(self, x: float) -> float:
        """Return the arcsine of x, in radians.

        Args:
            x: A real number (int or float) in the range [-1, 1].

        Returns:
            The arcsine of x as a float (in radians).

        Raises:
            TypeError: If x is not an int or float (bool excluded).
            ValueError: If x is not in the range [-1, 1].
        """
        return ScientificOperations.asin(x)

    def acos(self, x: float) -> float:
        """Return the arccosine of x, in radians.

        Args:
            x: A real number (int or float) in the range [-1, 1].

        Returns:
            The arccosine of x as a float (in radians).

        Raises:
            TypeError: If x is not an int or float (bool excluded).
            ValueError: If x is not in the range [-1, 1].
        """
        return ScientificOperations.acos(x)
