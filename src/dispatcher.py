"""Dispatch logic for executing calculations via CalculatorWithHistory.

This module provides run_calculation for binary arithmetic operations and
run_unary_calculation for scientific unary operations.  Both functions
instantiate a CalculatorWithHistory object and dispatch the named method.
The module contains no I/O and no parsing logic.
"""

from src.calculator_with_history import CalculatorWithHistory
from src.logger import get_logger


def run_calculation(
    a: float, b: float, method_name: str
) -> tuple[float, CalculatorWithHistory]:
    """Instantiate a CalculatorWithHistory and dispatch the named binary method.

    Args:
        a: The first operand.
        b: The second operand.
        method_name: The CalculatorWithHistory method to call
            (e.g. 'add', 'divide').

    Returns:
        A tuple of (result, calculator_instance) where result is the
        calculated float value and calculator_instance is the
        CalculatorWithHistory object whose ``get_history()`` reflects the
        completed operation.

    Raises:
        ZeroDivisionError: Propagated from CalculatorWithHistory.divide
            when b is zero.
        ValueError: Propagated from CalculatorWithHistory when inputs are
            invalid.
    """
    calc = CalculatorWithHistory()
    result: float = getattr(calc, method_name)(a, b)
    return result, calc


def run_unary_calculation(
    x: float, method_name: str
) -> tuple[float, CalculatorWithHistory]:
    """Instantiate a CalculatorWithHistory and dispatch the named unary method.

    Intended for scientific operations (sin, cos, tan, log, ln, exp, sqrt)
    that take a single operand.

    Args:
        x: The single operand.
        method_name: The CalculatorWithHistory method to call
            (e.g. 'sin', 'sqrt').

    Returns:
        A tuple of (result, calculator_instance) where result is the
        calculated float value and calculator_instance is the
        CalculatorWithHistory object whose ``get_history()`` reflects the
        completed operation.

    Raises:
        ValueError: Propagated from CalculatorWithHistory when the operand
            is outside the function's domain.
    """
    calc = CalculatorWithHistory()
    result: float = getattr(calc, method_name)(x)
    return result, calc
