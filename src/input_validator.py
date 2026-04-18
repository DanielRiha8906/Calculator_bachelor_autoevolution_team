"""Centralized validation of operations and operands for the calculator.

Provides exception classes and pure validation functions used by the
interactive input loop to guard against bad user input before dispatching
to the Calculator engine.
"""

from __future__ import annotations

# Maximum number of consecutive invalid inputs before a session is terminated.
MAX_RETRY_ATTEMPTS: int = 3


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------


class ValidationError(Exception):
    """Base exception for all input-validation failures."""


class InvalidOperationError(ValidationError):
    """Raised when the user supplies an operation key not in OPERATIONS."""


class InvalidOperandError(ValidationError):
    """Raised when an operand string cannot be parsed as a float."""


class OperandCountError(ValidationError):
    """Raised when the number of supplied operands does not match the expected count."""


# ---------------------------------------------------------------------------
# Validation functions
# ---------------------------------------------------------------------------


def validate_operation(choice: str, valid_operations: dict) -> str:
    """Validate that *choice* is a recognised operation key.

    Args:
        choice: The raw string entered by the user (already stripped/lowercased
            by the caller is recommended, but not required here).
        valid_operations: A mapping of valid operation keys to their metadata
            (e.g. ``OPERATIONS`` from :mod:`src.input_loop`).

    Returns:
        The validated operation key (identical to *choice* when valid).

    Raises:
        InvalidOperationError: If *choice* is not a key in *valid_operations*.
    """
    if choice not in valid_operations:
        raise InvalidOperationError(
            f"Unknown operation: '{choice}'. Type a valid operation key or 'exit'."
        )
    return choice


def validate_operands(raw_inputs: list[str], count: int) -> list[float]:
    """Validate and convert a list of raw operand strings to floats.

    Args:
        raw_inputs: Strings entered by the user, one per operand.
        count: The number of operands expected for the chosen operation.

    Returns:
        A list of ``float`` values corresponding to *raw_inputs*.

    Raises:
        OperandCountError: If ``len(raw_inputs) != count``.
        InvalidOperandError: If any element of *raw_inputs* cannot be
            converted to ``float``.
    """
    if len(raw_inputs) != count:
        raise OperandCountError(
            f"Expected {count} operand(s), got {len(raw_inputs)}."
        )

    operands: list[float] = []
    for raw in raw_inputs:
        try:
            operands.append(float(raw))
        except ValueError:
            raise InvalidOperandError(
                f"Invalid operand '{raw}': must be a numeric value."
            )
    return operands
