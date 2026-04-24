"""Core Calculator class that delegates to basic_operations and advanced_operations.

This module contains the canonical Calculator implementation.  All arithmetic
and mathematical logic is delegated to the pure-function modules
:mod:`~src.basic_operations` and :mod:`~src.advanced_operations`; this class
is responsible only for dispatch and history recording.
"""

from . import basic_operations
from . import advanced_operations


class Calculator:
    """A calculator that supports basic and advanced operations with history tracking."""

    def __init__(self) -> None:
        """Initialize the calculator with an empty operation history."""
        self._history: list[dict] = []

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
