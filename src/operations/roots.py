"""Root and exponentiation operation functions.

Standalone implementations of factorial, square, cube, square_root, and
cube_root operations.
"""

import math


def factorial(n) -> int:
    """Calculate the factorial of n.

    Args:
        n: A non-negative integer, or a float representing a whole number
           (e.g. 5.0). Must satisfy n >= 0.

    Returns:
        The factorial of n as an integer.

    Raises:
        TypeError: If n is a float with a non-integer value (e.g. 5.5).
        ValueError: If n is negative.
    """
    if isinstance(n, float):
        if n != int(n):
            raise TypeError("factorial() only accepts integer values, not non-integer floats")
        n = int(n)
    if n < 0:
        raise ValueError("factorial() not defined for negative values")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def square(x: float) -> float:
    """Return the square of x.

    Args:
        x: The number to square.

    Returns:
        x raised to the power of 2.
    """
    return x ** 2


def cube(x: float) -> float:
    """Return the cube of x.

    Args:
        x: The number to cube.

    Returns:
        x raised to the power of 3.
    """
    return x ** 3


def square_root(x: float) -> float:
    """Return the square root of x.

    Args:
        x: A non-negative number.

    Returns:
        The square root of x.

    Raises:
        ValueError: If x is negative.
    """
    if x < 0:
        raise ValueError("square_root() not defined for negative values")
    return math.sqrt(x)


def cube_root(x: float) -> float:
    """Return the cube root of x.

    Handles negative inputs correctly by preserving the sign of x.

    Args:
        x: The number to take the cube root of.

    Returns:
        The real-valued cube root of x.
    """
    if x == 0:
        return 0.0
    return math.copysign(abs(x) ** (1 / 3), x)
