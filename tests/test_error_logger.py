"""Comprehensive pytest tests for the ErrorLogger module.

This module tests the error logging functionality of src/error_logger.py,
including initialization, file persistence, entry formatting, context handling,
and error resilience.
"""

import logging
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from src.error_logger import ErrorLogger, _logger, _ensure_handler


# ==================== Initialization & Setup Tests ====================

class TestErrorLoggerInitialization:
    """Tests for ErrorLogger initialization and module-level setup."""

    def test_error_logger_instantiates_without_error(self):
        """Test that ErrorLogger can be instantiated without raising errors."""
        logger = ErrorLogger()
        assert logger is not None
        assert isinstance(logger, ErrorLogger)

    def test_multiple_error_logger_instances(self):
        """Test that multiple ErrorLogger instances can coexist."""
        logger1 = ErrorLogger()
        logger2 = ErrorLogger()
        assert logger1 is not logger2  # Different instances
        assert isinstance(logger1, ErrorLogger)
        assert isinstance(logger2, ErrorLogger)

    def test_logger_is_configured(self):
        """Test that the module-level logger is properly configured."""
        assert _logger.level == logging.ERROR
        assert _logger.name == "calculator.errors"

    def test_logger_propagate_disabled_after_handler_attached(self, tmp_path, monkeypatch):
        """Test that logger propagation is disabled after handler attachment."""
        monkeypatch.chdir(tmp_path)
        # Reset handler state for this test
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {})

        assert not _logger.propagate

    def test_error_log_file_not_created_until_first_error(self, tmp_path, monkeypatch):
        """Test that error.log is not created until first error is logged."""
        monkeypatch.chdir(tmp_path)
        # Reset handler state
        import src.error_logger as el
        el._handler_attached = False

        # Before calling log_error, file should not exist
        assert not (tmp_path / "error.log").exists()

        logger = ErrorLogger()
        logger.log_error("TEST", {"message": "test"})

        # After calling log_error, file should exist
        assert (tmp_path / "error.log").exists()


# ==================== Basic Logging Functionality Tests ====================

class TestBasicLogging:
    """Tests for basic error logging functionality."""

    def test_log_error_creates_file(self, tmp_path, monkeypatch):
        """Test that log_error() creates error.log if it doesn't exist."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST_ERROR", {"message": "test message"})

        assert (tmp_path / "error.log").exists()

    def test_log_error_writes_single_line(self, tmp_path, monkeypatch):
        """Test that each error is written as a single line."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST_ERROR", {"message": "test message"})

        content = (tmp_path / "error.log").read_text()
        lines = content.strip().split('\n')
        assert len(lines) == 1

    def test_log_error_appends_not_overwrites(self, tmp_path, monkeypatch):
        """Test that multiple errors are appended (not overwriting)."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("ERROR1", {"message": "first"})
        logger.log_error("ERROR2", {"message": "second"})

        content = (tmp_path / "error.log").read_text()
        lines = content.strip().split('\n')
        assert len(lines) == 2

    def test_log_error_does_not_raise(self, tmp_path, monkeypatch):
        """Test that log_error() never raises an exception."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        # Should not raise
        logger.log_error("TEST", {"message": "test"})

    def test_log_error_returns_none(self, tmp_path, monkeypatch):
        """Test that log_error() returns None."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        result = logger.log_error("TEST", {"message": "test"})
        assert result is None


# ==================== Log Entry Format Tests ====================

class TestLogEntryFormat:
    """Tests for the format of log entries."""

    def test_log_entry_contains_timestamp(self, tmp_path, monkeypatch):
        """Test that each log entry contains an ISO 8601 timestamp."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"message": "test"})

        content = (tmp_path / "error.log").read_text()
        # ISO 8601 timestamp format: YYYY-MM-DDTHH:MM:SS
        assert "T" in content
        assert "-" in content
        assert ":" in content

    def test_log_entry_contains_error_type(self, tmp_path, monkeypatch):
        """Test that log entry contains the error_type field."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("CUSTOM_ERROR_TYPE", {"message": "test"})

        content = (tmp_path / "error.log").read_text()
        assert "CUSTOM_ERROR_TYPE" in content

    def test_log_entry_contains_operation(self, tmp_path, monkeypatch):
        """Test that log entry contains the operation field."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"operation": "add", "message": "test"})

        content = (tmp_path / "error.log").read_text()
        assert "add" in content

    def test_log_entry_contains_operands(self, tmp_path, monkeypatch):
        """Test that log entry contains the operands field."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"operands": "5, 0", "message": "test"})

        content = (tmp_path / "error.log").read_text()
        assert "5, 0" in content

    def test_log_entry_contains_message(self, tmp_path, monkeypatch):
        """Test that log entry contains the message field."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"message": "custom error message"})

        content = (tmp_path / "error.log").read_text()
        assert "custom error message" in content

    def test_log_entry_format_is_pipe_delimited(self, tmp_path, monkeypatch):
        """Test that fields are separated by pipes (|)."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST_TYPE", {
            "operation": "test_op",
            "operands": "op1, op2",
            "message": "test msg"
        })

        content = (tmp_path / "error.log").read_text()
        # Should have format: TIMESTAMP | ERROR_TYPE | OPERATION | OPERANDS | MESSAGE
        assert content.count("|") >= 4

    def test_log_entry_single_line_format(self, tmp_path, monkeypatch):
        """Test that log entry is on a single line (newline at end only)."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {
            "operation": "add",
            "operands": "5, 3",
            "message": "test error"
        })

        content = (tmp_path / "error.log").read_text()
        lines = content.strip().split('\n')
        assert len(lines) == 1


# ==================== Error Type Tests ====================

class TestErrorTypes:
    """Tests for logging various error types."""

    def test_log_unsupported_operation_error(self, tmp_path, monkeypatch):
        """Test logging UNSUPPORTED_OPERATION error."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("UNSUPPORTED_OPERATION", {
            "operation": "xyz",
            "operands": "N/A",
            "message": "unknown operation 'xyz'"
        })

        content = (tmp_path / "error.log").read_text()
        assert "UNSUPPORTED_OPERATION" in content
        assert "xyz" in content

    def test_log_invalid_operand_error(self, tmp_path, monkeypatch):
        """Test logging INVALID_OPERAND error."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("INVALID_OPERAND", {
            "operation": "add",
            "operands": "abc",
            "message": "not a valid number"
        })

        content = (tmp_path / "error.log").read_text()
        assert "INVALID_OPERAND" in content
        assert "abc" in content

    def test_log_argument_count_mismatch_error(self, tmp_path, monkeypatch):
        """Test logging ARGUMENT_COUNT_MISMATCH error."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("ARGUMENT_COUNT_MISMATCH", {
            "operation": "add",
            "operands": "5",
            "message": "expects 2 operands, got 1"
        })

        content = (tmp_path / "error.log").read_text()
        assert "ARGUMENT_COUNT_MISMATCH" in content
        assert "add" in content

    def test_log_division_by_zero_error(self, tmp_path, monkeypatch):
        """Test logging DIVISION_BY_ZERO error."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("DIVISION_BY_ZERO", {
            "operation": "divide",
            "operands": "10, 0",
            "message": "cannot divide by zero"
        })

        content = (tmp_path / "error.log").read_text()
        assert "DIVISION_BY_ZERO" in content
        assert "divide" in content

    def test_log_invalid_domain_error(self, tmp_path, monkeypatch):
        """Test logging INVALID_DOMAIN error (e.g., sqrt(-1))."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("INVALID_DOMAIN", {
            "operation": "square_root",
            "operands": "-1",
            "message": "cannot take square root of negative number"
        })

        content = (tmp_path / "error.log").read_text()
        assert "INVALID_DOMAIN" in content
        assert "square_root" in content


# ==================== Context Handling Tests ====================

class TestContextHandling:
    """Tests for context field handling."""

    def test_missing_operation_renders_as_na(self, tmp_path, monkeypatch):
        """Test that missing 'operation' key renders as 'N/A'."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"message": "test"})  # no 'operation' key

        content = (tmp_path / "error.log").read_text()
        assert "N/A" in content

    def test_missing_operands_renders_as_na(self, tmp_path, monkeypatch):
        """Test that missing 'operands' key renders as 'N/A'."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"operation": "add"})  # no 'operands' key

        content = (tmp_path / "error.log").read_text()
        assert "N/A" in content

    def test_missing_message_renders_as_na(self, tmp_path, monkeypatch):
        """Test that missing 'message' key renders as 'N/A'."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"operation": "add", "operands": "5, 3"})  # no 'message'

        content = (tmp_path / "error.log").read_text()
        assert "N/A" in content

    def test_all_context_fields_present(self, tmp_path, monkeypatch):
        """Test that all context fields are logged when present."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {
            "operation": "add",
            "operands": "5, 3",
            "message": "test error"
        })

        content = (tmp_path / "error.log").read_text()
        assert "add" in content
        assert "5, 3" in content
        assert "test error" in content

    def test_context_values_are_stringified(self, tmp_path, monkeypatch):
        """Test that context values are converted to strings."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {
            "operation": "add",
            "operands": [5, 3],  # list, not string
            "message": 42  # int, not string
        })

        content = (tmp_path / "error.log").read_text()
        # Should contain string representation
        assert "5" in content
        assert "3" in content
        assert "42" in content

    def test_context_with_none_values(self, tmp_path, monkeypatch):
        """Test that None values in context are converted to 'N/A'."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {
            "operation": None,
            "operands": None,
            "message": None
        })

        content = (tmp_path / "error.log").read_text()
        # None is converted to string "None", but context.get() with None should render as N/A
        assert "N/A" in content or "None" in content

    def test_empty_context_dict(self, tmp_path, monkeypatch):
        """Test that empty context dict renders all fields as 'N/A'."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {})  # empty dict

        content = (tmp_path / "error.log").read_text()
        # Should have N/A for operation, operands, message
        na_count = content.count("N/A")
        assert na_count >= 3


# ==================== File Persistence Tests ====================

class TestFilePersistence:
    """Tests for file persistence and reusability."""

    def test_errors_persist_across_logger_instances(self, tmp_path, monkeypatch):
        """Test that errors written by one logger persist for another."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger1 = ErrorLogger()
        logger1.log_error("ERROR1", {"message": "first error"})

        # Create a new logger instance
        logger2 = ErrorLogger()
        logger2.log_error("ERROR2", {"message": "second error"})

        content = (tmp_path / "error.log").read_text()
        assert "first error" in content
        assert "second error" in content

    def test_file_can_be_read_back(self, tmp_path, monkeypatch):
        """Test that log file can be read and parsed."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {
            "operation": "add",
            "operands": "5, 3",
            "message": "test error"
        })

        content = (tmp_path / "error.log").read_text()
        lines = content.strip().split('\n')

        # Each line should be parseable
        for line in lines:
            parts = line.split(" | ")
            assert len(parts) == 5  # TIMESTAMP | ERROR_TYPE | OPERATION | OPERANDS | MESSAGE

    def test_append_mode_works_correctly(self, tmp_path, monkeypatch):
        """Test that append mode preserves existing content."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("ERROR1", {"message": "first"})

        # Create a second logger (simulating new process)
        logger2 = ErrorLogger()
        logger2.log_error("ERROR2", {"message": "second"})

        content = (tmp_path / "error.log").read_text()
        lines = content.strip().split('\n')
        assert len(lines) == 2
        assert "first" in lines[0]
        assert "second" in lines[1]


# ==================== Resilience Tests ====================

class TestResilience:
    """Tests for error handling and resilience."""

    def test_oserror_during_handler_setup_is_swallowed(self, tmp_path, monkeypatch):
        """Test that OSError during file handler setup doesn't crash."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        # Make the directory read-only to trigger OSError
        with patch('logging.FileHandler') as mock_fh:
            mock_fh.side_effect = OSError("Permission denied")

            logger = ErrorLogger()
            # Should not raise despite OSError
            logger.log_error("TEST", {"message": "test"})

    def test_exception_during_formatting_is_swallowed(self, tmp_path, monkeypatch):
        """Test that exceptions during formatting don't crash the app."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        # Context with an object that raises on str()
        problematic_obj = MagicMock()
        problematic_obj.__str__.side_effect = Exception("String conversion error")

        # Should not raise
        logger.log_error("TEST", {
            "operation": problematic_obj,
            "message": "test"
        })

    def test_logging_is_silent_on_failure(self, tmp_path, monkeypatch):
        """Test that logging failures are completely silent."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()

        # Intentionally cause a problem
        with patch.object(_logger, 'error', side_effect=Exception("Logger error")):
            # Should not raise or print anything
            result = logger.log_error("TEST", {"message": "test"})
            assert result is None


# ==================== Timestamp Tests ====================

class TestTimestampFormat:
    """Tests for timestamp format and validity."""

    def test_timestamp_is_iso_8601(self, tmp_path, monkeypatch):
        """Test that timestamp is in ISO 8601 format."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"message": "test"})

        import datetime
        content = (tmp_path / "error.log").read_text()
        # Should start with timestamp like 2023-01-15T10:30:45
        parts = content.split(" | ")
        timestamp = parts[0]

        # Try to parse it
        try:
            dt = datetime.datetime.fromisoformat(timestamp)
            assert dt is not None
        except ValueError:
            pytest.fail(f"Timestamp {timestamp} is not valid ISO 8601")

    def test_timestamp_has_seconds_precision(self, tmp_path, monkeypatch):
        """Test that timestamp has second-level precision."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"message": "test"})

        content = (tmp_path / "error.log").read_text()
        parts = content.split(" | ")
        timestamp = parts[0]

        # ISO 8601 with seconds: YYYY-MM-DDTHH:MM:SS
        import re
        pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
        assert re.match(pattern, timestamp)


# ==================== Integration Tests ====================

class TestIntegration:
    """Integration tests with multiple operations."""

    def test_multiple_error_types_in_sequence(self, tmp_path, monkeypatch):
        """Test logging multiple different error types."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("UNSUPPORTED_OPERATION", {"operation": "xyz"})
        logger.log_error("INVALID_OPERAND", {"operands": "abc"})
        logger.log_error("DIVISION_BY_ZERO", {"operation": "divide"})

        content = (tmp_path / "error.log").read_text()
        assert "UNSUPPORTED_OPERATION" in content
        assert "INVALID_OPERAND" in content
        assert "DIVISION_BY_ZERO" in content

    def test_context_with_special_characters(self, tmp_path, monkeypatch):
        """Test that special characters in context are handled."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {
            "operation": "op|with|pipes",
            "operands": "a,b,c",
            "message": "error with | symbols"
        })

        # Should not raise and should be parseable
        content = (tmp_path / "error.log").read_text()
        assert "error with | symbols" in content

    def test_large_context_values(self, tmp_path, monkeypatch):
        """Test that large context values are handled."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        large_value = "x" * 10000
        logger.log_error("TEST", {
            "operation": "add",
            "operands": large_value,
            "message": "test"
        })

        content = (tmp_path / "error.log").read_text()
        assert large_value in content

    def test_unicode_in_context(self, tmp_path, monkeypatch):
        """Test that Unicode characters in context are handled."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {
            "operation": "add_emoji",
            "operands": "🔢",
            "message": "error with emoji 😀"
        })

        content = (tmp_path / "error.log").read_text()
        assert "emoji" in content or "🔢" in content


# ==================== Singleton Pattern Tests ====================

class TestSingletonPattern:
    """Tests for the singleton handler pattern."""

    def test_handler_attached_flag_persists(self, tmp_path, monkeypatch):
        """Test that _handler_attached flag persists across calls."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST1", {"message": "first"})

        # Flag should be set
        assert el._handler_attached is True

        # Second call should not re-attach
        logger.log_error("TEST2", {"message": "second"})
        assert el._handler_attached is True

    def test_ensure_handler_idempotent(self, tmp_path, monkeypatch):
        """Test that _ensure_handler() is idempotent."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        # Remove all handlers first to start clean
        for handler in _logger.handlers[:]:
            _logger.removeHandler(handler)

        # Call multiple times
        _ensure_handler()
        handlers_after_first = len(_logger.handlers)
        _ensure_handler()
        handlers_after_second = len(_logger.handlers)
        _ensure_handler()
        handlers_after_third = len(_logger.handlers)

        # Handler count should not increase after first call
        assert handlers_after_first == 1
        assert handlers_after_second == 1
        assert handlers_after_third == 1
        assert el._handler_attached is True


# ==================== Edge Case Tests ====================

class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_empty_error_type_string(self, tmp_path, monkeypatch):
        """Test logging with empty error_type."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("", {"message": "test"})

        # Should log without raising
        content = (tmp_path / "error.log").read_text()
        assert "test" in content

    def test_very_long_error_type(self, tmp_path, monkeypatch):
        """Test logging with very long error_type."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        long_type = "ERROR_" + "X" * 10000
        logger = ErrorLogger()
        logger.log_error(long_type, {"message": "test"})

        content = (tmp_path / "error.log").read_text()
        assert long_type in content

    def test_context_with_numeric_values(self, tmp_path, monkeypatch):
        """Test that numeric context values are stringified correctly."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {
            "operation": "divide",
            "operands": 5.5,  # float, not string
            "message": 42  # int, not string
        })

        content = (tmp_path / "error.log").read_text()
        assert "5.5" in content
        assert "42" in content

    def test_context_with_extra_keys(self, tmp_path, monkeypatch):
        """Test that extra keys in context are ignored."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {
            "operation": "add",
            "operands": "5, 3",
            "message": "test",
            "extra_key": "extra_value",
            "another_key": 123
        })

        # Should not raise and should log the expected fields
        content = (tmp_path / "error.log").read_text()
        assert "add" in content
        assert "5, 3" in content
        assert "test" in content


# ==================== Module-Level Tests ====================

class TestModuleLevel:
    """Tests for module-level variables and functions."""

    def test_logger_name_is_calculator_errors(self):
        """Test that module logger has correct name."""
        assert _logger.name == "calculator.errors"

    def test_logger_level_is_error(self):
        """Test that module logger level is ERROR."""
        assert _logger.level == logging.ERROR

    def test_ensure_handler_function_exists(self):
        """Test that _ensure_handler function exists and is callable."""
        assert callable(_ensure_handler)

    def test_ensure_handler_returns_none(self, tmp_path, monkeypatch):
        """Test that _ensure_handler returns None."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        result = _ensure_handler()
        assert result is None


# ==================== Backward Compatibility Tests ====================


class TestBackwardCompatibility:
    """Tests verifying backward compatibility with new support package layout."""

    def test_import_error_logger_from_support_error_logging(self):
        """Test that ErrorLogger can be imported from src.support.error_logging."""
        from src.support.error_logging import ErrorLogger as SupportErrorLogger
        assert SupportErrorLogger is not None
        logger = SupportErrorLogger()
        assert isinstance(logger, SupportErrorLogger)

    def test_error_logger_both_imports_are_same_class(self):
        """Test that both import paths give the same ErrorLogger class."""
        from src.error_logger import ErrorLogger as CanonicalErrorLogger
        from src.support.error_logging import ErrorLogger as SupportErrorLogger
        assert CanonicalErrorLogger is SupportErrorLogger

    def test_canonical_error_logger_still_works(self, tmp_path, monkeypatch):
        """Test that canonical location still works for logging."""
        monkeypatch.chdir(tmp_path)
        import src.error_logger as el
        el._handler_attached = False

        logger = ErrorLogger()
        logger.log_error("TEST", {"message": "backward compat test"})

        content = (tmp_path / "error.log").read_text()
        assert "backward compat test" in content
