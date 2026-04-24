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
            ValueError: If n is a bool, float, str, None, a non-int type,
                or a negative integer.
        """
        if isinstance(n, bool):
            raise ValueError("boolean values are not supported")
        if isinstance(n, float):
            raise ValueError("got float, expected int")
        if isinstance(n, str):
            raise ValueError("got str, expected int")
        if n is None:
            raise ValueError("got NoneType, expected int")
        if not isinstance(n, int):
            raise ValueError("expected int")
        if n < 0:
            raise ValueError("negative numbers are not supported")
        if n in (0, 1):
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

