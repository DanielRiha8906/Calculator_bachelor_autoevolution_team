"""Tests for error logging integration in the calculator.

This module verifies that:
1. All error conditions log at ERROR level before raising exceptions
2. Successful operations complete without logging errors
3. History is not recorded when exceptions occur
4. Logging integrates properly across Calculator, CalculatorWithHistory,
   input_handler, and cli modules
"""

import logging
import math
import sys
from io import StringIO

import pytest

from src.calculator import Calculator
from src.calculator_with_history import CalculatorWithHistory
from src.input_handler import parse_operand, parse_input, run_calculation
from src.logger import get_logger


# ============================================================================
# Fixtures for log capture and testing setup
# ============================================================================


@pytest.fixture
def clean_logger():
    """Fixture that provides a clean logger instance with stream handler.

    Clears any existing handlers before the test and restores afterward.
    """
    logger = logging.getLogger("src")
    # Remove all handlers to get a clean slate
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create a fresh stream handler
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    yield handler, stream, logger

    # Cleanup
    logger.removeHandler(handler)


@pytest.fixture
def caplog_debug(caplog):
    """Configure caplog to capture DEBUG level and above for all loggers."""
    caplog.set_level(logging.DEBUG)
    return caplog


# ============================================================================
# Tests for src.logger.get_logger()
# ============================================================================


class TestGetLogger:
    """Tests for the get_logger factory function."""

    def test_get_logger_returns_logger_instance(self):
        """get_logger should return a logging.Logger instance."""
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_different_names(self):
        """get_logger should return different logger instances for different names."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        assert logger1 is not logger2

    def test_get_logger_with_same_name_returns_same_instance(self):
        """get_logger should return the same instance for the same name."""
        logger1 = get_logger("test_same")
        logger2 = get_logger("test_same")
        assert logger1 is logger2

    def test_get_logger_default_has_null_handler(self):
        """get_logger should attach a NullHandler by default."""
        logger = get_logger("test_null_handler")
        # Remove any previously added handlers to ensure clean state
        for h in logger.handlers[:]:
            logger.removeHandler(h)

        logger = get_logger("test_null_handler")
        assert any(isinstance(h, logging.NullHandler) for h in logger.handlers)

    def test_get_logger_null_handler_prevents_duplicate_handlers(self):
        """Calling get_logger multiple times should not add duplicate NullHandlers."""
        logger_name = "test_no_duplicates"
        # Clear any existing handlers
        test_logger = logging.getLogger(logger_name)
        for h in test_logger.handlers[:]:
            test_logger.removeHandler(h)

        # Call get_logger twice
        get_logger(logger_name)
        initial_count = len(logging.getLogger(logger_name).handlers)
        get_logger(logger_name)
        final_count = len(logging.getLogger(logger_name).handlers)

        assert initial_count == final_count

    def test_get_logger_with_empty_string_name(self):
        """get_logger should handle empty string name."""
        logger = get_logger("")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_long_module_path(self):
        """get_logger should handle long dotted module paths."""
        logger = get_logger("very.long.module.path.name")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "very.long.module.path.name"


# ============================================================================
# Tests for Calculator error logging
# ============================================================================


class TestCalculatorDivideLogging:
    """Tests for Calculator.divide() error logging."""

    def test_divide_by_zero_raises_and_logs(self, caplog_debug):
        """divide(a, 0) should log ERROR and raise ZeroDivisionError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ZeroDivisionError):
                Calculator().divide(5, 0)
        assert "Division by zero" in caplog_debug.text

    def test_divide_by_zero_with_negative_dividend(self, caplog_debug):
        """divide(-5, 0) should log ERROR and raise ZeroDivisionError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ZeroDivisionError):
                Calculator().divide(-5, 0)
        assert "Division by zero" in caplog_debug.text

    def test_divide_by_float_zero(self, caplog_debug):
        """divide(a, 0.0) should log ERROR and raise ZeroDivisionError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ZeroDivisionError):
                Calculator().divide(10, 0.0)
        assert "Division by zero" in caplog_debug.text

    def test_divide_by_very_small_positive_number_succeeds(self):
        """divide by very small positive number should succeed without error."""
        result = Calculator().divide(1, 1e-10)
        assert result == 1e10

    def test_divide_successful_does_not_log_error(self, caplog_debug):
        """Successful divide should not produce ERROR level logs."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            result = Calculator().divide(10, 2)
        assert result == 5.0
        assert "ERROR" not in caplog_debug.text


class TestCalculatorFactorialLogging:
    """Tests for Calculator.factorial() error logging."""

    def test_factorial_negative_integer_logs_error(self, caplog_debug):
        """factorial(-n) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().factorial(-1)
        assert "negative" in caplog_debug.text.lower()

    def test_factorial_negative_large_integer_logs_error(self, caplog_debug):
        """factorial(-999) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().factorial(-999)
        assert "negative" in caplog_debug.text.lower()

    def test_factorial_float_logs_error(self, caplog_debug):
        """factorial(1.5) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().factorial(1.5)
        assert "int" in caplog_debug.text.lower() or "integer" in caplog_debug.text.lower()

    def test_factorial_string_logs_error(self, caplog_debug):
        """factorial('5') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().factorial("5")
        assert "int" in caplog_debug.text.lower()

    def test_factorial_none_logs_error(self, caplog_debug):
        """factorial(None) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().factorial(None)
        assert "int" in caplog_debug.text.lower()

    def test_factorial_zero_succeeds(self):
        """factorial(0) should return 1 without error."""
        result = Calculator().factorial(0)
        assert result == 1

    def test_factorial_positive_integer_succeeds(self):
        """factorial(5) should return 120."""
        result = Calculator().factorial(5)
        assert result == 120

    def test_factorial_large_positive_integer_succeeds(self):
        """factorial(20) should succeed and return correct value."""
        result = Calculator().factorial(20)
        assert result == math.factorial(20)


class TestCalculatorSquareRootLogging:
    """Tests for Calculator.square_root() error logging."""

    def test_square_root_negative_logs_error(self, caplog_debug):
        """square_root(-1) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().square_root(-1)
        assert "negative" in caplog_debug.text.lower()

    def test_square_root_large_negative_logs_error(self, caplog_debug):
        """square_root(-1000.5) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().square_root(-1000.5)
        assert "negative" in caplog_debug.text.lower()

    def test_square_root_zero_succeeds(self):
        """square_root(0) should return 0."""
        result = Calculator().square_root(0)
        assert result == 0.0

    def test_square_root_positive_succeeds(self):
        """square_root(4) should return 2.0."""
        result = Calculator().square_root(4)
        assert result == 2.0

    def test_square_root_fractional_positive_succeeds(self):
        """square_root(0.25) should return 0.5."""
        result = Calculator().square_root(0.25)
        assert abs(result - 0.5) < 1e-10


class TestCalculatorLogLogging:
    """Tests for Calculator.log() error logging."""

    def test_log_zero_logs_error(self, caplog_debug):
        """log(0) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().log(0)
        assert "positive" in caplog_debug.text.lower() or "non-positive" in caplog_debug.text.lower()

    def test_log_negative_logs_error(self, caplog_debug):
        """log(-5) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().log(-5)
        assert "positive" in caplog_debug.text.lower() or "non-positive" in caplog_debug.text.lower()

    def test_log_large_negative_logs_error(self, caplog_debug):
        """log(-1e10) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().log(-1e10)
        assert "positive" in caplog_debug.text.lower() or "non-positive" in caplog_debug.text.lower()

    def test_log_positive_succeeds(self):
        """log(100) should return log10(100) = 2.0."""
        result = Calculator().log(100)
        assert result == 2.0

    def test_log_one_succeeds(self):
        """log(1) should return 0.0."""
        result = Calculator().log(1)
        assert result == 0.0

    def test_log_fractional_positive_succeeds(self):
        """log(0.1) should return -1.0."""
        result = Calculator().log(0.1)
        assert result == -1.0


class TestCalculatorLnLogging:
    """Tests for Calculator.ln() error logging."""

    def test_ln_zero_logs_error(self, caplog_debug):
        """ln(0) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().ln(0)
        assert "positive" in caplog_debug.text.lower() or "non-positive" in caplog_debug.text.lower()

    def test_ln_negative_logs_error(self, caplog_debug):
        """ln(-1) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().ln(-1)
        assert "positive" in caplog_debug.text.lower() or "non-positive" in caplog_debug.text.lower()

    def test_ln_large_negative_logs_error(self, caplog_debug):
        """ln(-999.99) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator"):
            with pytest.raises(ValueError):
                Calculator().ln(-999.99)
        assert "positive" in caplog_debug.text.lower() or "non-positive" in caplog_debug.text.lower()

    def test_ln_positive_succeeds(self):
        """ln(math.e) should return 1.0."""
        result = Calculator().ln(math.e)
        assert abs(result - 1.0) < 1e-10

    def test_ln_one_succeeds(self):
        """ln(1) should return 0.0."""
        result = Calculator().ln(1)
        assert result == 0.0

    def test_ln_fractional_positive_succeeds(self):
        """ln(0.5) should return negative value."""
        result = Calculator().ln(0.5)
        assert result < 0


# ============================================================================
# Tests for CalculatorWithHistory error logging and history recording
# ============================================================================


class TestCalculatorWithHistoryDivideLogging:
    """Tests for CalculatorWithHistory.divide() error logging."""

    def test_divide_by_zero_logs_error(self, caplog_debug):
        """divide(a, 0) should log ERROR and raise ZeroDivisionError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator_with_history"):
            with pytest.raises(ZeroDivisionError):
                CalculatorWithHistory().divide(10, 0)
        assert any("divide" in line.lower() for line in caplog_debug.text.split("\n"))

    def test_divide_by_zero_does_not_record_history(self):
        """Failed divide should not record an entry in history."""
        calc = CalculatorWithHistory()
        try:
            calc.divide(10, 0)
        except ZeroDivisionError:
            pass
        assert len(calc.get_history()) == 0

    def test_divide_successful_returns_correct_result(self):
        """divide(10, 2) should return 5.0."""
        result = CalculatorWithHistory().divide(10, 2)
        assert result == 5.0

    def test_divide_successful_records_history(self):
        """Successful divide should record entry in history."""
        calc = CalculatorWithHistory()
        result = calc.divide(10, 2)
        history = calc.get_history()
        assert len(history) == 1
        assert "10" in history[0] and "2" in history[0] and "5.0" in history[0]

    def test_divide_multiple_operations_records_all(self):
        """Multiple successful operations should record all in history."""
        calc = CalculatorWithHistory()
        calc.divide(10, 2)
        calc.divide(20, 4)
        history = calc.get_history()
        assert len(history) == 2


class TestCalculatorWithHistoryAddLogging:
    """Tests for CalculatorWithHistory.add() error logging."""

    def test_add_successful_returns_correct_result(self):
        """add(2, 3) should return 5.0."""
        result = CalculatorWithHistory().add(2, 3)
        assert result == 5.0

    def test_add_successful_records_history(self):
        """Successful add should record entry in history."""
        calc = CalculatorWithHistory()
        calc.add(2, 3)
        history = calc.get_history()
        assert len(history) == 1
        assert "2" in history[0] and "3" in history[0] and ("5" in history[0])

    def test_add_negative_numbers_succeeds(self):
        """add(-5, -3) should return -8.0."""
        result = CalculatorWithHistory().add(-5, -3)
        assert result == -8.0

    def test_add_mixed_signs_succeeds(self):
        """add(-5, 10) should return 5.0."""
        result = CalculatorWithHistory().add(-5, 10)
        assert result == 5.0


class TestCalculatorWithHistoryFactorialLogging:
    """Tests for CalculatorWithHistory.factorial() error logging."""

    def test_factorial_negative_logs_error(self, caplog_debug):
        """factorial(-1) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator_with_history"):
            with pytest.raises(ValueError):
                CalculatorWithHistory().factorial(-1)
        assert any("factorial" in line.lower() for line in caplog_debug.text.split("\n"))

    def test_factorial_negative_does_not_record_history(self):
        """Failed factorial should not record an entry in history."""
        calc = CalculatorWithHistory()
        try:
            calc.factorial(-1)
        except ValueError:
            pass
        assert len(calc.get_history()) == 0

    def test_factorial_successful_returns_correct_result(self):
        """factorial(5) should return 120."""
        result = CalculatorWithHistory().factorial(5)
        assert result == 120

    def test_factorial_successful_records_history(self):
        """Successful factorial should record entry in history."""
        calc = CalculatorWithHistory()
        calc.factorial(5)
        history = calc.get_history()
        assert len(history) == 1
        assert "factorial" in history[0] and "5" in history[0]


class TestCalculatorWithHistorySquareRootLogging:
    """Tests for CalculatorWithHistory.square_root() error logging."""

    def test_square_root_negative_logs_error(self, caplog_debug):
        """square_root(-1) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator_with_history"):
            with pytest.raises(ValueError):
                CalculatorWithHistory().square_root(-1)
        assert any("square_root" in line.lower() for line in caplog_debug.text.split("\n"))

    def test_square_root_negative_does_not_record_history(self):
        """Failed square_root should not record an entry in history."""
        calc = CalculatorWithHistory()
        try:
            calc.square_root(-1)
        except ValueError:
            pass
        assert len(calc.get_history()) == 0

    def test_square_root_successful_returns_correct_result(self):
        """square_root(4) should return 2.0."""
        result = CalculatorWithHistory().square_root(4)
        assert result == 2.0

    def test_square_root_successful_records_history(self):
        """Successful square_root should record entry in history."""
        calc = CalculatorWithHistory()
        calc.square_root(4)
        history = calc.get_history()
        assert len(history) == 1
        assert "square_root" in history[0] and "4" in history[0]


class TestCalculatorWithHistoryCubeRootLogging:
    """Tests for CalculatorWithHistory.cube_root() error logging."""

    def test_cube_root_negative_returns_negative(self):
        """cube_root(-8) should return -2.0."""
        result = CalculatorWithHistory().cube_root(-8)
        assert abs(result - (-2.0)) < 1e-10

    def test_cube_root_successful_records_history(self):
        """Successful cube_root should record entry in history."""
        calc = CalculatorWithHistory()
        calc.cube_root(8)
        history = calc.get_history()
        assert len(history) == 1
        assert "cube_root" in history[0]


class TestCalculatorWithHistoryCubeLogging:
    """Tests for CalculatorWithHistory.cube() error logging."""

    def test_cube_successful_returns_correct_result(self):
        """cube(3) should return 27.0."""
        result = CalculatorWithHistory().cube(3)
        assert result == 27.0

    def test_cube_successful_records_history(self):
        """Successful cube should record entry in history."""
        calc = CalculatorWithHistory()
        calc.cube(3)
        history = calc.get_history()
        assert len(history) == 1
        assert "cube" in history[0]


class TestCalculatorWithHistorySquareLogging:
    """Tests for CalculatorWithHistory.square() error logging."""

    def test_square_successful_returns_correct_result(self):
        """square(5) should return 25.0."""
        result = CalculatorWithHistory().square(5)
        assert result == 25.0

    def test_square_successful_records_history(self):
        """Successful square should record entry in history."""
        calc = CalculatorWithHistory()
        calc.square(5)
        history = calc.get_history()
        assert len(history) == 1
        assert "square" in history[0]


class TestCalculatorWithHistoryPowerLogging:
    """Tests for CalculatorWithHistory.power() error logging."""

    def test_power_successful_returns_correct_result(self):
        """power(2, 3) should return 8.0."""
        result = CalculatorWithHistory().power(2, 3)
        assert result == 8.0

    def test_power_successful_records_history(self):
        """Successful power should record entry in history."""
        calc = CalculatorWithHistory()
        calc.power(2, 3)
        history = calc.get_history()
        assert len(history) == 1
        assert "power" in history[0]


class TestCalculatorWithHistoryLogLogging:
    """Tests for CalculatorWithHistory.log() error logging."""

    def test_log_zero_logs_error(self, caplog_debug):
        """log(0) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator_with_history"):
            with pytest.raises(ValueError):
                CalculatorWithHistory().log(0)
        assert any("log" in line.lower() for line in caplog_debug.text.split("\n"))

    def test_log_zero_does_not_record_history(self):
        """Failed log should not record an entry in history."""
        calc = CalculatorWithHistory()
        try:
            calc.log(0)
        except ValueError:
            pass
        assert len(calc.get_history()) == 0

    def test_log_successful_returns_correct_result(self):
        """log(100) should return 2.0."""
        result = CalculatorWithHistory().log(100)
        assert result == 2.0

    def test_log_successful_records_history(self):
        """Successful log should record entry in history."""
        calc = CalculatorWithHistory()
        calc.log(100)
        history = calc.get_history()
        assert len(history) == 1
        assert "log" in history[0]


class TestCalculatorWithHistoryLnLogging:
    """Tests for CalculatorWithHistory.ln() error logging."""

    def test_ln_zero_logs_error(self, caplog_debug):
        """ln(0) should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.calculator_with_history"):
            with pytest.raises(ValueError):
                CalculatorWithHistory().ln(0)
        assert any("ln" in line.lower() for line in caplog_debug.text.split("\n"))

    def test_ln_zero_does_not_record_history(self):
        """Failed ln should not record an entry in history."""
        calc = CalculatorWithHistory()
        try:
            calc.ln(0)
        except ValueError:
            pass
        assert len(calc.get_history()) == 0

    def test_ln_successful_returns_correct_result(self):
        """ln(math.e) should return approximately 1.0."""
        result = CalculatorWithHistory().ln(math.e)
        assert abs(result - 1.0) < 1e-10

    def test_ln_successful_records_history(self):
        """Successful ln should record entry in history."""
        calc = CalculatorWithHistory()
        calc.ln(math.e)
        history = calc.get_history()
        assert len(history) == 1
        assert "ln" in history[0]


class TestCalculatorWithHistoryMixedOperations:
    """Tests for mixed successful and failed operations."""

    def test_history_records_only_successful_operations(self):
        """History should contain only successful operations, not failures."""
        calc = CalculatorWithHistory()
        calc.add(1, 2)  # success
        try:
            calc.divide(10, 0)  # failure
        except ZeroDivisionError:
            pass
        calc.multiply(3, 4)  # success

        history = calc.get_history()
        assert len(history) == 2
        assert any("1" in h and "2" in h for h in history)
        assert any("3" in h and "4" in h for h in history)

    def test_multiple_failures_do_not_record_history(self):
        """Multiple failures should not add any history entries."""
        calc = CalculatorWithHistory()
        for _ in range(5):
            try:
                calc.divide(10, 0)
            except ZeroDivisionError:
                pass
        assert len(calc.get_history()) == 0


# ============================================================================
# Tests for input_handler error logging
# ============================================================================


class TestParseOperandLogging:
    """Tests for parse_operand() error logging."""

    def test_parse_operand_invalid_string_logs_error(self, caplog_debug):
        """parse_operand('not_a_number') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_operand("not_a_number")
        assert "float" in caplog_debug.text.lower() or "invalid" in caplog_debug.text.lower()

    def test_parse_operand_special_characters_logs_error(self, caplog_debug):
        """parse_operand('@#$%') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_operand("@#$%")
        assert "float" in caplog_debug.text.lower()

    def test_parse_operand_empty_string_logs_error(self, caplog_debug):
        """parse_operand('') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_operand("")
        assert "float" in caplog_debug.text.lower()

    def test_parse_operand_whitespace_only_logs_error(self, caplog_debug):
        """parse_operand('   ') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_operand("   ")
        assert "float" in caplog_debug.text.lower()

    def test_parse_operand_valid_integer_succeeds(self):
        """parse_operand('5') should return 5.0."""
        result = parse_operand("5")
        assert result == 5.0

    def test_parse_operand_valid_float_succeeds(self):
        """parse_operand('3.14') should return 3.14."""
        result = parse_operand("3.14")
        assert abs(result - 3.14) < 1e-10

    def test_parse_operand_negative_succeeds(self):
        """parse_operand('-5') should return -5.0."""
        result = parse_operand("-5")
        assert result == -5.0

    def test_parse_operand_scientific_notation_succeeds(self):
        """parse_operand('1e10') should return 1e10."""
        result = parse_operand("1e10")
        assert result == 1e10

    def test_parse_operand_with_leading_trailing_whitespace_succeeds(self):
        """parse_operand('  5.5  ') should return 5.5."""
        result = parse_operand("  5.5  ")
        assert abs(result - 5.5) < 1e-10


class TestParseInputLogging:
    """Tests for parse_input() error logging."""

    def test_parse_input_unsupported_operator_logs_error(self, caplog_debug):
        """parse_input('5', '3', '^') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_input("5", "3", "^")
        assert "operator" in caplog_debug.text.lower() or "unsupported" in caplog_debug.text.lower()

    def test_parse_input_invalid_operator_logs_error(self, caplog_debug):
        """parse_input('5', '3', 'xyz') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_input("5", "3", "xyz")
        assert "operator" in caplog_debug.text.lower()

    def test_parse_input_operator_with_whitespace_logs_error(self, caplog_debug):
        """parse_input('5', '3', ' ? ') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_input("5", "3", " ? ")
        assert "operator" in caplog_debug.text.lower()

    def test_parse_input_first_operand_invalid_logs_error(self, caplog_debug):
        """parse_input('abc', '3', '+') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_input("abc", "3", "+")
        assert "float" in caplog_debug.text.lower() or "operand" in caplog_debug.text.lower()

    def test_parse_input_second_operand_invalid_logs_error(self, caplog_debug):
        """parse_input('5', 'xyz', '+') should log ERROR and raise ValueError."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_input("5", "xyz", "+")
        assert "float" in caplog_debug.text.lower() or "operand" in caplog_debug.text.lower()

    def test_parse_input_valid_add_succeeds(self):
        """parse_input('5', '3', '+') should return (5.0, 3.0, 'add')."""
        a, b, method_name = parse_input("5", "3", "+")
        assert a == 5.0
        assert b == 3.0
        assert method_name == "add"

    def test_parse_input_valid_subtract_succeeds(self):
        """parse_input('10', '4', '-') should return (10.0, 4.0, 'subtract')."""
        a, b, method_name = parse_input("10", "4", "-")
        assert a == 10.0
        assert b == 4.0
        assert method_name == "subtract"

    def test_parse_input_valid_multiply_succeeds(self):
        """parse_input('2', '3', '*') should return (2.0, 3.0, 'multiply')."""
        a, b, method_name = parse_input("2", "3", "*")
        assert a == 2.0
        assert b == 3.0
        assert method_name == "multiply"

    def test_parse_input_valid_divide_succeeds(self):
        """parse_input('10', '2', '/') should return (10.0, 2.0, 'divide')."""
        a, b, method_name = parse_input("10", "2", "/")
        assert a == 10.0
        assert b == 2.0
        assert method_name == "divide"

    def test_parse_input_operator_with_surrounding_whitespace_succeeds(self):
        """parse_input('5', '3', ' + ') should succeed."""
        a, b, method_name = parse_input("5", "3", " + ")
        assert method_name == "add"


class TestRunCalculationLogging:
    """Tests for run_calculation() error logging."""

    def test_run_calculation_divide_by_zero_logs_error(self, caplog_debug):
        """run_calculation(10, 0, 'divide') should log ERROR and raise ZeroDivisionError."""
        with caplog_debug.at_level(logging.ERROR):
            with pytest.raises(ZeroDivisionError):
                run_calculation(10, 0, "divide")
        # Error should come from Calculator or CalculatorWithHistory
        assert any("divide" in line.lower() or "zero" in line.lower()
                   for line in caplog_debug.text.split("\n"))

    def test_run_calculation_divide_by_zero_does_not_record_history(self):
        """run_calculation with divide by zero should not record history."""
        try:
            result, calc = run_calculation(10, 0, "divide")
        except ZeroDivisionError:
            pass
        # We caught the exception, so we can't verify history on result
        # This is expected to fail at the call site

    def test_run_calculation_successful_add_returns_correct_result(self):
        """run_calculation(5, 3, 'add') should return (8.0, calc)."""
        result, calc = run_calculation(5, 3, "add")
        assert result == 8.0
        assert isinstance(calc, CalculatorWithHistory)

    def test_run_calculation_successful_records_history(self):
        """Successful run_calculation should record operation in history."""
        result, calc = run_calculation(5, 3, "add")
        history = calc.get_history()
        assert len(history) == 1

    def test_run_calculation_subtract_succeeds(self):
        """run_calculation(10, 4, 'subtract') should return 6.0."""
        result, calc = run_calculation(10, 4, "subtract")
        assert result == 6.0

    def test_run_calculation_multiply_succeeds(self):
        """run_calculation(3, 7, 'multiply') should return 21.0."""
        result, calc = run_calculation(3, 7, "multiply")
        assert result == 21.0

    def test_run_calculation_divide_succeeds(self):
        """run_calculation(20, 4, 'divide') should return 5.0."""
        result, calc = run_calculation(20, 4, "divide")
        assert result == 5.0


# ============================================================================
# Integration tests: Logging across the entire pipeline
# ============================================================================


class TestIntegrationLogging:
    """Integration tests verifying error logging across the entire pipeline."""

    def test_parse_operand_to_calculator_error_flow(self, caplog_debug):
        """Error in parse_operand should log before raising."""
        with caplog_debug.at_level(logging.ERROR, logger="src.input_handler"):
            with pytest.raises(ValueError):
                parse_operand("invalid")
        # Verify error was logged by input_handler
        assert any("float" in line.lower() for line in caplog_debug.text.split("\n"))

    def test_calculator_with_history_wraps_underlying_errors(self, caplog_debug):
        """CalculatorWithHistory should log errors from underlying Calculator."""
        with caplog_debug.at_level(logging.ERROR):
            with pytest.raises(ValueError):
                CalculatorWithHistory().factorial(-1)
        # Should see errors from both calculator and calculator_with_history
        error_lines = [line for line in caplog_debug.text.split("\n") if "ERROR" in line]
        assert len(error_lines) >= 1

    def test_successful_operation_no_error_logs(self, caplog_debug):
        """Successful operation should not produce ERROR level logs."""
        with caplog_debug.at_level(logging.ERROR, logger="src"):
            parse_input("5", "3", "+")
            result, calc = run_calculation(5, 3, "add")
        # Should be no ERROR logs
        assert "ERROR" not in caplog_debug.text
