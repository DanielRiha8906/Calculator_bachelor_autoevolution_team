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
        if not isinstance(n, int) or isinstance(n, bool):
            raise TypeError("n must be an int")
        if n < 0:
            raise ValueError("n must be >= 0")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

