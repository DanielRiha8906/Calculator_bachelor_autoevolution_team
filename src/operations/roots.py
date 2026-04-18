"""Calculation engine layer — root extraction operations."""

import math


def square_root(x: float) -> float:
    """Compute the square root of a non-negative number.

    Args:
        x: The operand. Must be non-negative.

    Returns:
        The square root of x.

    Raises:
        ValueError: If x is negative.
    """
    if x < 0:
        raise ValueError(f"square_root requires a non-negative number, got {x}")
    return math.sqrt(x)


def cube_root(x: float) -> float:
    """Compute the cube root of a number.

    Negative inputs are supported via Python 3.12 math.cbrt.

    Args:
        x: The operand.

    Returns:
        The cube root of x.
    """
    return math.cbrt(x)
