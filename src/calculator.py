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
        """
        Compute the factorial of n (n!).

        Args:
            n: A non-negative integer.

        Returns:
            The factorial of n.

        Raises:
            ValueError: If n is negative or not an integer.
        """
        if not isinstance(n, int) or isinstance(n, bool):
            raise ValueError("Factorial is only defined for non-negative integers")
        if n < 0:
            raise ValueError("Factorial is only defined for non-negative integers")
        return math.factorial(n)

