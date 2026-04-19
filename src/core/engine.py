"""Core arithmetic engine for the Calculator application.

Provides the CalculationEngine class with basic arithmetic operations.
Scientific and root operations remain in the Calculator class which wraps
this engine.
"""


class CalculationEngine:
    """Perform basic arithmetic operations.

    This class handles only the four fundamental arithmetic operations.
    Scientific and root operations (factorial, power, logarithms, etc.) are
    provided by the Calculator class which delegates to this engine internally.
    """

    def add(self, a: float, b: float) -> float:
        """Return the sum of a and b.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            a + b.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Return the difference of a and b.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            a - b.
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Return the product of a and b.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            a * b.
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Return the quotient of a divided by b.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            a / b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
