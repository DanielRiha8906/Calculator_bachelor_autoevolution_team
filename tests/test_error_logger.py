"""Comprehensive pytest tests for the ErrorLogger feature.

Tests cover:
- ErrorLogger.__init__: custom file paths, defaults
- ErrorLogger.clear_errors: creates/truncates file, error handling
- ErrorLogger.log_error: appends entries, format correctness, error categories
- ErrorLogger.get_errors: reads back errors, handles missing files
- Integration with REPLInterface and CLIHandler
- File isolation between sessions
- Graceful error handling (non-writable paths)
- Special characters, long messages, and edge cases
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import patch, Mock
from io import StringIO
import datetime
import re

from src.error_logger import ErrorLogger
from src.repl import REPLInterface
from src.cli import CLIHandler
from src.calculator import Calculator


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def tmp_error_log_file(tmp_path):
    """Provide a temporary error log file path for test isolation."""
    return str(tmp_path / "error.log")


@pytest.fixture
def error_logger(tmp_error_log_file):
    """Provide an ErrorLogger instance with a temporary file."""
    return ErrorLogger(error_file=tmp_error_log_file)


@pytest.fixture
def calculator():
    """Provide a Calculator instance."""
    return Calculator()


@pytest.fixture
def repl_with_error_logger(calculator, tmp_error_log_file):
    """Provide a REPLInterface with error logger integration."""
    error_logger = ErrorLogger(error_file=tmp_error_log_file)
    repl = REPLInterface(calculator, error_logger=error_logger)
    return repl, error_logger, tmp_error_log_file


@pytest.fixture
def cli_with_error_logger(calculator, tmp_error_log_file):
    """Provide a CLIHandler with error logger integration."""
    error_logger = ErrorLogger(error_file=tmp_error_log_file)
    cli = CLIHandler(calculator, error_logger=error_logger)
    return cli, error_logger, tmp_error_log_file


# ==============================================================================
# TESTS: ErrorLogger Class Constants
# ==============================================================================

class TestErrorLoggerConstants:
    """Test suite for ErrorLogger class-level constants."""

    def test_invalid_input_constant(self):
        """Test INVALID_INPUT constant has correct value."""
        assert ErrorLogger.INVALID_INPUT == "INVALID_INPUT"

    def test_unsupported_operation_constant(self):
        """Test UNSUPPORTED_OPERATION constant has correct value."""
        assert ErrorLogger.UNSUPPORTED_OPERATION == "UNSUPPORTED_OPERATION"

    def test_calculation_error_constant(self):
        """Test CALCULATION_ERROR constant has correct value."""
        assert ErrorLogger.CALCULATION_ERROR == "CALCULATION_ERROR"

    def test_all_constants_are_strings(self):
        """Test that all constants are string type."""
        assert isinstance(ErrorLogger.INVALID_INPUT, str)
        assert isinstance(ErrorLogger.UNSUPPORTED_OPERATION, str)
        assert isinstance(ErrorLogger.CALCULATION_ERROR, str)


# ==============================================================================
# TESTS: ErrorLogger.__init__
# ==============================================================================

class TestErrorLoggerInit:
    """Test suite for ErrorLogger.__init__."""

    def test_init_with_default_file(self):
        """Test initialization with default error log file name."""
        error_logger = ErrorLogger()
        assert error_logger.error_file == "error.log"

    def test_init_with_custom_file_path(self, tmp_path):
        """Test initialization with custom file path."""
        custom_path = str(tmp_path / "custom_error.log")
        error_logger = ErrorLogger(error_file=custom_path)
        assert error_logger.error_file == custom_path

    def test_init_with_absolute_path(self, tmp_path):
        """Test initialization with absolute path."""
        abs_path = str(tmp_path.absolute() / "error.log")
        error_logger = ErrorLogger(error_file=abs_path)
        assert error_logger.error_file == abs_path

    def test_init_with_relative_path(self):
        """Test initialization with relative path."""
        error_logger = ErrorLogger(error_file="subdir/error.log")
        assert error_logger.error_file == "subdir/error.log"

    def test_init_attributes_set_correctly(self, tmp_error_log_file):
        """Test that __init__ sets attributes correctly."""
        error_logger = ErrorLogger(error_file=tmp_error_log_file)
        assert hasattr(error_logger, "error_file")
        assert error_logger.error_file == tmp_error_log_file


# ==============================================================================
# TESTS: ErrorLogger.clear_errors
# ==============================================================================

class TestClearErrors:
    """Test suite for clear_errors method."""

    def test_clear_errors_creates_new_file_if_missing(self, tmp_error_log_file):
        """Test that clear_errors creates file when it doesn't exist."""
        assert not os.path.exists(tmp_error_log_file)
        error_logger = ErrorLogger(error_file=tmp_error_log_file)
        error_logger.clear_errors()
        assert os.path.exists(tmp_error_log_file)
        assert os.path.getsize(tmp_error_log_file) == 0

    def test_clear_errors_truncates_existing_file(self, tmp_error_log_file):
        """Test that clear_errors truncates an existing file."""
        # Create a file with content
        with open(tmp_error_log_file, "w") as f:
            f.write("old error entry\n" * 10)
        assert os.path.getsize(tmp_error_log_file) > 0

        # Clear errors
        error_logger = ErrorLogger(error_file=tmp_error_log_file)
        error_logger.clear_errors()

        assert os.path.exists(tmp_error_log_file)
        assert os.path.getsize(tmp_error_log_file) == 0

    def test_clear_errors_multiple_times(self, tmp_error_log_file):
        """Test that clear_errors can be called multiple times safely."""
        error_logger = ErrorLogger(error_file=tmp_error_log_file)
        error_logger.clear_errors()
        error_logger.clear_errors()
        error_logger.clear_errors()
        assert os.path.exists(tmp_error_log_file)
        assert os.path.getsize(tmp_error_log_file) == 0

    def test_clear_errors_error_handling_unwritable_path(self):
        """Test that clear_errors handles OSError gracefully and logs to stderr."""
        # Use a non-existent directory path (will cause permission error)
        bad_path = "/invalid_nonexistent_directory_12345/error.log"
        error_logger = ErrorLogger(error_file=bad_path)

        # Capture stderr
        stderr_capture = StringIO()
        with patch("sys.stderr", stderr_capture):
            error_logger.clear_errors()  # Should not raise

        # Verify warning was written to stderr
        output = stderr_capture.getvalue()
        assert "Warning" in output
        assert "error.log" in output or "error_log" in output


# ==============================================================================
# TESTS: ErrorLogger.log_error
# ==============================================================================

class TestLogError:
    """Test suite for log_error method."""

    def test_log_invalid_input_error(self, error_logger, tmp_error_log_file):
        """Test logging an INVALID_INPUT error."""
        error_logger.clear_errors()
        exc = ValueError("Expected a number, got 'abc'")
        error_logger.log_error(
            ErrorLogger.INVALID_INPUT,
            "abc",
            exc
        )

        with open(tmp_error_log_file, "r") as f:
            content = f.read()
        assert "INVALID_INPUT" in content
        assert "abc" in content
        assert "Expected a number" in content

    def test_log_unsupported_operation_error(self, error_logger, tmp_error_log_file):
        """Test logging an UNSUPPORTED_OPERATION error."""
        error_logger.clear_errors()
        exc = ValueError("Unknown operation: 'foo'")
        error_logger.log_error(
            ErrorLogger.UNSUPPORTED_OPERATION,
            "foo(1, 2)",
            exc
        )

        with open(tmp_error_log_file, "r") as f:
            content = f.read()
        assert "UNSUPPORTED_OPERATION" in content
        assert "foo(1, 2)" in content
        assert "Unknown operation" in content

    def test_log_calculation_error(self, error_logger, tmp_error_log_file):
        """Test logging a CALCULATION_ERROR."""
        error_logger.clear_errors()
        exc = ZeroDivisionError("division by zero")
        error_logger.log_error(
            ErrorLogger.CALCULATION_ERROR,
            "divide(10, 0)",
            exc
        )

        with open(tmp_error_log_file, "r") as f:
            content = f.read()
        assert "CALCULATION_ERROR" in content
        assert "divide(10, 0)" in content
        assert "division by zero" in content

    def test_log_error_format_contains_timestamp(self, error_logger, tmp_error_log_file):
        """Test that log entry contains ISO 8601 timestamp."""
        error_logger.clear_errors()
        exc = ValueError("test error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "test_input", exc)

        with open(tmp_error_log_file, "r") as f:
            line = f.read().strip()

        # ISO 8601 format: YYYY-MM-DDTHH:MM:SS.mmmmmm or similar
        iso_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
        assert re.search(iso_pattern, line), f"No ISO timestamp found in: {line}"

    def test_log_error_format_contains_error_type(self, error_logger, tmp_error_log_file):
        """Test that log entry contains error type."""
        error_logger.clear_errors()
        exc = ValueError("test error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input", exc)

        with open(tmp_error_log_file, "r") as f:
            line = f.read().strip()

        assert "INVALID_INPUT" in line
        assert " | " in line

    def test_log_error_format_contains_input_repr(self, error_logger, tmp_error_log_file):
        """Test that log entry contains input parameter in repr format."""
        error_logger.clear_errors()
        exc = ValueError("test error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "my_input", exc)

        with open(tmp_error_log_file, "r") as f:
            line = f.read().strip()

        # Should have input=<repr'd string>
        assert "input=" in line
        assert "'my_input'" in line or '"my_input"' in line

    def test_log_error_format_contains_exception_message(self, error_logger, tmp_error_log_file):
        """Test that log entry contains exception message."""
        error_logger.clear_errors()
        exc = ValueError("specific error message")
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, "input", exc)

        with open(tmp_error_log_file, "r") as f:
            line = f.read().strip()

        assert "specific error message" in line

    def test_log_error_multiple_entries_append(self, error_logger, tmp_error_log_file):
        """Test that multiple log_error calls append (not overwrite)."""
        error_logger.clear_errors()
        exc1 = ValueError("first error")
        exc2 = ValueError("second error")
        exc3 = ValueError("third error")

        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input1", exc1)
        error_logger.log_error(ErrorLogger.UNSUPPORTED_OPERATION, "input2", exc2)
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, "input3", exc3)

        with open(tmp_error_log_file, "r") as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert "first error" in lines[0]
        assert "second error" in lines[1]
        assert "third error" in lines[2]

    def test_log_error_with_special_characters(self, error_logger, tmp_error_log_file):
        """Test logging error with special characters in input."""
        error_logger.clear_errors()
        exc = ValueError("error")
        error_logger.log_error(
            ErrorLogger.INVALID_INPUT,
            "input with 'quotes' and \"double quotes\"",
            exc
        )

        with open(tmp_error_log_file, "r") as f:
            content = f.read()

        # Should be parseable and contain the quotes
        assert "input with" in content

    def test_log_error_with_long_message(self, error_logger, tmp_error_log_file):
        """Test logging error with very long message."""
        error_logger.clear_errors()
        long_msg = "x" * 500
        exc = ValueError(long_msg)
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, "input", exc)

        with open(tmp_error_log_file, "r") as f:
            line = f.read().strip()

        assert long_msg in line

    def test_log_error_preserves_newlines_in_file(self, error_logger, tmp_error_log_file):
        """Test that each error is a separate line."""
        error_logger.clear_errors()
        exc1 = ValueError("error1")
        exc2 = ValueError("error2")

        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input1", exc1)
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input2", exc2)

        with open(tmp_error_log_file, "r") as f:
            lines = f.readlines()

        assert len(lines) == 2
        assert lines[0].endswith("\n")
        assert lines[1].endswith("\n")

    def test_log_error_file_io_failure_not_raises(self):
        """Test that log_error does not raise when file cannot be written."""
        bad_path = "/invalid_nonexistent_directory_12345/error.log"
        error_logger = ErrorLogger(error_file=bad_path)

        exc = ValueError("test error")
        stderr_capture = StringIO()
        with patch("sys.stderr", stderr_capture):
            # Should not raise
            error_logger.log_error(ErrorLogger.INVALID_INPUT, "input", exc)

        # Verify warning was written to stderr
        output = stderr_capture.getvalue()
        assert "Warning" in output
        assert "error.log" in output or "error_log" in output

    def test_log_error_with_various_exception_types(self, error_logger, tmp_error_log_file):
        """Test logging different exception types."""
        error_logger.clear_errors()

        exceptions = [
            ValueError("value error"),
            ZeroDivisionError("division by zero"),
            TypeError("type error"),
            OverflowError("overflow"),
        ]

        for exc in exceptions:
            error_logger.log_error(ErrorLogger.CALCULATION_ERROR, "input", exc)

        with open(tmp_error_log_file, "r") as f:
            lines = f.readlines()

        assert len(lines) == 4


# ==============================================================================
# TESTS: ErrorLogger.get_errors
# ==============================================================================

class TestGetErrors:
    """Test suite for get_errors method."""

    def test_get_errors_empty_file(self, error_logger, tmp_error_log_file):
        """Test get_errors returns empty list when log is empty."""
        error_logger.clear_errors()
        errors = error_logger.get_errors()
        assert errors == []

    def test_get_errors_missing_file(self, tmp_error_log_file):
        """Test get_errors returns empty list when log file doesn't exist."""
        error_logger = ErrorLogger(error_file=tmp_error_log_file)
        # Don't create the file
        assert not os.path.exists(tmp_error_log_file)
        errors = error_logger.get_errors()
        assert errors == []

    def test_get_errors_single_entry(self, error_logger, tmp_error_log_file):
        """Test get_errors returns single entry."""
        error_logger.clear_errors()
        exc = ValueError("test error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input", exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "INVALID_INPUT" in errors[0]
        assert "input" in errors[0]

    def test_get_errors_multiple_entries(self, error_logger, tmp_error_log_file):
        """Test get_errors returns all entries."""
        error_logger.clear_errors()
        exc1 = ValueError("error1")
        exc2 = ValueError("error2")
        exc3 = ValueError("error3")

        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input1", exc1)
        error_logger.log_error(ErrorLogger.UNSUPPORTED_OPERATION, "input2", exc2)
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, "input3", exc3)

        errors = error_logger.get_errors()
        assert len(errors) == 3
        assert any("error1" in e for e in errors)
        assert any("error2" in e for e in errors)
        assert any("error3" in e for e in errors)

    def test_get_errors_strips_trailing_newlines(self, error_logger, tmp_error_log_file):
        """Test that get_errors strips trailing newlines from entries."""
        error_logger.clear_errors()
        exc = ValueError("test error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input", exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert not errors[0].endswith("\n")

    def test_get_errors_file_not_readable_returns_empty(self):
        """Test get_errors returns empty list when file cannot be read."""
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        try:
            error_logger = ErrorLogger(error_file=tmp.name)
            # Make file unreadable (if possible on this OS)
            os.chmod(tmp.name, 0o000)

            stderr_capture = StringIO()
            with patch("sys.stderr", stderr_capture):
                errors = error_logger.get_errors()

            # Should return empty list, not raise
            assert errors == []
        finally:
            os.chmod(tmp.name, 0o644)
            os.unlink(tmp.name)

    def test_get_errors_preserves_order(self, error_logger, tmp_error_log_file):
        """Test that get_errors preserves entry order."""
        error_logger.clear_errors()
        for i in range(5):
            exc = ValueError(f"error_{i}")
            error_logger.log_error(ErrorLogger.CALCULATION_ERROR, f"input_{i}", exc)

        errors = error_logger.get_errors()
        assert len(errors) == 5
        for i, error_line in enumerate(errors):
            assert f"error_{i}" in error_line


# ==============================================================================
# TESTS: ErrorLogger File Separation and Session Isolation
# ==============================================================================

class TestErrorLoggerSeparation:
    """Test suite for error log separation and session isolation."""

    def test_error_log_separate_from_history_file(self, tmp_path, calculator):
        """Test that error log and history log are separate files."""
        from src.history import OperationHistory

        error_file = str(tmp_path / "error.log")
        history_file = str(tmp_path / "history.txt")

        error_logger = ErrorLogger(error_file=error_file)
        history = OperationHistory(history_file=history_file)

        error_logger.clear_errors()
        history.clear_history()

        # Log an error
        exc = ValueError("test error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input", exc)

        # Record a successful operation
        history.record_operation("add(2, 3) = 5")

        # Verify files are separate
        assert error_file != history_file
        with open(error_file, "r") as f:
            error_content = f.read()
        with open(history_file, "r") as f:
            history_content = f.read()

        # Error file should not have history
        assert "add(2, 3)" not in error_content
        # History file should not have errors
        assert "INVALID_INPUT" not in history_content

    def test_clear_errors_isolates_sessions(self, error_logger, tmp_error_log_file):
        """Test that clear_errors provides session isolation."""
        # Session 1
        error_logger.clear_errors()
        exc1 = ValueError("session 1 error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input1", exc1)

        errors = error_logger.get_errors()
        assert len(errors) == 1

        # Session 2: clear and start fresh
        error_logger.clear_errors()
        errors_after_clear = error_logger.get_errors()
        assert errors_after_clear == []

        # Log new error in session 2
        exc2 = ValueError("session 2 error")
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, "input2", exc2)

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "session 2 error" in errors[0]


# ==============================================================================
# TESTS: REPLInterface Error Logging Integration
# ==============================================================================

class TestREPLInterfaceErrorLogging:
    """Test suite for error logging integration in REPLInterface."""

    def test_repl_with_none_error_logger(self, calculator):
        """Test that REPL works with error_logger=None."""
        repl = REPLInterface(calculator, error_logger=None)
        assert repl.error_logger is None

    def test_repl_initialization_with_error_logger(self, repl_with_error_logger):
        """Test that REPL is initialized with error logger."""
        repl, error_logger, _ = repl_with_error_logger
        assert repl.error_logger is not None
        assert isinstance(repl.error_logger, ErrorLogger)

    def test_repl_logs_calculation_error_on_zero_division(self, repl_with_error_logger):
        """Test that REPL logs CALCULATION_ERROR on division by zero."""
        repl, error_logger, tmp_file = repl_with_error_logger
        error_logger.clear_errors()

        # Simulate executing divide(10, 0) which raises ZeroDivisionError
        exc = ZeroDivisionError("division by zero")
        operand_str = "10, 0"
        user_input = f"divide({operand_str})"
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, user_input, exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "CALCULATION_ERROR" in errors[0]
        assert "divide(10, 0)" in errors[0]

    def test_repl_logs_calculation_error_on_value_error(self, repl_with_error_logger):
        """Test that REPL logs CALCULATION_ERROR on ValueError."""
        repl, error_logger, tmp_file = repl_with_error_logger
        error_logger.clear_errors()

        # Simulate a calculation error (e.g., factorial of negative number)
        exc = ValueError("factorial() not defined for negative values")
        user_input = "factorial(-5)"
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, user_input, exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "CALCULATION_ERROR" in errors[0]
        assert "factorial(-5)" in errors[0]

    def test_repl_logs_calculation_error_on_type_error(self, repl_with_error_logger):
        """Test that REPL logs CALCULATION_ERROR on TypeError."""
        repl, error_logger, tmp_file = repl_with_error_logger
        error_logger.clear_errors()

        # Simulate a type error (e.g., factorial of float)
        exc = TypeError("'float' object cannot be interpreted as an integer")
        user_input = "factorial(3.5)"
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, user_input, exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "CALCULATION_ERROR" in errors[0]

    def test_repl_logs_calculation_error_on_overflow(self, repl_with_error_logger):
        """Test that REPL logs CALCULATION_ERROR on OverflowError."""
        repl, error_logger, tmp_file = repl_with_error_logger
        error_logger.clear_errors()

        # Simulate an overflow error
        exc = OverflowError("result too large")
        user_input = "power(10, 1000)"
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, user_input, exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "CALCULATION_ERROR" in errors[0]


# ==============================================================================
# TESTS: CLIHandler Error Logging Integration
# ==============================================================================

class TestCLIHandlerErrorLogging:
    """Test suite for error logging integration in CLIHandler."""

    def test_cli_with_none_error_logger(self, calculator):
        """Test that CLI works with error_logger=None."""
        cli = CLIHandler(calculator, error_logger=None)
        assert cli.error_logger is None

    def test_cli_initialization_with_error_logger(self, cli_with_error_logger):
        """Test that CLI is initialized with error logger."""
        cli, error_logger, _ = cli_with_error_logger
        assert cli.error_logger is not None
        assert isinstance(cli.error_logger, ErrorLogger)

    def test_cli_logs_unsupported_operation(self, cli_with_error_logger):
        """Test that CLI logs UNSUPPORTED_OPERATION for unknown operation."""
        cli, error_logger, _ = cli_with_error_logger
        error_logger.clear_errors()

        try:
            cli.execute(["unknown_op", "1", "2"])
        except ValueError:
            pass

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "UNSUPPORTED_OPERATION" in errors[0]

    def test_cli_logs_invalid_input_wrong_operand_count(self, cli_with_error_logger):
        """Test that CLI logs INVALID_INPUT for wrong operand count."""
        cli, error_logger, _ = cli_with_error_logger
        error_logger.clear_errors()

        try:
            cli.execute(["add", "5"])  # Missing second operand
        except ValueError:
            pass

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "INVALID_INPUT" in errors[0]

    def test_cli_logs_invalid_input_non_numeric_operand(self, cli_with_error_logger):
        """Test that CLI logs INVALID_INPUT for non-numeric operand."""
        cli, error_logger, _ = cli_with_error_logger
        error_logger.clear_errors()

        try:
            cli.execute(["add", "abc", "2"])  # Non-numeric operand
        except ValueError:
            pass

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "INVALID_INPUT" in errors[0]

    def test_cli_logs_calculation_error_division_by_zero(self, cli_with_error_logger):
        """Test that CLI logs CALCULATION_ERROR on division by zero."""
        cli, error_logger, _ = cli_with_error_logger
        error_logger.clear_errors()

        try:
            cli.execute(["divide", "10", "0"])
        except ZeroDivisionError:
            pass

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "CALCULATION_ERROR" in errors[0]

    def test_cli_logs_calculation_error_math_domain_error(self, cli_with_error_logger):
        """Test that CLI logs CALCULATION_ERROR on math domain error."""
        cli, error_logger, _ = cli_with_error_logger
        error_logger.clear_errors()

        # Logarithm of negative number should raise ValueError
        try:
            cli.execute(["logarithm", "-5", "10"])
        except ValueError:
            pass

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "CALCULATION_ERROR" in errors[0]

    def test_cli_successful_operation_not_logged_as_error(self, cli_with_error_logger):
        """Test that successful operations are not logged to error log."""
        cli, error_logger, _ = cli_with_error_logger
        error_logger.clear_errors()

        result = cli.execute(["add", "2", "3"])
        assert result == 5.0

        errors = error_logger.get_errors()
        assert errors == []

    def test_cli_error_logger_none_does_not_crash(self, calculator):
        """Test that execution with error_logger=None doesn't crash."""
        cli = CLIHandler(calculator, error_logger=None)

        # Should not raise or crash
        result = cli.execute(["add", "2", "3"])
        assert result == 5.0

    def test_cli_error_logger_none_with_error_still_raises(self, calculator):
        """Test that execution with error_logger=None still raises exception."""
        cli = CLIHandler(calculator, error_logger=None)

        with pytest.raises(ZeroDivisionError):
            cli.execute(["divide", "10", "0"])


# ==============================================================================
# TESTS: Edge Cases and Special Scenarios
# ==============================================================================

class TestErrorLoggerEdgeCases:
    """Test suite for edge cases and special scenarios."""

    def test_log_error_with_empty_input_string(self, error_logger, tmp_error_log_file):
        """Test logging error with empty input string."""
        error_logger.clear_errors()
        exc = ValueError("error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "", exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "input=''" in errors[0]

    def test_log_error_with_unicode_input(self, error_logger, tmp_error_log_file):
        """Test logging error with unicode characters in input."""
        error_logger.clear_errors()
        exc = ValueError("error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "π + e = ∑", exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1

    def test_log_error_with_very_long_input(self, error_logger, tmp_error_log_file):
        """Test logging error with very long input string."""
        error_logger.clear_errors()
        long_input = "x" * 10000
        exc = ValueError("error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, long_input, exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1

    def test_get_errors_preserves_multiline_exception_messages(self, error_logger, tmp_error_log_file):
        """Test that exception messages with special formatting are preserved."""
        error_logger.clear_errors()
        # Exceptions converted to string, so no actual newlines, but test special chars
        exc = ValueError("error with special: !@#$%^&*()")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input", exc)

        errors = error_logger.get_errors()
        assert len(errors) == 1
        assert "special" in errors[0]

    def test_log_error_repeated_rapidly(self, error_logger, tmp_error_log_file):
        """Test logging many errors rapidly."""
        error_logger.clear_errors()
        for i in range(100):
            exc = ValueError(f"error_{i}")
            error_logger.log_error(ErrorLogger.CALCULATION_ERROR, f"input_{i}", exc)

        errors = error_logger.get_errors()
        assert len(errors) == 100

    def test_error_logger_with_all_error_types(self, error_logger, tmp_error_log_file):
        """Test logging all three error types in one session."""
        error_logger.clear_errors()

        exc1 = ValueError("parse error")
        error_logger.log_error(ErrorLogger.INVALID_INPUT, "input1", exc1)

        exc2 = ValueError("unknown op")
        error_logger.log_error(ErrorLogger.UNSUPPORTED_OPERATION, "input2", exc2)

        exc3 = ZeroDivisionError("div by zero")
        error_logger.log_error(ErrorLogger.CALCULATION_ERROR, "input3", exc3)

        errors = error_logger.get_errors()
        assert len(errors) == 3

        error_types = [ErrorLogger.INVALID_INPUT, ErrorLogger.UNSUPPORTED_OPERATION, ErrorLogger.CALCULATION_ERROR]
        for error_type in error_types:
            assert any(error_type in e for e in errors)
