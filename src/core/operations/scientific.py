"""Scientific and advanced operations for the Calculator."""

import math


class ScientificOperations:
    """Encapsulates scientific/advanced arithmetic operations."""

    @staticmethod
    def factorial(n: int) -> int:
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("n must be an int")
        if n < 0:
            raise ValueError("n must be >= 0")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def square(x: float) -> float:
        """Return x squared.

        Args:
            x: A real number (int or float).

        Returns:
            x raised to the power of 2, as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
        """
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError("x must be an int or float")
        return float(x ** 2)

    @staticmethod
    def cube(x: float) -> float:
        """Return x cubed.

        Args:
            x: A real number (int or float).

        Returns:
            x raised to the power of 3, as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
        """
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError("x must be an int or float")
        return float(x ** 3)

    @staticmethod
    def square_root(x: float) -> float:
        """Return the square root of x.

        Args:
            x: A non-negative real number (int or float).

        Returns:
            The square root of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
            ValueError: If x is negative.
        """
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError("x must be an int or float")
        if x < 0:
            raise ValueError("x must be non-negative for square root")
        return math.sqrt(x)

    @staticmethod
    def cube_root(x: float) -> float:
        """Return the real-valued cube root of x.

        Handles negative inputs correctly by preserving the sign.

        Args:
            x: A real number (int or float).

        Returns:
            The real cube root of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
        """
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError("x must be an int or float")
        return math.copysign(abs(x) ** (1 / 3), x)

    @staticmethod
    def logarithm(x: float) -> float:
        """Return the base-10 logarithm of x.

        Args:
            x: A positive real number (int or float).

        Returns:
            The base-10 logarithm of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
            ValueError: If x is zero or negative.
        """
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError("x must be an int or float")
        if x <= 0:
            raise ValueError("x must be positive for logarithm")
        return math.log10(x)

    @staticmethod
    def natural_logarithm(x: float) -> float:
        """Return the natural logarithm of x.

        Args:
            x: A positive real number (int or float).

        Returns:
            The natural logarithm of x as a float.

        Raises:
            TypeError: If x is not an int or float (bool excluded).
            ValueError: If x is zero or negative.
        """
        if not isinstance(x, (int, float)) or isinstance(x, bool):
            raise TypeError("x must be an int or float")
        if x <= 0:
            raise ValueError("x must be positive for natural logarithm")
        return math.log(x)

    @staticmethod
    def power(base: float, exponent: float) -> float:
        """Return base raised to the power of exponent.

        Args:
            base: A real number (int or float).
            exponent: A real number (int or float).

        Returns:
            base ** exponent as a float. 0 ** 0 returns 1.0.

        Raises:
            TypeError: If base or exponent is not an int or float (bool excluded).
        """
        if not isinstance(base, (int, float)) or isinstance(base, bool):
            raise TypeError("base must be an int or float")
        if not isinstance(exponent, (int, float)) or isinstance(exponent, bool):
            raise TypeError("exponent must be an int or float")
        return float(base ** exponent)
