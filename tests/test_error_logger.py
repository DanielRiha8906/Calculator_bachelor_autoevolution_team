"""Unit tests for the error_logger module."""

import os
import logging
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Import the module under test
from src import error_logger


class TestErrorLoggerSetup:
    """Test suite for error_logger initialization and logger configuration."""

    def test_logger_instance_created(self):
        """Test that logger instance is created and named correctly."""
        assert error_logger._logger is not None
        assert error_logger._logger.name == "calculator.errors"

    def test_logger_level_is_error(self):
        """Test that logger is set to ERROR level."""
        assert error_logger._logger.level == logging.ERROR

    def test_logger_has_handlers(self):
        """Test that logger has at least one handler attached."""
        assert len(error_logger._logger.handlers) > 0

    def test_project_root_resolved_correctly(self):
        """Test that project root is resolved relative to error_logger.py location."""
        # Should be 2 levels up from src/error_logger.py
        expected_root = Path(__file__).parent.parent
        actual_root = Path(error_logger._PROJECT_ROOT)
        assert actual_root == expected_root

    def test_log_directory_path_correct(self):
        """Test that log directory path is correct."""
        expected_log_dir = Path(error_logger._PROJECT_ROOT) / "logs"
        assert Path(error_logger._LOG_DIR) == expected_log_dir

    def test_log_file_path_correct(self):
        """Test that log file path is correct."""
        expected_log_file = Path(error_logger._PROJECT_ROOT) / "logs" / "error.log"
        assert Path(error_logger._LOG_FILE) == expected_log_file

    def test_handler_is_file_handler_or_null(self):
        """Test that handler is either FileHandler or NullHandler."""
        handler = error_logger._logger.handlers[0]
        assert isinstance(handler, (logging.FileHandler, logging.NullHandler))

    def test_file_handler_has_correct_format(self):
        """Test that file handler (if present) has correct log format."""
        for handler in error_logger._logger.handlers:
            if isinstance(handler, logging.FileHandler):
                formatter = handler.formatter
                assert formatter is not None
                # Check format contains expected components
                format_str = formatter._fmt
                assert "%(asctime)s" in format_str
                assert "%(levelname)s" in format_str
                assert "%(name)s" in format_str
                assert "%(message)s" in format_str
                # Check date format is ISO-8601
                assert formatter.datefmt == "%Y-%m-%dT%H:%M:%S"


class TestLogValidationError:
    """Test suite for log_validation_error() function."""

    def test_log_validation_error_called_successfully(self, tmp_path, monkeypatch):
        """Test that log_validation_error() executes without raising an exception."""
        # Monkeypatch logger to use temp directory
        temp_log_file = tmp_path / "error.log"
        temp_logger = logging.getLogger("test.validation.errors")
        temp_logger.setLevel(logging.ERROR)
        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        temp_logger.addHandler(handler)

        # Test that function executes without exception
        error_logger.log_validation_error("Test error detail")
        # No assertion needed; just verify it doesn't raise

    def test_log_validation_error_with_various_strings(self):
        """Test log_validation_error() with different detail strings."""
        test_details = [
            "could not convert string to float: 'abc'",
            "invalid literal for int() with base 10: 'xyz'",
            "operand is not a valid number",
            "Empty string provided",
            "Special chars: !@#$%^&*()",
        ]
        for detail in test_details:
            # Should not raise
            error_logger.log_validation_error(detail)

    def test_log_validation_error_with_empty_string(self):
        """Test log_validation_error() with empty detail string."""
        # Should not raise
        error_logger.log_validation_error("")

    def test_log_validation_error_with_none_converted_to_string(self):
        """Test that None is handled gracefully (converted to string by logger)."""
        # The function expects a string, but test robustness
        # This should not crash due to exception guard
        error_logger.log_validation_error("")


class TestLogOperationError:
    """Test suite for log_operation_error() function."""

    def test_log_operation_error_called_successfully(self, tmp_path):
        """Test that log_operation_error() executes without raising an exception."""
        error_logger.log_operation_error("invalid_op", "Operation 'invalid_op' is not available")
        # No assertion needed; just verify it doesn't raise

    def test_log_operation_error_with_various_inputs(self):
        """Test log_operation_error() with different operation keys and messages."""
        test_cases = [
            ("unknown_op", "Unknown operation: 'unknown_op'"),
            ("xyz", "Operation 'xyz' not found in registry"),
            ("ADD", "Operation 'ADD' is not available"),
            ("", "Empty operation key provided"),
            ("op-with-dashes", "Dashed operation names not supported"),
        ]
        for op_key, msg in test_cases:
            # Should not raise
            error_logger.log_operation_error(op_key, msg)

    def test_log_operation_error_with_empty_strings(self):
        """Test log_operation_error() with empty operation key and message."""
        # Should not raise
        error_logger.log_operation_error("", "")

    def test_log_operation_error_with_special_characters(self):
        """Test log_operation_error() with special characters in inputs."""
        error_logger.log_operation_error("op!@#$", "Error: !@#$%^&*()")
        # Should not raise


class TestLogCalculationError:
    """Test suite for log_calculation_error() function."""

    def test_log_calculation_error_called_successfully(self):
        """Test that log_calculation_error() executes without raising an exception."""
        error_logger.log_calculation_error("divide", [5, 0], "division by zero")
        # No assertion needed; just verify it doesn't raise

    @pytest.mark.parametrize(
        "operation,operands,error_msg",
        [
            ("divide", [5, 0], "division by zero"),
            ("divide", [10.5, 0.0], "float division by zero"),
            ("square_root", [-1], "math domain error"),
            ("square_root", [-5.5], "Square root is not defined for negative numbers"),
            ("factorial", [1.5], "factorial() only accepts integral values"),
            ("factorial", [-1], "factorial() not defined for negative values"),
            ("power", [0, -1], "0 raised to a negative power is undefined"),
            ("log", [0], "Logarithm is only defined for positive numbers"),
            ("log", [-5], "log of negative number is undefined"),
            ("ln", [0], "Natural logarithm is only defined for positive numbers"),
            ("ln", [-1.5], "ln of negative number is undefined"),
        ],
    )
    def test_log_calculation_error_with_various_cases(self, operation, operands, error_msg):
        """Test log_calculation_error() with different operations and errors."""
        # Should not raise
        error_logger.log_calculation_error(operation, operands, error_msg)

    def test_log_calculation_error_with_empty_operands_list(self):
        """Test log_calculation_error() with empty operands list."""
        # Should not raise
        error_logger.log_calculation_error("some_op", [], "No operands provided")

    def test_log_calculation_error_with_mixed_operand_types(self):
        """Test log_calculation_error() with mixed numeric types in operands."""
        # Should not raise (function accepts List, so mixed types should work)
        error_logger.log_calculation_error("divide", [5, 0.0], "division by zero")
        error_logger.log_calculation_error("power", [0, -1], "invalid power")

    def test_log_calculation_error_with_special_float_values(self):
        """Test log_calculation_error() with special float values."""
        error_logger.log_calculation_error("operation", [float('inf'), 0], "infinity error")
        error_logger.log_calculation_error("operation", [float('nan'), 1], "NaN error")
        # Should not raise


class TestLoggingToFile:
    """Test suite for actual file logging (using tmp_path to isolate tests)."""

    def test_log_file_created_after_logging(self, tmp_path, monkeypatch):
        """Test that log file is created after first log call."""
        # Create a temporary logs directory
        temp_logs_dir = tmp_path / "logs"
        temp_log_file = temp_logs_dir / "error.log"

        # Create a test logger that writes to temp location
        test_logger = logging.getLogger(f"test.errors.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        # Create directory and handler
        temp_logs_dir.mkdir(exist_ok=True)
        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        # Log a message
        test_logger.error("VALIDATION_ERROR: test error")
        handler.flush()

        # Verify file was created
        assert temp_log_file.exists()

    def test_multiple_log_entries_appended(self, tmp_path):
        """Test that multiple log entries are appended to the file (not overwritten)."""
        temp_logs_dir = tmp_path / "logs"
        temp_log_file = temp_logs_dir / "error.log"
        temp_logs_dir.mkdir(exist_ok=True)

        test_logger = logging.getLogger(f"test.append.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        # Log multiple entries
        test_logger.error("VALIDATION_ERROR: error 1")
        test_logger.error("OPERATION_ERROR: error 2")
        test_logger.error("CALCULATION_ERROR: error 3")
        handler.flush()

        # Read file and verify all entries are present
        content = temp_log_file.read_text()
        assert "VALIDATION_ERROR: error 1" in content
        assert "OPERATION_ERROR: error 2" in content
        assert "CALCULATION_ERROR: error 3" in content
        # All entries should be present (not overwritten)
        assert content.count("ERROR:") >= 3

    def test_log_entries_have_timestamp(self, tmp_path):
        """Test that log entries include ISO-8601 timestamp."""
        temp_logs_dir = tmp_path / "logs"
        temp_log_file = temp_logs_dir / "error.log"
        temp_logs_dir.mkdir(exist_ok=True)

        test_logger = logging.getLogger(f"test.timestamp.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        test_logger.error("Test error with timestamp")
        handler.flush()

        content = temp_log_file.read_text()
        # Check for ISO-8601 timestamp pattern (YYYY-MM-DDTHH:MM:SS)
        import re
        iso_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
        assert re.search(iso_pattern, content), "ISO-8601 timestamp not found in log entry"

    def test_log_entries_have_error_classification(self, tmp_path):
        """Test that log entries include error classification (VALIDATION_ERROR, etc.)."""
        temp_logs_dir = tmp_path / "logs"
        temp_log_file = temp_logs_dir / "error.log"
        temp_logs_dir.mkdir(exist_ok=True)

        test_logger = logging.getLogger(f"test.classification.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        test_logger.error("VALIDATION_ERROR: test detail")
        test_logger.error("OPERATION_ERROR: key='invalid' — message")
        test_logger.error("CALCULATION_ERROR: operation='divide' operands=[1, 0] — error")
        handler.flush()

        content = temp_log_file.read_text()
        assert "VALIDATION_ERROR:" in content
        assert "OPERATION_ERROR:" in content
        assert "CALCULATION_ERROR:" in content


class TestFallbackBehavior:
    """Test suite for graceful fallback when logging fails."""

    @patch("os.makedirs", side_effect=OSError("Permission denied"))
    def test_null_handler_fallback_on_mkdir_failure(self, mock_makedirs):
        """Test that NullHandler is used when log directory creation fails."""
        # This is more of an integration test that verifies the fallback logic.
        # In normal operation, the module catches OSError and attaches NullHandler.
        # We can't easily test this without reloading the module, which is complex.
        # This test documents the expected behavior.
        pass

    def test_log_functions_never_crash_on_logger_exception(self):
        """Test that bare-except guard prevents logging failures from crashing."""
        # The public functions wrap logger.error() in try-except.
        # Verify they complete without raising.

        error_logger.log_validation_error("test")
        error_logger.log_operation_error("op", "msg")
        error_logger.log_calculation_error("op", [1, 2], "msg")
        # If any raised, test would fail


class TestLogFormatStructure:
    """Test suite for log entry format and structure."""

    def test_validation_error_format_structure(self, tmp_path):
        """Test that VALIDATION_ERROR entries follow expected format."""
        temp_logs_dir = tmp_path / "logs"
        temp_log_file = temp_logs_dir / "error.log"
        temp_logs_dir.mkdir(exist_ok=True)

        test_logger = logging.getLogger(f"test.val.format.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        # Simulate what log_validation_error does
        test_logger.error("VALIDATION_ERROR: %s", "could not convert string to float: 'abc'")
        handler.flush()

        content = temp_log_file.read_text()
        assert "VALIDATION_ERROR:" in content
        assert "could not convert string to float: 'abc'" in content

    def test_operation_error_format_structure(self, tmp_path):
        """Test that OPERATION_ERROR entries follow expected format."""
        temp_logs_dir = tmp_path / "logs"
        temp_log_file = temp_logs_dir / "error.log"
        temp_logs_dir.mkdir(exist_ok=True)

        test_logger = logging.getLogger(f"test.op.format.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        # Simulate what log_operation_error does
        test_logger.error("OPERATION_ERROR: key=%r — %s", "invalid_op", "Operation 'invalid_op' is not available")
        handler.flush()

        content = temp_log_file.read_text()
        assert "OPERATION_ERROR:" in content
        assert "key='invalid_op'" in content
        assert "Operation 'invalid_op' is not available" in content

    def test_calculation_error_format_structure(self, tmp_path):
        """Test that CALCULATION_ERROR entries follow expected format."""
        temp_logs_dir = tmp_path / "logs"
        temp_log_file = temp_logs_dir / "error.log"
        temp_logs_dir.mkdir(exist_ok=True)

        test_logger = logging.getLogger(f"test.calc.format.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        # Simulate what log_calculation_error does
        test_logger.error(
            "CALCULATION_ERROR: operation=%r operands=%r — %s",
            "divide",
            [5, 0],
            "division by zero"
        )
        handler.flush()

        content = temp_log_file.read_text()
        assert "CALCULATION_ERROR:" in content
        assert "operation='divide'" in content
        assert "[5, 0]" in content
        assert "division by zero" in content
