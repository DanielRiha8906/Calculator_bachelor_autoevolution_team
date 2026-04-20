"""Calculator state management.

Combines ``ArithmeticEngine`` (pure computation) with ``OperationHistory``
(record keeping) to expose the same public interface as the original monolithic
``Calculator`` class.

No imports from any presentation layer (cli, user_input, __main__) are
permitted here.
"""

from datetime import datetime

from src.history import OperationHistory
from src.logic.core import ArithmeticEngine
from src.operations import OperationRegistry, register_basic_operations, register_scientific_operations


class Calculator:
    """Stateful calculator that delegates arithmetic to ``ArithmeticEngine``
    and logs each operation via ``OperationHistory``.

    The public interface — method names and signatures — is identical to the
    original ``src.calculator.Calculator`` so that all existing callers
    continue to work without modification.
    """

    def __init__(self) -> None:
        self._engine: ArithmeticEngine = ArithmeticEngine()
        self._history: OperationHistory = OperationHistory()
        self._registry: OperationRegistry = OperationRegistry()
        self._mode: str = "normal"
        register_basic_operations(self._registry)
        register_scientific_operations(self._registry)

    # ------------------------------------------------------------------
    # History management
    # ------------------------------------------------------------------

    def get_history(self) -> list:
        """Return a copy of all recorded operation history entries.

        Returns:
            A list of ``OperationRecord`` instances in insertion order.
        """
        return self._history.get_history()

    def clear_history(self) -> None:
        """Remove all entries from the operation history."""
        self._history.clear_history()

    # ------------------------------------------------------------------
    # Mode management
    # ------------------------------------------------------------------

    def get_mode(self) -> str:
        """Return the current calculator mode.

        Returns:
            The current mode string — either ``"normal"`` or ``"scientific"``.
        """
        return self._mode

    def set_mode(self, mode: str) -> None:
        """Set the calculator mode.

        Args:
            mode: The desired mode. Must be ``"normal"`` or ``"scientific"``.

        Raises:
            ValueError: If *mode* is not one of the accepted values.
        """
        if mode not in ("normal", "scientific"):
            raise ValueError(
                f"Invalid mode '{mode}'. Must be 'normal' or 'scientific'."
            )
        self._mode = mode

    def is_scientific_mode(self) -> bool:
        """Check whether the calculator is in scientific mode.

        Returns:
            ``True`` if the current mode is ``"scientific"``, ``False`` otherwise.
        """
        return self._mode == "scientific"

    # ------------------------------------------------------------------
    # Arithmetic operations
    # ------------------------------------------------------------------

    def add(self, a: int | float, b: int | float) -> int | float:
        """Return the sum of *a* and *b* and record the operation.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            a + b
        """
        result = self._engine.add(a, b)
        self._history.add_record("add", [a, b], result, datetime.now())
        return result

    def subtract(self, a: int | float, b: int | float) -> int | float:
        """Return the difference *a* - *b* and record the operation.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            a - b
        """
        result = self._engine.subtract(a, b)
        self._history.add_record("subtract", [a, b], result, datetime.now())
        return result

    def multiply(self, a: int | float, b: int | float) -> int | float:
        """Return the product of *a* and *b* and record the operation.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            a * b
        """
        result = self._engine.multiply(a, b)
        self._history.add_record("multiply", [a, b], result, datetime.now())
        return result

    def divide(self, a: int | float, b: int | float) -> float:
        """Return the quotient *a* / *b* and record the operation.

        Args:
            a: Dividend.
            b: Divisor.

        Returns:
            a / b

        Raises:
            ZeroDivisionError: If *b* is zero.
        """
        result = self._engine.divide(a, b)
        self._history.add_record("divide", [a, b], result, datetime.now())
        return result

    def factorial(self, n: int) -> int:
        """Compute the factorial of a non-negative integer and record the operation.

        Args:
            n: The non-negative integer whose factorial is to be computed.
                Float values are accepted only when they represent an exact
                integer (e.g. 5.0), in which case they are treated as int.

        Returns:
            The factorial of n (n!). Returns 1 when n is 0.

        Raises:
            TypeError: If n is not an int or a float that equals an integer
                value.
            ValueError: If n is negative.
        """
        result = self._engine.factorial(n)
        # n may have been coerced to int inside the engine; retrieve the
        # normalised value from the engine result for the history record.
        n_recorded = int(n) if isinstance(n, float) and n.is_integer() else n
        self._history.add_record("factorial", [n_recorded], result, datetime.now())
        return result

    def square(self, x: int | float) -> int | float:
        """Compute the square of a number and record the operation.

        Args:
            x: The number to square. Must be an int or float (not bool or None).

        Returns:
            x squared. Returns int if x is int, float if x is float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        result = self._engine.square(x)
        self._history.add_record("square", [x], result, datetime.now())
        return result

    def cube(self, x: int | float) -> int | float:
        """Compute the cube of a number and record the operation.

        Args:
            x: The number to cube. Must be an int or float (not bool or None).

        Returns:
            x cubed. Returns int if x is int, float if x is float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        result = self._engine.cube(x)
        self._history.add_record("cube", [x], result, datetime.now())
        return result

    def square_root(self, x: int | float) -> float:
        """Compute the square root of a non-negative number and record the operation.

        Args:
            x: The number whose square root is to be computed. Must be an int
                or float (not bool or None) and must be non-negative.

        Returns:
            The square root of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
            ValueError: If x is negative.
        """
        result = self._engine.square_root(x)
        self._history.add_record("square_root", [x], result, datetime.now())
        return result

    def cube_root(self, x: int | float) -> float:
        """Compute the cube root of a number and record the operation.

        Args:
            x: The number whose cube root is to be computed. Must be an int or
                float (not bool or None). Negative values are supported.

        Returns:
            The cube root of x as a float, preserving the sign of x.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        result = self._engine.cube_root(x)
        self._history.add_record("cube_root", [x], result, datetime.now())
        return result

    def power(self, base: int | float, exponent: int | float) -> float:
        """Raise base to the power of exponent and record the operation.

        Args:
            base: The base value. Must be an int or float (not bool or None).
            exponent: The exponent value. Must be an int or float (not bool
                or None).

        Returns:
            base raised to the power of exponent, as a float.

        Raises:
            TypeError: If base or exponent is a bool, None, or any non-numeric
                type.
        """
        result = self._engine.power(base, exponent)
        self._history.add_record("power", [base, exponent], result, datetime.now())
        return result

    def log10(self, x: int | float) -> float:
        """Compute the base-10 logarithm of a positive number and record the operation.

        Args:
            x: The number whose base-10 logarithm is to be computed. Must be
                an int or float (not bool or None) and must be strictly positive.

        Returns:
            The base-10 logarithm of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
            ValueError: If x is less than or equal to zero.
        """
        result = self._engine.log10(x)
        self._history.add_record("log10", [x], result, datetime.now())
        return result

    def natural_log(self, x: int | float) -> float:
        """Compute the natural logarithm (base e) of a positive number and record the operation.

        Args:
            x: The number whose natural logarithm is to be computed. Must be
                an int or float (not bool or None) and must be strictly positive.

        Returns:
            The natural logarithm of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
            ValueError: If x is less than or equal to zero.
        """
        result = self._engine.natural_log(x)
        self._history.add_record("natural_log", [x], result, datetime.now())
        return result

    # ------------------------------------------------------------------
    # Scientific operations
    # ------------------------------------------------------------------

    def sin(self, x: float) -> float:
        """Compute the sine of *x* (in radians) and record the operation.

        Args:
            x: Angle in radians. Must be an int or float (not bool or None).

        Returns:
            The sine of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        result = self._engine.sin(x)
        self._history.add_record("sin", [x], result, datetime.now())
        return result

    def cos(self, x: float) -> float:
        """Compute the cosine of *x* (in radians) and record the operation.

        Args:
            x: Angle in radians. Must be an int or float (not bool or None).

        Returns:
            The cosine of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        result = self._engine.cos(x)
        self._history.add_record("cos", [x], result, datetime.now())
        return result

    def tan(self, x: float) -> float:
        """Compute the tangent of *x* (in radians) and record the operation.

        Args:
            x: Angle in radians. Must be an int or float (not bool or None).

        Returns:
            The tangent of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        result = self._engine.tan(x)
        self._history.add_record("tan", [x], result, datetime.now())
        return result

    def exp(self, x: float) -> float:
        """Compute e raised to the power of *x* and record the operation.

        Args:
            x: The exponent. Must be an int or float (not bool or None).

        Returns:
            math.e ** x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        result = self._engine.exp(x)
        self._history.add_record("exp", [x], result, datetime.now())
        return result
