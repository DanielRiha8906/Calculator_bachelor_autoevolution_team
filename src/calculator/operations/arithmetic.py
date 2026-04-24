"""Arithmetic operation implementations for the modular calculator.

Provides six concrete Operation subclasses for basic arithmetic:
add, subtract, multiply, divide, factorial, and modulo.
"""

import math

from src.calculator.operations import Operation


class ArithmeticAdd(Operation):
    """Addition of two numbers."""

    @property
    def name(self) -> str:
        return "add"

    @property
    def arity(self) -> int:
        return 2

    def execute(self, a: float, b: float) -> float:
        """Return a + b.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            The sum of a and b.
        """
        return a + b


class ArithmeticSubtract(Operation):
    """Subtraction of two numbers."""

    @property
    def name(self) -> str:
        return "subtract"

    @property
    def arity(self) -> int:
        return 2

    def execute(self, a: float, b: float) -> float:
        """Return a - b.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            The difference of a minus b.
        """
        return a - b


class ArithmeticMultiply(Operation):
    """Multiplication of two numbers."""

    @property
    def name(self) -> str:
        return "multiply"

    @property
    def arity(self) -> int:
        return 2

    def execute(self, a: float, b: float) -> float:
        """Return a * b.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            The product of a and b.
        """
        return a * b


class ArithmeticDivide(Operation):
    """Division of two numbers."""

    @property
    def name(self) -> str:
        return "divide"

    @property
    def arity(self) -> int:
        return 2

    def execute(self, a: float, b: float) -> float:
        """Return a / b.

        Args:
            a: Dividend.
            b: Divisor.

        Returns:
            The quotient of a divided by b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b


class ArithmeticFactorial(Operation):
    """Factorial of a non-negative integer."""

    @property
    def name(self) -> str:
        return "factorial"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the factorial of a.

        Args:
            a: A non-negative integer value.

        Returns:
            The factorial of a.

        Raises:
            ValueError: If a is not a non-negative integer.
        """
        n = int(a)
        if isinstance(a, bool) or a != n or n < 0:
            raise ValueError(
                f"factorial() requires a non-negative integer, got {a!r}"
            )
        return math.factorial(n)


class ArithmeticModulo(Operation):
    """Modulo (remainder) of two numbers."""

    @property
    def name(self) -> str:
        return "modulo"

    @property
    def arity(self) -> int:
        return 2

    def execute(self, a: float, b: float) -> float:
        """Return a % b.

        Args:
            a: Dividend.
            b: Divisor.

        Returns:
            The remainder of a divided by b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("modulo by zero")
        return a % b
