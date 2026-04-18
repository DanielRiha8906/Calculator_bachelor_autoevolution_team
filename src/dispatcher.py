"""Dispatch logic for executing calculations via CalculatorWithHistory.

This module provides the run_calculation function that instantiates a
CalculatorWithHistory object and dispatches the named arithmetic method.
It contains no I/O and no parsing logic.
"""

from src.calculator_with_history import CalculatorWithHistory
from src.logger import get_logger


def run_calculation(
    a: float, b: float, method_name: str
) -> tuple[float, CalculatorWithHistory]:
    """Instantiate a CalculatorWithHistory and dispatch the named method.

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
