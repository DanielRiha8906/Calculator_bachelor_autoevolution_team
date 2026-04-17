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

