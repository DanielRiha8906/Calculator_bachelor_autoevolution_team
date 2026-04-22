import pytest
import math
from src.calculator import Calculator


# ============================================================================
# Tests for divide() method - Division by Zero Feature
# ============================================================================

class TestDivideByZero:
    """Tests for the zero-divisor guard in Calculator.divide()"""

    def test_divide_positive_by_zero_raises_error(self):
        """Dividing positive number by zero raises ZeroDivisionError"""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calc.divide(10, 0)

    def test_divide_negative_by_zero_raises_error(self):
        """Dividing negative number by zero raises ZeroDivisionError"""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calc.divide(-10, 0)

    def test_divide_zero_by_zero_raises_error(self):
        """Dividing zero by zero raises ZeroDivisionError"""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calc.divide(0, 0)

    def test_divide_float_by_zero_raises_error(self):
        """Dividing float by zero raises ZeroDivisionError"""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calc.divide(3.14159, 0)

    def test_divide_by_zero_error_message(self):
        """Error message for division by zero is exact"""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError) as exc_info:
            calc.divide(100, 0)
        assert str(exc_info.value) == "Cannot divide by zero"


# ============================================================================
# Tests for divide() - Valid Division Operations
# ============================================================================

class TestDivideValid:
    """Tests for valid division operations"""

    def test_divide_integers_positive(self):
        """Dividing positive integers returns correct result"""
        calc = Calculator()
        result = calc.divide(10, 2)
        assert result == 5.0

    def test_divide_integers_negative_dividend(self):
        """Dividing negative by positive returns negative result"""
        calc = Calculator()
        result = calc.divide(-10, 2)
        assert result == -5.0

    def test_divide_integers_negative_divisor(self):
        """Dividing positive by negative returns negative result"""
        calc = Calculator()
        result = calc.divide(10, -2)
        assert result == -5.0

    def test_divide_both_negative(self):
        """Dividing two negative numbers returns positive result"""
        calc = Calculator()
        result = calc.divide(-10, -2)
        assert result == 5.0

    def test_divide_floats(self):
        """Dividing floats returns correct result"""
        calc = Calculator()
        result = calc.divide(7.5, 2.5)
        assert result == 3.0

    def test_divide_zero_numerator(self):
        """Dividing zero by non-zero number returns zero"""
        calc = Calculator()
        result = calc.divide(0, 5)
        assert result == 0.0

    def test_divide_uneven_result(self):
        """Dividing numbers with uneven result"""
        calc = Calculator()
        result = calc.divide(10, 3)
        assert pytest.approx(result, rel=1e-9) == 10 / 3

    def test_divide_very_small_divisor(self):
        """Dividing by very small non-zero number"""
        calc = Calculator()
        result = calc.divide(1, 1e-10)
        assert result == 1e10

    def test_divide_very_large_numbers(self):
        """Dividing very large numbers"""
        calc = Calculator()
        result = calc.divide(1e15, 1e5)
        assert result == 1e10

    def test_divide_fractional_result(self):
        """Division resulting in a fraction"""
        calc = Calculator()
        result = calc.divide(1, 2)
        assert result == 0.5

    def test_divide_mixed_int_float(self):
        """Division with mixed int and float"""
        calc = Calculator()
        result = calc.divide(10, 4.0)
        assert result == 2.5


# ============================================================================
# Tests for divide() - Edge Cases and Type Behavior
# ============================================================================

class TestDivideEdgeCases:
    """Edge case tests for divide()"""

    def test_divide_returns_float_type(self):
        """Result of divide() is always float type"""
        calc = Calculator()
        result = calc.divide(10, 2)
        assert isinstance(result, float)

    def test_divide_positive_infinity_numerator(self):
        """Dividing infinity by non-zero"""
        calc = Calculator()
        result = calc.divide(float('inf'), 2)
        assert result == float('inf')

    def test_divide_negative_infinity_numerator(self):
        """Dividing negative infinity by non-zero"""
        calc = Calculator()
        result = calc.divide(float('-inf'), 2)
        assert result == float('-inf')

    def test_divide_zero_by_negative_number(self):
        """Zero divided by negative number is negative zero (or zero)"""
        calc = Calculator()
        result = calc.divide(0, -5)
        assert result == 0.0

    def test_divide_very_close_to_zero_not_raises(self):
        """Division by number very close to zero (but not zero) does not raise"""
        calc = Calculator()
        result = calc.divide(1, 1e-300)
        # Should complete without raising ZeroDivisionError
        assert isinstance(result, float)


# ============================================================================
# Regression Tests - Other Operations Unaffected
# ============================================================================

class TestRegressionOtherOperations:
    """Verify that changes to divide() did not break other methods"""

    def test_add_positive_numbers(self):
        """Addition of positive numbers"""
        calc = Calculator()
        assert calc.add(5, 3) == 8

    def test_add_negative_numbers(self):
        """Addition with negative numbers"""
        calc = Calculator()
        assert calc.add(-5, -3) == -8

    def test_add_zero(self):
        """Addition with zero"""
        calc = Calculator()
        assert calc.add(5, 0) == 5

    def test_subtract_positive_numbers(self):
        """Subtraction of positive numbers"""
        calc = Calculator()
        assert calc.subtract(10, 3) == 7

    def test_subtract_negative_from_positive(self):
        """Subtracting negative from positive"""
        calc = Calculator()
        assert calc.subtract(10, -5) == 15

    def test_subtract_positive_from_negative(self):
        """Subtracting positive from negative"""
        calc = Calculator()
        assert calc.subtract(-10, 5) == -15

    def test_subtract_zero(self):
        """Subtraction with zero"""
        calc = Calculator()
        assert calc.subtract(5, 0) == 5

    def test_multiply_positive_numbers(self):
        """Multiplication of positive numbers"""
        calc = Calculator()
        assert calc.multiply(5, 3) == 15

    def test_multiply_by_zero(self):
        """Multiplication by zero"""
        calc = Calculator()
        assert calc.multiply(5, 0) == 0

    def test_multiply_by_negative(self):
        """Multiplication by negative number"""
        calc = Calculator()
        assert calc.multiply(5, -3) == -15

    def test_multiply_negative_numbers(self):
        """Multiplication of two negative numbers"""
        calc = Calculator()
        assert calc.multiply(-5, -3) == 15


# ============================================================================
# Integration Tests - Calculator Instance State
# ============================================================================

class TestCalculatorState:
    """Tests for calculator state and instance independence"""

    def test_multiple_instances_independent(self):
        """Multiple Calculator instances are independent"""
        calc1 = Calculator()
        calc2 = Calculator()
        result1 = calc1.divide(10, 2)
        result2 = calc2.divide(20, 4)
        assert result1 == 5.0
        assert result2 == 5.0

    def test_sequential_operations_on_same_instance(self):
        """Sequential operations on same instance"""
        calc = Calculator()
        result1 = calc.divide(10, 2)
        result2 = calc.divide(20, 4)
        result3 = calc.add(result1, result2)
        assert result3 == 10.0

    def test_divide_after_failed_divide_by_zero(self):
        """Valid division after catching ZeroDivisionError"""
        calc = Calculator()
        # First attempt should fail
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)
        # Second attempt with valid input should succeed
        result = calc.divide(10, 2)
        assert result == 5.0