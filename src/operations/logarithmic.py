"""Calculation engine layer — logarithmic operations."""

import math


def log(x: float) -> float:
    """Compute the base-10 logarithm of a positive number.

    Args:
        x: The operand. Must be positive.

    Returns:
        The base-10 logarithm of x.

    Raises:
        ValueError: If x is zero or negative.
    """
    if x <= 0:
        raise ValueError(f"log requires a positive number, got {x}")
    return math.log10(x)


def ln(x: float) -> float:
    """Compute the natural logarithm (base e) of a positive number.

    Args:
        x: The operand. Must be positive.

    Returns:
        The natural logarithm of x.

    Raises:
        ValueError: If x is zero or negative.
    """
    if x <= 0:
        raise ValueError(f"ln requires a positive number, got {x}")
    return math.log(x)
