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
            The factorial of n.

        Raises:
            ValueError: If n is not an integer or if n is negative.
        """
        if not isinstance(n, int):
            raise ValueError(f"factorial requires a non-negative integer, got {type(n).__name__!r}")
        if n < 0:
            raise ValueError(f"factorial is not defined for negative integers, got {n}")
        return math.factorial(n)

