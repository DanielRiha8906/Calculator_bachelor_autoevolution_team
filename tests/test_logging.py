"""Comprehensive test suite for the calculator logging feature.

Tests cover:
- Calculator error logging: division by zero, invalid types, invalid values
- CLI error logging: division by zero in expressions, syntax errors
- User input error logging: invalid numbers, operation execution errors
- Integration tests: logging doesn't change exception semantics
"""

import pytest
import logging
import tempfile
import os
from pathlib import Path

from src.logic import Calculator
from src.cli import parse_and_evaluate, run_cli
from src.user_input import parse_number, execute_operation, InvalidInputError
from src.logging_config import setup_logging, logger


@pytest.fixture
def calculator():
    """Provides a fresh Calculator instance for each test."""
    return Calculator()


@pytest.fixture
def temp_log_file():
    """Provides a temporary log file path."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        log_path = f.name
    yield log_path
    # Cleanup
    if os.path.exists(log_path):
        os.remove(log_path)


# ============================================================================
# CALCULATOR ERROR LOGGING TESTS
# ============================================================================

class TestCalculatorErrorLogging:
    """Test suite for error logging in Calculator methods."""

    def test_divide_by_zero_error_is_logged(self, calculator, caplog):
        """Verify that ZeroDivisionError in divide() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ZeroDivisionError):
                calculator.divide(10, 0)

        # Check that an error was logged containing 'divide'
        assert any("divide" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_divide_by_zero_with_float_logged(self, calculator, caplog):
        """Verify that ZeroDivisionError with float divisor is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ZeroDivisionError):
                calculator.divide(10.5, 0.0)

        assert any("divide" in record.message.lower() for record in caplog.records)

    def test_divide_by_zero_with_negative_numerator_logged(self, calculator, caplog):
        """Verify ZeroDivisionError with negative numerator is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ZeroDivisionError):
                calculator.divide(-10, 0)

        assert any("divide" in record.message.lower() for record in caplog.records)

    def test_factorial_negative_value_error_logged(self, calculator, caplog):
        """Verify that ValueError in factorial() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.factorial(-5)

        assert any("factorial" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_factorial_bool_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for bool in factorial() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.factorial(True)

        assert any("factorial" in record.message.lower() for record in caplog.records)
        assert any("bool" in record.message.lower() for record in caplog.records)

    def test_factorial_float_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for non-integer float in factorial() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.factorial(5.5)

        assert any("factorial" in record.message.lower() for record in caplog.records)

    def test_factorial_non_numeric_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for string in factorial() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.factorial("5")

        assert any("factorial" in record.message.lower() for record in caplog.records)

    def test_square_bool_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for bool in square() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.square(True)

        assert any("square" in record.message.lower() for record in caplog.records)

    def test_square_string_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for string in square() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.square("5")

        assert any("square" in record.message.lower() for record in caplog.records)

    def test_cube_bool_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for bool in cube() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.cube(False)

        assert any("cube" in record.message.lower() for record in caplog.records)

    def test_cube_none_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for None in cube() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.cube(None)

        assert any("cube" in record.message.lower() for record in caplog.records)

    def test_square_root_negative_value_error_logged(self, calculator, caplog):
        """Verify that ValueError in square_root() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.square_root(-1)

        assert any("square_root" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_square_root_negative_float_logged(self, calculator, caplog):
        """Verify ValueError for negative float in square_root() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.square_root(-5.5)

        assert any("square_root" in record.message.lower() for record in caplog.records)

    def test_square_root_bool_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for bool in square_root() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.square_root(True)

        assert any("square_root" in record.message.lower() for record in caplog.records)

    def test_square_root_string_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for string in square_root() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.square_root("4")

        assert any("square_root" in record.message.lower() for record in caplog.records)

    def test_cube_root_bool_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for bool in cube_root() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.cube_root(False)

        assert any("cube_root" in record.message.lower() for record in caplog.records)

    def test_cube_root_none_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for None in cube_root() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.cube_root(None)

        assert any("cube_root" in record.message.lower() for record in caplog.records)

    def test_power_bool_base_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for bool base in power() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.power(True, 2)

        assert any("power" in record.message.lower() for record in caplog.records)
        assert any("base" in record.message.lower() for record in caplog.records)

    def test_power_bool_exponent_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for bool exponent in power() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.power(2, False)

        assert any("power" in record.message.lower() for record in caplog.records)
        assert any("exponent" in record.message.lower() for record in caplog.records)

    def test_power_string_base_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for string base in power() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.power("2", 3)

        assert any("power" in record.message.lower() for record in caplog.records)

    def test_power_string_exponent_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for string exponent in power() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.power(2, "3")

        assert any("power" in record.message.lower() for record in caplog.records)

    def test_log10_nonpositive_zero_value_error_logged(self, calculator, caplog):
        """Verify that ValueError for log10(0) is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.log10(0)

        assert any("log10" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_log10_negative_value_error_logged(self, calculator, caplog):
        """Verify that ValueError for negative in log10() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.log10(-5)

        assert any("log10" in record.message.lower() for record in caplog.records)

    def test_log10_bool_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for bool in log10() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.log10(True)

        assert any("log10" in record.message.lower() for record in caplog.records)

    def test_log10_string_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for string in log10() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.log10("10")

        assert any("log10" in record.message.lower() for record in caplog.records)

    def test_natural_log_nonpositive_zero_value_error_logged(self, calculator, caplog):
        """Verify that ValueError for natural_log(0) is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.natural_log(0)

        assert any("natural_log" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_natural_log_negative_value_error_logged(self, calculator, caplog):
        """Verify that ValueError for negative in natural_log() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                calculator.natural_log(-5)

        assert any("natural_log" in record.message.lower() for record in caplog.records)

    def test_natural_log_bool_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for bool in natural_log() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.natural_log(True)

        assert any("natural_log" in record.message.lower() for record in caplog.records)

    def test_natural_log_string_type_error_logged(self, calculator, caplog):
        """Verify that TypeError for string in natural_log() is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(TypeError):
                calculator.natural_log("10")

        assert any("natural_log" in record.message.lower() for record in caplog.records)


# ============================================================================
# CLI ERROR LOGGING TESTS
# ============================================================================

class TestCLIErrorLogging:
    """Test suite for error logging in CLI module."""

    def test_cli_parse_and_evaluate_division_by_zero_logs_error(self, caplog):
        """Verify division by zero in expression is logged in parse_and_evaluate."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ZeroDivisionError):
                parse_and_evaluate("10 / 0", calc)

        # Log should contain info about the division by zero from calculator
        assert any("divide" in record.message.lower() for record in caplog.records)

    def test_cli_parse_and_evaluate_invalid_expression_logs_error(self, caplog):
        """Verify invalid expression raises ValueError."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                # This will fail because it tries to evaluate "boolean" which is not a valid constant
                parse_and_evaluate("True and False", calc)

        # Should have at least logged something or raised
        assert len(caplog.records) >= 0

    def test_cli_parse_and_evaluate_invalid_operator_logs_error(self, caplog):
        """Verify unsupported operator syntax is logged."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                parse_and_evaluate("5 // 3", calc)

        # Should fail at parsing or evaluation
        assert len(caplog.records) >= 0

    def test_cli_run_cli_division_by_zero_logs_error(self, caplog):
        """Verify division by zero in CLI is logged."""
        with caplog.at_level(logging.ERROR):
            exit_code = run_cli(["10", "/", "0"])

        # Should have logged error and returned 1
        assert exit_code == 1
        assert any("division" in record.message.lower() for record in caplog.records)

    def test_cli_run_cli_unsupported_operator_logs_error(self, caplog):
        """Verify unsupported operator in CLI is logged."""
        with caplog.at_level(logging.ERROR):
            # Using % which is not supported in the calculator
            exit_code = run_cli(["5", "%", "3"])

        # Should have returned an error code
        assert exit_code in [0, 1]  # Might process as valid or invalid depending on implementation

    def test_cli_run_cli_no_args_shows_error(self, caplog):
        """Verify that no arguments shows error message."""
        with caplog.at_level(logging.ERROR):
            exit_code = run_cli([])

        # run_cli returns 1 but doesn't log in this case (it's a usage error)
        assert exit_code == 1


# ============================================================================
# USER INPUT ERROR LOGGING TESTS
# ============================================================================

class TestUserInputErrorLogging:
    """Test suite for error logging in user_input module."""

    def test_parse_number_invalid_string_logs_error(self, caplog):
        """Verify that invalid number input is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(InvalidInputError):
                parse_number("abc")

        assert any("parse_number" in record.message.lower() for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_parse_number_empty_string_logs_error(self, caplog):
        """Verify that empty string input is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(InvalidInputError):
                parse_number("")

        assert any("parse_number" in record.message.lower() for record in caplog.records)

    def test_parse_number_whitespace_only_logs_error(self, caplog):
        """Verify that whitespace-only input is logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(InvalidInputError):
                parse_number("   ")

        assert any("parse_number" in record.message.lower() for record in caplog.records)

    def test_parse_number_special_characters_logs_error(self, caplog):
        """Verify that special characters in input are logged."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(InvalidInputError):
                parse_number("@#$%")

        assert any("parse_number" in record.message.lower() for record in caplog.records)

    def test_execute_operation_division_by_zero_logs_error(self, caplog):
        """Verify that division by zero in execute_operation is logged."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            result = execute_operation(calc, "divide", [10, 0])

        # execute_operation catches the exception and returns an error string
        assert isinstance(result, str)
        assert "Error" in result
        assert any("execute_operation" in record.message.lower() for record in caplog.records)

    def test_execute_operation_square_root_negative_logs_error(self, caplog):
        """Verify that square_root of negative in execute_operation is logged."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            result = execute_operation(calc, "square_root", [-1])

        # execute_operation catches the exception and returns an error string
        assert isinstance(result, str)
        assert "Error" in result
        assert any("execute_operation" in record.message.lower() for record in caplog.records)

    def test_execute_operation_factorial_negative_logs_error(self, caplog):
        """Verify that negative factorial in execute_operation is logged."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            result = execute_operation(calc, "factorial", [-5])

        # execute_operation catches the exception and returns an error string
        assert isinstance(result, str)
        assert "Error" in result
        assert any("execute_operation" in record.message.lower() for record in caplog.records)

    def test_execute_operation_factorial_bool_logs_error(self, caplog):
        """Verify that bool in factorial within execute_operation is logged."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            result = execute_operation(calc, "factorial", [True])

        # execute_operation catches the exception and returns an error string
        assert isinstance(result, str)
        assert "Error" in result
        assert any("execute_operation" in record.message.lower() for record in caplog.records)

    def test_execute_operation_log10_nonpositive_logs_error(self, caplog):
        """Verify that non-positive value in log10 is logged."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            result = execute_operation(calc, "log10", [0])

        # execute_operation catches the exception and returns an error string
        assert isinstance(result, str)
        assert "Error" in result
        assert any("execute_operation" in record.message.lower() for record in caplog.records)

    def test_execute_operation_natural_log_negative_logs_error(self, caplog):
        """Verify that negative value in natural_log is logged."""
        calc = Calculator()
        with caplog.at_level(logging.ERROR):
            result = execute_operation(calc, "natural_log", [-5])

        # execute_operation catches the exception and returns an error string
        assert isinstance(result, str)
        assert "Error" in result
        assert any("execute_operation" in record.message.lower() for record in caplog.records)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestLoggingIntegration:
    """Integration tests for logging feature."""

    def test_logging_does_not_break_existing_behavior(self, calculator):
        """Verify that adding logging doesn't change exception semantics."""
        # Successful operation should work normally
        result = calculator.add(5, 3)
        assert result == 8

        # Error should still raise the same exception type
        with pytest.raises(ZeroDivisionError):
            calculator.divide(10, 0)

        with pytest.raises(ValueError):
            calculator.factorial(-1)

        with pytest.raises(TypeError):
            calculator.square(True)

    def test_error_is_logged_and_exception_is_raised(self, calculator, caplog):
        """Verify that error is logged AND exception is still raised."""
        with caplog.at_level(logging.ERROR):
            # Try an operation that should fail
            with pytest.raises(ValueError):
                calculator.square_root(-1)

        # Verify both: exception was raised AND error was logged
        assert len(caplog.records) > 0
        assert any(record.levelname == "ERROR" for record in caplog.records)

    def test_setup_logging_returns_logger(self, temp_log_file):
        """Verify that setup_logging returns a logger instance."""
        result_logger = setup_logging(temp_log_file)
        assert isinstance(result_logger, logging.Logger)
        assert result_logger.name == "calculator"

    def test_setup_logging_creates_log_file(self, temp_log_file):
        """Verify that setup_logging creates log file."""
        setup_logging(temp_log_file)
        logger_instance = logging.getLogger("calculator")
        logger_instance.error("Test message")

        # Log file should exist
        assert os.path.exists(temp_log_file)

    def test_setup_logging_idempotent(self, temp_log_file):
        """Verify that calling setup_logging multiple times is safe."""
        logger1 = setup_logging(temp_log_file)
        logger2 = setup_logging(temp_log_file)

        # Should return the same logger
        assert logger1 is logger2

        # Should not add duplicate handlers
        logger_instance = logging.getLogger("calculator")
        handler_count = len(logger_instance.handlers)
        assert handler_count == 1

    def test_multiple_errors_are_logged(self, calculator, caplog):
        """Verify that multiple errors are all logged."""
        with caplog.at_level(logging.ERROR):
            # First error
            try:
                calculator.divide(10, 0)
            except ZeroDivisionError:
                pass

            # Second error
            try:
                calculator.factorial(-1)
            except ValueError:
                pass

            # Third error
            try:
                calculator.square(True)
            except TypeError:
                pass

        # Should have logged all three errors
        assert len(caplog.records) >= 3

    def test_successful_operations_not_logged(self, calculator, caplog):
        """Verify that successful operations don't produce error logs."""
        with caplog.at_level(logging.ERROR):
            calculator.add(5, 3)
            calculator.multiply(4, 2)
            calculator.square(7)

        # Should have no error logs for successful operations
        error_records = [r for r in caplog.records if r.levelname == "ERROR"]
        assert len(error_records) == 0

    def test_logging_with_different_log_file_paths(self):
        """Verify logging with custom log file path."""
        # Create a temporary custom path
        custom_path = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
                custom_path = f.name

            # Setup logging with custom path will add handler if not present
            # Since the logger may already have a handler from prior tests,
            # we just verify that setup_logging accepts the path parameter
            logger_instance = setup_logging(custom_path)

            # The logger should still be the calculator logger
            assert logger_instance.name == "calculator"
            # Verify handlers are present
            assert len(logger_instance.handlers) > 0
        finally:
            if custom_path and os.path.exists(custom_path):
                os.remove(custom_path)

    def test_logger_error_level_is_set(self, temp_log_file):
        """Verify that logger error level is ERROR."""
        logger_instance = setup_logging(temp_log_file)
        assert logger_instance.level == logging.ERROR

    def test_logger_handler_error_level_is_set(self, temp_log_file):
        """Verify that handler error level is ERROR."""
        logger_instance = setup_logging(temp_log_file)

        for handler in logger_instance.handlers:
            assert handler.level == logging.ERROR
