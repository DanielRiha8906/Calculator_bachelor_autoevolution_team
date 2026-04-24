"""Pure functions for advanced mathematical operations.

No state, no Calculator dependency.  All functions operate on plain numeric
arguments and return a numeric result.  Only the Python standard library
``math`` module is imported.  Callers are responsible for recording history
if needed.
"""

import math


def square(x: float) -> float:
    """Return x squared (x ** 2).

    Args:
        x: The number to square.

    Returns:
        x ** 2.
    """
    return x ** 2


def cube(x: float) -> float:
    """Return x cubed (x ** 3).

    Args:
        x: The number to cube.

    Returns:
        x ** 3.
    """
    return x ** 3


def square_root(x: float) -> float:
    """Return the square root of x.

    Args:
        x: The number to take the square root of.  Must be non-negative.

    Returns:
        math.sqrt(x).

    Raises:
        ValueError: If x is negative.
    """
    if x < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(x)


def cube_root(x: float) -> float:
    """Return the cube root of x.

    Handles negative inputs by computing -(abs(x) ** (1/3)) to avoid
    complex-number results from Python's native power operator on negatives.

    Args:
        x: The number to take the cube root of.

    Returns:
        The real-valued cube root of x.
    """
    if x == 0:
        return 0.0
    if x < 0:
        return -(abs(x) ** (1 / 3))
    return x ** (1 / 3)


def factorial(n: float) -> int:
    """Return the factorial of n.

    Args:
        n: A non-negative integer (or float representing an integer, e.g. 5.0).
            Boolean values are rejected.

    Returns:
        n! as an integer.

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
    return math.factorial(n)


def power(base: float, exp: float) -> float:
    """Return base raised to the power of exp.

    Args:
        base: The base number.
        exp: The exponent.

    Returns:
        base ** exp.
    """
    return base ** exp


def log(x: float) -> float:
    """Return the base-10 logarithm of x.

    Args:
        x: The number to take the logarithm of.  Must be positive.

    Returns:
        math.log10(x).

    Raises:
        ValueError: If x is less than or equal to 0.
    """
    if x <= 0:
        raise ValueError("Logarithm is only defined for positive numbers.")
    return math.log10(x)


def ln(x: float) -> float:
    """Return the natural logarithm of x.

    Args:
        x: The number to take the natural logarithm of.  Must be positive.

    Returns:
        math.log(x).

    Raises:
        ValueError: If x is less than or equal to 0.
    """
    if x <= 0:
        raise ValueError("Natural logarithm is only defined for positive numbers.")
    return math.log(x)
