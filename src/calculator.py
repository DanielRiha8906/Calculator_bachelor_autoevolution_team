import math


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

    def add(self, a, b):
        result = a + b
        self._record_operation("add", [a, b], result)
        return result

    def subtract(self, a, b):
        result = a - b
        self._record_operation("subtract", [a, b], result)
        return result

    def multiply(self, a, b):
        result = a * b
        self._record_operation("multiply", [a, b], result)
        return result

    def divide(self, a, b):
        result = a / b
        self._record_operation("divide", [a, b], result)
        return result

    def square(self, a):
        """Return a squared (a ** 2).

        Works for all real numbers.

        Args:
            a: The number to square.

        Returns:
            The square of a.
        """
        result = a ** 2
        self._record_operation("square", [a], result)
        return result

    def cube(self, a):
        """Return a cubed (a ** 3).

        Works for all real numbers.

        Args:
            a: The number to cube.

        Returns:
            The cube of a.
        """
        result = a ** 3
        self._record_operation("cube", [a], result)
        return result

    def square_root(self, a):
        """Return the square root of a.

        Args:
            a: The number to take the square root of. Must be non-negative.

        Returns:
            The square root of a.

        Raises:
            ValueError: If a is negative.
        """
        if a < 0:
            raise ValueError("Cannot take square root of a negative number.")
        result = math.sqrt(a)
        self._record_operation("square_root", [a], result)
        return result

    def cube_root(self, a):
        """Return the cube root of a.

        Handles negative inputs by computing -(abs(a) ** (1/3)).

        Args:
            a: The number to take the cube root of.

        Returns:
            The cube root of a.
        """
        if a == 0:
            result = 0.0
        elif a < 0:
            result = -(abs(a) ** (1 / 3))
        else:
            result = a ** (1 / 3)
        self._record_operation("cube_root", [a], result)
        return result

    def factorial(self, n):
        """Return the factorial of n.

        Args:
            n: A non-negative integer or a float representing an integer (e.g., 5.0).

        Returns:
            The factorial of n.

        Raises:
            ValueError: If n is negative, has a fractional part, or is a boolean.
        """
        if isinstance(n, bool):
            raise ValueError("Factorial is only defined for non-negative integers.")
        if isinstance(n, float):
            if n != int(n):
                raise ValueError("Factorial is only defined for non-negative integers.")
            n = int(n)
        elif not isinstance(n, int):
            raise ValueError("Factorial is only defined for non-negative integers.")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        result = math.factorial(n)
        self._record_operation("factorial", [n], result)
        return result

    def power(self, base, exp):
        """Return base raised to the power of exp.

        Args:
            base: The base number.
            exp: The exponent.

        Returns:
            base ** exp.
        """
        result = base ** exp
        self._record_operation("power", [base, exp], result)
        return result

    def log(self, a):
        """Return the base-10 logarithm of a.

        Args:
            a: The number to take the logarithm of. Must be positive.

        Returns:
            The base-10 logarithm of a.

        Raises:
            ValueError: If a is less than or equal to 0.
        """
        if a <= 0:
            raise ValueError("Logarithm is only defined for positive numbers.")
        result = math.log10(a)
        self._record_operation("log", [a], result)
        return result

    def ln(self, a):
        """Return the natural logarithm of a.

        Args:
            a: The number to take the natural logarithm of. Must be positive.

        Returns:
            The natural logarithm of a.

        Raises:
            ValueError: If a is less than or equal to 0.
        """
        if a <= 0:
            raise ValueError("Natural logarithm is only defined for positive numbers.")
        result = math.log(a)
        self._record_operation("ln", [a], result)
        return result
