import math


class Calculator:
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

