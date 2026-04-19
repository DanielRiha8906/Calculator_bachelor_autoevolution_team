"""Scientific operation functions.

Standalone implementations of power and logarithm operations.
"""

import math


def power(base: float, exponent: float) -> float:
    """Return base raised to the given exponent.

    Args:
        base: The base number.
        exponent: The exponent to raise the base to.

    Returns:
        base raised to the power of exponent.
    """
    return base ** exponent


def logarithm(x: float) -> float:
    """Return the base-10 logarithm of x.

    Args:
        x: A positive number.

    Returns:
        The base-10 logarithm of x.

    Raises:
        ValueError: If x is zero or negative.
    """
    if x <= 0:
        raise ValueError("logarithm() not defined for non-positive values")
    return math.log10(x)


def natural_logarithm(x: float) -> float:
    """Return the natural logarithm (base e) of x.

    Args:
        x: A positive number.

    Returns:
        The natural logarithm of x.

    Raises:
        ValueError: If x is zero or negative.
    """
    if x <= 0:
        raise ValueError("natural_logarithm() not defined for non-positive values")
    return math.log(x)
