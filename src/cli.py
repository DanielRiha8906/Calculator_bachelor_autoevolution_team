"""Backward-compatibility facade for the calculator CLI.

All user interface logic has been moved to :mod:`src.interface`.
This module re-exports every public and private symbol from that module
so that existing callers of ``src.cli`` continue to work without changes.
"""

from .interface import (
    MaxRetriesExceeded,
    OPERATIONS,
    prompt_for_first_number,
    prompt_for_operator,
    prompt_for_second_number,
    display_result,
    display_result_unary,
    display_result_binary,
    display_error,
    display_history,
    display_history_notification,
    persist_history_to_file,
    run_calculator,
    _format_history_entry,
    _get_operation_arity,
    _get_calculator_method,
    _get_display_symbol,
)

__all__ = [
    "MaxRetriesExceeded",
    "OPERATIONS",
    "prompt_for_first_number",
    "prompt_for_operator",
    "prompt_for_second_number",
    "display_result",
    "display_result_unary",
    "display_result_binary",
    "display_error",
    "display_history",
    "display_history_notification",
    "persist_history_to_file",
    "run_calculator",
    "_format_history_entry",
    "_get_operation_arity",
    "_get_calculator_method",
    "_get_display_symbol",
]
