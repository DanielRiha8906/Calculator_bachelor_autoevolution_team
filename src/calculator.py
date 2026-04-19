class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def factorial(self, n) -> int:
        """Calculate the factorial of n.

        Args:
            n: A non-negative integer, or a float representing a whole number
               (e.g. 5.0). Must satisfy n >= 0.

        Returns:
            The factorial of n as an integer.

        Raises:
            TypeError: If n is a float with a non-integer value (e.g. 5.5).
            ValueError: If n is negative.
        """
        if isinstance(n, float):
            if n != int(n):
                raise TypeError("factorial() only accepts integer values, not non-integer floats")
            n = int(n)
        if n < 0:
            raise ValueError("factorial() not defined for negative values")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

