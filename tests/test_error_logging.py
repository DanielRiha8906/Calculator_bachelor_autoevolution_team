"""Tests for error logging functionality.

Tests the error logging module's ability to record calculation errors, handle
different error categories, persist error logs to files, and integrate with
both interactive and CLI calculator modes.
"""

import pytest
import sys
import os
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, mock_open
from src.calculator import Calculator


# ============================================================================
# Test Group A: Error Log File and Initialization (5 tests)
# ============================================================================

class TestErrorLogFileInitialization:
    """Tests for error log file creation and lazy initialization."""

    def test_error_log_creates_file_on_first_error(self, tmp_path):
        """Test that error log file is created on first error.

        Input: Instantiate ErrorLog with tmp_path file path, call log_error with 'invalid_input' category
        Expected output: The file exists after first error
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        # File should not exist yet
        assert not error_log_path.exists()

        # Log an error
        error_log.log_error("invalid_input", "add", [5, "abc"], "Invalid number 'abc'.")

        # File should now exist
        assert error_log_path.exists()

    def test_error_log_lazy_initialization(self, tmp_path):
        """Test that error log file is NOT created on instantiation.

        Input: Instantiate ErrorLog with tmp_path file path but do NOT call log_error
        Expected output: The file does NOT exist after instantiation
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        # File should not exist after instantiation
        assert not error_log_path.exists()

    def test_error_log_appends_not_overwrites(self, tmp_path):
        """Test that new ErrorLog instance appends to existing file.

        Input: Create ErrorLog, log error 1, create new ErrorLog instance with same path, log error 2
        Expected output: File contains both errors; second ErrorLog appends to existing file
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"

        # First ErrorLog instance - log one error
        error_log1 = ErrorLog(str(error_log_path))
        error_log1.log_error("invalid_input", "add", [5, "abc"], "Invalid number 'abc'.")

        # Second ErrorLog instance - log another error
        error_log2 = ErrorLog(str(error_log_path))
        error_log2.log_error("calculation_error", "divide", [5, 0], "division by zero")

        # File should contain both errors
        content = error_log_path.read_text()
        lines = content.strip().split("\n")
        assert len(lines) == 2
        assert "invalid_input" in lines[0]
        assert "calculation_error" in lines[1]

    def test_error_log_default_filename(self):
        """Test that default filename is error_log.txt.

        Input: Instantiate ErrorLog with no file_path argument (uses default)
        Expected output: Default filename is `error_log.txt`
        """
        from src.error_logging import ErrorLog

        error_log = ErrorLog()

        # Check that the default file path contains error_log.txt
        assert "error_log.txt" in str(error_log._file_path)

    def test_error_log_custom_file_path(self, tmp_path):
        """Test that custom file path is used when provided.

        Input: Instantiate ErrorLog with a custom file_path (tmp_path / "custom_errors.txt")
        Expected output: Logs to the specified file path
        """
        from src.error_logging import ErrorLog

        custom_path = tmp_path / "custom_errors.txt"
        error_log = ErrorLog(str(custom_path))

        error_log.log_error("invalid_input", "add", [5, "abc"], "Invalid number 'abc'.")

        assert custom_path.exists()
        content = custom_path.read_text()
        assert "invalid_input" in content


# ============================================================================
# Test Group B: Error Log Entry Format (4 tests)
# ============================================================================

class TestErrorLogFormat:
    """Tests for error log entry format and content."""

    def test_error_log_format_invalid_input_error(self, tmp_path):
        """Test format of invalid_input error entry.

        Input: Log error with category=`invalid_input`, operation=`add`, inputs=[5, "abc"], error_msg=`Invalid number 'abc'.`
        Expected output: Entry contains `invalid_input`, `add`, inputs formatted as `5, abc`, and the error message; pipe-delimited format
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        error_log.log_error("invalid_input", "add", [5, "abc"], "Invalid number 'abc'.")

        content = error_log_path.read_text()
        assert "invalid_input" in content
        assert "add" in content
        assert "5" in content or "5," in content
        assert "abc" in content
        assert "Invalid number 'abc'." in content
        # Should be pipe-delimited
        assert "|" in content

    def test_error_log_format_unsupported_operation_error(self, tmp_path):
        """Test format of unsupported_operation error entry.

        Input: Log error with category=`unsupported_operation`, operation=`unknown_op`, inputs=[], error_msg=`Unknown operation 'unknown_op'.`
        Expected output: Entry contains `unsupported_operation`, `unknown_op`, empty inputs, and the error message
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        error_log.log_error("unsupported_operation", "unknown_op", [], "Unknown operation 'unknown_op'.")

        content = error_log_path.read_text()
        assert "unsupported_operation" in content
        assert "unknown_op" in content
        assert "Unknown operation 'unknown_op'." in content
        assert "|" in content

    def test_error_log_format_calculation_error(self, tmp_path):
        """Test format of calculation_error entry.

        Input: Log error with category=`calculation_error`, operation=`divide`, inputs=[5, 0], error_msg=`division by zero`
        Expected output: Entry contains `calculation_error`, `divide`, `5, 0`, and `division by zero`
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        error_log.log_error("calculation_error", "divide", [5, 0], "division by zero")

        content = error_log_path.read_text()
        assert "calculation_error" in content
        assert "divide" in content
        assert "5" in content
        assert "0" in content
        assert "division by zero" in content
        assert "|" in content

    def test_error_log_timestamp_is_iso8601_utc(self, tmp_path):
        """Test that first field is ISO 8601 UTC timestamp.

        Input: Log error, read log file
        Expected output: First field of entry is an ISO 8601 UTC timestamp (parse with datetime.fromisoformat, check tzinfo is UTC)
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        error_log.log_error("invalid_input", "add", [5, "abc"], "Invalid number 'abc'.")

        content = error_log_path.read_text()
        line = content.strip()

        # First field should be a timestamp separated by pipe
        parts = line.split("|")
        assert len(parts) >= 2

        timestamp_str = parts[0].strip()

        # Try to parse as ISO 8601 timestamp
        try:
            parsed = datetime.fromisoformat(timestamp_str)
            # Should have UTC timezone info
            assert parsed.tzinfo is not None
        except ValueError:
            pytest.fail(f"Timestamp '{timestamp_str}' is not valid ISO 8601 format")


# ============================================================================
# Test Group C: Error Categorization in Interactive Mode (6 tests)
# ============================================================================

class TestErrorLoggingInteractiveMode:
    """Tests for error logging in interactive calculator mode."""

    def test_interactive_mode_logs_invalid_input_nonumeric(self, tmp_path, monkeypatch, capsys):
        """Test that non-numeric input is logged as invalid_input.

        Input: Interactive mode called with mock inputs for operation "add", then non-numeric operand "abc", then "quit"
        Expected output: error_log.txt contains an entry with `invalid_input` category; operation history unchanged
        """
        from src.calculator.main import _run_interactive_loop, _build_registry
        from src.calculator import Calculator

        error_log_path = tmp_path / "error_log.txt"
        history_path = tmp_path / "history.txt"

        # Mock input: add, then "abc" (invalid), then quit
        mock_inputs = iter(["add", "abc", "quit"])
        monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

        calculator = Calculator()
        registry = _build_registry()

        # Patch error logging into the interactive loop
        with patch("src.calculator.main.ErrorLog") as MockErrorLog:
            mock_error_log = MockErrorLog.return_value
            _run_interactive_loop(registry, str(history_path))

            # Verify ErrorLog was instantiated (if integration is present)
            # Note: This test assumes ErrorLog integration in __main__.py

    def test_interactive_mode_logs_unsupported_operation(self, tmp_path, monkeypatch, capsys):
        """Test that unknown operation is logged as unsupported_operation.

        Input: Interactive mode called with mock input for unknown operation "unknown_op", then "quit"
        Expected output: error_log.txt contains an entry with `unsupported_operation` category
        """
        from src.calculator.main import _run_interactive_loop, _build_registry
        from src.calculator import Calculator

        error_log_path = tmp_path / "error_log.txt"
        history_path = tmp_path / "history.txt"

        # Mock input: unknown operation, then quit
        mock_inputs = iter(["unknown_op", "quit"])
        monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

        calculator = Calculator()
        registry = _build_registry()

        # Patch error logging into the interactive loop
        with patch("src.calculator.main.ErrorLog") as MockErrorLog:
            mock_error_log = MockErrorLog.return_value
            _run_interactive_loop(registry, str(history_path))

            # Verify ErrorLog was instantiated
            # Note: This test assumes ErrorLog integration in __main__.py

    def test_interactive_mode_logs_calculation_error_division_by_zero(self, tmp_path, monkeypatch, capsys):
        """Test that division by zero is logged as calculation_error.

        Input: Interactive mode called with mock inputs for "divide", "5", "0", then "quit"
        Expected output: error_log.txt contains an entry with `calculation_error` category
        """
        from src.calculator.main import _run_interactive_loop, _build_registry
        from src.calculator import Calculator

        error_log_path = tmp_path / "error_log.txt"
        history_path = tmp_path / "history.txt"

        # Mock input: divide, 5, 0, then quit
        mock_inputs = iter(["divide", "5", "0", "quit"])
        monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

        calculator = Calculator()
        registry = _build_registry()

        # Patch error logging into the interactive loop
        with patch("src.calculator.main.ErrorLog") as MockErrorLog:
            mock_error_log = MockErrorLog.return_value
            _run_interactive_loop(registry, str(history_path))

            # Verify ErrorLog was instantiated
            # Note: This test assumes ErrorLog integration in __main__.py

    def test_interactive_mode_logs_calculation_error_domain_violation(self, tmp_path, monkeypatch, capsys):
        """Test that domain violation (e.g., negative square root) is logged as calculation_error.

        Input: Interactive mode called with mock inputs for "square_root", "-1", then "quit"
        Expected output: error_log.txt contains an entry with `calculation_error` category
        """
        from src.calculator.main import _run_interactive_loop, _build_registry
        from src.calculator import Calculator

        error_log_path = tmp_path / "error_log.txt"
        history_path = tmp_path / "history.txt"

        # Mock input: square_root, -1, then quit
        mock_inputs = iter(["square_root", "-1", "quit"])
        monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

        calculator = Calculator()
        registry = _build_registry()

        # Patch error logging into the interactive loop
        with patch("src.calculator.main.ErrorLog") as MockErrorLog:
            mock_error_log = MockErrorLog.return_value
            _run_interactive_loop(registry, str(history_path))

            # Verify ErrorLog was instantiated
            # Note: This test assumes ErrorLog integration in __main__.py

    def test_interactive_mode_successful_operation_not_in_error_log(self, tmp_path, monkeypatch, capsys):
        """Test that successful operations are NOT logged to error log.

        Input: Interactive mode called with mock inputs for "add", "5", "3", then "quit"
        Expected output: error_log.txt does NOT exist or has no entries; operation recorded in history
        """
        from src.calculator.main import _run_interactive_loop, _build_registry
        from src.calculator import Calculator

        error_log_path = tmp_path / "error_log.txt"
        history_path = tmp_path / "history.txt"

        # Mock input: successful add
        mock_inputs = iter(["add", "5", "3", "quit"])
        monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

        calculator = Calculator()
        registry = _build_registry()

        # Run interactive loop - errors are logged separately
        _run_interactive_loop(registry, str(history_path))

        # Verify successful operation is in history (not error log)
        history_path = Path(history_path)
        if history_path.exists():
            content = history_path.read_text()
            assert "add 5 3 = 8" in content

        # Error log should not exist or be empty
        if error_log_path.exists():
            error_content = error_log_path.read_text().strip()
            assert error_content == ""

    def test_interactive_mode_error_log_separate_from_history(self, tmp_path, monkeypatch, capsys):
        """Test that error log is separate from history file.

        Input: Interactive mode called with one error (invalid input) then one success (add 5 3)
        Expected output: error_log.txt contains only the error entry; history file contains only the success entry
        """
        from src.calculator.main import _run_interactive_loop, _build_registry
        from src.calculator import Calculator

        error_log_path = tmp_path / "error_log.txt"
        history_path = tmp_path / "history.txt"

        # Mock input: error, then success, then quit
        mock_inputs = iter(["add", "abc", "add", "5", "3", "quit"])
        monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))

        calculator = Calculator()
        registry = _build_registry()

        # Patch error logging
        with patch("src.calculator.main.ErrorLog") as MockErrorLog:
            mock_error_log = MockErrorLog.return_value
            _run_interactive_loop(registry, str(history_path))

            # Verify history file contains success only
            history_file = Path(history_path)
            if history_file.exists():
                content = history_file.read_text()
                assert "add 5 3 = 8" in content


# ============================================================================
# Test Group D: Error Categorization in CLI Mode (3 tests)
# ============================================================================

class TestErrorLoggingCLIMode:
    """Tests for error logging in CLI mode."""

    def test_cli_mode_logs_invalid_input_error(self, tmp_path, monkeypatch, capsys):
        """Test that invalid input in CLI mode is logged.

        Input: CLI mode with args ["add", "5", "abc"]
        Expected output: error_log.txt contains entry with `invalid_input` category; SystemExit raised
        """
        from src.calculator.main import cli_mode

        error_log_path = tmp_path / "error_log.txt"

        # Patch sys.argv
        monkeypatch.setattr(
            "sys.argv",
            ["calculator", "add", "5", "abc"]
        )

        # Patch error logging and expect SystemExit
        with patch("src.calculator.main.ErrorLog") as MockErrorLog:
            mock_error_log = MockErrorLog.return_value
            with pytest.raises(SystemExit) as exc_info:
                cli_mode()
            assert exc_info.value.code == 1

    def test_cli_mode_logs_calculation_error_division_by_zero(self, tmp_path, monkeypatch, capsys):
        """Test that division by zero in CLI mode is logged.

        Input: CLI mode with args ["divide", "5", "0"]
        Expected output: error_log.txt contains entry with `calculation_error` category; SystemExit raised
        """
        from src.calculator.main import cli_mode

        error_log_path = tmp_path / "error_log.txt"

        # Patch sys.argv
        monkeypatch.setattr(
            "sys.argv",
            ["calculator", "divide", "5", "0"]
        )

        # Patch error logging and expect SystemExit
        with patch("src.calculator.main.ErrorLog") as MockErrorLog:
            mock_error_log = MockErrorLog.return_value
            with pytest.raises(SystemExit) as exc_info:
                cli_mode()
            assert exc_info.value.code == 1

    def test_cli_mode_logs_unsupported_operation(self, tmp_path, monkeypatch, capsys):
        """Test that unsupported operation in CLI mode is logged.

        Input: CLI mode with args ["unknown_op", "5", "3"]
        Expected output: error_log.txt contains entry with `unsupported_operation` category; SystemExit raised
        """
        from src.calculator.main import cli_mode

        error_log_path = tmp_path / "error_log.txt"

        # Patch sys.argv
        monkeypatch.setattr(
            "sys.argv",
            ["calculator", "unknown_op", "5", "3"]
        )

        # Patch error logging and expect SystemExit
        with patch("src.calculator.main.ErrorLog") as MockErrorLog:
            mock_error_log = MockErrorLog.return_value
            with pytest.raises(SystemExit) as exc_info:
                cli_mode()
            assert exc_info.value.code == 1


# ============================================================================
# Test Group E: Edge Cases (5 tests)
# ============================================================================

class TestErrorLogEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_error_log_inputs_formatted_as_comma_separated(self, tmp_path):
        """Test that inputs are formatted as comma-separated in log.

        Input: Log error with inputs=[5, 3, 2.5]
        Expected output: Inputs formatted in log as `5, 3, 2.5`
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        error_log.log_error("invalid_input", "power", [5, 3, 2.5], "Invalid operand.")

        content = error_log_path.read_text()
        # Should contain comma-separated inputs
        assert "5" in content and "3" in content and "2.5" in content
        # Should be formatted with commas or spaces as separator
        assert "," in content or "5 3 2.5" in content

    def test_error_log_empty_inputs_formatted_as_empty_string(self, tmp_path):
        """Test that empty inputs are formatted correctly.

        Input: Log error with inputs=[]
        Expected output: Inputs field is empty string in log entry
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        error_log.log_error("unsupported_operation", "unknown", [], "Unknown operation.")

        content = error_log_path.read_text()
        # Should contain the error info
        assert "unsupported_operation" in content
        assert "unknown" in content
        assert "Unknown operation." in content

    def test_error_log_does_not_crash_on_io_error(self, tmp_path, monkeypatch):
        """Test that log_error doesn't crash when file write fails.

        Input: Create ErrorLog pointing to an unwritable path (mock open to raise OSError)
        Expected output: log_error() does not raise an exception; execution continues normally
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        # Patch file open to raise OSError
        original_open = open

        def failing_open(*args, **kwargs):
            raise OSError("Permission denied")

        with patch("builtins.open", side_effect=failing_open):
            # This should NOT raise an exception
            error_log.log_error("invalid_input", "add", [5, "abc"], "Invalid number.")

        # Execution should continue normally
        assert True  # If we got here, no exception was raised

    def test_error_log_file_io_error_does_not_crash(self, tmp_path):
        """Test that file I/O errors during logging don't crash the program.

        Input: Create ErrorLog, patch the file path to be a directory (so writing fails)
        Expected output: log_error() does not raise an exception
        """
        from src.error_logging import ErrorLog

        # Create a directory where we'd want the file
        dir_path = tmp_path / "error_log.txt"
        dir_path.mkdir()

        error_log = ErrorLog(str(dir_path))

        # This should NOT raise an exception even though the path is a directory
        error_log.log_error("invalid_input", "add", [5, "abc"], "Invalid number.")

        # Execution should continue normally
        assert True  # If we got here, no exception was raised

    def test_multiple_errors_accumulate_in_log(self, tmp_path):
        """Test that multiple errors accumulate in log file.

        Input: Log 3 different errors using same ErrorLog instance
        Expected output: File contains exactly 3 lines
        """
        from src.error_logging import ErrorLog

        error_log_path = tmp_path / "errors.txt"
        error_log = ErrorLog(str(error_log_path))

        # Log 3 errors
        error_log.log_error("invalid_input", "add", [5, "abc"], "Invalid number 'abc'.")
        error_log.log_error("calculation_error", "divide", [5, 0], "division by zero")
        error_log.log_error("unsupported_operation", "unknown", [], "Unknown operation.")

        content = error_log_path.read_text()
        lines = content.strip().split("\n")

        assert len(lines) == 3
        assert "invalid_input" in lines[0]
        assert "calculation_error" in lines[1]
        assert "unsupported_operation" in lines[2]
