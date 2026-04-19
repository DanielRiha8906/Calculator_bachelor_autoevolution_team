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
            n: The non-negative integer whose factorial is to be computed.
                Float values are accepted only when they represent an exact
                integer (e.g. 5.0), in which case they are treated as int.

        Returns:
            The factorial of n (n!). Returns 1 when n is 0.

        Raises:
            TypeError: If n is not an int or a float that equals an integer
                value.
            ValueError: If n is negative.
        """
        if isinstance(n, bool):
            raise TypeError(
                f"Expected a non-negative integer, got {type(n).__name__}."
            )
        if isinstance(n, float):
            if not n.is_integer():
                raise TypeError(
                    f"Float value {n} is not an integer value; "
                    "cannot compute factorial."
                )
            n = int(n)
        if not isinstance(n, int):
            raise TypeError(
                f"Expected a non-negative integer, got {type(n).__name__}."
            )
        if n < 0:
            raise ValueError(
                f"Factorial is not defined for negative numbers; got {n}."
            )
        result: int = 1
        for i in range(2, n + 1):
            result *= i
        return result

