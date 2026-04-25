"""Core Calculator class that delegates to basic_operations and advanced_operations.

This module contains the canonical Calculator implementation.  All arithmetic
and mathematical logic is delegated to the pure-function modules
:mod:`~src.basic_operations`, :mod:`~src.advanced_operations`, and
:mod:`~src.scientific_operations`; this class is responsible only for dispatch
and history recording.
"""

from . import basic_operations
from . import advanced_operations
from . import scientific_operations


class Calculator:
    """A calculator that supports basic and advanced operations with history tracking."""

    def __init__(self) -> None:
        """Initialize the calculator with an empty operation history and normal mode."""
        self._history: list[dict] = []
        self._scientific_mode: bool = False

    def _record_operation(self, operation_name: str, operands, result) -> None:
        """Record a successfully completed operation to history.

        Args:
            operation_name: The name of the operation (e.g. 'add', 'square').
            operands: A single value or list/tuple of operand values.
            result: The computed result of the operation.
        """
        if not isinstance(operands, (list, tuple)):
            operands = [operands]
        self._history.append({
            "operation": operation_name,
            "operands": list(operands),
            "result": result
        })

    def get_history(self) -> list[dict]:
        """Return a copy of the operation history.

        Returns:
            A list of dicts, each with keys 'operation', 'operands', and 'result'.
        """
        return self._history.copy()

    def clear_history(self) -> None:
        """Clear the operation history."""
        self._history.clear()

    def add(self, a: float, b: float) -> float:
        """Return a + b and record the operation.

        Args:
            a: The first operand.
            b: The second operand.

        Returns:
            a + b.
        """
        result = basic_operations.add(a, b)
        self._record_operation("add", [a, b], result)
        return result

    def subtract(self, a: float, b: float) -> float:
        """Return a - b and record the operation.

        Args:
            a: The minuend.
            b: The subtrahend.

        Returns:
            a - b.
        """
        result = basic_operations.subtract(a, b)
        self._record_operation("subtract", [a, b], result)
        return result

    def multiply(self, a: float, b: float) -> float:
        """Return a * b and record the operation.

        Args:
            a: The first factor.
            b: The second factor.

        Returns:
            a * b.
        """
        result = basic_operations.multiply(a, b)
        self._record_operation("multiply", [a, b], result)
        return result

    def divide(self, a: float, b: float) -> float:
        """Return a / b and record the operation.

        Args:
            a: The dividend.
            b: The divisor.

        Returns:
            a / b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        result = basic_operations.divide(a, b)
        self._record_operation("divide", [a, b], result)
        return result

    def square(self, a: float) -> float:
        """Return a squared (a ** 2) and record the operation.

        Args:
            a: The number to square.

        Returns:
            a ** 2.
        """
        result = advanced_operations.square(a)
        self._record_operation("square", [a], result)
        return result

    def cube(self, a: float) -> float:
        """Return a cubed (a ** 3) and record the operation.

        Args:
            a: The number to cube.

        Returns:
            a ** 3.
        """
        result = advanced_operations.cube(a)
        self._record_operation("cube", [a], result)
        return result

    def square_root(self, a: float) -> float:
        """Return the square root of a and record the operation.

        Args:
            a: The number to take the square root of.  Must be non-negative.

        Returns:
            math.sqrt(a).

        Raises:
            ValueError: If a is negative.
        """
        result = advanced_operations.square_root(a)
        self._record_operation("square_root", [a], result)
        return result

    def cube_root(self, a: float) -> float:
        """Return the cube root of a and record the operation.

        Args:
            a: The number to take the cube root of.

        Returns:
            The real-valued cube root of a.
        """
        result = advanced_operations.cube_root(a)
        self._record_operation("cube_root", [a], result)
        return result

    def factorial(self, n: float) -> int:
        """Return the factorial of n and record the operation.

        Args:
            n: A non-negative integer (or float representing an integer).

        Returns:
            n! as an integer.

        Raises:
            ValueError: If n is negative, has a fractional part, or is a boolean.
        """
        result = advanced_operations.factorial(n)
        self._record_operation("factorial", [n], result)
        return result

    def power(self, base: float, exp: float) -> float:
        """Return base raised to exp and record the operation.

        Args:
            base: The base number.
            exp: The exponent.

        Returns:
            base ** exp.
        """
        result = advanced_operations.power(base, exp)
        self._record_operation("power", [base, exp], result)
        return result

    def log(self, a: float) -> float:
        """Return the base-10 logarithm of a and record the operation.

        Args:
            a: The number to take the logarithm of.  Must be positive.

        Returns:
            math.log10(a).

        Raises:
            ValueError: If a is less than or equal to 0.
        """
        result = advanced_operations.log(a)
        self._record_operation("log", [a], result)
        return result

    def ln(self, a: float) -> float:
        """Return the natural logarithm of a and record the operation.

        Args:
            a: The number to take the natural logarithm of.  Must be positive.

        Returns:
            math.log(a).

        Raises:
            ValueError: If a is less than or equal to 0.
        """
        result = advanced_operations.ln(a)
        self._record_operation("ln", [a], result)
        return result

    # ------------------------------------------------------------------
    # Scientific operations
    # ------------------------------------------------------------------

    def sin(self, x: float) -> float:
        """Return the sine of x (in radians) and record the operation.

        Args:
            x: The angle in radians.

        Returns:
            The sine of x.
        """
        result = scientific_operations.sin(x)
        self._record_operation("sin", [x], result)
        return result

    def cos(self, x: float) -> float:
        """Return the cosine of x (in radians) and record the operation.

        Args:
            x: The angle in radians.

        Returns:
            The cosine of x.
        """
        result = scientific_operations.cos(x)
        self._record_operation("cos", [x], result)
        return result

    def tan(self, x: float) -> float:
        """Return the tangent of x (in radians) and record the operation.

        Args:
            x: The angle in radians.

        Returns:
            The tangent of x.
        """
        result = scientific_operations.tan(x)
        self._record_operation("tan", [x], result)
        return result

    def asin(self, x: float) -> float:
        """Return the arc sine of x (in radians) and record the operation.

        Args:
            x: A value in the domain [-1, 1].

        Returns:
            The arc sine of x, in radians.

        Raises:
            ValueError: If x is outside the domain [-1, 1].
        """
        result = scientific_operations.asin(x)
        self._record_operation("asin", [x], result)
        return result

    def acos(self, x: float) -> float:
        """Return the arc cosine of x (in radians) and record the operation.

        Args:
            x: A value in the domain [-1, 1].

        Returns:
            The arc cosine of x, in radians.

        Raises:
            ValueError: If x is outside the domain [-1, 1].
        """
        result = scientific_operations.acos(x)
        self._record_operation("acos", [x], result)
        return result

    def atan(self, x: float) -> float:
        """Return the arc tangent of x (in radians) and record the operation.

        Args:
            x: Any real number.

        Returns:
            The arc tangent of x, in radians.
        """
        result = scientific_operations.atan(x)
        self._record_operation("atan", [x], result)
        return result

    def sinh(self, x: float) -> float:
        """Return the hyperbolic sine of x and record the operation.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic sine of x.
        """
        result = scientific_operations.sinh(x)
        self._record_operation("sinh", [x], result)
        return result

    def cosh(self, x: float) -> float:
        """Return the hyperbolic cosine of x and record the operation.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic cosine of x.
        """
        result = scientific_operations.cosh(x)
        self._record_operation("cosh", [x], result)
        return result

    def tanh(self, x: float) -> float:
        """Return the hyperbolic tangent of x and record the operation.

        Args:
            x: Any real number.

        Returns:
            The hyperbolic tangent of x.
        """
        result = scientific_operations.tanh(x)
        self._record_operation("tanh", [x], result)
        return result

    def exp(self, x: float) -> float:
        """Return e raised to the power of x and record the operation.

        Args:
            x: The exponent.

        Returns:
            e ** x.
        """
        result = scientific_operations.exp(x)
        self._record_operation("exp", [x], result)
        return result

    def get_pi(self) -> float:
        """Return the mathematical constant π and record the operation.

        Returns:
            The value of π (approximately 3.14159265358979).
        """
        result = scientific_operations.pi()
        self._record_operation("get_pi", [], result)
        return result

    def get_e(self) -> float:
        """Return the mathematical constant e and record the operation.

        Returns:
            The value of e (approximately 2.71828182845904).
        """
        result = scientific_operations.e()
        self._record_operation("get_e", [], result)
        return result

    # ------------------------------------------------------------------
    # Mode management
    # ------------------------------------------------------------------

    def enable_scientific_mode(self) -> None:
        """Enable scientific mode.

        When scientific mode is enabled, the UI may expose scientific operations
        such as trigonometric and hyperbolic functions.
        """
        self._scientific_mode = True

    def disable_scientific_mode(self) -> None:
        """Disable scientific mode, returning to normal mode."""
        self._scientific_mode = False

    def toggle_scientific_mode(self) -> None:
        """Toggle scientific mode on or off."""
        self._scientific_mode = not self._scientific_mode

    def is_scientific_mode(self) -> bool:
        """Return True if scientific mode is currently enabled, False otherwise.

        Returns:
            The current scientific mode state.
        """
        return self._scientific_mode
