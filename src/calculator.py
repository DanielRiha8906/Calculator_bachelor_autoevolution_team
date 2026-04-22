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

