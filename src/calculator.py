import logging
import math
from datetime import datetime

from .history import OperationHistory

logger = logging.getLogger("calculator")


class Calculator:
    def __init__(self) -> None:
        self._history: OperationHistory = OperationHistory()

    def get_history(self) -> list:
        """Return a copy of all recorded operation history entries.

        Returns:
            A list of ``OperationRecord`` instances in insertion order.
        """
        return self._history.get_history()

    def clear_history(self) -> None:
        """Remove all entries from the operation history."""
        self._history.clear_history()

    def add(self, a, b):
        result = a + b
        self._history.add_record("add", [a, b], result, datetime.now())
        return result

    def subtract(self, a, b):
        result = a - b
        self._history.add_record("subtract", [a, b], result, datetime.now())
        return result

    def multiply(self, a, b):
        result = a * b
        self._history.add_record("multiply", [a, b], result, datetime.now())
        return result

    def divide(self, a, b):
        if b == 0:
            logger.error(
                f"divide: division by zero attempted; a={a}, b={b}; ZeroDivisionError"
            )
        result = a / b
        self._history.add_record("divide", [a, b], result, datetime.now())
        return result

    def factorial(self, n: int) -> int:
        """Compute the factorial of a non-negative integer.

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
        if isinstance(n, bool):
            logger.error(
                f"factorial: invalid type {type(n).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected a non-negative integer, got {type(n).__name__}."
            )
        if isinstance(n, float):
            if not n.is_integer():
                logger.error(
                    f"factorial: non-integer float {n} provided; TypeError"
                )
                raise TypeError(
                    f"Float value {n} is not an integer value; "
                    "cannot compute factorial."
                )
            n = int(n)
        if not isinstance(n, int):
            logger.error(
                f"factorial: invalid type {type(n).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected a non-negative integer, got {type(n).__name__}."
            )
        if n < 0:
            logger.error(
                f"factorial: negative value {n} provided; ValueError"
            )
            raise ValueError(
                f"Factorial is not defined for negative numbers; got {n}."
            )
        result: int = 1
        for i in range(2, n + 1):
            result *= i
        self._history.add_record("factorial", [n], result, datetime.now())
        return result

    def square(self, x: int | float) -> int | float:
        """Compute the square of a number.

        Args:
            x: The number to square. Must be an int or float (not bool or None).

        Returns:
            x squared. Returns int if x is int, float if x is float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        if isinstance(x, bool):
            logger.error(
                f"square: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            logger.error(
                f"square: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        result = x * x
        self._history.add_record("square", [x], result, datetime.now())
        return result

    def cube(self, x: int | float) -> int | float:
        """Compute the cube of a number.

        Args:
            x: The number to cube. Must be an int or float (not bool or None).

        Returns:
            x cubed. Returns int if x is int, float if x is float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        if isinstance(x, bool):
            logger.error(
                f"cube: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            logger.error(
                f"cube: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        result = x * x * x
        self._history.add_record("cube", [x], result, datetime.now())
        return result

    def square_root(self, x: int | float) -> float:
        """Compute the square root of a non-negative number.

        Args:
            x: The number whose square root is to be computed. Must be an int
                or float (not bool or None) and must be non-negative.

        Returns:
            The square root of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
            ValueError: If x is negative.
        """
        if isinstance(x, bool):
            logger.error(
                f"square_root: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected a non-negative int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            logger.error(
                f"square_root: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected a non-negative int or float, got {type(x).__name__}."
            )
        if x < 0:
            logger.error(
                f"square_root: negative value {x} provided; math domain error"
            )
            raise ValueError(
                f"Square root is not defined for negative numbers; got {x}."
            )
        result = math.sqrt(x)
        self._history.add_record("square_root", [x], result, datetime.now())
        return result

    def cube_root(self, x: int | float) -> float:
        """Compute the cube root of a number.

        Args:
            x: The number whose cube root is to be computed. Must be an int or
                float (not bool or None). Negative values are supported.

        Returns:
            The cube root of x as a float, preserving the sign of x.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
        """
        if isinstance(x, bool):
            logger.error(
                f"cube_root: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            logger.error(
                f"cube_root: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float, got {type(x).__name__}."
            )
        result = math.copysign(abs(x) ** (1 / 3), x)
        self._history.add_record("cube_root", [x], result, datetime.now())
        return result

    def power(self, base: int | float, exponent: int | float) -> float:
        """Raise base to the power of exponent.

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
        if isinstance(base, bool):
            logger.error(
                f"power: invalid type {type(base).__name__} for base provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float for base, got {type(base).__name__}."
            )
        if not isinstance(base, (int, float)):
            logger.error(
                f"power: invalid type {type(base).__name__} for base provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float for base, got {type(base).__name__}."
            )
        if isinstance(exponent, bool):
            logger.error(
                f"power: invalid type {type(exponent).__name__} for exponent provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float for exponent, got {type(exponent).__name__}."
            )
        if not isinstance(exponent, (int, float)):
            logger.error(
                f"power: invalid type {type(exponent).__name__} for exponent provided; TypeError"
            )
            raise TypeError(
                f"Expected an int or float for exponent, got {type(exponent).__name__}."
            )
        result = float(base ** exponent)
        self._history.add_record("power", [base, exponent], result, datetime.now())
        return result

    def log10(self, x: int | float) -> float:
        """Compute the base-10 logarithm of a positive number.

        Args:
            x: The number whose base-10 logarithm is to be computed. Must be
                an int or float (not bool or None) and must be strictly positive.

        Returns:
            The base-10 logarithm of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
            ValueError: If x is less than or equal to zero.
        """
        if isinstance(x, bool):
            logger.error(
                f"log10: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected a positive int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            logger.error(
                f"log10: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected a positive int or float, got {type(x).__name__}."
            )
        if x <= 0:
            logger.error(
                f"log10: non-positive value {x} provided; ValueError"
            )
            raise ValueError(
                f"log10 is not defined for non-positive numbers; got {x}."
            )
        result = math.log10(x)
        self._history.add_record("log10", [x], result, datetime.now())
        return result

    def natural_log(self, x: int | float) -> float:
        """Compute the natural logarithm (base e) of a positive number.

        Args:
            x: The number whose natural logarithm is to be computed. Must be
                an int or float (not bool or None) and must be strictly positive.

        Returns:
            The natural logarithm of x as a float.

        Raises:
            TypeError: If x is a bool, None, or any non-numeric type.
            ValueError: If x is less than or equal to zero.
        """
        if isinstance(x, bool):
            logger.error(
                f"natural_log: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected a positive int or float, got {type(x).__name__}."
            )
        if not isinstance(x, (int, float)):
            logger.error(
                f"natural_log: invalid type {type(x).__name__} provided; TypeError"
            )
            raise TypeError(
                f"Expected a positive int or float, got {type(x).__name__}."
            )
        if x <= 0:
            logger.error(
                f"natural_log: non-positive value {x} provided; ValueError"
            )
            raise ValueError(
                f"Natural log is not defined for non-positive numbers; got {x}."
            )
        result = math.log(x)
        self._history.add_record("natural_log", [x], result, datetime.now())
        return result
