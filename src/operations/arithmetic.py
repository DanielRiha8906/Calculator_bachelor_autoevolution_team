"""Pure arithmetic operation functions.

Standalone implementations of the four basic arithmetic operations.
These delegate to CalculationEngine to avoid code duplication.
"""

from src.core.engine import CalculationEngine

_engine = CalculationEngine()


def add(a: float, b: float) -> float:
    """Return the sum of a and b.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        a + b.
    """
    return _engine.add(a, b)


def subtract(a: float, b: float) -> float:
    """Return the difference of a and b.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        a - b.
    """
    return _engine.subtract(a, b)


def multiply(a: float, b: float) -> float:
    """Return the product of a and b.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        a * b.
    """
    return _engine.multiply(a, b)


def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        a / b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    return _engine.divide(a, b)
