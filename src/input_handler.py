"""Backwards-compatible re-export shim for input_handler.

This module previously contained parsing and dispatch logic that has been
split into src.parser (pure parsing logic) and src.dispatcher (dispatch
logic). This shim re-exports all public names so that existing callers and
tests that import from src.input_handler continue to work without changes.

New code should import directly from src.parser or src.dispatcher.
"""

from src.dispatcher import run_calculation
from src.parser import BINARY_OPERATORS, parse_input, parse_operand

__all__ = [
    "BINARY_OPERATORS",
    "parse_operand",
    "parse_input",
    "run_calculation",
]
