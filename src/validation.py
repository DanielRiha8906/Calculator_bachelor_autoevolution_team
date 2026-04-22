"""Centralised input validation utilities for the calculator."""

from . import error_logger


class OperandValidationError(ValueError):
    """Raised when a string cannot be converted to a valid numeric operand."""


class OperationValidationError(ValueError):
    """Raised when a requested operation key is not available in the registry."""


def validate_operand(raw: str) -> float:
    """Convert a raw string to a float, raising a descriptive error on failure.

    Args:
        raw: The user-supplied string to convert.

    Returns:
        The parsed float value.

    Raises:
        OperandValidationError: If ``raw`` cannot be interpreted as a float.
    """
    try:
        return float(raw)
    except ValueError as exc:
        error_logger.log_validation_error(str(exc))
        raise OperandValidationError(
            f"'{raw}' is not a valid number"
        ) from exc


def validate_operation(choice: str, available_operations: dict) -> bool:
    """Check whether a choice string is a registered operation key.

    Args:
        choice: The user-supplied operation identifier.
        available_operations: Mapping of valid operation keys to descriptions.

    Returns:
        True if ``choice`` is a key in ``available_operations``, False otherwise.
    """
    if choice in available_operations:
        return True
    error_logger.log_operation_error(choice, f"Operation '{choice}' is not available")
    return False


def get_validation_error_message(error: Exception) -> str:
    """Return a user-friendly message string for a validation exception.

    Args:
        error: A validation exception instance.

    Returns:
        A descriptive, human-readable error message string.
    """
    return str(error)
