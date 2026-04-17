"""Input validation module for calculator interactive mode.

Provides operation and operand validation with configurable retry limits.
Retry counters are per-input-type (operation vs operand) and reset on valid input.
"""

from __future__ import annotations

from typing import Callable

MAX_RETRIES: int = 5


class RetryExhausted(Exception):
    """Raised when max retries exceeded for an input type."""

    def __init__(self, input_type: str, max_retries: int) -> None:
        self.input_type = input_type
        self.max_retries = max_retries
        super().__init__(
            f"Max retries ({max_retries}) exceeded for input type '{input_type}'."
        )


class RetryCounter:
    """Tracks consecutive failed attempts per input type."""

    def __init__(self) -> None:
        self._counts: dict[str, int] = {}

    def increment(self, input_type: str) -> int:
        """Increment counter for input_type, return new count.

        Args:
            input_type: Label identifying the category of input being tracked.

        Returns:
            The new counter value after incrementing.
        """
        self._counts[input_type] = self._counts.get(input_type, 0) + 1
        return self._counts[input_type]

    def reset(self, input_type: str) -> None:
        """Reset counter to 0 for input_type.

        Args:
            input_type: Label identifying the category of input to reset.
        """
        self._counts[input_type] = 0

    def get(self, input_type: str) -> int:
        """Get current count for input_type (0 if not tracked).

        Args:
            input_type: Label identifying the category of input to query.

        Returns:
            Current failure count, or 0 if the type has never been tracked.
        """
        return self._counts.get(input_type, 0)

    def is_exhausted(self, input_type: str, max_retries: int) -> bool:
        """Return True if count for input_type >= max_retries.

        Args:
            input_type: Label identifying the category of input to check.
            max_retries: The maximum number of allowed consecutive failures.

        Returns:
            True if the counter has reached or exceeded max_retries.
        """
        return self.get(input_type) >= max_retries


def validate_operation(op_key: str, operations: dict) -> str:
    """Validate that op_key is a supported operation.

    Args:
        op_key: The operation key entered by the user (already lowercased).
        operations: Dict mapping operation keys to their metadata.

    Returns:
        Normalized (lowercased) op_key if valid.

    Raises:
        ValueError: If op_key is not in operations, with list of available operations.
    """
    if op_key not in operations:
        available = ", ".join(sorted(operations.keys()))
        raise ValueError(
            f"Invalid operation '{op_key}'. Available operations: {available}"
        )
    return op_key


def validate_operand(
    raw_operand: str,
    coerce: Callable,
    operand_position: str = "",
) -> float:
    """Validate and coerce a single operand string to a numeric value.

    Args:
        raw_operand: The raw string entered by the user.
        coerce: A callable (e.g., float, int) to convert the string.
        operand_position: Optional label (e.g., "first", "second") for error context.

    Returns:
        Coerced numeric value.

    Raises:
        ValueError: If raw_operand cannot be coerced to a number.
    """
    try:
        return coerce(raw_operand)
    except (ValueError, TypeError):
        raise ValueError(
            f"Invalid operand '{raw_operand}': expected a numeric value."
        )
