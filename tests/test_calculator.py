import pytest
import math
from src.calculator import Calculator


@pytest.fixture
def calc():
    """Fixture providing a Calculator instance."""
    return Calculator()


# ============================================================================
# ADDITION TESTS
# ============================================================================

def test_add_positive_integers(calc):
    """Verify addition of two positive integers."""
    result = calc.add(5, 3)
    assert result == 8


def test_add_positive_integers_large(calc):
    """Verify addition of large positive integers."""
    result = calc.add(1000000, 2000000)
    assert result == 3000000


def test_add_negative_integers(calc):
    """Verify addition of two negative integers."""
    result = calc.add(-5, -3)
    assert result == -8


def test_add_mixed_sign_positive_result(calc):
    """Verify addition of mixed sign numbers resulting in positive."""
    result = calc.add(10, -3)
    assert result == 7


def test_add_mixed_sign_negative_result(calc):
    """Verify addition of mixed sign numbers resulting in negative."""
    result = calc.add(3, -10)
    assert result == -7


def test_add_zero_left_operand(calc):
    """Verify addition with zero as left operand."""
    result = calc.add(0, 5)
    assert result == 5


def test_add_zero_right_operand(calc):
    """Verify addition with zero as right operand."""
    result = calc.add(5, 0)
    assert result == 5


def test_add_both_zeros(calc):
    """Verify addition of zero and zero."""
    result = calc.add(0, 0)
    assert result == 0


def test_add_floating_point(calc):
    """Verify addition of floating-point numbers."""
    result = calc.add(2.5, 3.7)
    assert abs(result - 6.2) < 1e-10


def test_add_floating_point_negative(calc):
    """Verify addition of negative floating-point numbers."""
    result = calc.add(-2.5, -3.7)
    assert abs(result - (-6.2)) < 1e-10


def test_add_floating_point_mixed_sign(calc):
    """Verify addition of mixed sign floating-point numbers."""
    result = calc.add(5.5, -2.3)
    assert abs(result - 3.2) < 1e-10


def test_add_integer_and_float(calc):
    """Verify addition of integer and float."""
    result = calc.add(10, 2.5)
    assert abs(result - 12.5) < 1e-10


# ============================================================================
# SUBTRACTION TESTS
# ============================================================================

def test_subtract_positive_integers(calc):
    """Verify subtraction of two positive integers."""
    result = calc.subtract(10, 3)
    assert result == 7


def test_subtract_positive_integers_result_zero(calc):
    """Verify subtraction resulting in zero."""
    result = calc.subtract(5, 5)
    assert result == 0


def test_subtract_positive_integers_result_negative(calc):
    """Verify subtraction of positive integers resulting in negative."""
    result = calc.subtract(3, 10)
    assert result == -7


def test_subtract_negative_integers(calc):
    """Verify subtraction of two negative integers."""
    result = calc.subtract(-10, -3)
    assert result == -7


def test_subtract_negative_from_positive(calc):
    """Verify subtracting a negative number from positive (double negative)."""
    result = calc.subtract(10, -5)
    assert result == 15


def test_subtract_positive_from_negative(calc):
    """Verify subtracting a positive number from negative."""
    result = calc.subtract(-10, 5)
    assert result == -15


def test_subtract_zero_left_operand(calc):
    """Verify subtraction with zero as left operand."""
    result = calc.subtract(0, 5)
    assert result == -5


def test_subtract_zero_right_operand(calc):
    """Verify subtraction with zero as right operand."""
    result = calc.subtract(5, 0)
    assert result == 5


def test_subtract_both_zeros(calc):
    """Verify subtraction of zero from zero."""
    result = calc.subtract(0, 0)
    assert result == 0


def test_subtract_floating_point(calc):
    """Verify subtraction of floating-point numbers."""
    result = calc.subtract(7.5, 2.3)
    assert abs(result - 5.2) < 1e-10


def test_subtract_floating_point_negative(calc):
    """Verify subtraction with negative floating-point numbers."""
    result = calc.subtract(-5.5, -2.3)
    assert abs(result - (-3.2)) < 1e-10


def test_subtract_floating_point_mixed_sign(calc):
    """Verify subtraction of mixed sign floating-point numbers."""
    result = calc.subtract(5.5, -2.3)
    assert abs(result - 7.8) < 1e-10


def test_subtract_integer_and_float(calc):
    """Verify subtraction of integer and float."""
    result = calc.subtract(10, 2.5)
    assert abs(result - 7.5) < 1e-10


# ============================================================================
# MULTIPLICATION TESTS
# ============================================================================

def test_multiply_positive_integers(calc):
    """Verify multiplication of two positive integers."""
    result = calc.multiply(5, 3)
    assert result == 15


def test_multiply_positive_integers_large(calc):
    """Verify multiplication of large positive integers."""
    result = calc.multiply(1000, 2000)
    assert result == 2000000


def test_multiply_by_zero_right(calc):
    """Verify multiplication by zero (right operand)."""
    result = calc.multiply(5, 0)
    assert result == 0


def test_multiply_by_zero_left(calc):
    """Verify multiplication by zero (left operand)."""
    result = calc.multiply(0, 5)
    assert result == 0


def test_multiply_both_zeros(calc):
    """Verify multiplication of zero by zero."""
    result = calc.multiply(0, 0)
    assert result == 0


def test_multiply_by_one_right(calc):
    """Verify multiplication by one (right operand)."""
    result = calc.multiply(5, 1)
    assert result == 5


def test_multiply_by_one_left(calc):
    """Verify multiplication by one (left operand)."""
    result = calc.multiply(1, 5)
    assert result == 5


def test_multiply_negative_integers(calc):
    """Verify multiplication of two negative integers."""
    result = calc.multiply(-5, -3)
    assert result == 15


def test_multiply_negative_positive_integers(calc):
    """Verify multiplication of negative and positive integers."""
    result = calc.multiply(-5, 3)
    assert result == -15


def test_multiply_positive_negative_integers(calc):
    """Verify multiplication of positive and negative integers."""
    result = calc.multiply(5, -3)
    assert result == -15


def test_multiply_floating_point(calc):
    """Verify multiplication of floating-point numbers."""
    result = calc.multiply(2.5, 4.0)
    assert abs(result - 10.0) < 1e-10


def test_multiply_floating_point_negative(calc):
    """Verify multiplication of negative floating-point numbers."""
    result = calc.multiply(-2.5, -4.0)
    assert abs(result - 10.0) < 1e-10


def test_multiply_floating_point_mixed_sign(calc):
    """Verify multiplication of mixed sign floating-point numbers."""
    result = calc.multiply(2.5, -4.0)
    assert abs(result - (-10.0)) < 1e-10


def test_multiply_integer_and_float(calc):
    """Verify multiplication of integer and float."""
    result = calc.multiply(5, 2.5)
    assert abs(result - 12.5) < 1e-10


def test_multiply_fraction_result(calc):
    """Verify multiplication resulting in fractional value."""
    result = calc.multiply(0.5, 0.5)
    assert abs(result - 0.25) < 1e-10


# ============================================================================
# DIVISION TESTS (EXISTING + ADDITIONAL)
# ============================================================================

def test_division_by_zero(calc):
    """Verify that dividing by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(10, 0)


def test_division_by_zero_zero_numerator(calc):
    """Verify that 0/0 also raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(0, 0)


def test_division_normal(calc):
    """Verify normal division works correctly (regression check)."""
    result = calc.divide(10, 2)
    assert result == 5.0


def test_division_positive_integers(calc):
    """Verify division of two positive integers."""
    result = calc.divide(20, 4)
    assert result == 5.0


def test_division_negative_integers(calc):
    """Verify division of two negative integers."""
    result = calc.divide(-20, -4)
    assert result == 5.0


def test_division_negative_positive_integers(calc):
    """Verify division of negative by positive integer."""
    result = calc.divide(-20, 4)
    assert result == -5.0


def test_division_positive_negative_integers(calc):
    """Verify division of positive by negative integer."""
    result = calc.divide(20, -4)
    assert result == -5.0


def test_division_zero_numerator(calc):
    """Verify division with zero as numerator."""
    result = calc.divide(0, 5)
    assert result == 0.0


def test_division_floating_point(calc):
    """Verify division of floating-point numbers."""
    result = calc.divide(7.5, 2.5)
    assert abs(result - 3.0) < 1e-10


def test_division_floating_point_negative(calc):
    """Verify division of negative floating-point numbers."""
    result = calc.divide(-7.5, -2.5)
    assert abs(result - 3.0) < 1e-10


def test_division_floating_point_mixed_sign(calc):
    """Verify division of mixed sign floating-point numbers."""
    result = calc.divide(7.5, -2.5)
    assert abs(result - (-3.0)) < 1e-10


def test_division_integer_and_float(calc):
    """Verify division of integer by float."""
    result = calc.divide(10, 2.5)
    assert abs(result - 4.0) < 1e-10


def test_division_fractional_result(calc):
    """Verify division resulting in fractional value."""
    result = calc.divide(1, 3)
    assert abs(result - (1/3)) < 1e-10


def test_division_result_less_than_one(calc):
    """Verify division with result less than one."""
    result = calc.divide(1, 2)
    assert abs(result - 0.5) < 1e-10


# ============================================================================
# RESULT CHAINING TESTS
# ============================================================================

def test_add_result_chains_to_multiply(calc):
    """Verify output of add can be input to multiply."""
    result_add = calc.add(2, 3)
    assert isinstance(result_add, (int, float))
    result_multiply = calc.multiply(result_add, 2)
    assert result_multiply == 10


def test_add_result_chains_to_subtract(calc):
    """Verify output of add can be input to subtract."""
    result_add = calc.add(10, 5)
    assert isinstance(result_add, (int, float))
    result_subtract = calc.subtract(result_add, 3)
    assert result_subtract == 12


def test_add_result_chains_to_divide(calc):
    """Verify output of add can be input to divide."""
    result_add = calc.add(4, 6)
    assert isinstance(result_add, (int, float))
    result_divide = calc.divide(result_add, 2)
    assert result_divide == 5.0


def test_subtract_result_chains_to_multiply(calc):
    """Verify output of subtract can be input to multiply."""
    result_subtract = calc.subtract(10, 3)
    assert isinstance(result_subtract, (int, float))
    result_multiply = calc.multiply(result_subtract, 2)
    assert result_multiply == 14


def test_subtract_result_chains_to_add(calc):
    """Verify output of subtract can be input to add."""
    result_subtract = calc.subtract(20, 5)
    assert isinstance(result_subtract, (int, float))
    result_add = calc.add(result_subtract, 3)
    assert result_add == 18


def test_subtract_result_chains_to_divide(calc):
    """Verify output of subtract can be input to divide."""
    result_subtract = calc.subtract(20, 2)
    assert isinstance(result_subtract, (int, float))
    result_divide = calc.divide(result_subtract, 2)
    assert result_divide == 9.0


def test_multiply_result_chains_to_add(calc):
    """Verify output of multiply can be input to add."""
    result_multiply = calc.multiply(5, 3)
    assert isinstance(result_multiply, (int, float))
    result_add = calc.add(result_multiply, 2)
    assert result_add == 17


def test_multiply_result_chains_to_subtract(calc):
    """Verify output of multiply can be input to subtract."""
    result_multiply = calc.multiply(5, 4)
    assert isinstance(result_multiply, (int, float))
    result_subtract = calc.subtract(result_multiply, 3)
    assert result_subtract == 17


def test_multiply_result_chains_to_divide(calc):
    """Verify output of multiply can be input to divide."""
    result_multiply = calc.multiply(4, 5)
    assert isinstance(result_multiply, (int, float))
    result_divide = calc.divide(result_multiply, 2)
    assert result_divide == 10.0


def test_divide_result_chains_to_add(calc):
    """Verify output of divide can be input to add."""
    result_divide = calc.divide(10, 2)
    assert isinstance(result_divide, (int, float))
    result_add = calc.add(result_divide, 3)
    assert result_add == 8.0


def test_divide_result_chains_to_subtract(calc):
    """Verify output of divide can be input to subtract."""
    result_divide = calc.divide(20, 4)
    assert isinstance(result_divide, (int, float))
    result_subtract = calc.subtract(result_divide, 2)
    assert result_subtract == 3.0


def test_divide_result_chains_to_multiply(calc):
    """Verify output of divide can be input to multiply."""
    result_divide = calc.divide(15, 3)
    assert isinstance(result_divide, (int, float))
    result_multiply = calc.multiply(result_divide, 2)
    assert result_multiply == 10.0


def test_complex_chaining_add_subtract_multiply(calc):
    """Verify complex chaining: add -> subtract -> multiply."""
    result1 = calc.add(5, 5)
    assert isinstance(result1, (int, float))
    result2 = calc.subtract(result1, 2)
    assert isinstance(result2, (int, float))
    result3 = calc.multiply(result2, 2)
    assert result3 == 16


def test_complex_chaining_multiply_divide_add(calc):
    """Verify complex chaining: multiply -> divide -> add."""
    result1 = calc.multiply(10, 4)
    assert isinstance(result1, (int, float))
    result2 = calc.divide(result1, 5)
    assert isinstance(result2, (int, float))
    result3 = calc.add(result2, 1)
    assert abs(result3 - 9.0) < 1e-10