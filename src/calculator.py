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
            n: A non-negative integer. bool values are accepted and treated
               as their integer equivalents (False -> 0, True -> 1).

        Returns:
            The factorial of n as an integer. factorial(0) and factorial(1)
            both return 1.

        Raises:
            TypeError: If n is not an int (or bool). Floats, strings, None,
                and other types are rejected.
            ValueError: If n is a negative integer.

        Examples:
            >>> calc = Calculator()
            >>> calc.factorial(0)
            1
            >>> calc.factorial(5)
            120
        """
        if not isinstance(n, int):
            raise TypeError(
                f"factorial() requires an integer argument, got {type(n).__name__!r}"
            )
        if n < 0:
            raise ValueError(
                f"factorial() is not defined for negative integers, got {n}"
            )
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

