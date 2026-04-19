"""Interactive input collection for the Calculator application.

This module re-exports the input collection functions from
:mod:`src.interactive.session`, providing a dedicated module for input
handling concerns.  The canonical implementations of
:func:`get_operation_choice` and :func:`get_operands` live in
:mod:`src.interactive.session` so that the structural test invariants
of that module are preserved.

Import from this module when you need only the input collection layer
without the full session lifecycle.
"""

from .session import (
    _error_logger,
    get_operation_choice,
    get_operands,
    MAX_VALIDATION_ATTEMPTS,
    _HISTORY_TOKEN,
)

__all__ = [
    "_error_logger",
    "get_operation_choice",
    "get_operands",
    "MAX_VALIDATION_ATTEMPTS",
    "_HISTORY_TOKEN",
]
