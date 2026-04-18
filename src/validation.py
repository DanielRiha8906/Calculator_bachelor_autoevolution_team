"""Centralised input validation for the calculator.

This module provides pure validation helpers that are free of I/O side-effects
and carry no dependency on :mod:`src.input_loop`, ensuring there is no circular
import.  Both :mod:`src.input_loop` and :mod:`src.cli` may import from here.
"""

from __future__ import annotations

# Mirrors the OPERATIONS keys defined in src/input_loop.py.
# Must be kept in sync whenever input_loop.OPERATIONS is changed.
VALID_OPERATIONS: frozenset[str] = frozenset({
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "factorial",
    "square",
    "cube",
    "square_root",
    "cube_root",
    "log",
    "ln",
})


def validate_operation(operation: str) -> tuple[bool, str]:
    """Validate that *operation* is a recognised calculator operation.

    Args:
        operation: The raw operation string supplied by the user.

    Returns:
        A two-tuple ``(valid, error_message)``.  When *valid* is ``True``
        the operation is accepted and *error_message* is an empty string.
        When *valid* is ``False`` *error_message* describes the problem.
    """
    if operation in VALID_OPERATIONS:
        return (True, "")
    valid_list = ", ".join(sorted(VALID_OPERATIONS))
    return (False, f"Invalid operation. Valid operations are: {valid_list}")


def validate_operand(raw: str) -> tuple[bool, float, str]:
    """Validate that *raw* can be parsed as a floating-point operand.

    Args:
        raw: The raw string supplied by the user for an operand.

    Returns:
        A three-tuple ``(valid, value, error_message)``.  When *valid* is
        ``True``, *value* holds the parsed ``float`` and *error_message* is
        an empty string.  When *valid* is ``False``, *value* is ``0.0`` and
        *error_message* describes the problem.
    """
    try:
        return (True, float(raw), "")
    except ValueError:
        return (False, 0.0, "Invalid operand. Please enter a numeric value.")
