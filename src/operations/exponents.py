"""Calculation engine layer — exponent and power operations."""

import math


def power(base: float, exponent: float) -> float:
    """Raise base to the given exponent.

    Args:
        base: The base value.
        exponent: The exponent to raise the base to.

    Returns:
        base raised to the power of exponent (base ** exponent).
    """
    return base ** exponent


def factorial(n: int) -> int:
    """Compute the factorial of a non-negative integer.

    Args:
        n: The non-negative integer whose factorial is to be computed.

    Returns:
        The factorial of n (n!).

    Raises:
        ValueError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int):
        raise ValueError(f"n must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"n must be a non-negative integer, got {n}")
    return math.factorial(n)


def square(x: float) -> float:
    """Compute the square of a number.

    Args:
        x: The operand.

    Returns:
        x squared (x ** 2).
    """
    return x ** 2


def cube(x: float) -> float:
    """Compute the cube of a number.

    Args:
        x: The operand.

    Returns:
        x cubed (x ** 3).
    """
    return x ** 3
