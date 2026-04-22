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
            raise TypeError(
                f"factorial() requires a non-negative integer, got {type(n).__name__}"
            )
        if n < 0:
            raise ValueError(
                f"factorial() is not defined for negative integers, got {n}"
            )
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def square(self, x: float) -> float:
        """Return the square of x (x²).

        Args:
            x: The number to square.

        Returns:
            x multiplied by itself.
        """
        return x * x

    def cube(self, x: float) -> float:
        """Return the cube of x (x³).

        Args:
            x: The number to cube.

        Returns:
            x multiplied by itself twice.
        """
        return x * x * x

    def square_root(self, x: float) -> float:
        """Return the square root of x (√x).

        Args:
            x: The number to take the square root of.

        Returns:
            The non-negative square root of x.

        Raises:
            ValueError: If x is negative.
        """
        return math.sqrt(x)

    def cube_root(self, x: float) -> float:
        """Return the real cube root of x (∛x).

        Supports negative inputs by preserving the sign.

        Args:
            x: The number to take the cube root of.

        Returns:
            The real cube root of x.
        """
        return math.copysign(abs(x) ** (1 / 3), x)

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the given exponent (base^exponent).

        Args:
            base: The base number.
            exponent: The exponent to raise the base to.

        Returns:
            base raised to the power of exponent.
        """
        return base ** exponent

    def natural_log(self, x: float) -> float:
        """Return the natural logarithm of x (ln(x)).

        Args:
            x: The number to compute the natural log of.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
        """
        return math.log(x)

    def log_base_10(self, x: float) -> float:
        """Return the base-10 logarithm of x (log₁₀(x)).

        Args:
            x: The number to compute the base-10 log of.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is less than or equal to 0.
        """
        return math.log10(x)

