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
        """Return the factorial of n.

        Args:
            n: A non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n as an integer.

        Raises:
            TypeError: If n is a boolean or not an integer.
            ValueError: If n is a negative integer.
        """
        if isinstance(n, bool):
            raise TypeError(
                f"factorial() does not accept boolean values, got {n!r}"
            )
        if not isinstance(n, int):
            raise TypeError(
                f"factorial() only accepts non-negative integers, got {type(n).__name__!r}"
            )
        if n < 0:
            raise ValueError(
                f"factorial() is not defined for negative integers, got {n!r}"
            )
        return math.factorial(n)

