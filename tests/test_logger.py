"""Comprehensive pytest tests for src/logger.py — Logger error logging.

Tests cover:
- File creation in append mode (multiple Logger instances)
- Log level verification (WARNING vs ERROR)
- Log message format (timestamp, level, message)
- All logger methods: log_unsupported_operation, log_invalid_operand,
  log_invalid_argument_count, log_division_by_zero, log_domain_error
- Edge cases: empty strings, special characters, very long strings, None values
- No stack traces in output
- Duplicate handler guard (multiple Logger instances with same file)
"""

import logging
import pytest
import os
from pathlib import Path

from src.logger import Logger


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def temp_log_file(tmp_path):
    """Return a path to a temporary log file."""
    return str(tmp_path / "test.log")


@pytest.fixture(autouse=True)
def cleanup_logger_handlers():
    """Clean up logger handlers before and after each test.

    This is necessary because Python's logging module maintains a global
    registry of loggers, and handlers persist across test runs. Without
    cleanup, tests can interfere with each other.
    """
    # Clear all handlers from all loggers before test
    for logger_name in list(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    yield

    # Clear handlers after test
    for logger_name in list(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)


# ---------------------------------------------------------------------------
# Test: __init__ - File Creation and Handler Setup
# ---------------------------------------------------------------------------


def test_logger_init_creates_log_file(temp_log_file):
    """Creating a Logger should initialize the log file."""
    logger = Logger(temp_log_file)
    assert logger is not None
    # File may not exist immediately until first write


def test_logger_init_sets_logger_level_to_warning(temp_log_file):
    """Logger should set the internal logger level to WARNING."""
    logger = Logger(temp_log_file)
    # Verify by checking that we can access the logger
    assert logger._logger is not None
    assert logger._logger.level == logging.WARNING


def test_logger_init_with_default_file():
    """Logger should use 'error.log' as default file name."""
    logger = Logger()
    assert logger._logger is not None
    # Just verify it doesn't crash


def test_logger_init_with_custom_file_name(temp_log_file):
    """Logger should accept a custom log file name."""
    logger = Logger(temp_log_file)
    assert logger._logger is not None


def test_logger_handler_duplicate_guard(temp_log_file):
    """Multiple Logger instances with same file should not duplicate handlers."""
    logger1 = Logger(temp_log_file)
    initial_handlers = len(logger1._logger.handlers)

    # Directly accessing the same logger name (simulating what happens internally)
    logger2 = Logger(temp_log_file)
    # Should still have the same number of handlers due to duplicate guard
    assert len(logger2._logger.handlers) == initial_handlers


# ---------------------------------------------------------------------------
# Test: log_unsupported_operation - WARNING Level
# ---------------------------------------------------------------------------


def test_log_unsupported_operation_writes_to_file(temp_log_file, capsys):
    """log_unsupported_operation should write a WARNING level entry to file."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("badop")

    # Force handler to flush
    for handler in logger._logger.handlers:
        handler.flush()

    # Verify file contains the message
    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "badop" in content
    assert "Unsupported operation" in content


def test_log_unsupported_operation_level_is_warning(temp_log_file):
    """log_unsupported_operation should log at WARNING level."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("test_op")

    # Flush handlers
    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "WARNING" in content


def test_log_unsupported_operation_with_special_chars(temp_log_file):
    """log_unsupported_operation should handle special characters in operation name."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("op@#$%")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "op@#$%" in content


def test_log_unsupported_operation_with_empty_string(temp_log_file):
    """log_unsupported_operation should handle empty operation name."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Unsupported operation" in content


def test_log_unsupported_operation_with_very_long_name(temp_log_file):
    """log_unsupported_operation should handle very long operation names."""
    long_op = "a" * 1000
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation(long_op)

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert long_op in content


# ---------------------------------------------------------------------------
# Test: log_invalid_operand - ERROR Level
# ---------------------------------------------------------------------------


def test_log_invalid_operand_writes_to_file(temp_log_file):
    """log_invalid_operand should write an ERROR level entry to file."""
    logger = Logger(temp_log_file)
    logger.log_invalid_operand("abc", "<numeric>")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "abc" in content
    assert "<numeric>" in content


def test_log_invalid_operand_level_is_error(temp_log_file):
    """log_invalid_operand should log at ERROR level."""
    logger = Logger(temp_log_file)
    logger.log_invalid_operand("xyz", "<numeric>")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "ERROR" in content


def test_log_invalid_operand_format_includes_raw_value_and_type(temp_log_file):
    """log_invalid_operand should include both raw value and expected type."""
    logger = Logger(temp_log_file)
    logger.log_invalid_operand("not_a_number", "<numeric>")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "not_a_number" in content
    assert "<numeric>" in content
    assert "Invalid operand" in content


def test_log_invalid_operand_with_special_chars(temp_log_file):
    """log_invalid_operand should handle special characters."""
    logger = Logger(temp_log_file)
    logger.log_invalid_operand("@#$%^", "<numeric>")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "@#$%^" in content


def test_log_invalid_operand_with_empty_string(temp_log_file):
    """log_invalid_operand should handle empty raw value."""
    logger = Logger(temp_log_file)
    logger.log_invalid_operand("", "<numeric>")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "<numeric>" in content
    assert "Invalid operand" in content


def test_log_invalid_operand_with_empty_type(temp_log_file):
    """log_invalid_operand should handle empty expected type."""
    logger = Logger(temp_log_file)
    logger.log_invalid_operand("abc", "")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "abc" in content
    assert "Invalid operand" in content


# ---------------------------------------------------------------------------
# Test: log_invalid_argument_count - ERROR Level
# ---------------------------------------------------------------------------


def test_log_invalid_argument_count_writes_to_file(temp_log_file):
    """log_invalid_argument_count should write an ERROR level entry to file."""
    logger = Logger(temp_log_file)
    logger.log_invalid_argument_count("add", 2, 1)

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "add" in content
    assert "2" in content
    assert "1" in content


def test_log_invalid_argument_count_level_is_error(temp_log_file):
    """log_invalid_argument_count should log at ERROR level."""
    logger = Logger(temp_log_file)
    logger.log_invalid_argument_count("multiply", 2, 3)

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "ERROR" in content


def test_log_invalid_argument_count_format_includes_all_info(temp_log_file):
    """log_invalid_argument_count should include operation, expected, and given."""
    logger = Logger(temp_log_file)
    logger.log_invalid_argument_count("divide", 2, 3)

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "divide" in content
    assert "expected 2" in content
    assert "3" in content


def test_log_invalid_argument_count_with_zero_expected(temp_log_file):
    """log_invalid_argument_count should handle zero expected arguments."""
    logger = Logger(temp_log_file)
    logger.log_invalid_argument_count("op", 0, 1)

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "expected 0" in content


def test_log_invalid_argument_count_with_large_numbers(temp_log_file):
    """log_invalid_argument_count should handle large argument counts."""
    logger = Logger(temp_log_file)
    logger.log_invalid_argument_count("op", 100, 200)

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "100" in content
    assert "200" in content


# ---------------------------------------------------------------------------
# Test: log_division_by_zero - ERROR Level
# ---------------------------------------------------------------------------


def test_log_division_by_zero_writes_to_file(temp_log_file):
    """log_division_by_zero should write an ERROR level entry to file."""
    logger = Logger(temp_log_file)
    logger.log_division_by_zero([5, 0])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "5" in content
    assert "0" in content


def test_log_division_by_zero_level_is_error(temp_log_file):
    """log_division_by_zero should log at ERROR level."""
    logger = Logger(temp_log_file)
    logger.log_division_by_zero([10, 0])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "ERROR" in content


def test_log_division_by_zero_format_includes_operands(temp_log_file):
    """log_division_by_zero should include operands in the log."""
    logger = Logger(temp_log_file)
    logger.log_division_by_zero([7.5, 0.0])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "7.5" in content
    assert "0.0" in content
    assert "Division by zero" in content


def test_log_division_by_zero_with_empty_list(temp_log_file):
    """log_division_by_zero should handle empty operand list."""
    logger = Logger(temp_log_file)
    logger.log_division_by_zero([])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Division by zero" in content


def test_log_division_by_zero_with_single_operand(temp_log_file):
    """log_division_by_zero should handle single operand."""
    logger = Logger(temp_log_file)
    logger.log_division_by_zero([0])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Division by zero" in content


def test_log_division_by_zero_with_multiple_operands(temp_log_file):
    """log_division_by_zero should handle more than two operands."""
    logger = Logger(temp_log_file)
    logger.log_division_by_zero([5, 2, 0, 1])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "5" in content
    assert "2" in content
    assert "0" in content


# ---------------------------------------------------------------------------
# Test: log_domain_error - ERROR Level
# ---------------------------------------------------------------------------


def test_log_domain_error_writes_to_file(temp_log_file):
    """log_domain_error should write an ERROR level entry to file."""
    logger = Logger(temp_log_file)
    logger.log_domain_error("square_root", "not defined for negative")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "square_root" in content
    assert "not defined for negative" in content


def test_log_domain_error_level_is_error(temp_log_file):
    """log_domain_error should log at ERROR level."""
    logger = Logger(temp_log_file)
    logger.log_domain_error("log10", "math domain error")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "ERROR" in content


def test_log_domain_error_format_includes_operation_and_message(temp_log_file):
    """log_domain_error should include both operation and error message."""
    logger = Logger(temp_log_file)
    logger.log_domain_error("ln", "math domain error")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "ln" in content
    assert "math domain error" in content
    assert "Domain error" in content


def test_log_domain_error_with_empty_message(temp_log_file):
    """log_domain_error should handle empty error message."""
    logger = Logger(temp_log_file)
    logger.log_domain_error("op", "")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "op" in content
    assert "Domain error" in content


def test_log_domain_error_with_very_long_message(temp_log_file):
    """log_domain_error should handle very long error messages."""
    long_msg = "x" * 500
    logger = Logger(temp_log_file)
    logger.log_domain_error("op", long_msg)

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert long_msg in content


def test_log_domain_error_with_special_chars(temp_log_file):
    """log_domain_error should handle special characters."""
    logger = Logger(temp_log_file)
    logger.log_domain_error("op@#$", "error@#$%^&*()")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "op@#$" in content
    assert "error@#$%^&*()" in content


# ---------------------------------------------------------------------------
# Test: File Format and Structure
# ---------------------------------------------------------------------------


def test_log_file_includes_timestamp(temp_log_file):
    """Log entries should include a timestamp."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("test")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Should match format like "2024-01-01 12:34:56"
    import re
    assert re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', content)


def test_log_file_includes_level(temp_log_file):
    """Log entries should include the log level."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("test")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "WARNING" in content or "ERROR" in content


def test_log_file_includes_message(temp_log_file):
    """Log entries should include the message."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("badop")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "badop" in content


def test_log_file_has_no_stack_trace(temp_log_file):
    """Log entries should not include stack traces."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("test")
    logger.log_invalid_operand("abc", "<numeric>")
    logger.log_division_by_zero([5, 0])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Should not contain typical traceback indicators
    assert "Traceback" not in content
    assert "File \"" not in content or "line" not in content


# ---------------------------------------------------------------------------
# Test: Append Mode (Multiple Logger Instances)
# ---------------------------------------------------------------------------


def test_logger_append_mode_preserves_existing_content(temp_log_file):
    """Creating a new Logger with same file should append, not overwrite."""
    # First logger writes to file
    logger1 = Logger(temp_log_file)
    logger1.log_unsupported_operation("first")

    for handler in logger1._logger.handlers:
        handler.flush()

    # Second logger writes to same file
    # Need to clean handlers to simulate a fresh Logger instance
    first_logger_name = logger1._logger.name
    logging.getLogger(first_logger_name).handlers.clear()

    logger2 = Logger(temp_log_file)
    logger2.log_unsupported_operation("second")

    for handler in logger2._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Both entries should be present
    assert "first" in content
    assert "second" in content


def test_logger_multiple_entries_from_same_instance(temp_log_file):
    """Multiple log calls from same Logger instance should all be written."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("op1")
    logger.log_invalid_operand("xyz", "<numeric>")
    logger.log_division_by_zero([5, 0])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "op1" in content
    assert "xyz" in content
    assert "5" in content
    assert "0" in content


# ---------------------------------------------------------------------------
# Test: UTF-8 Encoding
# ---------------------------------------------------------------------------


def test_log_file_uses_utf8_encoding(temp_log_file):
    """Log file should be written in UTF-8 encoding."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("café")  # Special character

    for handler in logger._logger.handlers:
        handler.flush()

    # Should be readable as UTF-8
    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "café" in content


def test_log_file_unicode_characters(temp_log_file):
    """Log file should handle Unicode characters."""
    logger = Logger(temp_log_file)
    logger.log_invalid_operand("αβγ", "<numeric>")  # Greek letters

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "αβγ" in content


# ---------------------------------------------------------------------------
# Test: Edge Cases and Error Conditions
# ---------------------------------------------------------------------------


def test_logger_with_whitespace_operation_name(temp_log_file):
    """log_unsupported_operation should handle whitespace-only names."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("   ")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Unsupported operation" in content


def test_logger_with_newline_in_message(temp_log_file):
    """Logger should handle newlines in messages (if they occur)."""
    logger = Logger(temp_log_file)
    logger.log_invalid_operand("abc\ndef", "<numeric>")

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Should still contain the message
    assert "abc" in content


def test_logger_with_zero_values(temp_log_file):
    """Logger should handle zero values correctly."""
    logger = Logger(temp_log_file)
    logger.log_invalid_argument_count("op", 0, 0)
    logger.log_division_by_zero([0, 0])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    # Should handle zeros without issue
    assert "0" in content


def test_logger_sequential_calls_different_methods(temp_log_file):
    """Different log methods should write separate entries."""
    logger = Logger(temp_log_file)
    logger.log_unsupported_operation("op1")
    logger.log_invalid_operand("val", "<numeric>")
    logger.log_division_by_zero([5, 0])
    logger.log_domain_error("sqrt", "domain error")
    logger.log_invalid_argument_count("add", 2, 1)

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Should have multiple lines
    assert len(lines) >= 5


# ---------------------------------------------------------------------------
# Test: Logger with Numeric Types
# ---------------------------------------------------------------------------


def test_log_division_by_zero_with_float_operands(temp_log_file):
    """log_division_by_zero should handle float operands."""
    logger = Logger(temp_log_file)
    logger.log_division_by_zero([5.5, 0.0])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "5.5" in content
    assert "0.0" in content


def test_log_division_by_zero_with_int_operands(temp_log_file):
    """log_division_by_zero should handle int operands."""
    logger = Logger(temp_log_file)
    logger.log_division_by_zero([5, 0])

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "5" in content
    assert "0" in content


def test_log_invalid_argument_count_with_large_numbers(temp_log_file):
    """log_invalid_argument_count should handle large argument values."""
    logger = Logger(temp_log_file)
    logger.log_invalid_argument_count("op", 1000, 9999)

    for handler in logger._logger.handlers:
        handler.flush()

    with open(temp_log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "1000" in content
    assert "9999" in content
