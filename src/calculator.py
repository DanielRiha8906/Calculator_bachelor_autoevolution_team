"""Calculator facade that composes arithmetic and advanced operation modules.

All public method signatures, docstrings, return types, and error behaviours
are identical to the original monolithic implementation.  Each Calculator
instance owns its own ArithmeticOperations, AdvancedOperations, and
ScientificOperations instances and delegates every call to the appropriate
module.
"""

from src.operations.arithmetic import ArithmeticOperations
from src.operations.advanced import AdvancedOperations
from src.operations.scientific import ScientificOperations


class Calculator:
    """A facade that delegates mathematical operations to specialised modules.

    Attributes:
        _arithmetic: Handles add, subtract, multiply, divide.
        _advanced: Handles factorial, square, cube, roots, power, log, ln.
        _scientific: Handles sin, cos, tan, log, ln, exp, sqrt.
    """

    def __init__(self) -> None:
        """Initialise the Calculator with dedicated operation module instances."""
        self._arithmetic: ArithmeticOperations = ArithmeticOperations()
        self._advanced: AdvancedOperations = AdvancedOperations()
        self._scientific: ScientificOperations = ScientificOperations()

    def add(self, a: float, b: float) -> float:
        return self._arithmetic.add(a, b)

    def subtract(self, a: float, b: float) -> float:
        return self._arithmetic.subtract(a, b)

    def multiply(self, a: float, b: float) -> float:
        return self._arithmetic.multiply(a, b)

    def divide(self, a: float, b: float) -> float:
        return self._arithmetic.divide(a, b)

    def factorial(self, n: int) -> int:
        """Return the factorial of n.

        Args:
            n: A non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n.

        Raises:
            ValueError: If n is not an integer or if n is negative.
        """
        return self._advanced.factorial(n)

    def square(self, x: float) -> float:
        """Return the square of x.

        Args:
            x: The number to square.

        Returns:
            x multiplied by itself.
        """
        return self._advanced.square(x)

    def cube(self, x: float) -> float:
        """Return the cube of x.

        Args:
            x: The number to cube.

        Returns:
            x multiplied by itself twice.
        """
        return self._advanced.cube(x)

    def square_root(self, x: float) -> float:
        """Return the square root of x.

        Args:
            x: A non-negative number.

        Returns:
            The square root of x.

        Raises:
            ValueError: If x is negative.
        """
        return self._advanced.square_root(x)

    def cube_root(self, x: float) -> float:
        """Return the real cube root of x, supporting negative inputs.

        Args:
            x: The number whose cube root is to be computed.

        Returns:
            The real cube root of x.
        """
        return self._advanced.cube_root(x)

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the given exponent.

        Args:
            base: The base number.
            exponent: The exponent to raise the base to.

        Returns:
            base raised to the power of exponent. Returns 1.0 when both
            base and exponent are 0.
        """
        return self._advanced.power(base, exponent)

    def log(self, x: float) -> float:
        """Return the base-10 logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        return self._advanced.log(x)

    def ln(self, x: float) -> float:
        """Return the natural (base-e) logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        return self._advanced.ln(x)

    # ------------------------------------------------------------------
    # Scientific operations (unary)
    # ------------------------------------------------------------------

    def sin(self, x: float) -> float:
        """Return the sine of x (in radians).

        Args:
            x: The angle in radians.

        Returns:
            The sine of x.
        """
        return self._scientific.sin(x)

    def cos(self, x: float) -> float:
        """Return the cosine of x (in radians).

        Args:
            x: The angle in radians.

        Returns:
            The cosine of x.
        """
        return self._scientific.cos(x)

    def tan(self, x: float) -> float:
        """Return the tangent of x (in radians).

        Args:
            x: The angle in radians.

        Returns:
            The tangent of x.
        """
        return self._scientific.tan(x)

    def exp(self, x: float) -> float:
        """Return e raised to the power of x.

        Args:
            x: The exponent.

        Returns:
            e ** x.
        """
        return self._scientific.exp(x)

    def sqrt(self, x: float) -> float:
        """Return the square root of x.

        Args:
            x: A non-negative number.

        Returns:
            The square root of x.

        Raises:
            ValueError: If x is negative.
        """
        return self._scientific.sqrt(x)
