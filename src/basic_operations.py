"""Pure functions for basic arithmetic operations.

No state, no Calculator dependency.  All functions operate on plain numeric
arguments and return a numeric result.  Callers are responsible for recording
history if needed.
"""


def add(a: float, b: float) -> float:
    """Return the sum of a and b.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        a + b.
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a minus b.

    Args:
        a: The minuend.
        b: The subtrahend.

    Returns:
        a - b.
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b.

    Args:
        a: The first factor.
        b: The second factor.

    Returns:
        a * b.
    """
    return a * b


def divide(a: float, b: float) -> float:
    """Return a divided by b.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        a / b.

    Raises:
        ZeroDivisionError: If b is zero (raised naturally by Python).
    """
    return a / b
