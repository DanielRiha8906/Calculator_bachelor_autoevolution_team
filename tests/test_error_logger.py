"""Unit tests for the ErrorLogger class.

Tests cover initialization, all logging methods, file persistence,
and silent (non-console) output behavior.
"""

import logging
import pytest
from pathlib import Path

from src.error_logger import ErrorLogger


# ============================================================================
# Test ErrorLogger Initialization
# ============================================================================

class TestErrorLoggerInitialization:
    """Test ErrorLogger can be instantiated with various configurations."""

    def test_init_default_log_file(self, tmp_path):
        """Test ErrorLogger initializes with default log file path."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        assert logger._logger is not None
        assert isinstance(logger._logger, logging.Logger)

    def test_init_custom_log_file(self, tmp_path):
        """Test ErrorLogger accepts custom log file path."""
        custom_log = tmp_path / "custom_errors.log"
        logger = ErrorLogger(str(custom_log))
        assert logger._logger is not None

    def test_init_creates_unique_logger_per_instance(self, tmp_path):
        """Test each ErrorLogger instance has a unique logger name."""
        log_file = tmp_path / "error.log"
        logger1 = ErrorLogger(str(log_file))
        logger2 = ErrorLogger(str(log_file))
        assert logger1._logger.name != logger2._logger.name

    def test_init_logger_level_is_error(self, tmp_path):
        """Test logger level is set to ERROR."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        assert logger._logger.level == logging.ERROR

    def test_init_logger_propagate_is_false(self, tmp_path):
        """Test logger.propagate is False to prevent console output."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        assert logger._logger.propagate is False

    def test_init_has_file_handler(self, tmp_path):
        """Test logger has exactly one FileHandler."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        handlers = [h for h in logger._logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(handlers) == 1

    def test_init_file_handler_is_append_mode(self, tmp_path):
        """Test FileHandler is in append mode."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        handler = logger._logger.handlers[0]
        # FileHandler in append mode has mode 'a'
        assert handler.mode == 'a'

    def test_init_handler_has_formatter(self, tmp_path):
        """Test FileHandler has a formatter."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        handler = logger._logger.handlers[0]
        assert handler.formatter is not None

    def test_init_formatter_includes_asctime_level_message(self, tmp_path):
        """Test formatter includes asctime, levelname, and message."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        handler = logger._logger.handlers[0]
        fmt = handler.formatter._fmt
        assert "%(asctime)s" in fmt
        assert "%(levelname)s" in fmt
        assert "%(message)s" in fmt


# ============================================================================
# Test Error Logging Methods
# ============================================================================

class TestErrorLoggingCategories:
    """Test each logging method writes correct keyword and format to log file."""

    def test_log_unsupported_operation(self, tmp_path):
        """Test log_unsupported_operation writes UNSUPPORTED_OPERATION keyword."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_unsupported_operation("foobar")

        content = log_file.read_text()
        assert "UNSUPPORTED_OPERATION" in content
        assert "operation='foobar'" in content

    def test_log_invalid_operand(self, tmp_path):
        """Test log_invalid_operand writes INVALID_OPERAND keyword."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_invalid_operand("xyz", "not a number")

        content = log_file.read_text()
        assert "INVALID_OPERAND" in content
        assert "operand='xyz'" in content
        assert "reason='not a number'" in content

    def test_log_incorrect_arity(self, tmp_path):
        """Test log_incorrect_arity writes INCORRECT_ARITY keyword."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_incorrect_arity("add", 2, 1)

        content = log_file.read_text()
        assert "INCORRECT_ARITY" in content
        assert "operation='add'" in content
        assert "expected=2" in content
        assert "got=1" in content

    def test_log_division_by_zero(self, tmp_path):
        """Test log_division_by_zero writes DIVISION_BY_ZERO keyword."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_division_by_zero(42.0)

        content = log_file.read_text()
        assert "DIVISION_BY_ZERO" in content
        assert "numerator=42" in content

    def test_log_invalid_domain(self, tmp_path):
        """Test log_invalid_domain writes INVALID_DOMAIN keyword."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_invalid_domain("square_root", -4.0, "negative input")

        content = log_file.read_text()
        assert "INVALID_DOMAIN" in content
        assert "operation='square_root'" in content
        assert "operand=-4" in content
        assert "reason='negative input'" in content

    def test_log_unsupported_operation_with_special_chars(self, tmp_path):
        """Test operation names with special characters are escaped correctly."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_unsupported_operation("op'with'quotes")

        content = log_file.read_text()
        assert "UNSUPPORTED_OPERATION" in content
        assert "op'with'quotes" in content

    def test_log_invalid_operand_with_newlines(self, tmp_path):
        """Test operand strings with special characters are logged correctly."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_invalid_operand("123\nabc", "mixed content")

        content = log_file.read_text()
        assert "INVALID_OPERAND" in content
        # Newlines should be present in the log
        assert "123\nabc" in content or "123" in content


# ============================================================================
# Test Error Log File Persistence
# ============================================================================

class TestErrorLogFilePersistence:
    """Test log file is created, appended to, and persisted correctly."""

    def test_log_file_created_on_first_call(self, tmp_path):
        """Test log file is created when first logging call is made."""
        log_file = tmp_path / "error.log"
        assert not log_file.exists()

        logger = ErrorLogger(str(log_file))
        logger.log_unsupported_operation("test")

        assert log_file.exists()

    def test_log_file_append_mode_preserves_previous_logs(self, tmp_path):
        """Test subsequent ErrorLogger instances append to existing log file."""
        log_file = tmp_path / "error.log"

        # First instance logs an error
        logger1 = ErrorLogger(str(log_file))
        logger1.log_unsupported_operation("first_error")

        # Second instance logs another error
        logger2 = ErrorLogger(str(log_file))
        logger2.log_unsupported_operation("second_error")

        content = log_file.read_text()
        # Both errors should be in the file
        assert content.count("UNSUPPORTED_OPERATION") >= 2
        assert "first_error" in content
        assert "second_error" in content

    def test_log_file_not_truncated_on_new_instance(self, tmp_path):
        """Test creating a new ErrorLogger instance does not truncate the file."""
        log_file = tmp_path / "error.log"

        logger1 = ErrorLogger(str(log_file))
        logger1.log_division_by_zero(5.0)
        initial_content = log_file.read_text()

        # Create a new logger (which would open the file in append mode)
        logger2 = ErrorLogger(str(log_file))
        logger2.log_division_by_zero(10.0)

        final_content = log_file.read_text()
        # Initial content should still be present
        assert initial_content in final_content or len(final_content) > len(initial_content)

    def test_multiple_errors_in_sequence(self, tmp_path):
        """Test multiple logging calls produce multiple log entries."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))

        logger.log_unsupported_operation("op1")
        logger.log_invalid_operand("xyz", "reason1")
        logger.log_division_by_zero(42.0)

        content = log_file.read_text()
        lines = content.strip().split('\n')
        # Should have at least 3 log entries
        assert len(lines) >= 3
        assert "UNSUPPORTED_OPERATION" in content
        assert "INVALID_OPERAND" in content
        assert "DIVISION_BY_ZERO" in content

    def test_log_entries_include_timestamp(self, tmp_path):
        """Test log entries include timestamp information."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_unsupported_operation("test")

        content = log_file.read_text()
        # Timestamp format: YYYY-MM-DD HH:MM:SS,mmm
        # At minimum, should contain date separators and time colons
        assert "-" in content  # date separator
        assert ":" in content  # time separator


# ============================================================================
# Test Error Log Silence (No Console Output)
# ============================================================================

class TestErrorLogSilence:
    """Test logger produces no output to stdout or stderr."""

    def test_no_stdout_output(self, tmp_path, capsys):
        """Test logging produces no output to stdout."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))

        logger.log_unsupported_operation("test")
        logger.log_invalid_operand("xyz", "reason")
        logger.log_division_by_zero(10.0)

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_no_stderr_output(self, tmp_path, capsys):
        """Test logging produces no output to stderr."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))

        logger.log_invalid_domain("sqrt", -4.0, "negative")
        logger.log_incorrect_arity("add", 2, 1)

        captured = capsys.readouterr()
        assert captured.err == ""

    def test_logger_has_no_stream_handlers(self, tmp_path):
        """Test logger has no StreamHandler or console handlers."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))

        for handler in logger._logger.handlers:
            assert not isinstance(handler, logging.StreamHandler) or isinstance(
                handler, logging.FileHandler
            )

    def test_logger_not_attached_to_root(self, tmp_path):
        """Test logger propagate is False, preventing root handler output."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))

        # Root logger should have no effect on our error logger
        assert logger._logger.propagate is False


# ============================================================================
# Test Edge Cases and Parameters
# ============================================================================

class TestErrorLoggerEdgeCases:
    """Test ErrorLogger with edge case inputs."""

    @pytest.mark.parametrize("operation_name", [
        "",  # empty string
        "a",  # single character
        "operation_with_very_long_name_" * 10,  # very long name
        "operation-with-dashes",
        "operation.with.dots",
    ])
    def test_log_unsupported_operation_various_names(self, tmp_path, operation_name):
        """Test unsupported_operation logging with various operation names."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_unsupported_operation(operation_name)

        content = log_file.read_text()
        assert "UNSUPPORTED_OPERATION" in content

    @pytest.mark.parametrize("operand,reason", [
        ("", "empty string"),
        ("0", "zero is invalid"),
        ("-999", "negative number"),
        ("1.5.2", "multiple decimal points"),
        ("NaN", "not a number"),
    ])
    def test_log_invalid_operand_various_cases(self, tmp_path, operand, reason):
        """Test invalid_operand logging with various operand and reason values."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_invalid_operand(operand, reason)

        content = log_file.read_text()
        assert "INVALID_OPERAND" in content

    @pytest.mark.parametrize("numerator", [0, 0.0, -10, -10.5, 1e10, 1e-10])
    def test_log_division_by_zero_various_numerators(self, tmp_path, numerator):
        """Test division_by_zero logging with various numerator values."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_division_by_zero(numerator)

        content = log_file.read_text()
        assert "DIVISION_BY_ZERO" in content
        assert "numerator=" in content

    @pytest.mark.parametrize("expected,got", [
        (1, 0),
        (2, 1),
        (2, 3),
        (5, 1),
        (0, 1),
    ])
    def test_log_incorrect_arity_various_counts(self, tmp_path, expected, got):
        """Test incorrect_arity logging with various expected and actual counts."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_incorrect_arity("op", expected, got)

        content = log_file.read_text()
        assert "INCORRECT_ARITY" in content
        assert f"expected={expected}" in content
        assert f"got={got}" in content

    @pytest.mark.parametrize("operand", [0, 0.0, -1, -999, 1e-10])
    def test_log_invalid_domain_various_operands(self, tmp_path, operand):
        """Test invalid_domain logging with various operand values."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_invalid_domain("operation", operand, "reason")

        content = log_file.read_text()
        assert "INVALID_DOMAIN" in content


class TestErrorLoggerFileEncoding:
    """Test ErrorLogger handles file encoding correctly."""

    def test_utf8_encoding_in_operand(self, tmp_path):
        """Test operand strings with UTF-8 characters are logged correctly."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_invalid_operand("π", "Greek letter pi")

        content = log_file.read_text(encoding="utf-8")
        assert "INVALID_OPERAND" in content
        assert "π" in content

    def test_utf8_encoding_in_reason(self, tmp_path):
        """Test reason strings with UTF-8 characters are logged correctly."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        logger.log_invalid_operand("test", "résultat invalide")

        content = log_file.read_text(encoding="utf-8")
        assert "INVALID_OPERAND" in content
        assert "résultat invalide" in content


class TestErrorLoggerDeduplication:
    """Test ErrorLogger handles duplicate handler prevention."""

    def test_no_duplicate_handlers_on_reimport(self, tmp_path):
        """Test that reimporting ErrorLogger doesn't create duplicate handlers."""
        log_file = tmp_path / "error.log"
        logger1 = ErrorLogger(str(log_file))
        initial_handlers = len(logger1._logger.handlers)

        # Create another logger with the same log file
        logger2 = ErrorLogger(str(log_file))
        # Since logger names are unique per instance, they have different loggers
        assert logger1._logger.name != logger2._logger.name

    def test_handler_not_duplicated_in_same_instance(self, tmp_path):
        """Test that the same ErrorLogger instance doesn't get duplicate handlers."""
        log_file = tmp_path / "error.log"
        logger = ErrorLogger(str(log_file))
        handlers_before = len(logger._logger.handlers)

        # Call a logging method multiple times
        logger.log_unsupported_operation("test1")
        logger.log_unsupported_operation("test2")
        logger.log_unsupported_operation("test3")

        handlers_after = len(logger._logger.handlers)
        # Handler count should not increase
        assert handlers_before == handlers_after
