import logging
import math

from src.logger import get_logger


class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        logger = get_logger(__name__)
        if b == 0:
            logger.error(f"Division by zero: {a} / {b}")
            raise ZeroDivisionError("division by zero")
        return a / b

    def factorial(self, n: int) -> int:
        """Return the factorial of n.

        Args:
            n: A non-negative integer whose factorial is to be computed.

        Returns:
            The factorial of n.

        Raises:
            ValueError: If n is not an integer or if n is negative.
        """
        logger = get_logger(__name__)
        if not isinstance(n, int):
            logger.error(f"factorial({n!r}) failed: expected int, got {type(n).__name__!r}")
            raise ValueError(f"factorial requires a non-negative integer, got {type(n).__name__!r}")
        if n < 0:
            logger.error(f"factorial({n}) failed: negative integer")
            raise ValueError(f"factorial is not defined for negative integers, got {n}")
        return math.factorial(n)

    def square(self, x: float) -> float:
        """Return the square of x.

        Args:
            x: The number to square.

        Returns:
            x multiplied by itself.
        """
        return x * x

    def cube(self, x: float) -> float:
        """Return the cube of x.

        Args:
            x: The number to cube.

        Returns:
            x multiplied by itself twice.
        """
        return x * x * x

    def square_root(self, x: float) -> float:
        """Return the square root of x.

        Args:
            x: A non-negative number.

        Returns:
            The square root of x.

        Raises:
            ValueError: If x is negative.
        """
        logger = get_logger(__name__)
        if x < 0:
            logger.error(f"square_root({x}) failed: negative number")
            raise ValueError(f"square_root requires a non-negative number, got {x}")
        return math.sqrt(x)

    def cube_root(self, x: float) -> float:
        """Return the real cube root of x, supporting negative inputs.

        Args:
            x: The number whose cube root is to be computed.

        Returns:
            The real cube root of x.
        """
        return math.copysign(abs(x) ** (1 / 3), x)

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the given exponent.

        Args:
            base: The base number.
            exponent: The exponent to raise the base to.

        Returns:
            base raised to the power of exponent. Returns 1.0 when both
            base and exponent are 0.
        """
        return math.pow(base, exponent)

    def log(self, x: float) -> float:
        """Return the base-10 logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            The base-10 logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        logger = get_logger(__name__)
        if x <= 0:
            logger.error(f"log({x}) failed: non-positive number")
            raise ValueError(f"log requires a positive number, got {x}")
        return math.log10(x)

    def ln(self, x: float) -> float:
        """Return the natural (base-e) logarithm of x.

        Args:
            x: A strictly positive number.

        Returns:
            The natural logarithm of x.

        Raises:
            ValueError: If x is zero or negative.
        """
        logger = get_logger(__name__)
        if x <= 0:
            logger.error(f"ln({x}) failed: non-positive number")
            raise ValueError(f"ln requires a positive number, got {x}")
        return math.log(x)

