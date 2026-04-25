"""Scientific operation implementations for the modular calculator.

Provides nineteen concrete Operation subclasses for scientific calculations:
square, cube, square_root, cube_root, power, log10, ln, sin, cos, tan,
asin, acos, atan, sinh, cosh, tanh, exp, pi (constant), and e (constant).
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


class ScientificSin(Operation):
    """Sine of an angle given in radians."""

    @property
    def name(self) -> str:
        return "sin"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the sine of a (in radians).

        Args:
            a: Angle in radians.

        Returns:
            The sine of a.
        """
        return math.sin(a)


class ScientificCos(Operation):
    """Cosine of an angle given in radians."""

    @property
    def name(self) -> str:
        return "cos"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the cosine of a (in radians).

        Args:
            a: Angle in radians.

        Returns:
            The cosine of a.
        """
        return math.cos(a)


class ScientificTan(Operation):
    """Tangent of an angle given in radians."""

    @property
    def name(self) -> str:
        return "tan"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the tangent of a (in radians).

        Args:
            a: Angle in radians.

        Returns:
            The tangent of a.
        """
        return math.tan(a)


class ScientificAsin(Operation):
    """Arcsine (inverse sine) of a value in the domain [-1, 1]."""

    @property
    def name(self) -> str:
        return "asin"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the arcsine of a in radians.

        Args:
            a: A value in the domain [-1, 1].

        Returns:
            The arcsine of a in radians, in the range [-pi/2, pi/2].

        Raises:
            ValueError: If a is outside the domain [-1, 1].
        """
        if a < -1 or a > 1:
            raise ValueError(
                f"asin() domain error: argument {a} is outside [-1, 1]"
            )
        return math.asin(a)


class ScientificAcos(Operation):
    """Arccosine (inverse cosine) of a value in the domain [-1, 1]."""

    @property
    def name(self) -> str:
        return "acos"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the arccosine of a in radians.

        Args:
            a: A value in the domain [-1, 1].

        Returns:
            The arccosine of a in radians, in the range [0, pi].

        Raises:
            ValueError: If a is outside the domain [-1, 1].
        """
        if a < -1 or a > 1:
            raise ValueError(
                f"acos() domain error: argument {a} is outside [-1, 1]"
            )
        return math.acos(a)


class ScientificAtan(Operation):
    """Arctangent (inverse tangent) of a value."""

    @property
    def name(self) -> str:
        return "atan"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the arctangent of a in radians.

        Args:
            a: A real number (no domain restriction).

        Returns:
            The arctangent of a in radians, in the range (-pi/2, pi/2).
        """
        return math.atan(a)


class ScientificSinh(Operation):
    """Hyperbolic sine of a value."""

    @property
    def name(self) -> str:
        return "sinh"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the hyperbolic sine of a.

        Args:
            a: A real number.

        Returns:
            The hyperbolic sine of a.
        """
        return math.sinh(a)


class ScientificCosh(Operation):
    """Hyperbolic cosine of a value."""

    @property
    def name(self) -> str:
        return "cosh"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the hyperbolic cosine of a.

        Args:
            a: A real number.

        Returns:
            The hyperbolic cosine of a.
        """
        return math.cosh(a)


class ScientificTanh(Operation):
    """Hyperbolic tangent of a value."""

    @property
    def name(self) -> str:
        return "tanh"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return the hyperbolic tangent of a.

        Args:
            a: A real number.

        Returns:
            The hyperbolic tangent of a, in the range (-1, 1).
        """
        return math.tanh(a)


class ScientificExp(Operation):
    """Exponential function: e raised to the power of a."""

    @property
    def name(self) -> str:
        return "exp"

    @property
    def arity(self) -> int:
        return 1

    def execute(self, a: float) -> float:
        """Return e raised to the power of a.

        Args:
            a: The exponent.

        Returns:
            e ** a.
        """
        return math.exp(a)


class ScientificPi(Operation):
    """Mathematical constant pi (zero-operand constant operation)."""

    @property
    def name(self) -> str:
        return "pi"

    @property
    def arity(self) -> int:
        return 0

    def execute(self) -> float:
        """Return the mathematical constant pi.

        Returns:
            math.pi (~3.141592653589793).
        """
        return math.pi


class ScientificE(Operation):
    """Mathematical constant e (zero-operand constant operation)."""

    @property
    def name(self) -> str:
        return "e"

    @property
    def arity(self) -> int:
        return 0

    def execute(self) -> float:
        """Return the mathematical constant e.

        Returns:
            math.e (~2.718281828459045).
        """
        return math.e
