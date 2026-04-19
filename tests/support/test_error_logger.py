"""Tests for ErrorLogger from src.support.error_logger."""

import os
import pytest
import tempfile
from src.support.error_logger import ErrorLogger


class TestErrorLoggerInitialization:
    """Test ErrorLogger initialization."""

    def test_error_logger_default_filename(self):
        """Test default error log filename."""
        logger = ErrorLogger()
        assert logger.error_file == "error.log"

    def test_error_logger_custom_filename(self):
        """Test custom error log filename."""
        logger = ErrorLogger("custom_error.log")
        assert logger.error_file == "custom_error.log"

    def test_error_logger_with_full_path(self):
        """Test error logger with full path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            assert logger.error_file == filepath


class TestErrorLoggerConstants:
    """Test ErrorLogger class constants."""

    def test_invalid_input_constant(self):
        """Test INVALID_INPUT constant."""
        assert ErrorLogger.INVALID_INPUT == "INVALID_INPUT"

    def test_unsupported_operation_constant(self):
        """Test UNSUPPORTED_OPERATION constant."""
        assert ErrorLogger.UNSUPPORTED_OPERATION == "UNSUPPORTED_OPERATION"

    def test_calculation_error_constant(self):
        """Test CALCULATION_ERROR constant."""
        assert ErrorLogger.CALCULATION_ERROR == "CALCULATION_ERROR"

    def test_constants_are_strings(self):
        """Test that constants are strings."""
        assert isinstance(ErrorLogger.INVALID_INPUT, str)
        assert isinstance(ErrorLogger.UNSUPPORTED_OPERATION, str)
        assert isinstance(ErrorLogger.CALCULATION_ERROR, str)


class TestErrorLoggerClearErrors:
    """Test ErrorLogger.clear_errors method."""

    def test_clear_errors_creates_file(self):
        """Test that clear_errors creates the file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()
            assert os.path.exists(filepath)

    def test_clear_errors_truncates_existing_file(self):
        """Test that clear_errors truncates existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            # Create file with content
            with open(filepath, "w") as f:
                f.write("old error entry\n")

            logger = ErrorLogger(filepath)
            logger.clear_errors()

            with open(filepath, "r") as f:
                content = f.read()
            assert content == ""

    def test_clear_errors_idempotent(self):
        """Test that clear_errors can be called multiple times."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()
            logger.clear_errors()  # Should not raise
            assert os.path.exists(filepath)

    def test_clear_errors_invalid_directory(self):
        """Test clear_errors with invalid directory (gracefully handles error)."""
        logger = ErrorLogger("/invalid/directory/error.log")
        # Should not raise, but logs to stderr
        logger.clear_errors()


class TestErrorLoggerLogError:
    """Test ErrorLogger.log_error method."""

    def test_log_error_single_entry(self):
        """Test logging a single error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            exc = ValueError("test error")
            logger.log_error(ErrorLogger.CALCULATION_ERROR, "test input", exc)

            with open(filepath, "r") as f:
                content = f.read()

            # Should contain error type, input, and exception message
            assert "CALCULATION_ERROR" in content
            assert "input='test input'" in content
            assert "test error" in content
            # Should have ISO8601 timestamp
            assert "T" in content  # ISO format has T separator

    def test_log_error_invalid_input_error_type(self):
        """Test logging INVALID_INPUT error type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            exc = ValueError("invalid number")
            logger.log_error(ErrorLogger.INVALID_INPUT, "abc", exc)

            with open(filepath, "r") as f:
                content = f.read()

            assert "INVALID_INPUT" in content
            assert "input='abc'" in content

    def test_log_error_unsupported_operation_error_type(self):
        """Test logging UNSUPPORTED_OPERATION error type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            exc = ValueError("unknown operation")
            logger.log_error(ErrorLogger.UNSUPPORTED_OPERATION, "xyz", exc)

            with open(filepath, "r") as f:
                content = f.read()

            assert "UNSUPPORTED_OPERATION" in content
            assert "input='xyz'" in content

    def test_log_error_multiple_entries(self):
        """Test logging multiple errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            exc1 = ValueError("error 1")
            exc2 = ZeroDivisionError("error 2")

            logger.log_error(ErrorLogger.CALCULATION_ERROR, "input1", exc1)
            logger.log_error(ErrorLogger.CALCULATION_ERROR, "input2", exc2)

            with open(filepath, "r") as f:
                lines = f.readlines()

            assert len(lines) == 2
            assert "error 1" in lines[0]
            assert "error 2" in lines[1]

    def test_log_error_preserves_exception_message(self):
        """Test that exception message is preserved."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            exc = ValueError("division by zero")
            logger.log_error(ErrorLogger.CALCULATION_ERROR, "5 / 0", exc)

            with open(filepath, "r") as f:
                content = f.read()

            assert "division by zero" in content

    def test_log_error_with_special_characters_in_input(self):
        """Test logging error with special characters in user input."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            exc = ValueError("test")
            user_input = "test'\"special\\chars"
            logger.log_error(ErrorLogger.INVALID_INPUT, user_input, exc)

            with open(filepath, "r") as f:
                content = f.read()

            assert "input=" in content

    def test_log_error_with_empty_input(self):
        """Test logging error with empty input string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            exc = ValueError("empty input")
            logger.log_error(ErrorLogger.INVALID_INPUT, "", exc)

            with open(filepath, "r") as f:
                content = f.read()

            assert "input=''" in content

    def test_log_error_with_very_long_message(self):
        """Test logging error with very long exception message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            long_msg = "x" * 1000
            exc = ValueError(long_msg)
            logger.log_error(ErrorLogger.CALCULATION_ERROR, "input", exc)

            with open(filepath, "r") as f:
                content = f.read()

            assert long_msg in content

    def test_log_error_format_structure(self):
        """Test that logged error has correct format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            exc = ValueError("test error")
            logger.log_error(ErrorLogger.CALCULATION_ERROR, "test_input", exc)

            with open(filepath, "r") as f:
                content = f.read().strip()

            # Format should be: timestamp | error_type | input=... | exception_msg
            parts = content.split(" | ")
            assert len(parts) == 4
            # First part should be ISO timestamp
            assert "-" in parts[0]  # Date separator
            assert ":" in parts[0]  # Time separator
            assert parts[1] == "CALCULATION_ERROR"
            assert "input=" in parts[2]
            assert "test error" in parts[3]


class TestErrorLoggerGetErrors:
    """Test ErrorLogger.get_errors method."""

    def test_get_errors_empty(self):
        """Test get_errors with empty error log."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            result = logger.get_errors()
            assert result == []

    def test_get_errors_nonexistent_file(self):
        """Test get_errors with nonexistent file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "nonexistent.log")
            logger = ErrorLogger(filepath)

            result = logger.get_errors()
            assert result == []

    def test_get_errors_single_entry(self):
        """Test get_errors with single error entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            exc = ValueError("test error")
            logger.log_error(ErrorLogger.CALCULATION_ERROR, "input", exc)

            result = logger.get_errors()
            assert len(result) == 1
            assert "CALCULATION_ERROR" in result[0]

    def test_get_errors_multiple_entries(self):
        """Test get_errors with multiple error entries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            logger.log_error(ErrorLogger.CALCULATION_ERROR, "input1", ValueError("error1"))
            logger.log_error(ErrorLogger.INVALID_INPUT, "input2", ValueError("error2"))
            logger.log_error(ErrorLogger.UNSUPPORTED_OPERATION, "input3", ValueError("error3"))

            result = logger.get_errors()
            assert len(result) == 3

    def test_get_errors_strips_newlines(self):
        """Test that get_errors strips trailing newlines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            # Manually write file with newlines
            with open(filepath, "w") as f:
                f.write("error entry 1\n")
                f.write("error entry 2\n")

            logger = ErrorLogger(filepath)
            result = logger.get_errors()

            assert result == ["error entry 1", "error entry 2"]
            # Ensure no trailing newlines in entries
            for entry in result:
                assert not entry.endswith("\n")

    def test_get_errors_returns_copy(self):
        """Test that get_errors returns a fresh list each time."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()
            logger.log_error(ErrorLogger.CALCULATION_ERROR, "input", ValueError("error"))

            result1 = logger.get_errors()
            result2 = logger.get_errors()

            assert result1 == result2
            assert result1 is not result2


class TestErrorLoggerIntegration:
    """Integration tests for ErrorLogger."""

    def test_clear_then_log_then_get(self):
        """Test workflow: clear -> log -> get."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)

            logger.clear_errors()
            assert logger.get_errors() == []

            logger.log_error(ErrorLogger.CALCULATION_ERROR, "input1", ValueError("error1"))
            logger.log_error(ErrorLogger.INVALID_INPUT, "input2", ValueError("error2"))

            result = logger.get_errors()
            assert len(result) == 2

    def test_multiple_clear_calls(self):
        """Test that multiple clear calls work correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)

            logger.clear_errors()
            logger.log_error(ErrorLogger.CALCULATION_ERROR, "input1", ValueError("error1"))
            assert len(logger.get_errors()) == 1

            logger.clear_errors()
            assert logger.get_errors() == []

            logger.log_error(ErrorLogger.INVALID_INPUT, "input2", ValueError("error2"))
            assert len(logger.get_errors()) == 1

    def test_session_isolation(self):
        """Test that different instances with same file are isolated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")

            logger1 = ErrorLogger(filepath)
            logger1.clear_errors()
            logger1.log_error(ErrorLogger.CALCULATION_ERROR, "input1", ValueError("error1"))

            # New instance with same file
            logger2 = ErrorLogger(filepath)
            result = logger2.get_errors()

            assert len(result) == 1
            assert "CALCULATION_ERROR" in result[0]

    def test_all_error_types(self):
        """Test logging all error types."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "error.log")
            logger = ErrorLogger(filepath)
            logger.clear_errors()

            error_types = [
                ErrorLogger.INVALID_INPUT,
                ErrorLogger.UNSUPPORTED_OPERATION,
                ErrorLogger.CALCULATION_ERROR
            ]

            for error_type in error_types:
                logger.log_error(error_type, f"input_{error_type}", ValueError(error_type))

            result = logger.get_errors()
            assert len(result) == 3
            for error_type in error_types:
                assert any(error_type in entry for entry in result)
