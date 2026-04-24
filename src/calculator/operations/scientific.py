"""Scientific operation implementations for the modular calculator.

Provides seven concrete Operation subclasses for scientific calculations:
square, cube, square_root, cube_root, power, log10, and ln.
"""

import math

from src.calculator.operations import Operation


class ScientificSquare(Operation):
    """Square of a number."""

    @property
    def name(self) -> str:
        return "square"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return a ** 2.

        Args:
            a: The number to square.

        Returns:
            a raised to the power of 2.
        """
        return a ** 2


class ScientificCube(Operation):
    """Cube of a number."""

    @property
    def name(self) -> str:
        return "cube"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return a ** 3.

        Args:
            a: The number to cube.

        Returns:
            a raised to the power of 3.
        """
        return a ** 3


class ScientificSquareRoot(Operation):
    """Square root of a non-negative number."""

    @property
    def name(self) -> str:
        return "square_root"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the square root of a.

        Args:
            a: A non-negative real number.

        Returns:
            The principal square root of a.

        Raises:
            ValueError: If a is negative.
        """
        if a < 0:
            raise ValueError("square_root() is not defined for negative numbers")
        return math.sqrt(a)


class ScientificCubeRoot(Operation):
    """Real cube root of a number (supports negative inputs)."""

    @property
    def name(self) -> str:
        return "cube_root"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the real cube root of a.

        Args:
            a: A real number (including negatives).

        Returns:
            The real cube root of a, preserving the sign for negative inputs.
        """
        return math.pow(abs(a), 1 / 3) * (-1 if a < 0 else 1)


class ScientificPower(Operation):
    """Raise a base to an exponent."""

    @property
    def name(self) -> str:
        return "power"

    @property
    def arity(self) -> int:
        return 2

    def execute(self, a: float, b: float) -> float:
        """Return a ** b.

        Args:
            a: The base value.
            b: The exponent value.

        Returns:
            a raised to the power of b.
        """
        return a ** b


class ScientificLog10(Operation):
    """Base-10 logarithm of a positive number."""

    @property
    def name(self) -> str:
        return "log10"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return log base-10 of a.

        Args:
            a: A positive real number.

        Returns:
            The base-10 logarithm of a.

        Raises:
            ValueError: If a is zero or negative.
        """
        if a <= 0:
            raise ValueError("log10() is not defined for non-positive numbers")
        return math.log10(a)


class ScientificLn(Operation):
    """Natural logarithm of a positive number."""

    @property
    def name(self) -> str:
        return "ln"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the natural logarithm of a.

        Args:
            a: A positive real number.

        Returns:
            The natural logarithm of a.

        Raises:
            ValueError: If a is zero or negative.
        """
        if a <= 0:
            raise ValueError("ln() is not defined for non-positive numbers")
        return math.log(a)
