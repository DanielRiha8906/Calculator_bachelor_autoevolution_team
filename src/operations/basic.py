"""Concrete operation classes for basic arithmetic.

Each class wraps one arithmetic operation exposed by ``ArithmeticEngine`` and
conforms to the ``Operation`` interface.  All actual computation is delegated
to ``ArithmeticEngine`` — no arithmetic logic is duplicated here.

``register_basic_operations`` registers all 12 operations with a given
``OperationRegistry``.
"""

from src.logic.core import ArithmeticEngine
from src.operations.base import Operation, OperationRegistry

_engine = ArithmeticEngine()


class Add(Operation):
    """Binary addition operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"add"``
        """
        return "add"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            2
        """
        return 2

    def execute(self, *args: int | float) -> float:
        """Add two numbers.

        Args:
            *args: Exactly two numeric operands.

        Returns:
            The sum of the two operands.
        """
        return _engine.add(args[0], args[1])


class Subtract(Operation):
    """Binary subtraction operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"subtract"``
        """
        return "subtract"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            2
        """
        return 2

    def execute(self, *args: int | float) -> float:
        """Subtract second operand from first.

        Args:
            *args: Exactly two numeric operands.

        Returns:
            The difference (args[0] - args[1]).
        """
        return _engine.subtract(args[0], args[1])


class Multiply(Operation):
    """Binary multiplication operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"multiply"``
        """
        return "multiply"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            2
        """
        return 2

    def execute(self, *args: int | float) -> float:
        """Multiply two numbers.

        Args:
            *args: Exactly two numeric operands.

        Returns:
            The product of the two operands.
        """
        return _engine.multiply(args[0], args[1])


class Divide(Operation):
    """Binary division operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"divide"``
        """
        return "divide"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            2
        """
        return 2

    def execute(self, *args: int | float) -> float:
        """Divide first operand by second.

        Args:
            *args: Exactly two numeric operands.

        Returns:
            The quotient (args[0] / args[1]).

        Raises:
            ZeroDivisionError: If the divisor is zero.
        """
        return _engine.divide(args[0], args[1])


class Factorial(Operation):
    """Unary factorial operation."""

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

    def execute(self, *args: int | float) -> float:
        """Compute the factorial of a non-negative integer.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            The factorial of args[0].

        Raises:
            TypeError: If the operand is not an integer value.
            ValueError: If the operand is negative.
        """
        return _engine.factorial(args[0])


class Square(Operation):
    """Unary square operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"square"``
        """
        return "square"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the square of a number.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            args[0] squared.

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
        """
        return _engine.square(args[0])


class Cube(Operation):
    """Unary cube operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"cube"``
        """
        return "cube"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the cube of a number.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            args[0] cubed.

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
        """
        return _engine.cube(args[0])


class SquareRoot(Operation):
    """Unary square root operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"square_root"``
        """
        return "square_root"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the square root of a non-negative number.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            The square root of args[0].

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
            ValueError: If the operand is negative.
        """
        return _engine.square_root(args[0])


class CubeRoot(Operation):
    """Unary cube root operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"cube_root"``
        """
        return "cube_root"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the cube root of a number.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            The cube root of args[0].

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
        """
        return _engine.cube_root(args[0])


class Power(Operation):
    """Binary power/exponentiation operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"power"``
        """
        return "power"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            2
        """
        return 2

    def execute(self, *args: int | float) -> float:
        """Raise base to the power of exponent.

        Args:
            *args: Exactly two numeric operands (base, exponent).

        Returns:
            args[0] raised to the power of args[1].

        Raises:
            TypeError: If either operand is a bool or non-numeric type.
        """
        return _engine.power(args[0], args[1])


class Log10(Operation):
    """Unary base-10 logarithm operation."""

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
        """Compute the base-10 logarithm of a positive number.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            The base-10 logarithm of args[0].

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
            ValueError: If the operand is less than or equal to zero.
        """
        return _engine.log10(args[0])


class NaturalLog(Operation):
    """Unary natural logarithm operation."""

    def name(self) -> str:
        """Return the operation name.

        Returns:
            ``"natural_log"``
        """
        return "natural_log"

    def operand_count(self) -> int:
        """Return the number of operands required.

        Returns:
            1
        """
        return 1

    def execute(self, *args: int | float) -> float:
        """Compute the natural logarithm (base e) of a positive number.

        Args:
            *args: Exactly one numeric operand.

        Returns:
            The natural logarithm of args[0].

        Raises:
            TypeError: If the operand is a bool or non-numeric type.
            ValueError: If the operand is less than or equal to zero.
        """
        return _engine.natural_log(args[0])


def register_basic_operations(registry: OperationRegistry) -> None:
    """Register all 12 basic arithmetic operations with the given registry.

    Operations registered: add, subtract, multiply, divide, factorial,
    square, cube, square_root, cube_root, power, log10, natural_log.

    Args:
        registry: The ``OperationRegistry`` instance to register operations into.
    """
    registry.register("add", Add())
    registry.register("subtract", Subtract())
    registry.register("multiply", Multiply())
    registry.register("divide", Divide())
    registry.register("factorial", Factorial())
    registry.register("square", Square())
    registry.register("cube", Cube())
    registry.register("square_root", SquareRoot())
    registry.register("cube_root", CubeRoot())
    registry.register("power", Power())
    registry.register("log10", Log10())
    registry.register("natural_log", NaturalLog())
