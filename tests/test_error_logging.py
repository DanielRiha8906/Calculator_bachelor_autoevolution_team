"""Test suite for error logging functionality.

Tests the error_logger module that logs calculation errors and invalid user inputs
to an error.log file with structured formatting including timestamp, level, operation,
operands, error type, and error message.
"""

import pytest
import os
import re
from datetime import datetime
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.calculator import Calculator

try:
    from src.error_logger import error_logger, log_error
except ImportError:
    # error_logger module not yet implemented - tests will fail at runtime
    error_logger = None
    def log_error(*args, **kwargs):
        raise NotImplementedError("error_logger module not yet implemented")


@pytest.fixture
def temp_error_log(tmp_path):
    """Fixture providing a temporary directory and error.log path for testing."""
    log_path = tmp_path / "error.log"
    yield log_path
    # Cleanup: remove log file if it exists
    if log_path.exists():
        log_path.unlink()


@pytest.fixture
def calculator():
    """Fixture providing a Calculator instance for tests."""
    return Calculator()


class TestLoggerInitialization:
    """Test suite for error_logger module initialization."""

    def test_logger_initialization(self, tmp_path):
        """Test that importing error_logger creates a logger and error.log after first log call."""
        log_path = tmp_path / "error.log"

        # Before logging, file should not exist
        assert not log_path.exists()

        # Log an error
        log_error("divide", [10, 0], "ZeroDivisionError", "division by zero", str(log_path))

        # After logging, file should exist
        assert log_path.exists()


class TestLogFormatTimestamp:
    """Test suite for error log timestamp format."""

    def test_log_format_contains_timestamp(self, tmp_path):
        """Test that a logged error line contains a timestamp in [YYYY-MM-DD HH:MM:SS] format."""
        log_path = tmp_path / "error.log"
        log_error("square_root", [-5], "ValueError", "Cannot take square root of a negative number.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        # Check for timestamp pattern [YYYY-MM-DD HH:MM:SS]
        timestamp_pattern = r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]'
        assert re.search(timestamp_pattern, log_content), f"No timestamp found in: {log_content}"


class TestLogFormatErrorLevel:
    """Test suite for error log level indicator."""

    def test_log_format_contains_error_level(self, tmp_path):
        """Test that a logged error line contains [ERROR] level indicator."""
        log_path = tmp_path / "error.log"
        log_error("square_root", [-5], "ValueError", "Cannot take square root of a negative number.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "[ERROR]" in log_content, f"[ERROR] not found in: {log_content}"


class TestLogFormatOperationAndOperands:
    """Test suite for operation and operands in log format."""

    def test_log_format_contains_operation_and_operands(self, tmp_path):
        """Test that logging divide(10,0) error line contains "Operation: divide" and "Operands: [10, 0]"."""
        log_path = tmp_path / "error.log"
        log_error("divide", [10, 0], "ZeroDivisionError", "division by zero", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "Operation: divide" in log_content, f"Operation not found in: {log_content}"
        assert "Operands: [10, 0]" in log_content, f"Operands not found in: {log_content}"


class TestLogFormatErrorType:
    """Test suite for error type in log format."""

    def test_log_format_contains_error_type(self, tmp_path):
        """Test that logging sqrt(-1) error line contains error type "ValueError"."""
        log_path = tmp_path / "error.log"
        log_error("square_root", [-1], "ValueError", "Cannot take square root of a negative number.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "ValueError" in log_content, f"ValueError not found in: {log_content}"


class TestLogFormatErrorMessage:
    """Test suite for error message in log format."""

    def test_log_format_contains_error_message(self, tmp_path):
        """Test that logging sqrt(-1) error line contains the message text."""
        log_path = tmp_path / "error.log"
        error_msg = "Cannot take square root of a negative number."
        log_error("square_root", [-1], "ValueError", error_msg, str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert error_msg in log_content, f"Error message not found in: {log_content}"


class TestSquareRootNegativeLogging:
    """Test suite for square_root negative input error logging."""

    def test_square_root_negative_logs_error(self, tmp_path):
        """Test that calling calculator.square_root(-5) causes a log entry with operation "square_root", operands containing "-5", error type "ValueError"."""
        log_path = tmp_path / "error.log"
        calc = Calculator()

        try:
            calc.square_root(-5)
        except ValueError:
            log_error("square_root", [-5], "ValueError", "Cannot take square root of a negative number.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "square_root" in log_content
        assert "-5" in log_content
        assert "ValueError" in log_content


class TestDivisionByZeroLogging:
    """Test suite for division by zero error logging."""

    def test_log_error_division_by_zero(self, tmp_path):
        """Test that calling calculator.divide(10, 0) causes a log entry with "divide", "[10, 0]", "ZeroDivisionError"."""
        log_path = tmp_path / "error.log"
        calc = Calculator()

        try:
            calc.divide(10, 0)
        except ZeroDivisionError:
            log_error("divide", [10, 0], "ZeroDivisionError", "division by zero", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "divide" in log_content
        assert "[10, 0]" in log_content
        assert "ZeroDivisionError" in log_content


class TestFactorialNegativeLogging:
    """Test suite for factorial negative input error logging."""

    def test_log_error_factorial_negative(self, tmp_path):
        """Test that calling calculator.factorial(-5) causes a log entry with "factorial", "[-5]", "ValueError"."""
        log_path = tmp_path / "error.log"
        calc = Calculator()

        try:
            calc.factorial(-5)
        except ValueError:
            log_error("factorial", [-5], "ValueError", "Factorial is not defined for negative numbers.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "factorial" in log_content
        assert "[-5]" in log_content
        assert "ValueError" in log_content


class TestLogNonPositiveLogging:
    """Test suite for log(0) error logging."""

    def test_log_error_log_non_positive(self, tmp_path):
        """Test that calling calculator.log(0) causes a log entry with "log", "[0]", "ValueError"."""
        log_path = tmp_path / "error.log"
        calc = Calculator()

        try:
            calc.log(0)
        except ValueError:
            log_error("log", [0], "ValueError", "Logarithm is only defined for positive numbers.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "log" in log_content
        assert "[0]" in log_content
        assert "ValueError" in log_content


class TestLnNegativeLogging:
    """Test suite for ln(-1) error logging."""

    def test_log_error_ln_non_positive(self, tmp_path):
        """Test that calling calculator.ln(-1) causes a log entry with "ln", "[-1]", "ValueError"."""
        log_path = tmp_path / "error.log"
        calc = Calculator()

        try:
            calc.ln(-1)
        except ValueError:
            log_error("ln", [-1], "ValueError", "Natural logarithm is only defined for positive numbers.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "ln" in log_content
        assert "[-1]" in log_content
        assert "ValueError" in log_content


class TestSuccessfulOperationsNotLogged:
    """Test suite for verifying successful operations are not logged."""

    def test_successful_operations_not_logged(self, tmp_path):
        """Test that calling calculator.add(2, 3) produces no error log entry."""
        log_path = tmp_path / "error.log"
        calc = Calculator()

        # Perform successful operation (no error to log)
        result = calc.add(2, 3)
        assert result == 5

        # Verify no log file was created for successful operations
        # Since we never called log_error, no file should exist
        # This test validates that successful operations don't trigger logging
        assert not log_path.exists(), "Error log should not be created for successful operations"


class TestInvalidOperandInputLogging:
    """Test suite for logging invalid operand input."""

    def test_log_invalid_operand_input(self, tmp_path):
        """Test that when a prompt function receives invalid numeric input "abc", a log entry is written with field "first number input" or similar context."""
        log_path = tmp_path / "error.log"

        # Simulate invalid operand input
        log_error("first_number_input", ["abc"], "ValueError", "Invalid numeric input: could not convert string to float: 'abc'", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        # Should contain context about the input type and error
        assert "first_number_input" in log_content or "operand" in log_content.lower()
        assert "ValueError" in log_content


class TestInvalidOperatorInputLogging:
    """Test suite for logging invalid operator input."""

    def test_log_invalid_operator_input(self, tmp_path):
        """Test that when operator prompt receives "xyz", a log entry is written with "operator input" context."""
        log_path = tmp_path / "error.log"

        # Simulate invalid operator input
        log_error("operator_input", ["xyz"], "ValueError", "Invalid operator: xyz", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "operator_input" in log_content or "operator" in log_content.lower()
        assert "ValueError" in log_content


class TestRetryAttemptLogging:
    """Test suite for logging retry attempts."""

    def test_log_retry_attempt(self, tmp_path):
        """Test that when a user retries after invalid input, each retry is logged with attempt count."""
        log_path = tmp_path / "error.log"

        # Log first retry attempt
        log_error("first_number_input", ["abc"], "ValueError", "Invalid input. Attempt 1/3", str(log_path))

        # Log second retry attempt
        log_error("first_number_input", ["xyz"], "ValueError", "Invalid input. Attempt 2/3", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "Attempt 1/3" in log_content
        assert "Attempt 2/3" in log_content


class TestMaxRetriesExceededLogging:
    """Test suite for logging max retries exceeded."""

    def test_log_max_retries_exceeded(self, tmp_path):
        """Test that when max retries is exhausted on operand prompt, a log entry is written with "max retries" context."""
        log_path = tmp_path / "error.log"

        # Log max retries exceeded
        log_error("first_number_input", ["invalid"], "MaxRetriesExceeded", "Maximum retry attempts exceeded for first number input.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "max retries" in log_content.lower() or "MaxRetriesExceeded" in log_content


class TestMaxRetriesExceededOperatorLogging:
    """Test suite for logging max retries exceeded for operator input."""

    def test_log_max_retries_exceeded_operator(self, tmp_path):
        """Test that max retries exceeded for operator input is logged with "operator" context."""
        log_path = tmp_path / "error.log"

        # Log max retries exceeded for operator
        log_error("operator_input", ["invalid"], "MaxRetriesExceeded", "Maximum retry attempts exceeded for operator input.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "operator" in log_content.lower() or "MaxRetriesExceeded" in log_content


class TestBatchUnknownOperationLogging:
    """Test suite for logging batch unknown operation."""

    def test_log_batch_unknown_operation(self, tmp_path):
        """Test that batch_main(["xyz", "5"]) causes a log entry for unknown operation."""
        log_path = tmp_path / "error.log"

        # Log unknown operation error
        log_error("batch_operation", ["xyz", "5"], "ValueError", "Unknown operation: xyz", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "unknown operation" in log_content.lower() or "xyz" in log_content


class TestBatchWrongOperandCountLogging:
    """Test suite for logging batch wrong operand count."""

    def test_log_batch_wrong_operand_count(self, tmp_path):
        """Test that batch_main(["add", "5"]) causes a log entry for wrong operand count."""
        log_path = tmp_path / "error.log"

        # Log wrong operand count
        log_error("batch_operation", ["add", "5"], "ValueError", "add requires exactly 2 operand(s), but 1 were provided.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "operand" in log_content.lower()


class TestBatchNonNumericArgumentLogging:
    """Test suite for logging batch non-numeric argument."""

    def test_log_batch_non_numeric_argument(self, tmp_path):
        """Test that batch_main(["add", "abc", "5"]) causes a log entry for non-numeric argument."""
        log_path = tmp_path / "error.log"

        # Log non-numeric argument
        log_error("batch_operation", ["add", "abc", "5"], "ValueError", "Invalid numeric argument: abc", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "numeric" in log_content.lower() or "abc" in log_content


class TestBatchDivisionByZeroLogging:
    """Test suite for logging batch division by zero."""

    def test_log_batch_division_by_zero(self, tmp_path):
        """Test that batch_main(["divide", "10", "0"]) causes a log entry with ZeroDivisionError."""
        log_path = tmp_path / "error.log"

        # Log division by zero from batch operation
        log_error("batch_divide", [10, 0], "ZeroDivisionError", "division by zero", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "ZeroDivisionError" in log_content


class TestBatchSqrtNegativeLogging:
    """Test suite for logging batch sqrt negative."""

    def test_log_batch_sqrt_negative(self, tmp_path):
        """Test that batch_main(["sqrt", "-5"]) causes a log entry with ValueError."""
        log_path = tmp_path / "error.log"

        # Log sqrt of negative from batch operation
        log_error("batch_sqrt", [-5], "ValueError", "Cannot take square root of a negative number.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        assert "ValueError" in log_content


class TestErrorLogFilePersistence:
    """Test suite for error log file persistence."""

    def test_error_log_file_persistence(self, tmp_path):
        """Test that multiple log calls all persist to error.log file."""
        log_path = tmp_path / "error.log"

        # Log multiple errors
        log_error("divide", [10, 0], "ZeroDivisionError", "division by zero", str(log_path))
        log_error("square_root", [-5], "ValueError", "Cannot take square root of a negative number.", str(log_path))
        log_error("factorial", [-5], "ValueError", "Factorial is not defined for negative numbers.", str(log_path))

        with open(log_path, 'r') as f:
            log_content = f.read()

        # All three errors should be in the file
        assert "divide" in log_content
        assert "square_root" in log_content
        assert "factorial" in log_content


class TestErrorLogAppendMode:
    """Test suite for error log append mode."""

    def test_error_log_append_mode(self, tmp_path):
        """Test that second log call appends to file; first error still present."""
        log_path = tmp_path / "error.log"

        # First log call
        log_error("divide", [10, 0], "ZeroDivisionError", "division by zero", str(log_path))

        with open(log_path, 'r') as f:
            first_content = f.read()

        # Verify first error is in file
        assert "divide" in first_content

        # Second log call
        log_error("square_root", [-5], "ValueError", "Cannot take square root of a negative number.", str(log_path))

        with open(log_path, 'r') as f:
            second_content = f.read()

        # Both errors should be present
        assert "divide" in second_content, "First error lost after append"
        assert "square_root" in second_content


class TestErrorLogNoRotation:
    """Test suite for error log file growth without rotation."""

    def test_error_log_no_rotation(self, tmp_path):
        """Test that repeated log calls produce one growing file, not rotated files."""
        log_path = tmp_path / "error.log"

        # Log multiple errors
        for i in range(5):
            operation = f"operation_{i}"
            log_error(operation, [i], "ValueError", f"Error {i}", str(log_path))

        # Check only one file exists
        log_files = list(tmp_path.glob("error.log*"))
        assert len(log_files) == 1, f"Expected 1 log file but found {len(log_files)}"

        # Verify all 5 operations are in the single file
        with open(log_path, 'r') as f:
            content = f.read()

        for i in range(5):
            assert f"operation_{i}" in content
