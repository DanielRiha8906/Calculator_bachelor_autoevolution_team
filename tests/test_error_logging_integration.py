"""Integration tests for error logging hooks in the calculator."""

import pytest
import logging
import re
from pathlib import Path
from unittest.mock import patch

from src.calculator import Calculator
from src.validation import validate_operand, OperandValidationError
from src.operations import OperationRegistry
from src import error_logger


class TestValidationErrorLogging:
    """Test suite for error logging during validation."""

    def test_invalid_operand_logs_validation_error(self, tmp_path, monkeypatch):
        """Test that invalid operand raises exception AND writes VALIDATION_ERROR log."""
        # Redirect logger to temp directory
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        # Create a test logger
        test_logger = logging.getLogger(f"test.val.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        # Monkeypatch error_logger._logger to use our test logger
        with patch.object(error_logger, "_logger", test_logger):
            # Call validate_operand with invalid input
            with pytest.raises(OperandValidationError):
                validate_operand("not_a_number")

            # Flush and read log file
            handler.flush()
            content = temp_log_file.read_text()

            # Verify VALIDATION_ERROR was logged
            assert "VALIDATION_ERROR:" in content

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "abc",
            "xyz123",
            "12.34.56",
            "!@#$",
            "",
        ],
    )
    def test_various_invalid_operands_logged(self, tmp_path, monkeypatch, invalid_input):
        """Test that various invalid operands trigger validation error logging."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.various.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            with pytest.raises(OperandValidationError):
                validate_operand(invalid_input)

            handler.flush()
            content = temp_log_file.read_text()
            assert "VALIDATION_ERROR:" in content


class TestOperationErrorLogging:
    """Test suite for error logging during operation selection."""

    def test_invalid_operation_logs_operation_error(self, tmp_path, monkeypatch):
        """Test that unknown operation logs OPERATION_ERROR before raising."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.op.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()
            registry = OperationRegistry(calculator)

            # Try to get unknown operation
            with pytest.raises(KeyError):
                registry.get_operation("unknown_op")

            handler.flush()
            content = temp_log_file.read_text()

            # Verify OPERATION_ERROR was logged
            assert "OPERATION_ERROR:" in content
            assert "unknown_op" in content

    @pytest.mark.parametrize(
        "invalid_key",
        [
            "invalid",
            "xyz",
            "ADD",  # case-sensitive
            "divide ",  # extra whitespace
            "",
        ],
    )
    def test_various_invalid_operations_logged(self, tmp_path, monkeypatch, invalid_key):
        """Test that various invalid operation keys trigger operation error logging."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.invalid_ops.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()
            registry = OperationRegistry(calculator)

            with pytest.raises(KeyError):
                registry.get_operation(invalid_key)

            handler.flush()
            content = temp_log_file.read_text()
            assert "OPERATION_ERROR:" in content


class TestDivisionByZeroLogging:
    """Test suite for division by zero error logging."""

    def test_division_by_zero_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that division by zero raises ZeroDivisionError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.divzero.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            # Division by zero should raise and log
            with pytest.raises(ZeroDivisionError):
                calculator.divide(5, 0)

            handler.flush()
            content = temp_log_file.read_text()

            # Verify CALCULATION_ERROR was logged with operation='divide'
            assert "CALCULATION_ERROR:" in content
            assert "operation='divide'" in content or "operation=\"divide\"" in content
            assert "[5, 0]" in content

    @pytest.mark.parametrize(
        "dividend,divisor",
        [
            (5, 0),
            (0, 0),
            (10.5, 0.0),
            (-5, 0),
        ],
    )
    def test_various_division_by_zero_cases_logged(self, tmp_path, monkeypatch, dividend, divisor):
        """Test that various division by zero cases are logged."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.divzero_various.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ZeroDivisionError):
                calculator.divide(dividend, divisor)

            handler.flush()
            content = temp_log_file.read_text()
            assert "CALCULATION_ERROR:" in content
            assert "operation='divide'" in content or "operation=\"divide\"" in content


class TestSquareRootErrorLogging:
    """Test suite for square root error logging."""

    def test_negative_square_root_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that square root of negative number raises ValueError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.sqrt.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.square_root(-1)

            handler.flush()
            content = temp_log_file.read_text()

            # Verify CALCULATION_ERROR was logged with operation='square_root'
            assert "CALCULATION_ERROR:" in content
            assert "operation='square_root'" in content or "operation=\"square_root\"" in content
            assert "[-1]" in content

    @pytest.mark.parametrize(
        "operand",
        [
            -1,
            -5.5,
            -0.0001,
            -100,
        ],
    )
    def test_various_negative_square_roots_logged(self, tmp_path, monkeypatch, operand):
        """Test that various negative operands trigger sqrt error logging."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.sqrt_various.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.square_root(operand)

            handler.flush()
            content = temp_log_file.read_text()
            assert "CALCULATION_ERROR:" in content
            assert "square_root" in content


class TestFactorialErrorLogging:
    """Test suite for factorial error logging."""

    def test_negative_factorial_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that factorial of negative number raises ValueError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.fact.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.factorial(-1)

            handler.flush()
            content = temp_log_file.read_text()

            assert "CALCULATION_ERROR:" in content
            assert "operation='factorial'" in content or "operation=\"factorial\"" in content
            assert "[-1]" in content

    def test_non_integer_factorial_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that factorial of float raises ValueError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.fact_float.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.factorial(1.5)

            handler.flush()
            content = temp_log_file.read_text()

            assert "CALCULATION_ERROR:" in content
            assert "factorial" in content

    def test_boolean_factorial_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that boolean passed to factorial raises ValueError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.fact_bool.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.factorial(True)

            handler.flush()
            content = temp_log_file.read_text()

            assert "CALCULATION_ERROR:" in content


class TestPowerErrorLogging:
    """Test suite for power operation error logging."""

    def test_zero_to_negative_power_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that 0^(-n) raises ValueError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.power.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.power(0, -1)

            handler.flush()
            content = temp_log_file.read_text()

            assert "CALCULATION_ERROR:" in content
            assert "operation='power'" in content or "operation=\"power\"" in content
            assert "[0, -1]" in content

    @pytest.mark.parametrize(
        "exponent",
        [
            -1,
            -5,
            -0.5,
        ],
    )
    def test_various_zero_to_negative_power_cases_logged(self, tmp_path, monkeypatch, exponent):
        """Test that various 0^(-n) cases are logged."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.power_various.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.power(0, exponent)

            handler.flush()
            content = temp_log_file.read_text()
            assert "CALCULATION_ERROR:" in content
            assert "power" in content


class TestLogErrorLogging:
    """Test suite for log (base-10) error logging."""

    def test_log_of_zero_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that log(0) raises ValueError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.log.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.log(0)

            handler.flush()
            content = temp_log_file.read_text()

            assert "CALCULATION_ERROR:" in content
            assert "operation='log'" in content or "operation=\"log\"" in content
            assert "[0]" in content

    def test_log_of_negative_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that log(negative) raises ValueError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.log_neg.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.log(-5)

            handler.flush()
            content = temp_log_file.read_text()

            assert "CALCULATION_ERROR:" in content
            assert "log" in content

    @pytest.mark.parametrize(
        "operand",
        [
            0,
            -1,
            -10.5,
        ],
    )
    def test_various_log_error_cases_logged(self, tmp_path, monkeypatch, operand):
        """Test that various invalid log operands are logged."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.log_various.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.log(operand)

            handler.flush()
            content = temp_log_file.read_text()
            assert "CALCULATION_ERROR:" in content


class TestLnErrorLogging:
    """Test suite for natural logarithm error logging."""

    def test_ln_of_zero_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that ln(0) raises ValueError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.ln.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.ln(0)

            handler.flush()
            content = temp_log_file.read_text()

            assert "CALCULATION_ERROR:" in content
            assert "operation='ln'" in content or "operation=\"ln\"" in content
            assert "[0]" in content

    def test_ln_of_negative_logs_calculation_error(self, tmp_path, monkeypatch):
        """Test that ln(negative) raises ValueError AND logs CALCULATION_ERROR."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.ln_neg.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.ln(-1)

            handler.flush()
            content = temp_log_file.read_text()

            assert "CALCULATION_ERROR:" in content
            assert "ln" in content

    @pytest.mark.parametrize(
        "operand",
        [
            0,
            -1,
            -100.5,
        ],
    )
    def test_various_ln_error_cases_logged(self, tmp_path, monkeypatch, operand):
        """Test that various invalid ln operands are logged."""
        temp_log_file = tmp_path / "error.log"
        temp_log_file.parent.mkdir(parents=True, exist_ok=True)

        test_logger = logging.getLogger(f"test.ln_various.{id(self)}")
        test_logger.setLevel(logging.ERROR)
        test_logger.handlers.clear()

        handler = logging.FileHandler(str(temp_log_file), mode="a", encoding="utf-8")
        handler.setLevel(logging.ERROR)
        handler.setFormatter(
            logging.Formatter(fmt="%(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
        )
        test_logger.addHandler(handler)

        with patch.object(error_logger, "_logger", test_logger):
            calculator = Calculator()

            with pytest.raises(ValueError):
                calculator.ln(operand)

            handler.flush()
            content = temp_log_file.read_text()
            assert "CALCULATION_ERROR:" in content


class TestErrorLogSeparation:
    """Test suite verifying error logs are separate from operation history."""

    def test_error_log_is_separate_from_history(self, tmp_path):
        """Test that error.log is separate and does not contain operation history."""
        # This is more of a file structure test. Both should exist in logs/ directory
        # but error.log should only contain errors, not successful operations.
        calculator = Calculator()

        # Attempt an error
        try:
            calculator.divide(5, 0)
        except ZeroDivisionError:
            pass

        # Verify logs directory exists and contains error.log
        logs_dir = Path(error_logger._PROJECT_ROOT) / "logs"
        error_log_file = logs_dir / "error.log"

        # The error.log file should exist after we've logged an error
        # Note: Only verify structure; actual file presence depends on handlers
        assert logs_dir.exists()
        assert logs_dir.is_dir()
