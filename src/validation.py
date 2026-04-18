"""Interaction layer — input validation.

Validates and sanitizes user input before it is dispatched to the Calculator.
Part of the interaction layer; has no direct role in arithmetic computation.

This module provides pure validation helpers that are free of I/O side-effects
and carry no dependency on :mod:`src.input_loop`, ensuring there is no circular
import.  Both :mod:`src.input_loop` and :mod:`src.cli` may import from here.
"""

from __future__ import annotations

from .mode import Mode, get_operations_for_mode

# Mirrors the OPERATIONS keys defined in src/input_loop.py.
# Must be kept in sync whenever input_loop.OPERATIONS is changed.
# Used as the default (all-operations) set when no mode is provided.
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
    "history",
})


def validate_operation(
    operation: str,
    mode: Mode | None = None,
) -> tuple[bool, str]:
    """Validate that *operation* is a recognised calculator operation.

    When *mode* is ``None`` the validation is performed against the full set
    of known operations (``VALID_OPERATIONS``), which preserves existing
    behaviour for CLI callers and tests that do not pass a mode.

    When *mode* is provided the validation is restricted to the operations
    available in that mode (via :func:`~src.mode.get_operations_for_mode`).

    Args:
        operation: The raw operation string supplied by the user.
        mode: Optional :class:`~src.mode.Mode` value.  When given, only
            operations valid for that mode are accepted.

    Returns:
        A two-tuple ``(valid, error_message)``.  When *valid* is ``True``
        the operation is accepted and *error_message* is an empty string.
        When *valid* is ``False`` *error_message* describes the problem.
    """
    if mode is None:
        allowed = VALID_OPERATIONS
    else:
        allowed = get_operations_for_mode(mode)

    if operation in allowed:
        return (True, "")
    valid_list = ", ".join(sorted(allowed))
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
