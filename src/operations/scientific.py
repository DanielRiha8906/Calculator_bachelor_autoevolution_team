"""Concrete operation classes for scientific functions.

Each class wraps one scientific operation exposed by ``ArithmeticEngine`` and
conforms to the ``Operation`` interface.  All actual computation is delegated
to ``ArithmeticEngine`` — no arithmetic logic is duplicated here.

``register_scientific_operations`` registers all four operations (sin, cos,
tan, exp) with a given ``OperationRegistry``.
"""

from src.logic.core import ArithmeticEngine
from src.operations.base import Operation, OperationRegistry

_engine = ArithmeticEngine()


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
        """Compute the sine of the operand (in radians).

        Args:
            *args: Exactly one numeric operand (angle in radians).

        Returns:
            The sine of args[0].

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
        """
        return _engine.sin(args[0])


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
        """Compute the cosine of the operand (in radians).

        Args:
            *args: Exactly one numeric operand (angle in radians).

        Returns:
            The cosine of args[0].

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
        """
        return _engine.cos(args[0])


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
        """Compute the tangent of the operand (in radians).

        Args:
            *args: Exactly one numeric operand (angle in radians).

        Returns:
            The tangent of args[0].

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
        """
        return _engine.tan(args[0])


class Exp(Operation):
    """Unary natural exponential operation (e^x)."""

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
        """Compute e raised to the power of the operand.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            math.e ** args[0].

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
        """
        return _engine.exp(args[0])


def register_scientific_operations(registry: OperationRegistry) -> None:
    """Register all four scientific operations with the given registry.

    Operations registered: sin, cos, tan, exp.

    Args:
        registry: The ``OperationRegistry`` instance to register operations into.
    """
    registry.register("sin", Sin())
    registry.register("cos", Cos())
    registry.register("tan", Tan())
    registry.register("exp", Exp())
