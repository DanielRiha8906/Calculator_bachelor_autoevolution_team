"""Result formatting utilities for the Calculator application.

This module provides helpers for converting calculation results into
human-readable strings for display.  It has no dependency on I/O, session
state, or CLI argument parsing.
"""


def format_result(result: int | float) -> str:
    """Format a calculation result for display.

    Args:
        result: A numeric calculation result (int or float).

    Returns:
        The string representation of *result*.

    Examples:
        >>> format_result(42)
        '42'
        >>> format_result(3.14)
        '3.14'
    """
    return str(result)
