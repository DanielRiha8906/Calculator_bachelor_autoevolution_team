"""Arithmetic operation module for the calculator application.

Provides basic binary arithmetic operations: addition, subtraction,
multiplication, and division.  Division by zero is caught and re-raised
as a ZeroDivisionError after logging the error.
"""

from src.logger import get_logger
from src.operations.base import OperationModule


class ArithmeticOperations(OperationModule):
    """Implements the four basic arithmetic operations.

    All methods mirror the signatures and error behaviour of the
    original Calculator class so that the Calculator facade can
    delegate to this module transparently.
    """

    def add(self, a: float, b: float) -> float:
        """Return the sum of a and b.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The sum a + b.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Return the difference a minus b.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The difference a - b.
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Return the product of a and b.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            The product a * b.
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Return the quotient of a divided by b.

        Args:
            a: The numerator.
            b: The denominator.

        Returns:
            The quotient a / b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        logger = get_logger(__name__)
        if b == 0:
            logger.error(f"Division by zero: {a} / {b}")
            raise ZeroDivisionError("division by zero")
        return a / b
