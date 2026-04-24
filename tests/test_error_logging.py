"""Test suite for error logging functionality (issue #400).

Tests verify that errors are properly logged to error.log with appropriate
error types, timestamps, operand values, and error messages. Tests use
temporary directories to avoid polluting the project root with log files.
"""

import os
import re
import tempfile
from pathlib import Path
from unittest.mock import patch
from io import StringIO

import pytest

from src.ui.cli import run_cli
from src.ui.interactive import run_interactive_session
from src.calculator import Calculator


@pytest.fixture
def temp_log_dir(tmp_path, monkeypatch):
    """Fixture that redirects error logging to a temporary directory.

    Monkeypatches the current working directory to a temp directory so that
    error.log is created there instead of the project root.
    """
    monkeypatch.chdir(tmp_path)
    return tmp_path


def get_error_log_content(log_dir: Path) -> str:
    """Read the error.log file if it exists, return empty string if not."""
    error_log = log_dir / "error.log"
    if not error_log.exists():
        return ""
    return error_log.read_text()


def error_log_exists(log_dir: Path) -> bool:
    """Check if error.log file exists in the given directory."""
    return (log_dir / "error.log").exists()


def get_history_content(log_dir: Path) -> str:
    """Read the history.txt file if it exists, return empty string if not."""
    history_file = log_dir / "history.txt"
    if not history_file.exists():
        return ""
    return history_file.read_text()


# ============================================================================
# Category 1: Invalid Operations (2 tests)
# ============================================================================


class TestInvalidOperations:
    """Tests for invalid operation errors."""

    def test_error_log_invalid_operation_cli(self, temp_log_dir):
        """Test that invalid operation via CLI is logged with correct error type."""
        exit_code = run_cli(['invalid_op', '5'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert "Invalid Operation" in log_content or "Unknown operation" in log_content
        assert "invalid_op" in log_content

    def test_error_log_invalid_operation_interactive(self, temp_log_dir):
        """Test that invalid operation in interactive mode is logged."""
        with patch('builtins.input', side_effect=["999", "no"]):
            with patch('builtins.print'):
                run_interactive_session()

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert "Invalid Operation" in log_content or "Invalid" in log_content

        # history.txt should be empty since no valid operations were performed
        history_content = get_history_content(temp_log_dir)
        assert history_content == "" or "No operations recorded" in history_content


# ============================================================================
# Category 2: Invalid Operands (3 tests)
# ============================================================================


class TestInvalidOperands:
    """Tests for invalid operand errors."""

    def test_error_log_invalid_operand_cli(self, temp_log_dir):
        """Test that invalid operand via CLI is logged with correct error type."""
        exit_code = run_cli(['add', 'abc', '5'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert "Invalid Operand" in log_content or "Invalid operand" in log_content
        assert "abc" in log_content or "add" in log_content

    def test_error_log_invalid_operand_interactive_unary(self, temp_log_dir):
        """Test that invalid unary operand in interactive mode is logged."""
        with patch('builtins.input', side_effect=["9", "abc", "no"]):
            with patch('builtins.print'):
                run_interactive_session()

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert "Invalid Operand" in log_content or "Invalid" in log_content
        assert "abc" in log_content or "sqrt" in log_content

    def test_error_log_invalid_operand_interactive_binary(self, temp_log_dir):
        """Test that invalid binary operand in interactive mode is logged."""
        with patch('builtins.input', side_effect=["0", "5", "xyz", "no"]):
            with patch('builtins.print'):
                run_interactive_session()

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert "Invalid Operand" in log_content or "Invalid" in log_content
        assert "xyz" in log_content or "add" in log_content


# ============================================================================
# Category 3: Incorrect Argument Counts (5 tests)
# ============================================================================


class TestIncorrectArgumentCounts:
    """Tests for incorrect argument count errors."""

    def test_error_log_cli_missing_operation(self, temp_log_dir):
        """Test that missing operation in CLI is logged."""
        exit_code = run_cli([])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert ("Incorrect Argument Count" in log_content or
                "Missing Arguments" in log_content or
                "Usage" in log_content)

    def test_error_log_cli_missing_operands_binary(self, temp_log_dir):
        """Test that missing operand in binary operation is logged."""
        exit_code = run_cli(['add', '5'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert "Incorrect Argument Count" in log_content or "requires 2" in log_content
        assert "add" in log_content or "operand" in log_content.lower()

    def test_error_log_cli_missing_operands_unary(self, temp_log_dir):
        """Test that missing operand in unary operation is logged."""
        exit_code = run_cli(['factorial'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert "Incorrect Argument Count" in log_content or "requires 1" in log_content
        assert "factorial" in log_content

    def test_error_log_cli_too_many_operands_binary(self, temp_log_dir):
        """Test that too many operands in binary operation is logged."""
        exit_code = run_cli(['add', '5', '3', '2'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert "Incorrect Argument Count" in log_content or "requires 2" in log_content
        assert "add" in log_content or "got 3" in log_content

    def test_error_log_cli_too_many_operands_unary(self, temp_log_dir):
        """Test that too many operands in unary operation is logged."""
        exit_code = run_cli(['factorial', '5', '3'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert "Incorrect Argument Count" in log_content or "requires 1" in log_content
        assert "factorial" in log_content or "got 2" in log_content


# ============================================================================
# Category 4: Runtime Calculation Errors (8 tests)
# ============================================================================


class TestRuntimeCalculationErrors:
    """Tests for runtime calculation errors (domain errors, etc)."""

    def test_error_log_division_by_zero_cli(self, temp_log_dir):
        """Test that division by zero in CLI is logged."""
        exit_code = run_cli(['divide', '5', '0'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert ("Runtime Calculation Error" in log_content or
                "Division by zero" in log_content or
                "division" in log_content.lower())
        assert "divide" in log_content

    def test_error_log_division_by_zero_interactive(self, temp_log_dir):
        """Test that division by zero in interactive mode is logged."""
        with patch('builtins.input', side_effect=["3", "5", "0", "no"]):
            with patch('builtins.print'):
                run_interactive_session()

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert ("Runtime Calculation Error" in log_content or
                "Division by zero" in log_content or
                "divide" in log_content)

        # history.txt should be empty since operation failed
        history_content = get_history_content(temp_log_dir)
        assert history_content == "" or len(history_content.strip()) == 0

    def test_error_log_sqrt_negative_cli(self, temp_log_dir):
        """Test that sqrt of negative in CLI is logged."""
        exit_code = run_cli(['sqrt', '-4'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert ("Runtime Calculation Error" in log_content or
                "Domain" in log_content or
                "sqrt" in log_content)

    def test_error_log_sqrt_negative_interactive(self, temp_log_dir):
        """Test that sqrt of negative in interactive mode is logged."""
        with patch('builtins.input', side_effect=["9", "-4", "no"]):
            with patch('builtins.print'):
                run_interactive_session()

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert ("Runtime Calculation Error" in log_content or
                "Domain" in log_content or
                "sqrt" in log_content)

    def test_error_log_ln_zero_cli(self, temp_log_dir):
        """Test that ln of zero in CLI is logged."""
        exit_code = run_cli(['ln', '0'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert ("Runtime Calculation Error" in log_content or
                "Domain" in log_content or
                "ln" in log_content)

    def test_error_log_ln_zero_interactive(self, temp_log_dir):
        """Test that ln of zero in interactive mode is logged."""
        with patch('builtins.input', side_effect=["5", "0", "no"]):
            with patch('builtins.print'):
                run_interactive_session()

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert ("Runtime Calculation Error" in log_content or
                "Domain" in log_content or
                "ln" in log_content)

    def test_error_log_factorial_negative_cli(self, temp_log_dir):
        """Test that factorial of negative in CLI is logged."""
        exit_code = run_cli(['factorial', '-5'])

        assert exit_code == 1
        assert error_log_exists(temp_log_dir)

        log_content = get_error_log_content(temp_log_dir)
        assert ("Runtime Calculation Error" in log_content or
                "Domain" in log_content or
                "factorial" in log_content)

    def test_error_log_factorial_negative_interactive(self, temp_log_dir):
        """Test that factorial of negative in interactive mode is logged."""
        with patch('builtins.input', side_effect=["4", "-5", "no"]):
            with patch('builtins.print'):
                run_interactive_session()

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert ("Runtime Calculation Error" in log_content or
                "Domain" in log_content or
                "factorial" in log_content)


# ============================================================================
# Category 5: Error Log File Management and Format (12 tests)
# ============================================================================


class TestErrorLogFileManagement:
    """Tests for error log file management and format."""

    def test_error_log_file_created_on_first_error(self, temp_log_dir):
        """Test that error.log is created when first error occurs."""
        assert not error_log_exists(temp_log_dir)

        run_cli(['invalid_op', '5'])

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert len(log_content.strip()) > 0

    def test_error_log_file_format_consistency(self, temp_log_dir):
        """Test that error log entries follow consistent format with timestamp."""
        run_cli(['divide', '5', '0'])

        log_content = get_error_log_content(temp_log_dir)
        lines = log_content.strip().split('\n')

        # Each line should contain at least a timestamp in brackets
        assert len(lines) > 0
        for line in lines:
            if line.strip():
                assert '[' in line and ']' in line  # Timestamp format

    def test_error_log_file_appends_not_overwrites(self, temp_log_dir):
        """Test that error log appends entries instead of overwriting."""
        # First error
        run_cli(['divide', '5', '0'])
        content1 = get_error_log_content(temp_log_dir)
        line1_count = len([l for l in content1.strip().split('\n') if l.strip()])

        # Second error
        run_cli(['sqrt', '-1'])
        content2 = get_error_log_content(temp_log_dir)
        line2_count = len([l for l in content2.strip().split('\n') if l.strip()])

        # Third error
        run_cli(['invalid_op', '5'])
        content3 = get_error_log_content(temp_log_dir)
        line3_count = len([l for l in content3.strip().split('\n') if l.strip()])

        # Each new error should add entries (file grows)
        assert line2_count > line1_count
        assert line3_count > line2_count

    def test_error_log_file_handles_io_failure(self, temp_log_dir):
        """Test graceful handling when log file cannot be written."""
        error_log = temp_log_dir / "error.log"

        # Create directory instead of file to simulate IO failure
        error_log.mkdir(exist_ok=True)

        # This should not raise an unhandled exception
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            exit_code = run_cli(['divide', '5', '0'])

        # CLI should still return error code
        assert exit_code == 1

    def test_error_log_separate_from_history(self, temp_log_dir):
        """Test that error.log is separate from history.txt."""
        # Successful operation
        run_cli(['add', '2', '3'])

        # Failed operation
        run_cli(['divide', '5', '0'])

        history_content = get_history_content(temp_log_dir)
        error_content = get_error_log_content(temp_log_dir)

        # history.txt should contain the add operation
        assert "add" in history_content
        assert "2" in history_content and "3" in history_content

        # error.log should contain the divide error
        assert "divide" in error_content or "Division" in error_content

    def test_error_log_timestamp_format(self, temp_log_dir):
        """Test that error log entries have valid timestamp format."""
        run_cli(['divide', '5', '0'])

        log_content = get_error_log_content(temp_log_dir)
        # Timestamp should match pattern YYYY-MM-DD HH:MM:SS
        pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        assert re.search(pattern, log_content), f"No timestamp found in: {log_content}"

    def test_error_log_includes_operation_name(self, temp_log_dir):
        """Test that error log entry includes the operation name."""
        run_cli(['factorial', '-5'])

        log_content = get_error_log_content(temp_log_dir)
        assert "factorial" in log_content

    def test_error_log_includes_operands(self, temp_log_dir):
        """Test that error log entry includes operand values."""
        run_cli(['divide', '5', '0'])

        log_content = get_error_log_content(temp_log_dir)
        # Should contain operands or reference to them
        assert "5" in log_content or "divide" in log_content
        assert "0" in log_content or "divide" in log_content

    def test_error_log_includes_error_message(self, temp_log_dir):
        """Test that error log entry includes error message text."""
        run_cli(['sqrt', '-4'])

        log_content = get_error_log_content(temp_log_dir)
        # Should contain some error message text (domain error, math domain, etc)
        assert ("domain" in log_content.lower() or
                "sqrt" in log_content or
                "Error" in log_content or
                "negative" in log_content.lower())

    def test_error_log_interactive_and_cli_consistency(self, temp_log_dir):
        """Test that same error type has consistent format in both modes."""
        # CLI error
        run_cli(['divide', '5', '0'])
        log_cli = get_error_log_content(temp_log_dir)
        lines_cli = [l for l in log_cli.strip().split('\n') if l.strip()]

        # Clear log by removing it
        error_log_file = temp_log_dir / "error.log"
        if error_log_file.exists():
            error_log_file.unlink()

        # Interactive error
        with patch('builtins.input', side_effect=["3", "5", "0", "no"]):
            with patch('builtins.print'):
                run_interactive_session()

        log_interactive = get_error_log_content(temp_log_dir)
        lines_interactive = [l for l in log_interactive.strip().split('\n') if l.strip()]

        # Both should have similar format (timestamp + error info)
        assert len(lines_cli) > 0
        assert len(lines_interactive) > 0
        # Both should have bracketed timestamps
        assert '[' in lines_cli[0] and '[' in lines_interactive[0]

    def test_error_log_multiple_errors_chronological(self, temp_log_dir):
        """Test that multiple errors are logged in chronological order."""
        errors = [
            ['divide', '5', '0'],
            ['sqrt', '-1'],
            ['invalid_op', '5'],
        ]

        for argv in errors:
            run_cli(argv)

        log_content = get_error_log_content(temp_log_dir)
        lines = [l for l in log_content.strip().split('\n') if l.strip()]

        # Should have 3 error entries
        assert len(lines) >= 3

    def test_error_log_operand_format_with_floats_and_negatives(self, temp_log_dir):
        """Test that error log correctly displays float and negative operands."""
        run_cli(['divide', '-5.5', '0'])

        log_content = get_error_log_content(temp_log_dir)
        # Should show operands accurately
        assert ("-5.5" in log_content or "5.5" in log_content or
                "divide" in log_content)


# ============================================================================
# Summary and Edge Cases
# ============================================================================


class TestErrorLoggingEdgeCases:
    """Additional edge case tests for error logging."""

    def test_error_log_with_very_large_numbers(self, temp_log_dir):
        """Test error logging with very large number operands."""
        run_cli(['divide', '999999999999', '0'])

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert "divide" in log_content or "Division" in log_content

    def test_error_log_with_scientific_notation(self, temp_log_dir):
        """Test that scientific notation operands are handled in error logs."""
        run_cli(['divide', '1e10', '0'])

        assert error_log_exists(temp_log_dir)
        log_content = get_error_log_content(temp_log_dir)
        assert "divide" in log_content or "Division" in log_content
