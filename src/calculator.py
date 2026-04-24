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
            ValueError: If n is not an int, is a float, or is negative.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            raise ValueError(
                f"factorial() requires a non-negative integer, got {type(n).__name__!r}"
            )
        if n < 0:
            raise ValueError(
                f"factorial() is not defined for negative integers, got {n}"
            )
        return math.factorial(n)

    def square(self, x: float | int) -> float | int:
        """Compute x squared.

        Args:
            x: A real number to be squared.

        Returns:
            x raised to the power of 2.
        """
        return x ** 2

    def cube(self, x: float | int) -> float | int:
        """Compute x cubed.

        Args:
            x: A real number to be cubed (negative values preserve sign).

        Returns:
            x raised to the power of 3.
        """
        return x ** 3

    def square_root(self, x: float | int) -> float:
        """Compute the square root of x.

        Args:
            x: A non-negative real number.

        Returns:
            The principal square root of x as a float.

        Raises:
            ValueError: If x is negative.
        """
        if x < 0:
            raise ValueError("square_root() is not defined for negative numbers")
        return math.sqrt(x)

    def cube_root(self, x: float | int) -> float:
        """Compute the real cube root of x.

        Args:
            x: A real number (including negatives).

        Returns:
            The real cube root of x as a float.
        """
        if x >= 0:
            return x ** (1 / 3)
        return -((-x) ** (1 / 3))

    def power(self, base: float | int, exponent: float | int) -> float | int:
        """Compute base raised to the given exponent.

        Args:
            base: The base value.
            exponent: The exponent value.

        Returns:
            base raised to exponent.

        Raises:
            ValueError: If base is negative and exponent is not an integer.
        """
        if base < 0 and not isinstance(exponent, int):
            raise ValueError("power() with negative base requires integer exponent")
        return base ** exponent

    def log10(self, x: float | int) -> float:
        """Compute the base-10 logarithm of x.

        Args:
            x: A positive real number.

        Returns:
            The base-10 logarithm of x as a float.

        Raises:
            ValueError: If x is zero or negative.
        """
        if x <= 0:
            raise ValueError("log10() is not defined for non-positive numbers")
        return math.log10(x)

    def ln(self, x: float | int) -> float:
        """Compute the natural logarithm of x.

        Args:
            x: A positive real number.

        Returns:
            The natural logarithm of x as a float.

        Raises:
            ValueError: If x is zero or negative.
        """
        if x <= 0:
            raise ValueError("ln() is not defined for non-positive numbers")
        return math.log(x)

