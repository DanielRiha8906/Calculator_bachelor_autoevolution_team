"""Interactive input handling for the Calculator application.

This module is a backward-compatibility shim.  All implementation has been
moved to the following canonical locations:

* :mod:`src.core.operations` — operation registry (no UI)
* :mod:`src.interface.menu_renderer` — menu display
* :mod:`src.interactive.input_handler` — operation choice and operand collection
* :mod:`src.interactive.session` — interactive CLI session loop

Importing from this module continues to work as before so that existing call
sites do not need to be updated immediately.
"""

from .interface.menu_renderer import display_menu
from .interactive.input_handler import (
    _error_logger,
    get_operation_choice,
    get_operands,
    MAX_VALIDATION_ATTEMPTS,
    _HISTORY_TOKEN,
)
from .interactive.session import run_interactive_session
from .core.operations import get_operation_registry

__all__ = [
    "display_menu",
    "get_operation_choice",
    "get_operands",
    "run_interactive_session",
    "MAX_VALIDATION_ATTEMPTS",
    "get_operation_registry",
]
