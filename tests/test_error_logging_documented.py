"""Test documented error logging behavior.

Verifies that error logging functions work as documented:
- Different error types are logged with appropriate categories
- Error context (parameters) is preserved
- Multiple errors accumulate in append mode
- Logging is silent (no console output)
"""

import pytest
import tempfile
import os
from pathlib import Path

from src.error_logger import ErrorLogger
from src.core.calculator import Calculator


class TestErrorLogging:
    """Test error logging behavior as documented in SESSION_BEHAVIOR.md."""

    @pytest.fixture
    def temp_log_file(self):
        """Create a temporary log file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = os.path.join(tmpdir, "error.log")
            yield log_path

    def test_unsupported_operation_logged(self, temp_log_file):
        """Test unsupported operation is logged with UNSUPPORTED_OPERATION category."""
        logger = ErrorLogger(temp_log_file)
        logger.log_unsupported_operation("foobar")

        content = Path(temp_log_file).read_text()
        assert "UNSUPPORTED_OPERATION" in content
        assert "operation='foobar'" in content

    def test_invalid_operand_logged(self, temp_log_file):
        """Test invalid operand is logged with INVALID_OPERAND category."""
        logger = ErrorLogger(temp_log_file)
        logger.log_invalid_operand("abc", "could not convert to float")

        content = Path(temp_log_file).read_text()
        assert "INVALID_OPERAND" in content
        assert "operand='abc'" in content
        assert "reason='could not convert to float'" in content

    def test_division_by_zero_logged(self, temp_log_file):
        """Test division by zero is logged with DIVISION_BY_ZERO category."""
        logger = ErrorLogger(temp_log_file)
        logger.log_division_by_zero(10.0)

        content = Path(temp_log_file).read_text()
        assert "DIVISION_BY_ZERO" in content
        assert "numerator=10" in content

    def test_invalid_domain_logged(self, temp_log_file):
        """Test domain error is logged with INVALID_DOMAIN category."""
        logger = ErrorLogger(temp_log_file)
        logger.log_invalid_domain("square_root", -1.0, "negative number")

        content = Path(temp_log_file).read_text()
        assert "INVALID_DOMAIN" in content
        assert "operation='square_root'" in content
        assert "operand=-1" in content
        assert "reason='negative number'" in content

    def test_error_log_format(self, temp_log_file):
        """Test error log has expected format with timestamp and level."""
        logger = ErrorLogger(temp_log_file)
        logger.log_unsupported_operation("test_op")

        content = Path(temp_log_file).read_text()
        # Should contain ERROR level in brackets
        assert "[ERROR]" in content
        # Should contain the operation category
        assert "UNSUPPORTED_OPERATION" in content

    def test_silent_logging_no_console_output(self, temp_log_file, capsys):
        """Test that logging does not produce console output."""
        logger = ErrorLogger(temp_log_file)

        # Call multiple logging methods
        logger.log_unsupported_operation("op1")
        logger.log_invalid_operand("xyz", "reason")
        logger.log_division_by_zero(10.0)

        # Capture console output
        captured = capsys.readouterr()
        # Should not have any output to stdout or stderr from logging
        assert captured.out == ""
        assert captured.err == ""

    def test_error_log_append_mode(self, temp_log_file):
        """Test that error logs accumulate (append mode)."""
        logger1 = ErrorLogger(temp_log_file)
        logger1.log_unsupported_operation("op1")

        # Create a new logger pointing to same file
        logger2 = ErrorLogger(temp_log_file)
        logger2.log_invalid_operand("abc", "reason")

        content = Path(temp_log_file).read_text()
        # Both errors should be in the file
        assert "op1" in content
        assert "abc" in content
        assert content.count("ERROR") >= 2  # At least two error entries

    def test_incorrect_arity_logged(self, temp_log_file):
        """Test incorrect arity is logged with INCORRECT_ARITY category."""
        logger = ErrorLogger(temp_log_file)
        logger.log_incorrect_arity("add", 2, 1)

        content = Path(temp_log_file).read_text()
        assert "INCORRECT_ARITY" in content
        assert "operation='add'" in content
        assert "expected=2" in content
        assert "got=1" in content

    def test_log_context_preserved(self, temp_log_file):
        """Test that all error context is preserved in logs."""
        logger = ErrorLogger(temp_log_file)

        # Log various errors with context
        logger.log_unsupported_operation("weird_op_123")
        logger.log_invalid_operand("1.2.3", "Multiple decimal points")
        logger.log_division_by_zero(999.5)

        content = Path(temp_log_file).read_text()
        assert "weird_op_123" in content
        assert "1.2.3" in content
        assert "Multiple decimal points" in content
        assert "999.5" in content

    def test_multiple_error_types_logged_sequentially(self, temp_log_file):
        """Test multiple error types can be logged in sequence."""
        logger = ErrorLogger(temp_log_file)

        logger.log_unsupported_operation("fake")
        logger.log_invalid_operand("not_a_num", "parse failed")
        logger.log_division_by_zero(5.0)
        logger.log_invalid_domain("sqrt", -4.0, "negative")

        content = Path(temp_log_file).read_text()
        assert "UNSUPPORTED_OPERATION" in content
        assert "INVALID_OPERAND" in content
        assert "DIVISION_BY_ZERO" in content
        assert "INVALID_DOMAIN" in content

    def test_error_logger_with_custom_log_file_path(self):
        """Test ErrorLogger works with custom log file paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_log = os.path.join(tmpdir, "custom_errors.log")
            logger = ErrorLogger(custom_log)
            logger.log_unsupported_operation("test")

            assert Path(custom_log).exists()
            content = Path(custom_log).read_text()
            assert "UNSUPPORTED_OPERATION" in content

    def test_error_logger_special_characters_in_context(self, temp_log_file):
        """Test that special characters in error context are handled."""
        logger = ErrorLogger(temp_log_file)

        logger.log_unsupported_operation("op-with_special*chars!@#")
        logger.log_invalid_operand("1.2.3.4", "Multiple decimal points!!")

        content = Path(temp_log_file).read_text()
        # Special characters should be preserved
        assert "op-with_special*chars!@#" in content
        assert "1.2.3.4" in content
        assert "Multiple decimal points!!" in content

    def test_log_division_by_zero_various_numerators(self, temp_log_file):
        """Test log_division_by_zero with various numerator values."""
        logger = ErrorLogger(temp_log_file)

        numerators = [0.0, 1.0, 10.5, -5.0, 999.999]
        for num in numerators:
            temp_log = os.path.join(os.path.dirname(temp_log_file), f"error_{id(num)}.log")
            logger_tmp = ErrorLogger(temp_log)
            logger_tmp.log_division_by_zero(num)

            content = Path(temp_log).read_text()
            assert "DIVISION_BY_ZERO" in content
            assert f"numerator={num}" in content

    def test_invalid_domain_various_operations(self, temp_log_file):
        """Test log_invalid_domain with various operation names."""
        logger = ErrorLogger(temp_log_file)

        operations = ["square_root", "logarithm", "natural_logarithm"]
        for op in operations:
            temp_log = os.path.join(os.path.dirname(temp_log_file), f"error_{op}.log")
            logger_tmp = ErrorLogger(temp_log)
            logger_tmp.log_invalid_domain(op, -1.0, "negative input")

            content = Path(temp_log).read_text()
            assert "INVALID_DOMAIN" in content
            assert f"operation='{op}'" in content
            assert "operand=-1" in content

    @pytest.mark.parametrize("operation,expected,got", [
        ("add", 2, 1),
        ("sqrt", 1, 2),
        ("multiply", 2, 3),
    ])
    def test_incorrect_arity_various_operations(self, temp_log_file, operation, expected, got):
        """Test log_incorrect_arity with various operation and arity values."""
        logger = ErrorLogger(temp_log_file)
        logger.log_incorrect_arity(operation, expected, got)

        content = Path(temp_log_file).read_text()
        assert "INCORRECT_ARITY" in content
        assert f"operation='{operation}'" in content
        assert f"expected={expected}" in content
        assert f"got={got}" in content
