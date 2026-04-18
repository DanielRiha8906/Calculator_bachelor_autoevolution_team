"""Tests for src/error_logger.py.

Tests the ErrorLogger class's ability to record categorised error events
to both in-memory list and a persistent log file. File I/O is isolated
using temporary directories to avoid polluting the repository.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

import pytest

from src.error_logger import (
    INVALID_INPUT,
    UNSUPPORTED_OPERATION,
    CALCULATION_ERROR,
    UNEXPECTED_ERROR,
    ERROR_CATEGORIES,
    ErrorLogger,
)


# ---------------------------------------------------------------------------
# ErrorLogger.__init__ tests
# ---------------------------------------------------------------------------


def test_error_logger_init_creates_file_if_missing(tmp_path: Path) -> None:
    """__init__ must create the log file if it does not exist."""
    log_file = tmp_path / "error.log"
    assert not log_file.exists()

    ErrorLogger(str(log_file))

    assert log_file.exists()


def test_error_logger_init_does_not_truncate_existing_file(tmp_path: Path) -> None:
    """__init__ must preserve existing file content (append mode)."""
    log_file = tmp_path / "error.log"
    original_content = "Previous session content\n"
    log_file.write_text(original_content, encoding="utf-8")

    ErrorLogger(str(log_file))

    # Content must still exist
    assert log_file.read_text(encoding="utf-8") == original_content


def test_error_logger_init_history_empty_list(tmp_path: Path) -> None:
    """__init__ must initialize _history to an empty list."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    assert logger._history == []
    assert isinstance(logger._history, list)


def test_error_logger_init_default_file_path() -> None:
    """__init__ with no argument must use 'error.log' as default path."""
    logger = ErrorLogger()

    assert logger._file_path == "error.log"

    # Clean up the file
    if Path("error.log").exists():
        Path("error.log").unlink()


def test_error_logger_init_custom_file_path(tmp_path: Path) -> None:
    """__init__ with custom path must use that path."""
    custom_path = tmp_path / "custom_errors.log"
    logger = ErrorLogger(str(custom_path))

    assert logger._file_path == str(custom_path)
    assert custom_path.exists()


def test_error_logger_init_file_creation_failure_prints_stderr(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """__init__ on unwritable path must print to stderr and not raise."""
    # Create a path that cannot be written to
    bad_path = tmp_path / "nonexistent_parent" / "error.log"

    # This should not raise, but print to stderr
    logger = ErrorLogger(str(bad_path))

    captured = capsys.readouterr()
    assert "ErrorLogger" in captured.err
    assert "could not initialise" in captured.err.lower()
    # Logger should still be usable in memory-only mode
    assert logger._history == []


# ---------------------------------------------------------------------------
# ErrorLogger.log_error() tests
# ---------------------------------------------------------------------------


def test_error_logger_log_error_adds_to_history(tmp_path: Path) -> None:
    """log_error must append entry to _history."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(CALCULATION_ERROR, "Division by zero", {})

    assert len(logger._history) == 1
    assert CALCULATION_ERROR in logger._history[0]


def test_error_logger_log_error_writes_to_file(tmp_path: Path) -> None:
    """log_error must write entry to the log file."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(CALCULATION_ERROR, "Division by zero", {})

    content = log_file.read_text(encoding="utf-8")
    assert CALCULATION_ERROR in content
    assert "Division by zero" in content


def test_error_logger_log_error_format_with_empty_context(tmp_path: Path) -> None:
    """log_error with empty context must use [TIMESTAMP] [CATEGORY] Message format."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(INVALID_INPUT, "Bad input", {})

    entry = logger._history[0]
    # Format: [TIMESTAMP] [CATEGORY] Message
    assert entry.startswith("[")
    assert "] [" in entry
    assert INVALID_INPUT in entry
    assert "Bad input" in entry
    # No pipe separator for empty context
    assert " | " not in entry


def test_error_logger_log_error_format_with_single_key_context(
    tmp_path: Path,
) -> None:
    """log_error with single key context must include | separator and key=value."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(
        CALCULATION_ERROR,
        "Error message",
        {"operation": "divide"}
    )

    entry = logger._history[0]
    assert " | " in entry
    assert "operation=divide" in entry


def test_error_logger_log_error_format_with_multiple_keys(
    tmp_path: Path,
) -> None:
    """log_error with multiple keys must join with semicolons."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(
        CALCULATION_ERROR,
        "Error message",
        {"operation": "divide", "operands": [10.0, 0.0], "error": "division by zero"}
    )

    entry = logger._history[0]
    assert " | " in entry
    assert ";" in entry
    # All keys should be present
    assert "operation=" in entry
    assert "operands=" in entry
    assert "error=" in entry


def test_error_logger_log_error_preserves_insertion_order(tmp_path: Path) -> None:
    """Multiple log_error calls must be recorded in insertion order."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(CALCULATION_ERROR, "First error", {})
    logger.log_error(INVALID_INPUT, "Second error", {})
    logger.log_error(UNEXPECTED_ERROR, "Third error", {})

    assert len(logger._history) == 3
    assert CALCULATION_ERROR in logger._history[0]
    assert INVALID_INPUT in logger._history[1]
    assert UNEXPECTED_ERROR in logger._history[2]


def test_error_logger_log_error_file_io_failure_prints_stderr(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """log_error on write failure must print to stderr and not raise."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    # Mock open to raise OSError
    with patch("builtins.open", side_effect=OSError("Permission denied")):
        # Should not raise
        logger.log_error(CALCULATION_ERROR, "Test error", {})

    captured = capsys.readouterr()
    assert "ErrorLogger" in captured.err
    assert "failed to write" in captured.err.lower()


def test_error_logger_log_error_entry_still_in_memory_on_file_failure(
    tmp_path: Path,
) -> None:
    """log_error must add to _history even if file write fails."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    with patch("builtins.open", side_effect=OSError("Permission denied")):
        logger.log_error(CALCULATION_ERROR, "Test error", {})

    # Entry must still be in memory
    assert len(logger._history) == 1
    assert CALCULATION_ERROR in logger._history[0]


def test_error_logger_log_error_special_characters_in_message(tmp_path: Path) -> None:
    """log_error must handle special characters in message."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    message = "Error: 'quoted' \"double\" | pipe ; semicolon"
    logger.log_error(INVALID_INPUT, message, {})

    entry = logger._history[0]
    assert message in entry


def test_error_logger_log_error_very_long_message(tmp_path: Path) -> None:
    """log_error must handle very long messages."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    long_msg = "x" * 10000
    logger.log_error(CALCULATION_ERROR, long_msg, {})

    assert len(logger._history[0]) > 10000


def test_error_logger_log_error_unicode_characters(tmp_path: Path) -> None:
    """log_error must handle unicode characters in messages and context."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(
        INVALID_INPUT,
        "Errör: ñ é ü 日本語 🔥",
        {"context": "test™"}
    )

    entry = logger._history[0]
    assert "Errör" in entry
    assert "🔥" in entry
    # Verify file was written with UTF-8
    content = log_file.read_text(encoding="utf-8")
    assert "Errör" in content


# ---------------------------------------------------------------------------
# ErrorLogger.get_errors() tests
# ---------------------------------------------------------------------------


def test_error_logger_get_errors_returns_copy(tmp_path: Path) -> None:
    """get_errors must return a copy, not the original list."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(CALCULATION_ERROR, "Error 1", {})
    errors1 = logger.get_errors()
    errors2 = logger.get_errors()

    assert errors1 == errors2
    assert errors1 is not errors2  # Different objects


def test_error_logger_get_errors_empty_initially(tmp_path: Path) -> None:
    """get_errors must return empty list when no errors logged."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    assert logger.get_errors() == []


def test_error_logger_get_errors_returns_chronological_order(tmp_path: Path) -> None:
    """get_errors must return entries in insertion order."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(CALCULATION_ERROR, "First", {})
    logger.log_error(INVALID_INPUT, "Second", {})
    logger.log_error(UNEXPECTED_ERROR, "Third", {})

    errors = logger.get_errors()
    assert len(errors) == 3
    assert "First" in errors[0]
    assert "Second" in errors[1]
    assert "Third" in errors[2]


def test_error_logger_get_errors_mutation_does_not_affect_logger(
    tmp_path: Path,
) -> None:
    """Mutating the returned list must not affect the logger's internal state."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(CALCULATION_ERROR, "Original", {})
    errors = logger.get_errors()
    errors.clear()

    # Logger must still have the entry
    assert len(logger.get_errors()) == 1


# ---------------------------------------------------------------------------
# ErrorLogger._format_entry tests
# ---------------------------------------------------------------------------


def test_error_logger_format_entry_with_empty_context(tmp_path: Path) -> None:
    """_format_entry with empty context must not include pipe separator."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    timestamp = "2026-04-18T12:34:56Z"
    entry = logger._format_entry(timestamp, INVALID_INPUT, "Bad input", {})

    # Expected: [2026-04-18T12:34:56Z] [INVALID_INPUT] Bad input
    assert entry == "[2026-04-18T12:34:56Z] [INVALID_INPUT] Bad input"
    assert " | " not in entry


def test_error_logger_format_entry_with_single_context_item(tmp_path: Path) -> None:
    """_format_entry with one context key must format as [TIMESTAMP] [CATEGORY] Message | key=value."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    timestamp = "2026-04-18T12:34:56Z"
    entry = logger._format_entry(
        timestamp,
        CALCULATION_ERROR,
        "Error msg",
        {"operation": "divide"}
    )

    assert "[2026-04-18T12:34:56Z] [CALCULATION_ERROR] Error msg | operation=divide" == entry


def test_error_logger_format_entry_with_multiple_context_items(tmp_path: Path) -> None:
    """_format_entry with multiple keys must join with semicolons."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    timestamp = "2026-04-18T12:34:56Z"
    context = {"op": "add", "a": 1, "b": 2}
    entry = logger._format_entry(timestamp, INVALID_INPUT, "Test", context)

    # Entry must include all keys and use semicolons
    assert "[2026-04-18T12:34:56Z] [INVALID_INPUT] Test | " in entry
    assert "op=add" in entry
    assert "a=1" in entry
    assert "b=2" in entry
    # Must use semicolons to separate
    parts = entry.split(" | ")[1].split("; ")
    assert len(parts) == 3


def test_error_logger_format_entry_human_readable(tmp_path: Path) -> None:
    """_format_entry output must be human-readable and parseable."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    timestamp = "2026-04-18T12:34:56Z"
    entry = logger._format_entry(
        timestamp,
        CALCULATION_ERROR,
        "Division by zero occurred",
        {"operation": "divide", "operands": [10, 0]}
    )

    # Must be single-line, readable format
    assert "\n" not in entry
    assert "[" in entry and "]" in entry  # Timestamps bracketed
    assert CALCULATION_ERROR in entry
    assert "Division by zero" in entry
    assert "|" in entry


# ---------------------------------------------------------------------------
# ErrorLogger — session isolation tests
# ---------------------------------------------------------------------------


def test_error_logger_multiple_instances_independent(tmp_path: Path) -> None:
    """Two ErrorLogger instances must have independent in-memory lists."""
    log_file = tmp_path / "error.log"

    logger1 = ErrorLogger(str(log_file))
    logger1.log_error(CALCULATION_ERROR, "Error from logger1", {})

    logger2 = ErrorLogger(str(log_file))
    logger2.log_error(INVALID_INPUT, "Error from logger2", {})

    # Each instance's in-memory list is independent
    assert len(logger1.get_errors()) == 1
    assert len(logger2.get_errors()) == 1
    # But both wrote to the same file
    content = log_file.read_text(encoding="utf-8")
    assert "Error from logger1" in content
    assert "Error from logger2" in content


def test_error_logger_file_append_across_instances(tmp_path: Path) -> None:
    """Second ErrorLogger instance must append to file, not truncate."""
    log_file = tmp_path / "error.log"

    logger1 = ErrorLogger(str(log_file))
    logger1.log_error(CALCULATION_ERROR, "First entry", {})

    # Create new instance pointing to same file
    logger2 = ErrorLogger(str(log_file))
    logger2.log_error(INVALID_INPUT, "Second entry", {})

    content = log_file.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    assert len(lines) == 2
    assert "First entry" in lines[0]
    assert "Second entry" in lines[1]


def test_error_logger_all_category_constants_defined() -> None:
    """All error category constants must be defined and in ERROR_CATEGORIES."""
    assert INVALID_INPUT in ERROR_CATEGORIES
    assert UNSUPPORTED_OPERATION in ERROR_CATEGORIES
    assert CALCULATION_ERROR in ERROR_CATEGORIES
    assert UNEXPECTED_ERROR in ERROR_CATEGORIES
    assert len(ERROR_CATEGORIES) == 4


def test_error_logger_log_all_categories(tmp_path: Path) -> None:
    """log_error must accept all defined error categories."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(INVALID_INPUT, "Invalid input error", {})
    logger.log_error(UNSUPPORTED_OPERATION, "Unsupported operation error", {})
    logger.log_error(CALCULATION_ERROR, "Calculation error", {})
    logger.log_error(UNEXPECTED_ERROR, "Unexpected error", {})

    errors = logger.get_errors()
    assert len(errors) == 4
    assert any(INVALID_INPUT in e for e in errors)
    assert any(UNSUPPORTED_OPERATION in e for e in errors)
    assert any(CALCULATION_ERROR in e for e in errors)
    assert any(UNEXPECTED_ERROR in e for e in errors)


def test_error_logger_timestamp_format_iso8601(tmp_path: Path) -> None:
    """log_error must include ISO-8601 formatted timestamps."""
    log_file = tmp_path / "error.log"
    logger = ErrorLogger(str(log_file))

    logger.log_error(CALCULATION_ERROR, "Test", {})

    entry = logger._history[0]
    # Check for ISO-8601 format: YYYY-MM-DDTHH:MM:SS±HH:MM or Z
    assert "T" in entry  # ISO-8601 has T separator
    assert "[" in entry  # Timestamp is bracketed
    # Extract timestamp between first [ and ]
    import re
    match = re.search(r"\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[Z+-].*?)\]", entry)
    assert match is not None
