"""Comprehensive tests for scientific wrapper methods in Calculator class.

Tests cover:
- Each scientific method (sin, cos, tan, exp, log, sqrt) returns correct value
- Each method records to history with correct operation_name
- ValueError propagates from engine for domain violations
"""

import pytest
import math
from src.logic import Calculator


@pytest.fixture
def calculator():
    """Provides a fresh Calculator instance for each test."""
    return Calculator()


# ============================================================================
# SINE OPERATION TESTS
# ============================================================================

class TestCalculatorSin:
    """Test suite for Calculator.sin wrapper method."""

    def test_sin_zero_returns_correct_value(self, calculator):
        """Test sin(0) returns 0."""
        assert calculator.sin(0) == pytest.approx(0.0)

    def test_sin_pi_over_2_returns_correct_value(self, calculator):
        """Test sin(pi/2) returns 1."""
        assert calculator.sin(math.pi / 2) == pytest.approx(1.0)

    def test_sin_pi_over_4_returns_correct_value(self, calculator):
        """Test sin(pi/4) returns sqrt(2)/2."""
        assert calculator.sin(math.pi / 4) == pytest.approx(math.sqrt(2) / 2)

    def test_sin_recorded_in_history(self, calculator):
        """Test that sin operation is recorded in history."""
        calculator.sin(1.0)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "sin"
        assert record.operands == [1.0]
        assert record.result == pytest.approx(math.sin(1.0))

    def test_sin_float_recorded_in_history(self, calculator):
        """Test that sin with float is recorded in history."""
        x = math.pi / 6
        calculator.sin(x)
        history = calculator.get_history()

        record = history[0]
        assert record.operation_name == "sin"
        assert record.operands == [x]

    def test_sin_bool_raises_typeerror(self, calculator):
        """Test that sin(bool) raises TypeError."""
        with pytest.raises(TypeError):
            calculator.sin(True)

    def test_sin_bool_does_not_record_history(self, calculator):
        """Test that sin with bool does not record to history."""
        try:
            calculator.sin(True)
        except TypeError:
            pass
        assert len(calculator.get_history()) == 0

    def test_sin_negative_angle_recorded(self, calculator):
        """Test that sin with negative angle is recorded."""
        calculator.sin(-math.pi / 2)
        history = calculator.get_history()

        assert len(history) == 1
        assert history[0].operation_name == "sin"


# ============================================================================
# COSINE OPERATION TESTS
# ============================================================================

class TestCalculatorCos:
    """Test suite for Calculator.cos wrapper method."""

    def test_cos_zero_returns_correct_value(self, calculator):
        """Test cos(0) returns 1."""
        assert calculator.cos(0) == pytest.approx(1.0)

    def test_cos_pi_returns_correct_value(self, calculator):
        """Test cos(pi) returns -1."""
        assert calculator.cos(math.pi) == pytest.approx(-1.0)

    def test_cos_pi_over_4_returns_correct_value(self, calculator):
        """Test cos(pi/4) returns sqrt(2)/2."""
        assert calculator.cos(math.pi / 4) == pytest.approx(math.sqrt(2) / 2)

    def test_cos_recorded_in_history(self, calculator):
        """Test that cos operation is recorded in history."""
        calculator.cos(1.0)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "cos"
        assert record.operands == [1.0]
        assert record.result == pytest.approx(math.cos(1.0))

    def test_cos_bool_raises_typeerror(self, calculator):
        """Test that cos(bool) raises TypeError."""
        with pytest.raises(TypeError):
            calculator.cos(False)

    def test_cos_bool_does_not_record_history(self, calculator):
        """Test that cos with bool does not record to history."""
        try:
            calculator.cos(True)
        except TypeError:
            pass
        assert len(calculator.get_history()) == 0


# ============================================================================
# TANGENT OPERATION TESTS
# ============================================================================

class TestCalculatorTan:
    """Test suite for Calculator.tan wrapper method."""

    def test_tan_zero_returns_correct_value(self, calculator):
        """Test tan(0) returns 0."""
        assert calculator.tan(0) == pytest.approx(0.0)

    def test_tan_pi_over_4_returns_correct_value(self, calculator):
        """Test tan(pi/4) returns 1."""
        assert calculator.tan(math.pi / 4) == pytest.approx(1.0)

    def test_tan_recorded_in_history(self, calculator):
        """Test that tan operation is recorded in history."""
        calculator.tan(0.5)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "tan"
        assert record.operands == [0.5]
        assert record.result == pytest.approx(math.tan(0.5))

    def test_tan_pi_over_2_raises_valueerror(self, calculator):
        """Test that tan(pi/2) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.tan(math.pi / 2)

    def test_tan_undefined_does_not_record_history(self, calculator):
        """Test that tan at undefined point does not record to history."""
        try:
            calculator.tan(math.pi / 2)
        except ValueError:
            pass
        assert len(calculator.get_history()) == 0

    def test_tan_bool_raises_typeerror(self, calculator):
        """Test that tan(bool) raises TypeError."""
        with pytest.raises(TypeError):
            calculator.tan(True)


# ============================================================================
# EXPONENTIAL OPERATION TESTS
# ============================================================================

class TestCalculatorExp:
    """Test suite for Calculator.exp wrapper method."""

    def test_exp_zero_returns_correct_value(self, calculator):
        """Test exp(0) returns 1."""
        assert calculator.exp(0) == pytest.approx(1.0)

    def test_exp_one_returns_correct_value(self, calculator):
        """Test exp(1) returns e."""
        assert calculator.exp(1) == pytest.approx(math.e)

    def test_exp_negative_one_returns_correct_value(self, calculator):
        """Test exp(-1) returns 1/e."""
        assert calculator.exp(-1) == pytest.approx(1 / math.e)

    def test_exp_recorded_in_history(self, calculator):
        """Test that exp operation is recorded in history."""
        calculator.exp(0)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "exp"
        assert record.operands == [0]
        assert record.result == pytest.approx(1.0)

    def test_exp_with_float_recorded(self, calculator):
        """Test that exp with float is recorded."""
        calculator.exp(1.5)
        history = calculator.get_history()

        assert len(history) == 1
        assert history[0].operation_name == "exp"
        assert history[0].result == pytest.approx(math.exp(1.5))

    def test_exp_bool_raises_typeerror(self, calculator):
        """Test that exp(bool) raises TypeError."""
        with pytest.raises(TypeError):
            calculator.exp(True)

    def test_exp_bool_does_not_record_history(self, calculator):
        """Test that exp with bool does not record to history."""
        try:
            calculator.exp(False)
        except TypeError:
            pass
        assert len(calculator.get_history()) == 0


# ============================================================================
# NATURAL LOGARITHM OPERATION TESTS
# ============================================================================

class TestCalculatorLog:
    """Test suite for Calculator.log wrapper method."""

    def test_log_one_returns_correct_value(self, calculator):
        """Test log(1) returns 0."""
        assert calculator.log(1) == pytest.approx(0.0)

    def test_log_e_returns_correct_value(self, calculator):
        """Test log(e) returns 1."""
        assert calculator.log(math.e) == pytest.approx(1.0)

    def test_log_e_squared_returns_correct_value(self, calculator):
        """Test log(e^2) returns 2."""
        assert calculator.log(math.e ** 2) == pytest.approx(2.0)

    def test_log_recorded_in_history(self, calculator):
        """Test that log operation is recorded in history."""
        calculator.log(math.e)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "log"
        assert record.operands == [math.e]
        assert record.result == pytest.approx(1.0)

    def test_log_zero_raises_valueerror(self, calculator):
        """Test that log(0) raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log(0)

    def test_log_negative_raises_valueerror(self, calculator):
        """Test that log of negative raises ValueError."""
        with pytest.raises(ValueError):
            calculator.log(-1)

    def test_log_invalid_does_not_record_history(self, calculator):
        """Test that log with invalid input does not record to history."""
        try:
            calculator.log(-5)
        except ValueError:
            pass
        assert len(calculator.get_history()) == 0

    def test_log_bool_raises_typeerror(self, calculator):
        """Test that log(bool) raises TypeError."""
        with pytest.raises(TypeError):
            calculator.log(True)


# ============================================================================
# SQUARE ROOT OPERATION TESTS
# ============================================================================

class TestCalculatorSqrt:
    """Test suite for Calculator.sqrt wrapper method."""

    def test_sqrt_zero_returns_correct_value(self, calculator):
        """Test sqrt(0) returns 0."""
        assert calculator.sqrt(0) == pytest.approx(0.0)

    def test_sqrt_one_returns_correct_value(self, calculator):
        """Test sqrt(1) returns 1."""
        assert calculator.sqrt(1) == pytest.approx(1.0)

    def test_sqrt_four_returns_correct_value(self, calculator):
        """Test sqrt(4) returns 2."""
        assert calculator.sqrt(4) == pytest.approx(2.0)

    def test_sqrt_two_returns_correct_value(self, calculator):
        """Test sqrt(2) returns sqrt(2)."""
        assert calculator.sqrt(2) == pytest.approx(math.sqrt(2))

    def test_sqrt_recorded_in_history(self, calculator):
        """Test that sqrt operation is recorded in history."""
        calculator.sqrt(4)
        history = calculator.get_history()

        assert len(history) == 1
        record = history[0]
        assert record.operation_name == "sqrt"
        assert record.operands == [4]
        assert record.result == pytest.approx(2.0)

    def test_sqrt_with_float_recorded(self, calculator):
        """Test that sqrt with float is recorded."""
        calculator.sqrt(0.25)
        history = calculator.get_history()

        assert len(history) == 1
        assert history[0].operation_name == "sqrt"
        assert history[0].result == pytest.approx(0.5)

    def test_sqrt_negative_raises_valueerror(self, calculator):
        """Test that sqrt of negative raises ValueError."""
        with pytest.raises(ValueError):
            calculator.sqrt(-1)

    def test_sqrt_invalid_does_not_record_history(self, calculator):
        """Test that sqrt with negative does not record to history."""
        try:
            calculator.sqrt(-4)
        except ValueError:
            pass
        assert len(calculator.get_history()) == 0

    def test_sqrt_bool_raises_typeerror(self, calculator):
        """Test that sqrt(bool) raises TypeError."""
        with pytest.raises(TypeError):
            calculator.sqrt(True)

    def test_sqrt_bool_does_not_record_history(self, calculator):
        """Test that sqrt with bool does not record to history."""
        try:
            calculator.sqrt(False)
        except TypeError:
            pass
        assert len(calculator.get_history()) == 0


# ============================================================================
# MULTIPLE SCIENTIFIC OPERATIONS
# ============================================================================

class TestCalculatorMultipleScientific:
    """Test suite for multiple scientific operations in sequence."""

    def test_multiple_scientific_operations_recorded_in_order(self, calculator):
        """Test that multiple scientific operations are recorded in order."""
        calculator.sin(0)
        calculator.exp(1)
        calculator.sqrt(4)

        history = calculator.get_history()
        assert len(history) == 3
        assert history[0].operation_name == "sin"
        assert history[1].operation_name == "exp"
        assert history[2].operation_name == "sqrt"

    def test_mixed_scientific_and_basic_operations(self, calculator):
        """Test mixing scientific and basic operations."""
        calculator.add(1, 2)
        calculator.sin(0)
        calculator.multiply(3, 4)
        calculator.exp(1)

        history = calculator.get_history()
        assert len(history) == 4
        assert history[0].operation_name == "add"
        assert history[1].operation_name == "sin"
        assert history[2].operation_name == "multiply"
        assert history[3].operation_name == "exp"

    def test_scientific_operations_accumulate_history(self, calculator):
        """Test that multiple scientific operations accumulate."""
        for i in range(1, 5):
            calculator.sqrt(i * i)

        history = calculator.get_history()
        assert len(history) == 4
        for record in history:
            assert record.operation_name == "sqrt"

    def test_clear_history_after_scientific_operations(self, calculator):
        """Test that clear_history works after scientific operations."""
        calculator.sin(1.0)
        calculator.cos(2.0)
        calculator.exp(3.0)

        assert len(calculator.get_history()) == 3
        calculator.clear_history()
        assert len(calculator.get_history()) == 0

    def test_scientific_operations_with_negative_values(self, calculator):
        """Test scientific operations with negative values."""
        calculator.sin(-math.pi / 4)
        calculator.exp(-1)
        calculator.cos(-math.pi / 3)

        history = calculator.get_history()
        assert len(history) == 3
        for record in history:
            assert record.result is not None
