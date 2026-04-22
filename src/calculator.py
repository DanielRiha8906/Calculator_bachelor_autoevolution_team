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
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError(
                f"factorial() argument must be an integer, not {type(n).__name__}"
            )
        if n < 0:
            raise ValueError("factorial() not defined for negative values")
        return math.factorial(n)

