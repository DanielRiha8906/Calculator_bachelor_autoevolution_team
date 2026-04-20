"""Tests for CalculationEngine from src.core.engine."""

import pytest
from src.core.engine import CalculationEngine


class TestCalculationEngineAdd:
    """Test CalculationEngine.add method."""

    def test_add_positive_integers(self):
        """Test adding two positive integers."""
        engine = CalculationEngine()
        assert engine.add(2, 3) == 5

    def test_add_negative_integers(self):
        """Test adding two negative integers."""
        engine = CalculationEngine()
        assert engine.add(-2, -3) == -5

    def test_add_mixed_sign(self):
        """Test adding positive and negative integers."""
        engine = CalculationEngine()
        assert engine.add(5, -3) == 2

    def test_add_zero_left(self):
        """Test adding with zero on the left."""
        engine = CalculationEngine()
        assert engine.add(0, 5) == 5

    def test_add_zero_right(self):
        """Test adding with zero on the right."""
        engine = CalculationEngine()
        assert engine.add(5, 0) == 5

    def test_add_both_zeros(self):
        """Test adding two zeros."""
        engine = CalculationEngine()
        assert engine.add(0, 0) == 0

    def test_add_floats(self):
        """Test adding two floats."""
        engine = CalculationEngine()
        assert engine.add(1.5, 2.5) == 4.0

    def test_add_float_negative(self):
        """Test adding negative floats."""
        engine = CalculationEngine()
        assert engine.add(-1.5, -2.5) == -4.0

    def test_add_mixed_int_float(self):
        """Test adding integer and float."""
        engine = CalculationEngine()
        assert engine.add(2, 3.5) == 5.5

    def test_add_very_large_numbers(self):
        """Test adding very large numbers."""
        engine = CalculationEngine()
        assert engine.add(1e10, 1e10) == 2e10

    def test_add_very_small_floats(self):
        """Test adding very small floats."""
        engine = CalculationEngine()
        result = engine.add(1e-10, 2e-10)
        assert abs(result - 3e-10) < 1e-15


class TestCalculationEngineSubtract:
    """Test CalculationEngine.subtract method."""

    def test_subtract_positive_integers(self):
        """Test subtracting two positive integers."""
        engine = CalculationEngine()
        assert engine.subtract(5, 3) == 2

    def test_subtract_result_zero(self):
        """Test subtraction resulting in zero."""
        engine = CalculationEngine()
        assert engine.subtract(5, 5) == 0

    def test_subtract_result_negative(self):
        """Test subtraction resulting in negative."""
        engine = CalculationEngine()
        assert engine.subtract(3, 5) == -2

    def test_subtract_negative_integers(self):
        """Test subtracting negative integers."""
        engine = CalculationEngine()
        assert engine.subtract(-2, -3) == 1

    def test_subtract_negative_from_positive(self):
        """Test subtracting negative from positive."""
        engine = CalculationEngine()
        assert engine.subtract(5, -3) == 8

    def test_subtract_positive_from_negative(self):
        """Test subtracting positive from negative."""
        engine = CalculationEngine()
        assert engine.subtract(-5, 3) == -8

    def test_subtract_zero_left(self):
        """Test subtracting with zero on the left."""
        engine = CalculationEngine()
        assert engine.subtract(0, 5) == -5

    def test_subtract_zero_right(self):
        """Test subtracting with zero on the right."""
        engine = CalculationEngine()
        assert engine.subtract(5, 0) == 5

    def test_subtract_both_zeros(self):
        """Test subtracting two zeros."""
        engine = CalculationEngine()
        assert engine.subtract(0, 0) == 0

    def test_subtract_floats(self):
        """Test subtracting floats."""
        engine = CalculationEngine()
        assert engine.subtract(5.5, 2.5) == 3.0

    def test_subtract_float_negative(self):
        """Test subtracting negative floats."""
        engine = CalculationEngine()
        assert engine.subtract(-5.5, -2.5) == -3.0

    def test_subtract_mixed_int_float(self):
        """Test subtracting integer and float."""
        engine = CalculationEngine()
        assert engine.subtract(5, 2.5) == 2.5


class TestCalculationEngineMultiply:
    """Test CalculationEngine.multiply method."""

    def test_multiply_positive_integers(self):
        """Test multiplying two positive integers."""
        engine = CalculationEngine()
        assert engine.multiply(3, 4) == 12

    def test_multiply_by_zero_left(self):
        """Test multiplying with zero on the left."""
        engine = CalculationEngine()
        assert engine.multiply(0, 5) == 0

    def test_multiply_by_zero_right(self):
        """Test multiplying with zero on the right."""
        engine = CalculationEngine()
        assert engine.multiply(5, 0) == 0

    def test_multiply_both_zeros(self):
        """Test multiplying two zeros."""
        engine = CalculationEngine()
        assert engine.multiply(0, 0) == 0

    def test_multiply_by_one_left(self):
        """Test multiplying with one on the left."""
        engine = CalculationEngine()
        assert engine.multiply(1, 5) == 5

    def test_multiply_by_one_right(self):
        """Test multiplying with one on the right."""
        engine = CalculationEngine()
        assert engine.multiply(5, 1) == 5

    def test_multiply_negative_integers(self):
        """Test multiplying two negative integers."""
        engine = CalculationEngine()
        assert engine.multiply(-3, -4) == 12

    def test_multiply_negative_positive(self):
        """Test multiplying negative and positive."""
        engine = CalculationEngine()
        assert engine.multiply(-3, 4) == -12

    def test_multiply_floats(self):
        """Test multiplying floats."""
        engine = CalculationEngine()
        assert engine.multiply(2.5, 4.0) == 10.0

    def test_multiply_float_negative(self):
        """Test multiplying negative floats."""
        engine = CalculationEngine()
        assert engine.multiply(-2.5, -4.0) == 10.0

    def test_multiply_mixed_int_float(self):
        """Test multiplying integer and float."""
        engine = CalculationEngine()
        assert engine.multiply(3, 2.5) == 7.5

    def test_multiply_fraction_result(self):
        """Test multiplication resulting in fraction."""
        engine = CalculationEngine()
        assert engine.multiply(0.5, 0.5) == 0.25

    def test_multiply_very_large_numbers(self):
        """Test multiplying very large numbers."""
        engine = CalculationEngine()
        assert engine.multiply(1e10, 2e10) == 2e20


class TestCalculationEngineDivide:
    """Test CalculationEngine.divide method."""

    def test_divide_positive_integers(self):
        """Test dividing two positive integers."""
        engine = CalculationEngine()
        assert engine.divide(6, 3) == 2.0

    def test_divide_normal(self):
        """Test normal division."""
        engine = CalculationEngine()
        assert engine.divide(10, 2) == 5.0

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ZeroDivisionError."""
        engine = CalculationEngine()
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            engine.divide(5, 0)

    def test_divide_by_zero_zero_numerator(self):
        """Test that 0/0 raises ZeroDivisionError."""
        engine = CalculationEngine()
        with pytest.raises(ZeroDivisionError):
            engine.divide(0, 0)

    def test_divide_zero_numerator(self):
        """Test dividing zero by non-zero."""
        engine = CalculationEngine()
        assert engine.divide(0, 5) == 0.0

    def test_divide_negative_integers(self):
        """Test dividing two negative integers."""
        engine = CalculationEngine()
        assert engine.divide(-6, -3) == 2.0

    def test_divide_negative_positive(self):
        """Test dividing negative by positive."""
        engine = CalculationEngine()
        assert engine.divide(-6, 3) == -2.0

    def test_divide_positive_negative(self):
        """Test dividing positive by negative."""
        engine = CalculationEngine()
        assert engine.divide(6, -3) == -2.0

    def test_divide_floats(self):
        """Test dividing floats."""
        engine = CalculationEngine()
        assert engine.divide(5.0, 2.0) == 2.5

    def test_divide_float_negative(self):
        """Test dividing negative floats."""
        engine = CalculationEngine()
        assert engine.divide(-5.0, -2.0) == 2.5

    def test_divide_mixed_int_float(self):
        """Test dividing integer by float."""
        engine = CalculationEngine()
        assert engine.divide(5, 2.0) == 2.5

    def test_divide_fractional_result(self):
        """Test division with fractional result."""
        engine = CalculationEngine()
        assert engine.divide(1, 3) == pytest.approx(0.3333333, rel=1e-5)

    def test_divide_result_less_than_one(self):
        """Test division resulting in less than one."""
        engine = CalculationEngine()
        assert engine.divide(1, 2) == 0.5

    def test_divide_very_large_by_small(self):
        """Test dividing very large by very small."""
        engine = CalculationEngine()
        result = engine.divide(1e10, 1e-5)
        assert result == pytest.approx(1e15)

    def test_divide_very_small_by_large(self):
        """Test dividing very small by very large."""
        engine = CalculationEngine()
        result = engine.divide(1e-10, 1e5)
        assert result == pytest.approx(1e-15)


class TestCalculationEngineEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_engine_instance_isolation(self):
        """Test that separate engine instances are independent."""
        engine1 = CalculationEngine()
        engine2 = CalculationEngine()
        assert engine1.add(1, 2) == engine2.add(1, 2)

    def test_multiple_operations_in_sequence(self):
        """Test chaining multiple operations."""
        engine = CalculationEngine()
        result = engine.add(2, 3)  # 5
        result = engine.multiply(result, 2)  # 10
        result = engine.subtract(result, 5)  # 5
        assert result == 5

    def test_divide_one_by_very_small_number(self):
        """Test dividing by very small number."""
        engine = CalculationEngine()
        result = engine.divide(1, 1e-100)
        assert result == 1e100

    def test_operations_with_negative_zero(self):
        """Test operations handling negative zero."""
        engine = CalculationEngine()
        # Python typically treats -0.0 and 0.0 as equivalent
        assert engine.add(-0.0, 5) == 5.0
