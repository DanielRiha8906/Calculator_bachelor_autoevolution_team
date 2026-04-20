"""Backward-compatibility re-export — implementation lives in src.presentation.interactive."""
from src.presentation.interactive import (
    InvalidInputError,
    OperandRetryExceeded,
    OPERATIONS,
    BASIC_OPERATIONS,
    SCIENTIFIC_OPERATIONS,
    parse_number,
    get_operands,
    execute_operation,
    format_result,
    run_interactive,
    MAX_RETRIES,
)

__all__ = [
    "InvalidInputError",
    "OperandRetryExceeded",
    "OPERATIONS",
    "BASIC_OPERATIONS",
    "SCIENTIFIC_OPERATIONS",
    "parse_number",
    "get_operands",
    "execute_operation",
    "format_result",
    "run_interactive",
    "MAX_RETRIES",
]
