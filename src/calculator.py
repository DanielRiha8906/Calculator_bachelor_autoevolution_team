"""Calculation engine layer.

Contains the Calculator class which handles all mathematical operations
with no I/O side effects.

Internally delegates to the operations subpackage modules:
  - operations.arithmetic  : add, subtract, multiply, divide
  - operations.exponents   : power, factorial, square, cube
  - operations.roots       : square_root, cube_root
  - operations.logarithmic : log, ln
"""

from src.operations import arithmetic, exponents, logarithmic, roots


class Calculator:
    """Pure calculation engine.

    All methods perform arithmetic operations and return results.
    No input/output or user interaction occurs in this class.
    """

    def add(self, a, b):
        return arithmetic.add(a, b)

    def subtract(self, a, b):
        return arithmetic.subtract(a, b)

    def multiply(self, a, b):
        return arithmetic.multiply(a, b)

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
        return arithmetic.divide(a, b)

    def factorial(self, n: int) -> int:
        """Compute the factorial of a non-negative integer.

        Args:
            n: The non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n (n!).

        Raises:
            ValueError: If n is not an integer.
            ValueError: If n is negative.
        """
        return exponents.factorial(n)

    def square(self, x: float) -> float:
        """Compute the square of a number.

        Args:
            x: The operand.

        Returns:
            x squared (x ** 2).
        """
        return exponents.square(x)

    def cube(self, x: float) -> float:
        """Compute the cube of a number.

        Args:
            x: The operand.

        Returns:
            x cubed (x ** 3).
        """
        return exponents.cube(x)

    def square_root(self, x: float) -> float:
        """Compute the square root of a non-negative number.

        Args:
            x: The operand. Must be non-negative.

        Returns:
            The square root of x.

        Raises:
            ValueError: If x is negative.
        """
        return roots.square_root(x)

    def cube_root(self, x: float) -> float:
        """Compute the cube root of a number.

        Negative inputs are supported via Python 3.12 math.cbrt.

        Args:
            x: The operand.

        Returns:
            The cube root of x.
        """
        return roots.cube_root(x)

    def power(self, base: float, exponent: float) -> float:
        """Raise base to the given exponent.

        Args:
            base: The base value.
            exponent: The exponent to raise the base to.

        Returns:
            base raised to the power of exponent (base ** exponent).
        """
        return exponents.power(base, exponent)

    def log(self, x: float) -> float:
        """Compute the base-10 logarithm of a positive number.

        Args:
            x: The operand. Must be positive.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        return logarithmic.log(x)

    def ln(self, x: float) -> float:
        """Compute the natural logarithm (base e) of a positive number.

        Args:
            x: The operand. Must be positive.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        return logarithmic.ln(x)
