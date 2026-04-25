"""Pure scientific operation functions.

This module contains stateless mathematical functions for trigonometric,
inverse trigonometric, hyperbolic, exponential operations, and mathematical
constants.  All functions have no side effects and no dependency on the
Calculator class.
"""

import math


def sin(x: float) -> float:
    """Return the sine of x (in radians).

    Args:
        x: The angle in radians.

    Returns:
        The sine of x.
    """
    return math.sin(x)


def cos(x: float) -> float:
    """Return the cosine of x (in radians).

    Args:
        x: The angle in radians.

    Returns:
        The cosine of x.
    """
    return math.cos(x)


def tan(x: float) -> float:
    """Return the tangent of x (in radians).

    Args:
        x: The angle in radians.

    Returns:
        The tangent of x.
    """
    return math.tan(x)


def asin(x: float) -> float:
    """Return the arc sine of x (in radians).

    Args:
        x: A value in the domain [-1, 1].

    Returns:
        The arc sine of x, in radians.

    Raises:
        ValueError: If x is outside the domain [-1, 1].
    """
    if x < -1 or x > 1:
        raise ValueError(
            f"asin domain error: x must be in [-1, 1], got {x}"
        )
    return math.asin(x)


def acos(x: float) -> float:
    """Return the arc cosine of x (in radians).

    Args:
        x: A value in the domain [-1, 1].

    Returns:
        The arc cosine of x, in radians.

    Raises:
        ValueError: If x is outside the domain [-1, 1].
    """
    if x < -1 or x > 1:
        raise ValueError(
            f"acos domain error: x must be in [-1, 1], got {x}"
        )
    return math.acos(x)


def atan(x: float) -> float:
    """Return the arc tangent of x (in radians).

    Args:
        x: Any real number.

    Returns:
        The arc tangent of x, in radians.
    """
    return math.atan(x)


def sinh(x: float) -> float:
    """Return the hyperbolic sine of x.

    Args:
        x: Any real number.

    Returns:
        The hyperbolic sine of x.
    """
    return math.sinh(x)


def cosh(x: float) -> float:
    """Return the hyperbolic cosine of x.

    Args:
        x: Any real number.

    Returns:
        The hyperbolic cosine of x.
    """
    return math.cosh(x)


def tanh(x: float) -> float:
    """Return the hyperbolic tangent of x.

    Args:
        x: Any real number.

    Returns:
        The hyperbolic tangent of x.
    """
    return math.tanh(x)


def exp(x: float) -> float:
    """Return e raised to the power of x.

    Args:
        x: The exponent.

    Returns:
        e ** x.
    """
    return math.exp(x)


def pi() -> float:
    """Return the mathematical constant π.

    Returns:
        The value of π (approximately 3.14159265358979).
    """
    return math.pi


def e() -> float:
    """Return the mathematical constant e.

    Returns:
        The value of e (approximately 2.71828182845904).
    """
    return math.e
