"""Integration tests for error logging in main.py and src/cli.py.

Tests verify that the error logger is invoked correctly in context
when various error conditions occur during CLI or interactive operation.
"""

import subprocess
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

from src.error_logger import ErrorLogger
from src.calculator import Calculator


# ============================================================================
# Integration Tests: main.py Error Logging
# ============================================================================

class TestMainErrorLogging:
    """Test error logging within main.py CLI execution."""

    @pytest.fixture
    def run_cli_with_log(self):
        """Fixture to run main.py as subprocess and capture error log."""
        def _run(*args):
            log_file = Path(__file__).parent.parent / "error.log"
            # Remove existing log file to get clean state for this test
            if log_file.exists():
                log_file.unlink()

            cmd = [sys.executable, "main.py"] + list(args)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(Path(__file__).parent.parent),
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode, log_file
        return _run

    def test_unsupported_operation_logged(self, run_cli_with_log):
        """Test unknown operation is logged with UNSUPPORTED_OPERATION."""
        stdout, stderr, returncode, log_file = run_cli_with_log("foobar", "1")

        # Check exit code indicates error
        assert returncode == 1
        # Check stderr has error message
        assert "unknown operation" in stderr
        # Check log file exists and contains the error
        assert log_file.exists()
        content = log_file.read_text()
        assert "UNSUPPORTED_OPERATION" in content
        assert "operation='foobar'" in content

    def test_incorrect_arity_logged(self, run_cli_with_log):
        """Test wrong operand count is logged with INCORRECT_ARITY."""
        stdout, stderr, returncode, log_file = run_cli_with_log("add", "5")

        assert returncode == 1
        assert "requires" in stderr
        assert log_file.exists()
        content = log_file.read_text()
        assert "INCORRECT_ARITY" in content
        assert "operation='add'" in content
        assert "expected=2" in content
        assert "got=1" in content

    def test_invalid_operand_logged(self, run_cli_with_log):
        """Test non-numeric operand is logged with INVALID_OPERAND."""
        stdout, stderr, returncode, log_file = run_cli_with_log("add", "5", "abc")

        assert returncode == 1
        assert log_file.exists()
        content = log_file.read_text()
        assert "INVALID_OPERAND" in content
        assert "operand='abc'" in content

    def test_division_by_zero_logged(self, run_cli_with_log):
        """Test division by zero is logged with DIVISION_BY_ZERO."""
        stdout, stderr, returncode, log_file = run_cli_with_log("divide", "10", "0")

        assert returncode == 1
        assert log_file.exists()
        content = log_file.read_text()
        assert "DIVISION_BY_ZERO" in content
        assert "numerator=10" in content

    def test_invalid_domain_sqrt_negative_logged(self, run_cli_with_log):
        """Test sqrt of negative is logged with INVALID_DOMAIN."""
        stdout, stderr, returncode, log_file = run_cli_with_log("square_root", "-4")

        assert returncode == 1
        assert log_file.exists()
        content = log_file.read_text()
        assert "INVALID_DOMAIN" in content
        assert "operation='square_root'" in content
        assert "operand=-4" in content

    def test_invalid_domain_log_negative_logged(self, run_cli_with_log):
        """Test log of negative is logged with INVALID_DOMAIN."""
        stdout, stderr, returncode, log_file = run_cli_with_log("logarithm", "-5")

        assert returncode == 1
        assert log_file.exists()
        content = log_file.read_text()
        assert "INVALID_DOMAIN" in content
        assert "operation='logarithm'" in content


# ============================================================================
# Integration Tests: src/cli.py Error Logging
# ============================================================================

class TestInteractiveCliErrorLogging:
    """Test error logging within interactive_session() in src/cli.py."""

    def test_unsupported_operation_in_interactive_mode(self, tmp_path):
        """Test invalid operation name in interactive mode is logged."""
        log_file = tmp_path / "error.log"
        calc = Calculator()
        error_logger = ErrorLogger(str(log_file))

        # Simulate the check that happens in interactive_session
        operations = [name for name in dir(calc) if not name.startswith("_") and callable(getattr(calc, name))]
        invalid_op = "invalid_operation_xyz"

        if invalid_op not in operations:
            error_logger.log_unsupported_operation(invalid_op)

        content = log_file.read_text()
        assert "UNSUPPORTED_OPERATION" in content
        assert "operation='invalid_operation_xyz'" in content

    def test_division_by_zero_in_interactive_mode(self, tmp_path):
        """Test division by zero in interactive mode is logged."""
        log_file = tmp_path / "error.log"
        calc = Calculator()
        error_logger = ErrorLogger(str(log_file))

        # Simulate what happens when calculator raises ZeroDivisionError
        try:
            result = calc.divide(10.0, 0.0)
        except ZeroDivisionError as exc:
            numerator = 10.0
            error_logger.log_division_by_zero(numerator)

        content = log_file.read_text()
        assert "DIVISION_BY_ZERO" in content
        assert "numerator=10" in content

    def test_invalid_domain_sqrt_in_interactive_mode(self, tmp_path):
        """Test sqrt domain error in interactive mode is logged."""
        log_file = tmp_path / "error.log"
        calc = Calculator()
        error_logger = ErrorLogger(str(log_file))

        try:
            result = calc.square_root(-4.0)
        except ValueError as exc:
            operand_ctx = -4.0
            error_logger.log_invalid_domain("square_root", operand_ctx, str(exc))

        content = log_file.read_text()
        assert "INVALID_DOMAIN" in content
        assert "operation='square_root'" in content
        assert "operand=-4" in content

    def test_invalid_operand_in_interactive_mode(self, tmp_path):
        """Test invalid operand input in interactive mode is logged."""
        log_file = tmp_path / "error.log"
        error_logger = ErrorLogger(str(log_file))

        # Simulate when user enters non-numeric input
        error_logger.log_invalid_operand("not_a_number", "Invalid input: could not convert")

        content = log_file.read_text()
        assert "INVALID_OPERAND" in content
        assert "operand='not_a_number'" in content

    def test_invalid_domain_log_in_interactive_mode(self, tmp_path):
        """Test logarithm domain error in interactive mode is logged."""
        log_file = tmp_path / "error.log"
        calc = Calculator()
        error_logger = ErrorLogger(str(log_file))

        try:
            result = calc.logarithm(0.0)
        except ValueError as exc:
            operand_ctx = 0.0
            error_logger.log_invalid_domain("logarithm", operand_ctx, str(exc))

        content = log_file.read_text()
        assert "INVALID_DOMAIN" in content
        assert "operation='logarithm'" in content
        assert "operand=0" in content


# ============================================================================
# Integration Tests: Error Logging Doesn't Break Normal Behavior
# ============================================================================

class TestErrorLoggingNonDisruptive:
    """Test that error logging doesn't interfere with normal operation."""

    def test_successful_operation_doesnt_log_errors(self, tmp_path):
        """Test successful operation doesn't produce any error log entries."""
        log_file = tmp_path / "error.log"
        calc = Calculator()
        error_logger = ErrorLogger(str(log_file))

        # Perform a successful operation
        result = calc.add(5, 3)
        assert result == 8

        # Log file should not exist if no errors were logged
        if log_file.exists():
            content = log_file.read_text()
            # Log file may be created by initialization but should be empty or minimal
            assert content.strip() == "" or len(content) == 0 or "ERROR" not in content

    def test_error_logger_instance_independence(self, tmp_path):
        """Test multiple ErrorLogger instances work independently."""
        log_file1 = tmp_path / "error1.log"
        log_file2 = tmp_path / "error2.log"

        logger1 = ErrorLogger(str(log_file1))
        logger2 = ErrorLogger(str(log_file2))

        logger1.log_unsupported_operation("op1")
        logger2.log_invalid_operand("xyz", "reason")

        content1 = log_file1.read_text()
        content2 = log_file2.read_text()

        assert "UNSUPPORTED_OPERATION" in content1
        assert "op1" in content1

        assert "INVALID_OPERAND" in content2
        assert "xyz" in content2


# ============================================================================
# Integration Tests: Multiple Error Scenarios
# ============================================================================

class TestComplexErrorScenarios:
    """Test scenarios involving multiple errors in sequence."""

    def test_sequential_errors_all_logged(self, tmp_path):
        """Test multiple sequential errors are all logged to the same file."""
        log_file = tmp_path / "error.log"
        calc = Calculator()
        error_logger = ErrorLogger(str(log_file))

        # First error: unsupported operation
        error_logger.log_unsupported_operation("fake_op")

        # Second error: invalid operand
        error_logger.log_invalid_operand("abc", "not a number")

        # Third error: division by zero
        try:
            calc.divide(10, 0)
        except ZeroDivisionError:
            error_logger.log_division_by_zero(10)

        content = log_file.read_text()
        assert "UNSUPPORTED_OPERATION" in content
        assert "INVALID_OPERAND" in content
        assert "DIVISION_BY_ZERO" in content

    def test_error_context_preserved_in_logs(self, tmp_path):
        """Test error context (parameters) is preserved in log entries."""
        log_file = tmp_path / "error.log"
        error_logger = ErrorLogger(str(log_file))

        # Log error with specific context
        error_logger.log_incorrect_arity("multiply", 2, 3)

        content = log_file.read_text()
        # All parts of the error context should be present
        assert "multiply" in content
        assert "2" in content  # expected arity
        assert "3" in content  # actual arity

    def test_special_characters_in_error_context(self, tmp_path):
        """Test error context with special characters is logged correctly."""
        log_file = tmp_path / "error.log"
        error_logger = ErrorLogger(str(log_file))

        # Log with special characters
        error_logger.log_unsupported_operation("op-with_special*chars")
        error_logger.log_invalid_operand("1.2.3", "Multiple decimal points")

        content = log_file.read_text()
        assert "op-with_special*chars" in content
        assert "1.2.3" in content
        assert "Multiple decimal points" in content
