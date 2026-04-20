"""Concrete operation classes for scientific arithmetic.

Each class wraps one scientific operation and conforms to the ``Operation``
interface.  All actual computation is performed using Python's ``math``
standard library.

``register_scientific_operations`` registers all 8 scientific operation
instances with a given ``OperationRegistry``.
"""

import math

from src.operations.base import Operation, OperationRegistry


class Sin(Operation):
    """Unary sine operation (input in radians)."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"sin"``
        """
        return "sin"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the sine of args[0] (in radians).

        Args:
            *args: Exactly one numeric operand.

        Returns:
            math.sin(args[0])
        """
        return math.sin(args[0])


class Cos(Operation):
    """Unary cosine operation (input in radians)."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"cos"``
        """
        return "cos"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the cosine of args[0] (in radians).

        Args:
            *args: Exactly one numeric operand.

        Returns:
            math.cos(args[0])
        """
        return math.cos(args[0])


class Tan(Operation):
    """Unary tangent operation (input in radians)."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"tan"``
        """
        return "tan"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the tangent of args[0] (in radians).

        Raises ValueError when cos(args[0]) is effectively zero (i.e. at odd
        multiples of pi/2) using a tolerance of 1e-9.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            math.tan(args[0])

        Raises:
            ValueError: If the tangent is undefined at the given value.
        """
        x = args[0]
        if abs(math.cos(x)) < 1e-9:
            raise ValueError(
                f"Tangent is undefined at x={x} (cos(x) is effectively zero)."
            )
        return math.tan(x)


class Exp(Operation):
    """Unary exponential operation (e^x)."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"exp"``
        """
        return "exp"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute e raised to the power of args[0].

        Args:
            *args: Exactly one numeric operand.

        Returns:
            math.exp(args[0])
        """
        return math.exp(args[0])


class Log(Operation):
    """Unary natural logarithm operation (base e)."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"log"``
        """
        return "log"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the natural logarithm of args[0].

        Args:
            *args: Exactly one numeric operand.

        Returns:
            math.log(args[0])

        Raises:
            ValueError: If args[0] is less than or equal to zero.
        """
        x = args[0]
        if x <= 0:
            raise ValueError(
                f"log is not defined for non-positive numbers; got {x}."
            )
        return math.log(x)


class Log10(Operation):
    """Unary base-10 logarithm operation (scientific variant)."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"log10"``
        """
        return "log10"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the base-10 logarithm of args[0].

        Args:
            *args: Exactly one numeric operand.

        Returns:
            math.log10(args[0])

        Raises:
            ValueError: If args[0] is less than or equal to zero.
        """
        x = args[0]
        if x <= 0:
            raise ValueError(
                f"log10 is not defined for non-positive numbers; got {x}."
            )
        return math.log10(x)


class Sqrt(Operation):
    """Unary square root operation (scientific variant)."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"sqrt"``
        """
        return "sqrt"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the square root of args[0].

        Args:
            *args: Exactly one numeric operand.

        Returns:
            math.sqrt(args[0])

        Raises:
            ValueError: If args[0] is negative.
        """
        x = args[0]
        if x < 0:
            raise ValueError(
                f"sqrt is not defined for negative numbers; got {x}."
            )
        return math.sqrt(x)


class Factorial(Operation):
    """Unary factorial operation (scientific variant).

    Accepts any numeric value that represents a non-negative integer.
    Raises ValueError for negative inputs or non-integer float values.
    """

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"factorial"``
        """
        return "factorial"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> int:
        """Compute the factorial of args[0].

        The operand is cast to ``int`` via ``int(n)``; non-integer floats and
        negative values raise ``ValueError``.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            math.factorial(int(args[0]))

        Raises:
            ValueError: If args[0] is negative or a non-integer float.
        """
        n = args[0]
        if isinstance(n, float) and not n.is_integer():
            raise ValueError(
                f"factorial requires a non-negative integer; got non-integer float {n}."
            )
        n_int = int(n)
        if n_int < 0:
            raise ValueError(
                f"factorial is not defined for negative numbers; got {n_int}."
            )
        return math.factorial(n_int)


def register_scientific_operations(registry: OperationRegistry) -> None:
    """Register all 8 scientific operations with the given registry.

    Operations registered: sin, cos, tan, exp, log, log10, sqrt, factorial.

    Note: ``factorial`` and ``log10`` overlap with basic operation names that
    may already be registered.  If ``register_basic_operations`` was called
    first, these entries will be overwritten with the scientific variants.
    To avoid this, callers may register only the operations they need.

    Args:
        registry: The ``OperationRegistry`` instance to register operations into.
    """
    registry.register("sin", Sin())
    registry.register("cos", Cos())
    registry.register("tan", Tan())
    registry.register("exp", Exp())
    registry.register("log", Log())
    registry.register("log10", Log10())
    registry.register("sqrt", Sqrt())
    registry.register("factorial", Factorial())
