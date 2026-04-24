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
        """Return the factorial of a non-negative integer n.

        Args:
            n: A non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n.

        Raises:
            TypeError: If n is not an integer (booleans are rejected).
            ValueError: If n is negative.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("Factorial requires a non-negative integer")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        return math.factorial(n)

